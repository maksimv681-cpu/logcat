#!/usr/bin/env python3
"""
Drag Streets local test server.

Services
--------
HTTP  :8080  /v1/auth/{login,register,session,logout}
TCP   :8992  logic  (primary)
TCP   :8993  content
TCP   :8994  logic  (secondary)
TCP   :8995  content (secondary)

The TCP protocol is the game's native gateway protocol:
    4-byte big-endian frame length (everything after this field)
    32-byte digest (the client ignores incoming digest bytes)
    4-byte big-endian packet id
    4-byte big-endian error/status field
    4-byte big-endian sequence field
    body (AES-128/ECB/PKCS5 after the connect handshake)

Connect (packet 7) is plaintext.  The client sends
    random ^ 0x55555555
as 8 bytes.  Its AES key is
    random || random
where random = sent_value ^ 0x55555555.  The server echoes the same 8 bytes
back, then encrypts/decrypts every other packet body except ping (6).

InitRequest (1910) is answered with a minimal, local test profile. The profile
is intentionally a new-player profile with an empty garage; it is enough to
complete player initialization and reveal the next client-side requirements.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import socket
import struct
import sys
import threading
import time
import zlib
import zipfile
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# ---------------------------------------------------------------------------
# Constants / helpers
# ---------------------------------------------------------------------------

CONNECT_XOR = 0x55555555
MAX_FRAME = 16 * 1024 * 1024

# Packet 3 response body begins with an application-level 32-bit result code.
# Zero is success. The current client accepts this empty manifest after the result.
EMPTY_PATCH_CONTAINER_BODY = bytes.fromhex("00 00 00 00")

# Protobuf payloads carried by fB1 are length-prefixed inside the packet body:
# fB1.J(bytes) writes uint32_be(length) + bytes, and fB1.r() reads it back.
# CheckBanResponseProto.status = OK (enum value 1), field 1 => 08 01.
CHECK_BAN_OK_PROTO = bytes.fromhex("08 01")
CHECK_BAN_OK_BODY = struct.pack(">I", len(CHECK_BAN_OK_PROTO)) + CHECK_BAN_OK_PROTO

# q80 enum in the supplied client has 85 database categories. The Android
# Logcat exposed a required invariant in ChampionshipDatabaseProto: the client
# calls pJ.c(level).g() for levels 1..8 while building Ke1. An empty championship
# message therefore crashes with a NullPointerException. Supply a minimal,
# structurally valid league row for every enum level, and empty protobufs for
# the other categories.
DATABASE_FIELD_IDS = (
    *range(1, 14), *range(15, 22), *range(23, 45),
    *range(46, 55), *range(56, 70), *range(71, 91),
)
CHAMPIONSHIP_DATABASE_FIELD_ID = 64
AVATARS_DATABASE_FIELD_ID = 86
VINYL_MARKET_BLOCK_DATABASE_FIELD_ID = 65
# Packet 50015 uses database-map type IDs, not DatabaseProto field numbers.
# The client map requests avatar catalog type 86 and championship type 64.
CHAMPIONSHIP_DATABASE_TYPE_ID = 64
AVATARS_DATABASE_TYPE_ID = 86
VINYL_MARKET_BLOCK_DATABASE_TYPE_ID = 65
CHAMPIONSHIP_LEVELS = tuple(range(1, 9))
CHAMPIONSHIP_ICON = "champ_league_undefined"  # Known atlas region in the client.
CHAMPIONSHIP_NAME_KEY = "CHAMPIONSHIP_LEAGUE"  # Present in the client localization.
AVATAR_BASE_ID = 1
AVATAR_FRAME_ID = 1
AVATAR_BASE_ICON = "temporary_icon"  # Referenced by the client's Avatars atlas.
AVATAR_FRAME_ICON = AVATAR_BASE_ICON  # Reuse the confirmed existing atlas region; avatar_frame_blue is absent.
# CRC reported by the latest Android client log (SRLAB-CRC-ACTUAL/EXPECTED).
# Deliberately changed from the previous test build (0xE6FEB91B).
# AU.c compares this version with dbcache.protobin and skips packet 50015
# when they match. Bumping it forces the client to request and apply the
# corrected database instead of reusing its stale local cache.
TARGET_DATABASE_CRC32 = 0xA17C4D2C


def _protobuf_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("protobuf varint helper only accepts non-negative integers")
    out = bytearray()
    while value > 0x7F:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def _protobuf_int32_field(field_id: int, value: int) -> bytes:
    # protobuf int32 encodes negative values as a sign-extended 10-byte varint.
    # Several source catalogs contain negative color IDs and sentinel values.
    value = int(value)
    if value < 0:
        value = (1 << 64) + value
    return _protobuf_varint(field_id << 3) + _protobuf_varint(value)


def _protobuf_bytes_field(field_id: int, value: bytes) -> bytes:
    return (
        _protobuf_varint((field_id << 3) | 2)
        + _protobuf_varint(len(value))
        + value
    )


def _protobuf_string_field(field_id: int, value: str) -> bytes:
    return _protobuf_bytes_field(field_id, value.encode("utf-8"))


def build_championship_database_proto() -> bytes:
    """Serialize ChampionshipDatabaseProto with league records for levels 1..8.

    BaseChampLeagueProto fields are taken from ChampionshipContainer.proto:
      1 level, 2 rank_count, 3 stars_count, 4 icon, 5 name_key.
    A single rank and star is the smallest usable positive league configuration;
    the undefined icon is a real region referenced by the client as its fallback.
    """
    result = bytearray()
    for level in CHAMPIONSHIP_LEVELS:
        league = b"".join((
            _protobuf_int32_field(1, level),
            _protobuf_int32_field(2, 1),
            _protobuf_int32_field(3, 1),
            _protobuf_string_field(4, CHAMPIONSHIP_ICON),
            _protobuf_string_field(5, CHAMPIONSHIP_NAME_KEY),
        ))
        result.extend(_protobuf_bytes_field(1, league))
    return bytes(result)


CHAMPIONSHIP_DATABASE_PROTO = build_championship_database_proto()


def build_avatars_database_proto() -> bytes:
    """Build the smallest avatar catalog required by the default local profile.

    Database.AvatarsDatabaseProto fields (confirmed in the client's generated
    Database$AvatarsDatabaseProto): 1=avatars_base, 2=predicates, 3=frames_base.
    AbstractBaseEntityProto fields: 1=id, 2=icon, 5=hide_unavailable, 6=type.
    Type 0 is the static atlas-region model handled by C0410ik.
    """
    avatar_base = b"".join((
        _protobuf_int32_field(1, AVATAR_BASE_ID),
        _protobuf_string_field(2, AVATAR_BASE_ICON),
        _protobuf_int32_field(5, 0),
        _protobuf_int32_field(6, 0),
    ))
    avatar_frame = b"".join((
        _protobuf_int32_field(1, AVATAR_FRAME_ID),
        _protobuf_string_field(2, AVATAR_FRAME_ICON),
        _protobuf_int32_field(5, 0),
        _protobuf_int32_field(6, 0),
    ))
    return b"".join((
        _protobuf_bytes_field(1, avatar_base),  # avatars_base
        _protobuf_bytes_field(3, avatar_frame),  # frames_base
    ))


AVATARS_DATABASE_PROTO_RAW = build_avatars_database_proto()


SETTINGS_DATABASE_FIELD_ID = 41
SETTING_CURRENT_HOLIDAY = "currentHoliday"
SETTING_CURRENT_SEASON = "currentSeason"


def _build_enum_setting(key: str, allowed_values: tuple[str, ...], current_value: str) -> bytes:
    """Build BaseSettingProto whose BaseParamProto carries a valid enum value.

    P92.b()/P92.c() dereference these settings and then call
    C0296Oq.e().c(), so the settings must exist and have enum_value populated.
    """
    if current_value not in allowed_values:
        raise ValueError(f"{current_value!r} is not in {key} enum")
    enum_values = "enum(" + ",".join(allowed_values) + ")"
    enum_proto = b"".join((
        _protobuf_string_field(1, enum_values),  # BaseParamEnumProto.values
        _protobuf_string_field(2, current_value),  # current_value
    ))
    param_proto = b"".join((
        _protobuf_string_field(1, "enum"),  # BaseParamProto.type
        _protobuf_bytes_field(7, enum_proto),  # enum_value
    ))
    return b"".join((
        _protobuf_string_field(1, key),  # BaseSettingProto.key
        _protobuf_bytes_field(2, param_proto),  # param
    ))


def build_settings_database_proto() -> bytes:
    """Build required global settings consumed during player initialization.

    The client P92.b() requires currentHoliday and P92.c() requires currentSeason.
    An empty SettingsDatabaseProto makes P92.a.get(key) return null, then
    invokes Oq.e() on that null reference.
    """
    holiday = _build_enum_setting(
        SETTING_CURRENT_HOLIDAY,
        ("NONE", "NEW_YEAR", "HALLOWEEN"),
        "NONE",
    )
    season = _build_enum_setting(
        SETTING_CURRENT_SEASON,
        ("SUMMER", "AUTUMN", "WINTER", "SPRING"),
        "AUTUMN",
    )
    return _protobuf_bytes_field(1, holiday) + _protobuf_bytes_field(1, season)


SETTINGS_DATABASE_PROTO = build_settings_database_proto()


def build_vinyl_market_blocks_database_proto() -> bytes:
    """Serialize real BaseVinylBlockProto entries required by QN2.c().

    Database.VinylMarketBlockDatabaseProto.items is repeated field 1.
    Base.BaseVinylBlockProto fields are confirmed from the client's generated
    protobuf descriptor: baseId=1, name=2, isBestsellers=3, depth=4,
    price=5, tax=6, uploadTax=7, maxVinylPerUser=8, minSalesCount=9.
    Money messages are included as valid empty messages (zero-valued money).
    """
    def varint(value: int) -> bytes:
        out = bytearray()
        while value > 0x7F:
            out.append((value & 0x7F) | 0x80)
            value >>= 7
        out.append(value)
        return bytes(out)

    def vfield(number: int, value: int) -> bytes:
        return varint(number << 3) + varint(value)

    def bfield(number: int, value: bytes) -> bytes:
        return varint((number << 3) | 2) + varint(len(value)) + value

    def block(base_id: int, name: str, bestsellers: bool) -> bytes:
        out = bytearray()
        out += vfield(1, base_id)
        out += bfield(2, name.encode("utf-8"))
        if bestsellers:
            out += vfield(3, 1)
        out += vfield(4, 10)              # depth
        out += bfield(5, b"")             # zero price MoneyProto
        out += bfield(7, b"")             # zero uploadTax MoneyProto
        out += vfield(8, 10)              # maxVinylPerUser; VT0 reads this
        return bytes(out)

    # At least one non-bestsellers block is mandatory: VT0 calls QN2.c().d().
    # Keep a separate bestsellers block because QN2.b() searches for it.
    items = (block(1, "default", False), block(2, "bestsellers", True))
    return b"".join(bfield(1, item) for item in items)


VINYL_MARKET_BLOCKS_DATABASE_PROTO = build_vinyl_market_blocks_database_proto()

# The tutorial requests base car ID 147. Build that catalog entry from the
# real Lada 2101 record (source baseId=1), retaining its valid component IDs.
TUTORIAL_CAR_BASE_ID = 147
TUTORIAL_CAR_SOURCE_BASE_ID = 1
TUTORIAL_USER_CAR_ID = 1


def _protobuf_float_field(field_id: int, value: float) -> bytes:
    return _protobuf_varint((field_id << 3) | 5) + struct.pack("<f", float(value))


def _protobuf_signed_int32_field(field_id: int, value: int) -> bytes:
    value = int(value)
    if value < 0:
        value = (1 << 64) + value
    return _protobuf_varint(field_id << 3) + _protobuf_varint(value)


def _protobuf_bool_field(field_id: int, value: bool) -> bytes:
    return _protobuf_int32_field(field_id, 1 if value else 0)


def _db_items(filename: str, root_key: str) -> list[dict]:
    # The user may launch this script from a nested custom-server folder.
    # Walk upward to the repository root instead of assuming __file__/db.
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = []
    current = here
    for _ in range(10):
        candidates.append(os.path.join(current, "db", filename))
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    path = next((candidate for candidate in candidates if os.path.isfile(candidate)), None)
    if path is None:
        raise FileNotFoundError(
            f"cannot find db/{filename} next to server.py or in its parent directories"
        )
    with open(path, "r", encoding="utf-8") as fh:
        root = json.load(fh)
    items = root.get(root_key, {}).get("items")
    if not isinstance(items, list):
        raise RuntimeError(f"{path}: missing {root_key}.items")
    return items


def _db_record(filename: str, root_key: str, wanted_id: int,
               nested_base: bool = True) -> dict:
    items = _db_items(filename, root_key)
    for item in items:
        base = item.get("base") if nested_base else item
        if isinstance(base, dict) and int(base.get("baseId", -1)) == int(wanted_id):
            return item
    raise RuntimeError(f"{filename}: base_id={wanted_id} not found")


def _money_proto(value: dict | None) -> bytes:
    value = value or {}
    fields = (
        (1, "money"), (2, "gold"), (3, "tournamentPoints"),
        (4, "topPoints"), (6, "upgradePoints"),
    )
    return b"".join(
        _protobuf_int32_field(field, int(value.get(key, 0) or 0))
        for field, key in fields if value.get(key, 0)
    )


def _upgrade_base_proto(base: dict) -> bytes:
    out = bytearray()
    int_fields = ((1, "baseId"), (7, "shopIndex"), (10, "level"),
                  (11, "baseSetId"))
    float_fields = ((2, "weight"), (3, "min"), (4, "max"), (9, "control"))
    string_fields = ((6, "icon"), (13, "keyName"),
                     (14, "watermarkIconName"))
    for field, key in int_fields:
        if base.get(key) is not None:
            out += _protobuf_int32_field(field, int(base[key]))
    for field, key in float_fields:
        if base.get(key) is not None:
            out += _protobuf_float_field(field, float(base[key]))
    if base.get("price"):
        out += _protobuf_bytes_field(5, _money_proto(base["price"]))
    for field, key in string_fields:
        if base.get(key):
            out += _protobuf_string_field(field, str(base[key]))
    for value in base.get("carClasses", []) or []:
        out += _protobuf_string_field(12, str(value))
    if base.get("isTradedInMarket") is not None:
        out += _protobuf_bool_field(15, bool(base["isTradedInMarket"]))
    # grade is an enum with a client-specific numeric mapping; omit it and
    # retain the protobuf default instead of guessing an enum value.
    return bytes(out)


def _serialize_car_record(car: dict) -> bytes:
    out = bytearray()
    int_fields = {
        "diskBaseId": 13, "tiresBaseId": 14,
        "frontSuspensionBaseId": 15, "frontSpringBaseId": 16,
        "frontBrakeBaseId": 17, "rearSuspensionBaseId": 18,
        "rearSpringBaseId": 19, "rearBrakeBaseId": 20,
        "baseId": 27, "level": 29, "shopIndex": 31, "baseColor": 32,
        "rearBumperBaseId": 34, "centerBumperBaseId": 35,
        "frontBumperBaseId": 36, "engineBaseId": 37,
        "transmissionBaseId": 42, "maxDiskSize": 43,
        "frontDiskBaseId": 59, "diskBaseColorId": 60,
        "frontDiskBaseColorId": 61, "frontTiresBaseId": 62,
        "frontDiskPartBaseId": 63, "backDiskPartBaseId": 64,
        "frontDiskPartColorId": 65, "backDiskPartColorId": 66,
        "flashId": 67, "spoilerId": 68, "rearDiskSkinBaseId": 70,
        "frontDiskSkinBaseId": 71, "stroboscopeId": 73,
    }
    float_fields = {
        "chassisWidth": 1, "arcRadius": 2, "carMass": 3,
        "massClierence": 4, "massBalance": 5, "clirence": 6,
        "brakeTraction": 7, "driveTraction": 8, "cx": 38,
        "square": 39, "carMassDelta": 44, "gripBonus": 45,
        "baseCx": 56, "baseHp": 57, "baseCarMass": 58,
    }
    bool_fields = {
        "isSwap": 46, "isFrontEngine": 47, "isForbiddenToSwap": 49,
        "isRoll": 50, "isCantInstallSpoiler": 51,
        "isCantInstallFlasher": 54,
    }
    for key, field in int_fields.items():
        if car.get(key) is not None:
            out += _protobuf_int32_field(field, int(car[key]))
    for key, field in float_fields.items():
        if car.get(key) is not None:
            out += _protobuf_float_field(field, float(car[key]))
    for key, field in bool_fields.items():
        if car.get(key) is not None:
            out += _protobuf_bool_field(field, bool(car[key]))
    if car.get("image"):
        out += _protobuf_string_field(21, str(car["image"]))
    if car.get("carClass"):
        out += _protobuf_string_field(30, str(car["carClass"]))
    if car.get("nitroBlowParticle"):
        out += _protobuf_string_field(69, str(car["nitroBlowParticle"]))
    if car.get("price"):
        out += _protobuf_bytes_field(28, _money_proto(car["price"]))
    align = {"LEFT": 0, "CENTER": 1, "RIGHT": 2}
    for key, field in (("frontSupportAlign", 40), ("rearSupportAlign", 41)):
        if car.get(key) is not None:
            name = str(car[key]).upper()
            if name not in align:
                raise RuntimeError(f"unknown {key} enum value: {name}")
            if align[name]:
                out += _protobuf_int32_field(field, align[name])
    return bytes(out)


def _serialize_disk_record(item: dict) -> bytes:
    return b"".join((
        _protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))),
        _protobuf_float_field(2, item.get("radius", 0)),
        _protobuf_string_field(3, item.get("image", "")),
    ))


def _serialize_tires_record(item: dict) -> bytes:
    out = bytearray(_protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))))
    for field, key in ((2, "radius"), (3, "width"), (4, "side"),
                       (5, "friction"), (7, "frictionCoefficient"),
                       (8, "temperatureCoefficient")):
        if item.get(key) is not None:
            out += _protobuf_float_field(field, float(item[key]))
    if item.get("image"):
        out += _protobuf_string_field(6, str(item["image"]))
    if item.get("color") is not None:
        out += _protobuf_int32_field(9, int(item["color"]))
    return bytes(out)


def _serialize_spring_record(item: dict) -> bytes:
    out = bytearray(_protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))))
    if item.get("frequency") is not None:
        out += _protobuf_float_field(2, float(item["frequency"]))
    if item.get("image"):
        out += _protobuf_string_field(3, str(item["image"]))
    return bytes(out)


def _serialize_suspension_record(item: dict) -> bytes:
    out = bytearray(_protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))))
    if item.get("damping") is not None:
        out += _protobuf_float_field(2, float(item["damping"]))
    for field, key in ((3, "cylinderImage"), (4, "pistonImage")):
        if item.get(key):
            out += _protobuf_string_field(field, str(item[key]))
    return bytes(out)


def _serialize_brake_record(item: dict) -> bytes:
    out = bytearray(_protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))))
    if item.get("radius") is not None:
        out += _protobuf_float_field(2, float(item["radius"]))
    if item.get("supportWidth") is not None:
        out += _protobuf_float_field(3, float(item["supportWidth"]))
    for field, key in ((4, "type"), (5, "image"), (6, "supportImage")):
        if item.get(key):
            out += _protobuf_string_field(field, str(item[key]))
    return bytes(out)


def _serialize_parts_record(item: dict) -> bytes:
    out = bytearray(_protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))))
    if item.get("type"):
        out += _protobuf_string_field(2, str(item["type"]))
    for field, key in ((3, "rimSize"), (4, "rimRazval"), (5, "weightDelta")):
        if item.get(key) is not None:
            out += _protobuf_float_field(field, float(item[key]))
    return bytes(out)


def _serialize_engine_record(item: dict) -> bytes:
    out = bytearray(_protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))))
    if item.get("volume") is not None:
        out += _protobuf_float_field(2, float(item["volume"]))
    if item.get("cutOffRpm") is not None:
        out += _protobuf_float_field(3, float(item["cutOffRpm"]))
    for point in item.get("dynoPoints", []) or []:
        point_proto = b"".join((
            _protobuf_float_field(1, float(point.get("rpm", 0))),
            _protobuf_float_field(2, float(point.get("torque", 0))),
        ))
        out += _protobuf_bytes_field(4, point_proto)
    for value in item.get("classes", []) or []:
        out += _protobuf_string_field(5, str(value))
    # The source JSON omits the engine-type enum. Keep its protobuf default.
    return bytes(out)


def _serialize_transmission_record(item: dict) -> bytes:
    out = bytearray(_protobuf_bytes_field(1, _upgrade_base_proto(item.get("base", {}))))
    for gear in item.get("gears", []) or []:
        gear_proto = (
            _protobuf_signed_int32_field(1, int(gear.get("gearNumber", 0)))
            + _protobuf_float_field(2, float(gear.get("gearValue", 0)))
        )
        out += _protobuf_bytes_field(2, gear_proto)
    if item.get("mainGear") is not None:
        out += _protobuf_float_field(3, float(item["mainGear"]))
    if item.get("shiftSpeed") is not None:
        out += _protobuf_float_field(4, float(item["shiftSpeed"]))
    return bytes(out)


def _serialize_color_record(item: dict) -> bytes:
    out = bytearray()
    if item.get("baseId") is not None:
        out += _protobuf_int32_field(1, int(item["baseId"]))
    if item.get("price"):
        out += _protobuf_bytes_field(2, _money_proto(item["price"]))
    color_type = {"COLOR": 0, "TINT": 1}.get(str(item.get("type", "COLOR")).upper(), 0)
    if color_type:
        out += _protobuf_int32_field(4, color_type)
    if item.get("shopIndex") is not None:
        out += _protobuf_int32_field(5, int(item["shopIndex"]))
    for color in item.get("colors", []) or []:
        color_proto = b""
        if color.get("color") is not None:
            color_proto += _protobuf_int32_field(1, int(color["color"]))
        if color.get("delta") is not None:
            color_proto += _protobuf_float_field(2, float(color["delta"]))
        out += _protobuf_bytes_field(7, color_proto)
    return bytes(out)


def _catalog_proto(items: list[dict], serializer) -> bytes:
    return b"".join(_protobuf_bytes_field(1, serializer(item)) for item in items)


def build_tutorial_car_catalogs() -> dict[int, bytes]:
    source_car = next(
        (item for item in _db_items("carDatabase.json", "carDatabase")
         if int(item.get("baseId", -1)) == TUTORIAL_CAR_SOURCE_BASE_ID),
        None,
    )
    if source_car is None:
        raise RuntimeError(
            f"db/carDatabase.json has no source base_id={TUTORIAL_CAR_SOURCE_BASE_ID}"
        )
    # Clone the complete Lada 2101 record under the ID requested by the
    # tutorial. Keep all component IDs unchanged so every referenced catalog
    # record resolves normally on the client.
    car = dict(source_car)
    car["baseId"] = TUTORIAL_CAR_BASE_ID
    # The client resolves both rear and front wheel catalogs while building
    # C0259Mn. The JSON omits the front IDs for this starter, so explicitly
    # reuse the matching rear disk/tires instead of leaving IDs at zero.
    car["frontDiskBaseId"] = int(car.get("frontDiskBaseId") or car["diskBaseId"])
    car["frontTiresBaseId"] = int(car.get("frontTiresBaseId") or car["tiresBaseId"])

    disk = _db_record("diskDatabase.json", "diskDatabase", int(car["diskBaseId"]))
    tires = _db_record("tiresDatabase.json", "tiresDatabase", int(car["tiresBaseId"]))
    springs = [
        _db_record("springDatabase.json", "springDatabase", int(car[key]))
        for key in ("frontSpringBaseId", "rearSpringBaseId")
    ]
    suspension = _db_record("suspensionDatabase.json", "suspensionDatabase",
                            int(car["frontSuspensionBaseId"]))
    brakes = [
        _db_record("brakeDatabase.json", "brakeDatabase", int(car[key]))
        for key in ("frontBrakeBaseId", "rearBrakeBaseId")
    ]
    parts = [
        _db_record("partsDatabase.json", "partsDatabase", int(car[key]))
        for key in ("frontBumperBaseId", "centerBumperBaseId", "rearBumperBaseId")
    ]
    engine = _db_record("engineDatabase.json", "engineDatabase", int(car["engineBaseId"]))
    transmission = _db_record("transmissionDatabase.json", "transmissionDatabase",
                              int(car["transmissionBaseId"]))
    color = _db_record("colorDatabase.json", "colorDatabase", int(car["baseColor"]),
                       nested_base=False)

    return {
        1: _protobuf_bytes_field(1, _serialize_car_record(car)),
        2: _catalog_proto([disk], _serialize_disk_record),
        3: _catalog_proto([tires], _serialize_tires_record),
        4: _catalog_proto(springs, _serialize_spring_record),
        5: _catalog_proto([suspension], _serialize_suspension_record),
        7: _catalog_proto(brakes, _serialize_brake_record),
        9: _catalog_proto(parts, _serialize_parts_record),
        15: _catalog_proto([transmission], _serialize_transmission_record),
        16: _catalog_proto([color], _serialize_color_record),
        26: _catalog_proto([engine], _serialize_engine_record),
    }


try:
    TUTORIAL_CAR_DATABASE_PROTOS = build_tutorial_car_catalogs()
    TUTORIAL_CAR_DATABASE_PROTO = TUTORIAL_CAR_DATABASE_PROTOS[1]
except Exception:
    # When started by double-click on Windows, keep the console visible so
    # a missing JSON file or malformed catalog is not hidden by instant exit.
    import traceback
    print("\\nERROR: failed to build the starter-car database catalogs.", file=sys.stderr, flush=True)
    traceback.print_exc()
    if __name__ == "__main__":
        try:
            input("\\nPress Enter to close...")
        except EOFError:
            pass
    raise


def build_tutorial_car_settings_proto() -> bytes:
    # jG.f6(CarSettingsProto) reads the packed data buffer directly.
    # It consumes 39 fixed bytes, then four versioned manager blocks:
    # GearSetManager, IgnitionTimeSetManager, TiresPSISetManager,
    # SuspensionSetManager. Each empty manager is: uint16 version=1,
    # int32 current_page=0, int32 item_count=0.
    fixed = struct.pack(
        ">ffiiiiBfffBB",
        0.0, 0.0,       # muffler offsets
        1, 3, 2, 2,     # RPM settings: e, g, f, h
        0,              # launch control
        0.0, 0.0, 0.0,  # i, j, p
        0, 0,           # nitro enabled, visible spoiler
    )
    empty_manager = struct.pack(">Hii", 1, 0, 0)
    packed_data = fixed + empty_manager * 4
    assert len(fixed) == 39 and len(packed_data) == 79
    # CarSettingsProto.data is field 24 (bytes).
    return _protobuf_bytes_field(24, packed_data)


def build_tutorial_user_car_proto(base_id: int) -> bytes:
    # UserCarProto: id=field 1, base_id=field 2,
    # number=field 34, settings=field 35.
    #
    # OG2.r1() unconditionally calls ME.f6(getSettings()). jG.f6() then
    # reads three floats immediately from CarSettingsProto.data; an absent
    # settings message yields an empty buffer and BufferUnderflowException
    # at ByteBuffer.getFloat() (jG.q7, called from OG2.r1).
    car_number = b"".join((
        _protobuf_int32_field(1, TUTORIAL_USER_CAR_ID),  # car_id
        _protobuf_int32_field(2, 1),                     # region
        _protobuf_int32_field(3, 1),                     # number
        _protobuf_int32_field(5, 0),                     # country=RU
    ))
    car_settings = build_tutorial_car_settings_proto()
    return b"".join((
        _protobuf_int32_field(1, TUTORIAL_USER_CAR_ID),
        _protobuf_int32_field(2, int(base_id)),
        _protobuf_bytes_field(34, car_number),
        _protobuf_bytes_field(35, car_settings),
    ))




def _build_database_proto_with_crc(target_crc32: int) -> tuple[bytes, bytes, bytes]:
    """Add a harmless unknown protobuf field to AvatarsDatabaseProto so the
    complete DatabaseProto CRC matches the value required by this client build.

    Protobuf parsers preserve unknown fields. The avatar catalog records remain
    unchanged; field 1000 is deliberately unused by the game schema.
    """
    def outer(avatar_proto: bytes) -> bytes:
        chunks = []
        for field_id in DATABASE_FIELD_IDS:
            if field_id == CHAMPIONSHIP_DATABASE_FIELD_ID:
                value = CHAMPIONSHIP_DATABASE_PROTO
            elif field_id == SETTINGS_DATABASE_FIELD_ID:
                value = SETTINGS_DATABASE_PROTO
            elif field_id == VINYL_MARKET_BLOCK_DATABASE_FIELD_ID:
                value = VINYL_MARKET_BLOCKS_DATABASE_PROTO
            elif field_id == AVATARS_DATABASE_FIELD_ID:
                value = avatar_proto
            else:
                value = TUTORIAL_CAR_DATABASE_PROTOS.get(field_id, b"")
            chunks.append(_protobuf_bytes_field(field_id, value))
        return b"".join(chunks)

    marker = lambda patch: _protobuf_bytes_field(1000, patch)
    base_avatar = AVATARS_DATABASE_PROTO_RAW + marker(b"\x00" * 4)
    base_crc = zlib.crc32(outer(base_avatar)) & 0xFFFFFFFF
    columns = []
    for bit in range(32):
        patch = bytearray(4)
        patch[bit // 8] ^= 1 << (bit % 8)
        columns.append((zlib.crc32(outer(AVATARS_DATABASE_PROTO_RAW + marker(bytes(patch)))) & 0xFFFFFFFF) ^ base_crc)

    rhs = target_crc32 ^ base_crc
    rows = []
    for out_bit in range(32):
        mask = sum(((columns[var_bit] >> out_bit) & 1) << var_bit for var_bit in range(32))
        rows.append([mask, (rhs >> out_bit) & 1])
    pivot = 0
    pivot_columns = []
    for col in range(32):
        selected = next((r for r in range(pivot, 32) if (rows[r][0] >> col) & 1), None)
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        for r in range(32):
            if r != pivot and ((rows[r][0] >> col) & 1):
                rows[r][0] ^= rows[pivot][0]
                rows[r][1] ^= rows[pivot][1]
        pivot_columns.append(col)
        pivot += 1
    if pivot != 32:
        raise RuntimeError("could not solve DatabaseProto CRC adjustment")
    solution = 0
    for row, col in enumerate(pivot_columns):
        if rows[row][1]:
            solution |= 1 << col
    patch = bytes((solution >> (8 * i)) & 0xFF for i in range(4))
    avatar_proto = AVATARS_DATABASE_PROTO_RAW + marker(patch)
    database_proto = outer(avatar_proto)
    actual = zlib.crc32(database_proto) & 0xFFFFFFFF
    if actual != target_crc32:
        raise RuntimeError(f"DatabaseProto CRC adjustment failed: {actual:08X} != {target_crc32:08X}")
    return avatar_proto, database_proto, patch


AVATARS_DATABASE_PROTO, BOOTSTRAP_DATABASE_PROTO, DATABASE_CRC_PATCH = _build_database_proto_with_crc(TARGET_DATABASE_CRC32)
BOOTSTRAP_DATABASE_CRC32 = zlib.crc32(BOOTSTRAP_DATABASE_PROTO) & 0xFFFFFFFF


def build_bootstrap_database_proto() -> bytes:
    """Serialize DatabaseProto with settings, championship, vinyl blocks and avatar catalogs."""
    out = bytearray()
    for field_id in DATABASE_FIELD_IDS:
        if field_id == CHAMPIONSHIP_DATABASE_FIELD_ID:
            value = CHAMPIONSHIP_DATABASE_PROTO
        elif field_id == SETTINGS_DATABASE_FIELD_ID:
            value = SETTINGS_DATABASE_PROTO
        elif field_id == VINYL_MARKET_BLOCK_DATABASE_FIELD_ID:
            value = VINYL_MARKET_BLOCKS_DATABASE_PROTO
        elif field_id == AVATARS_DATABASE_FIELD_ID:
            value = AVATARS_DATABASE_PROTO
        else:
            value = TUTORIAL_CAR_DATABASE_PROTOS.get(field_id, b"")
        out.extend(_protobuf_bytes_field(field_id, value))
    return bytes(out)


# The CRC-adjusted serialized bytes above are authoritative for this client
# build. Keep the builder available for structural tests and guard against drift.
if build_bootstrap_database_proto() != BOOTSTRAP_DATABASE_PROTO:
    raise RuntimeError("DatabaseProto builder diverged from CRC-adjusted payload")
if (
    len(DATABASE_FIELD_IDS) != 85
    or len(CHAMPIONSHIP_LEVELS) != 8
    or len(SETTINGS_DATABASE_PROTO) == 0
    or len(AVATARS_DATABASE_PROTO) == 0
    or len(VINYL_MARKET_BLOCKS_DATABASE_PROTO) == 0
):
    raise RuntimeError(
        "bootstrap DatabaseProto layout mismatch: "
        f"fields={len(DATABASE_FIELD_IDS)}, "
        f"championship_bytes={len(CHAMPIONSHIP_DATABASE_PROTO)}, "
        f"settings_bytes={len(SETTINGS_DATABASE_PROTO)}, "
        f"avatars_bytes={len(AVATARS_DATABASE_PROTO)}, "
        f"vinyl_blocks_bytes={len(VINYL_MARKET_BLOCKS_DATABASE_PROTO)}, "
        f"crc32=0x{BOOTSTRAP_DATABASE_CRC32:08X}"
    )


def _read_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while offset < len(data) and shift <= 63:
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, offset
        shift += 7
    raise ValueError("invalid or truncated protobuf varint")


def parse_length_prefixed_proto(packet_body: bytes) -> bytes:
    """Return the protobuf bytes inside fB1's uint32-length-prefixed body."""
    if len(packet_body) < 4:
        raise ValueError("protobuf body is missing its 4-byte length prefix")
    declared = struct.unpack_from(">I", packet_body, 0)[0]
    actual = len(packet_body) - 4
    if declared != actual:
        raise ValueError(
            f"protobuf length prefix says {declared}, but {actual} bytes follow"
        )
    return packet_body[4:]


def parse_init_request(packet_body: bytes) -> dict:
    """Read the fields of ProtocolProtoContainer.InitRequest."""
    proto = parse_length_prefixed_proto(packet_body)
    result = {
        "time_zone_id": "UTC",
        "lang": "ru",
        "client_time": 0,
        "is_wi_fi": False,
        "client_platform": "unknown",
    }
    pos = 0
    while pos < len(proto):
        tag, pos = _read_varint(proto, pos)
        field_id, wire_type = tag >> 3, tag & 7
        if field_id == 0:
            raise ValueError("invalid InitRequest field number 0")
        if wire_type == 0:
            value, pos = _read_varint(proto, pos)
            if field_id == 3:
                result["client_time"] = value
            elif field_id == 4:
                result["is_wi_fi"] = bool(value)
        elif wire_type == 1:
            pos += 8
        elif wire_type == 2:
            size, pos = _read_varint(proto, pos)
            end = pos + size
            if end > len(proto):
                raise ValueError("truncated InitRequest length-delimited field")
            value = proto[pos:end]
            if field_id in (1, 2, 5):
                decoded = value.decode("utf-8", errors="strict")
                result[{1: "time_zone_id", 2: "lang", 5: "client_platform"}[field_id]] = decoded
            pos = end
        elif wire_type == 5:
            pos += 4
        else:
            raise ValueError(f"unsupported InitRequest wire type {wire_type}")
        if pos > len(proto):
            raise ValueError("truncated InitRequest field")
    return result


def _stable_user_id(login: str) -> int:
    # A compact positive int64 is less likely to break code that also uses
    # IDs as int32 cache keys, while remaining stable for each local account.
    value = int.from_bytes(hashlib.sha256(("drag-streets-user:" + login).encode("utf-8")).digest()[:4], "big")
    return (value & 0x7FFFFFFF) or 1


def _safe_profile_name(value: str) -> str:
    # UserInfoProto.name is displayed directly by the client. Keep the value
    # short, printable, and non-empty; avoid inventing a platform identity.
    cleaned = "".join(ch for ch in value if ch.isprintable())
    cleaned = " ".join(cleaned.split())[:20]
    return cleaned if len(cleaned) >= 2 else "Local Player"


def build_local_chat_proto() -> bytes:
    """Create loaded PUBLIC and PRIVATE rooms required by the startup scene.

    C1925wL.h(PUBLIC) is called during player setup; without a non-empty,
    loaded ChatProto the client throws CHAT_NOT_LOADED. The chat UI also asks
    for PRIVATE, so both built-in room types are present.
    ChatRoomProto: id=1, type=2, messages=3, is_loaded=4, is_locked=5,
    is_banned=6, name=7. DM enum values: PUBLIC=1, PRIVATE=3.
    """
    def room(room_id: str, room_type: int, name: str) -> bytes:
        return b"".join((
            _protobuf_string_field(1, room_id),
            _protobuf_int32_field(2, room_type),
            _protobuf_int32_field(4, 1),  # is_loaded=true
            _protobuf_int32_field(5, 0),  # is_locked=false
            _protobuf_int32_field(6, 0),  # is_banned=false
            _protobuf_string_field(7, name),
        ))

    public_room = room("local-public", 1, "Общий чат")
    private_room = room("local-private", 3, "Личные сообщения")
    return (
        _protobuf_bytes_field(1, public_room)
        + _protobuf_bytes_field(1, private_room)
    )


def build_avatar_unlocked_proto() -> bytes:
    """Mark the fallback avatar and frame IDs as unlocked for a new local user."""
    frame_items_state = _protobuf_int32_field(1, AVATAR_FRAME_ID)
    return b"".join((
        _protobuf_int32_field(1, AVATAR_BASE_ID),  # avatar_base_entity_id
        _protobuf_bytes_field(5, frame_items_state),  # frames_state.unlocked_ids
    ))


def build_local_user_proto(account: dict, lang: str) -> tuple[bytes, int, str]:
    """Build a minimal UserProto accepted by DG2.f6 and the first-user flow.

    Schema is taken from the supplied/recovered User.proto, UserInfo.proto,
    Money.proto, Fuel.proto, and Garage.proto definitions.
    """
    login = str(account.get("login") or "local")[:64]
    name = _safe_profile_name(str(account.get("nickname") or login))
    user_id = _stable_user_id(login)
    language = lang if lang in {"ru", "en", "de", "fr", "es", "pt", "tr", "pl"} else "ru"

    # UserInfoProto: name=1, id=3, lang=4, type=5 (USER=1), level=12.
    user_info = b"".join((
        _protobuf_string_field(1, name),
        _protobuf_int32_field(3, user_id),
        _protobuf_string_field(4, language),
        _protobuf_int32_field(5, 1),
        _protobuf_int32_field(12, 1),
        _protobuf_int32_field(20, AVATAR_BASE_ID),  # avatar_base_entity_id
        _protobuf_int32_field(21, AVATAR_FRAME_ID),  # avatar_frame_id
    ))

    # Starter balances/resources are local test values, not production data.
    money = b"".join((
        _protobuf_int32_field(1, 100000),
        _protobuf_int32_field(2, 100),
    ))
    fuel = b"".join((
        _protobuf_int32_field(1, 0),
        _protobuf_int32_field(3, 100),
    ))
    # GarageProto with current_id=0 and no cars. This is the explicit
    # first-user/no-car state used by the client's initial dealer flow.
    garage = _protobuf_int32_field(1, 0)

    # UserProto: id=1, level=2, money=4, fuel=5, info=6, garage=7,
    # social_type=20 (GPGS=1, first valid proto enum), is_legal=25.
    user = b"".join((
        _protobuf_int32_field(1, user_id),
        _protobuf_int32_field(2, 1),
        _protobuf_bytes_field(4, money),
        _protobuf_bytes_field(5, fuel),
        _protobuf_bytes_field(6, user_info),
        _protobuf_bytes_field(7, garage),
        _protobuf_bytes_field(13, build_local_chat_proto()),  # chat
        _protobuf_int32_field(20, 1),
        _protobuf_int32_field(25, 1),
        _protobuf_string_field(29, "local-public"),  # last_room_id
        _protobuf_bytes_field(64, build_avatar_unlocked_proto()),  # unlock_avatars
    ))
    return user, user_id, name


def build_init_response(packet_body: bytes, account: dict) -> tuple[bytes, dict]:
    """Build a length-prefixed InitResponse containing a minimal local player."""
    request = parse_init_request(packet_body)
    user_proto, user_id, nickname = build_local_user_proto(account, request["lang"])
    time_zone = request["time_zone_id"] or "UTC"

    # ProtocolProtoContainer.InitResponse fields:
    # user=1, team_comp_lobby_exist=2, delta_time=3, time_zone_id=4,
    # bank_discount=5, unread_news_count=6. Use explicit default values.
    response_proto = b"".join((
        _protobuf_bytes_field(1, user_proto),
        _protobuf_int32_field(2, 0),
        _protobuf_int32_field(3, 0),
        _protobuf_string_field(4, time_zone),
        _protobuf_int32_field(5, 0),
        _protobuf_int32_field(6, 0),
    ))
    response_body = struct.pack(">I", len(response_proto)) + response_proto
    info = {
        "user_id": user_id,
        "nickname": nickname,
        "lang": request["lang"],
        "time_zone_id": time_zone,
        "client_platform": request["client_platform"],
        "is_wi_fi": request["is_wi_fi"],
        "client_time": request["client_time"],
        "protobuf_bytes": len(response_proto),
        "body_bytes": len(response_body),
        "chat_rooms": 2,
    }
    return response_body, info


def parse_hash_data_request_types(packet_body: bytes) -> list[int]:
    """Read the fB1 length-prefixed HashDataProto and return its type IDs."""
    if len(packet_body) < 4:
        raise ValueError("HashDataProto is missing its 4-byte length prefix")
    declared = struct.unpack_from(">I", packet_body, 0)[0]
    if declared != len(packet_body) - 4:
        raise ValueError(
            f"HashDataProto length prefix says {declared}, "
            f"but {len(packet_body) - 4} bytes follow"
        )
    proto = packet_body[4:]
    result: list[int] = []
    pos = 0
    while pos < len(proto):
        tag, pos = _read_varint(proto, pos)
        field_number, wire_type = tag >> 3, tag & 7
        if field_number == 0:
            raise ValueError("invalid protobuf field number 0")
        if wire_type == 0:
            value, pos = _read_varint(proto, pos)
            if field_number == 1:
                result.append(value)
        elif wire_type == 1:
            pos += 8
        elif wire_type == 2:
            size, pos = _read_varint(proto, pos)
            end = pos + size
            if end > len(proto):
                raise ValueError("truncated length-delimited protobuf field")
            if field_number == 1:
                packed_pos = pos
                while packed_pos < end:
                    value, packed_pos = _read_varint(proto, packed_pos)
                    result.append(value)
                if packed_pos != end:
                    raise ValueError("invalid packed enum field")
            pos = end
        elif wire_type == 5:
            pos += 4
        else:
            raise ValueError(f"unsupported protobuf wire type {wire_type}")
        if pos > len(proto):
            raise ValueError("truncated protobuf field")
    return result


def _zip_database_proto(proto_bytes: bytes) -> bytes:
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("database.pb", proto_bytes)
    return archive.getvalue()





def build_bootstrap_database_response() -> bytes:
    """Build count + typed, length-prefixed ZIP blobs for packet 50015.

    Map type IDs are a separate namespace from outer DatabaseProto field IDs:
    type 41 settings, type 64 championship, type 86 avatar catalog. Other
    categories remain present with empty protobuf payloads.
    """
    settings_zip = _zip_database_proto(SETTINGS_DATABASE_PROTO)
    championship_zip = _zip_database_proto(CHAMPIONSHIP_DATABASE_PROTO)
    avatars_zip = _zip_database_proto(AVATARS_DATABASE_PROTO)
    car_database_zip = _zip_database_proto(TUTORIAL_CAR_DATABASE_PROTO)
    # QN2.e() rebuilds its TreeMap from items; an empty proto leaves QN2.c()
    # null and crashes VT0. Supply both normal and bestsellers blocks.
    vinyl_market_blocks_zip = _zip_database_proto(VINYL_MARKET_BLOCKS_DATABASE_PROTO)

    out = bytearray(struct.pack(">I", len(DATABASE_FIELD_IDS)))
    for type_id in DATABASE_FIELD_IDS:
        if type_id == SETTINGS_DATABASE_FIELD_ID:
            payload = settings_zip
        elif type_id == CHAMPIONSHIP_DATABASE_TYPE_ID:
            payload = championship_zip
        elif type_id == AVATARS_DATABASE_TYPE_ID:
            payload = avatars_zip
        elif type_id == VINYL_MARKET_BLOCK_DATABASE_TYPE_ID:
            payload = vinyl_market_blocks_zip
        elif type_id in TUTORIAL_CAR_DATABASE_PROTOS:
            payload = _zip_database_proto(TUTORIAL_CAR_DATABASE_PROTOS[type_id])
        else:
            payload = b""
        out.extend(struct.pack(">I", type_id))
        out.extend(struct.pack(">I", len(payload)))
        out.extend(payload)
    return bytes(out)


BOOTSTRAP_DATABASE_MAP_RESPONSE = build_bootstrap_database_response()
if len(BOOTSTRAP_DATABASE_MAP_RESPONSE) <= 4 + 85 * 8:
    raise RuntimeError("championship database response is missing its zipped section")


# Startup requests discovered in the client sources:
# 9003 (0x232B) is a one-way command (G00.C, no callback), so it must not
# receive a response. 9011 (0x2333) requests friend requests and has a callback.
# 990045 (0xF1B5D) is an EventCommandProto with scheduleInfo set; its callback
# requires EventCommandProto.ResultProto.scheduleInfoResult.
EMPTY_FRIEND_REQUESTS_RESPONSE = b""
# ResultProto.scheduleInfoResult (field 3) ->
# GetEventScheduleInfoProto.ResultProto.eventInfoContainer (field 1) ->
# empty EventInfoContainerProto. No active event is represented by no instance
# and no schedule; the client converter explicitly handles this state.
EMPTY_EVENT_SCHEDULE_RESULT_PROTO = bytes.fromhex("1A 02 0A 00")
# fB1.r() reads protobuf messages from a uint32-length-prefixed buffer.
# The command callback uses the same framing as InitResponse/checkBan.
EMPTY_EVENT_SCHEDULE_RESULT_BODY = (
    struct.pack(">I", len(EMPTY_EVENT_SCHEDULE_RESULT_PROTO))
    + EMPTY_EVENT_SCHEDULE_RESULT_PROTO
)

PACKET_NAMES = {
    1: "getContentVersion",
    2: "getContentPart",
    3: "getPatchContainer",
    4: "getPatchFile",
    5: "checkVersion",
    6: "ping",
    7: "connect",
    100: "reserved",
    1803: "checkBan",
    1910: "initRequest",
    50015: "database",
    206: "getTutorialUserCar",
    9003: "oneWayStartupCommand",
    9011: "getFriendRequests",
    990045: "eventCommand.scheduleInfo",
    990024: "vkAuth",
}

LOGIN_RE = re.compile(r"^[a-z0-9._-]{3,32}$")
REGISTER_RE = re.compile(r"^[a-z0-9._-]{3,24}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def pkcs5_pad(data: bytes) -> bytes:
    n = 16 - (len(data) % 16)
    return data + bytes([n]) * n


def pkcs5_unpad(data: bytes) -> bytes:
    if not data or len(data) % 16:
        raise ValueError("not a padded AES block")
    n = data[-1]
    if n < 1 or n > 16 or data[-n:] != bytes([n]) * n:
        raise ValueError("bad PKCS5 padding")
    return data[:-n]


def aes_encrypt(key: bytes, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    enc = cipher.encryptor()
    return enc.update(pkcs5_pad(data)) + enc.finalize()


def aes_decrypt(key: bytes, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    dec = cipher.decryptor()
    return pkcs5_unpad(dec.update(data) + dec.finalize())


def derive_key(connect_body: bytes) -> bytes:
    if len(connect_body) != 8:
        raise ValueError(f"connect body is {len(connect_body)} bytes, expected 8")
    sent = struct.unpack(">Q", connect_body)[0]
    random = (sent ^ CONNECT_XOR) & 0xFFFFFFFFFFFFFFFF
    raw = random.to_bytes(8, "big")
    return raw + raw


def make_frame(
    packet_id: int,
    status: int,
    sequence: int,
    body: bytes,
    key: Optional[bytes] = None,
    encrypt: bool = False,
) -> bytes:
    wire_body = aes_encrypt(key, body) if (encrypt and key is not None) else body
    payload = (
        b"\x00" * 32
        + struct.pack(">III", packet_id, status, sequence)
        + wire_body
    )
    return struct.pack(">I", len(payload)) + payload


def parse_frame(data: bytes):
    if len(data) >= 44:
        digest = data[:32]
        packet_id, status, sequence = struct.unpack(">III", data[32:44])
        body = data[44:]
    elif len(data) >= 12:
        digest = None
        packet_id, status, sequence = struct.unpack(">III", data[:12])
        body = data[12:]
    else:
        raise ValueError(f"frame too short: {len(data)}")
    return digest, packet_id, status, sequence, body


def recv_exact(sock: socket.socket, size: int) -> Optional[bytes]:
    chunks = []
    remaining = size
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            return None
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def hexdump(data: bytes, limit: int = 512) -> str:
    shown = data[:limit]
    text = shown.hex(" ")
    if len(data) > limit:
        text += f" ... ({len(data)} bytes total)"
    return text


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

class ServerState:
    def __init__(self, base_dir: str, check_version: int,
                 content_check_version: int, content_ports: set[int],
                 answer_init: bool, db_response: Optional[bytes],
                 host: str = "127.0.0.1"):
        self.base_dir = base_dir
        self.log_dir = os.path.join(base_dir, "logs")
        self.capture_dir = os.path.join(base_dir, "captures")
        self.account_file = os.path.join(base_dir, "accounts.json")
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.capture_dir, exist_ok=True)

        self.check_version = check_version
        self.content_check_version = content_check_version
        self.content_ports = set(content_ports)
        self.answer_init = answer_init
        self.db_response = db_response  # None => dynamically build explicit empty DB sections
        self.host = host

        self._log_lock = threading.Lock()
        self._accounts_lock = threading.Lock()
        self.accounts = self._load_accounts()
        self.active_account = {"login": "local", "nickname": "Local Player"}
        self.stop_event = threading.Event()

    # -- logging ---------------------------------------------------------
    def log(self, message: str) -> None:
        line = f"[{utc_now()}] {message}"
        with self._log_lock:
            print(line, flush=True)
            try:
                with open(os.path.join(self.log_dir, "server.log"), "a",
                          encoding="utf-8") as fh:
                    fh.write(line + "\n")
            except OSError:
                pass

    def log_packet(self, port: int, remote: str, packet_id: int, status: int,
                   sequence: int, body: bytes, encrypted: bool) -> None:
        name = PACKET_NAMES.get(packet_id, "unknown")
        self.log(
            f"TCP {port} {remote} packet={packet_id}({name}) status={status} "
            f"seq={sequence} enc={encrypted} len={len(body)} body={hexdump(body)}"
        )

    # -- captures --------------------------------------------------------
    def save_capture(self, port: int, packet_id: int, body: bytes) -> str:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        name = f"{packet_id}-{port}-{stamp}.bin"
        path = os.path.join(self.capture_dir, name)
        with open(path, "wb") as fh:
            fh.write(body)
        with open(path + ".txt", "w", encoding="utf-8") as fh:
            fh.write(f"packet={packet_id} port={port} len={len(body)}\n")
            fh.write(body.hex(" ") + "\n")
        self.log(f"saved capture {path}")
        return path

    # -- accounts --------------------------------------------------------
    def _load_accounts(self) -> dict:
        try:
            with open(self.account_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                return data
        except (OSError, ValueError):
            pass
        return {}

    def _save_accounts(self) -> None:
        tmp = self.account_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.accounts, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, self.account_file)

    def token_for(self, login: str) -> str:
        digest = hashlib.sha256(("drag-streets-local:" + login).encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")

    def upsert_account(self, login: str, password: str, nickname: str) -> dict:
        with self._accounts_lock:
            record = self.accounts.get(login)
            if record is None:
                record = {
                    "login": login,
                    "password": password,
                    "nickname": nickname,
                    "token": self.token_for(login),
                }
            else:
                record["password"] = password
                if nickname:
                    record["nickname"] = nickname
                if len(record.get("token", "")) != 43:
                    record["token"] = self.token_for(login)
            self.accounts[login] = record
            self._save_accounts()
            return dict(record)

    def login_account(self, login: str, password: str) -> dict:
        with self._accounts_lock:
            record = self.accounts.get(login)
        if record is None:
            return self.upsert_account(login, password, login)
        # Local test server: accept every password, but keep the record stable.
        with self._accounts_lock:
            record["password"] = password
            self.accounts[login] = record
            self._save_accounts()
        return dict(record)

    def session_account(self, token: str) -> dict:
        with self._accounts_lock:
            for record in self.accounts.values():
                if record.get("token") == token:
                    account = dict(record)
                    self.active_account = {"login": account["login"], "nickname": account["nickname"]}
                    return account
        # Unknown token: keep the client's 43-char token and use a local profile.
        login = "local"
        account = {
            "login": login,
            "nickname": "Local Player",
            "token": token if len(token) == 43 else self.token_for(login),
        }
        with self._accounts_lock:
            self.active_account = {"login": account["login"], "nickname": account["nickname"]}
        return account


# ---------------------------------------------------------------------------
# HTTP auth
# ---------------------------------------------------------------------------

class AuthHandler(BaseHTTPRequestHandler):
    server_version = "DragStreetsLocalAuth/1.0"
    state: ServerState  # set on the server object at runtime

    def log_message(self, fmt, *args):  # silence default noisy logging
        pass

    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        raw = self.rfile.read(length) if length else b"{}"
        try:
            value = json.loads(raw.decode("utf-8"))
            return value if isinstance(value, dict) else {}
        except (ValueError, UnicodeDecodeError):
            return {}

    def _bearer(self) -> str:
        value = self.headers.get("Authorization", "")
        if value.lower().startswith("bearer "):
            return value[7:].strip()
        return ""

    def do_POST(self):
        state: ServerState = self.server.state  # type: ignore[attr-defined]
        path = self.path.split("?", 1)[0]
        payload = self._read_json()
        state.log(f"HTTP {self.client_address[0]} POST {path} body={payload!r}")

        if path == "/v1/auth/register":
            login = str(payload.get("login", "")).strip().lower()
            password = str(payload.get("password", ""))
            nickname = str(payload.get("nickname", "") or login).strip() or login
            if not REGISTER_RE.fullmatch(login) or not password:
                self._send_json(400, {"error": "invalid_login"})
                return
            record = state.upsert_account(login, password, nickname)
            self._send_json(200, {
                "token": record["token"],
                "login": record["login"],
                "nickname": record["nickname"],
            })
            return

        if path == "/v1/auth/login":
            login = str(payload.get("login", "")).strip().lower()
            password = str(payload.get("password", ""))
            if not LOGIN_RE.fullmatch(login) or not password:
                self._send_json(400, {"error": "invalid_login"})
                return
            record = state.login_account(login, password)
            self._send_json(200, {
                "token": record["token"],
                "login": record["login"],
                "nickname": record["nickname"],
            })
            return

        if path == "/v1/auth/session":
            token = self._bearer()
            if not token:
                self._send_json(401, {"error": "unauthorized"})
                return
            record = state.session_account(token)
            self._send_json(200, {
                "token": record["token"],
                "login": record["login"],
                "nickname": record["nickname"],
            })
            return

        if path == "/v1/auth/logout":
            self._send_json(200, {})
            return

        self._send_json(404, {"error": "not_found"})

    def do_GET(self):
        self._send_json(405, {"error": "post_required"})


class AuthServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, handler, state: ServerState):
        super().__init__(address, handler)
        self.state = state


# ---------------------------------------------------------------------------
# TCP game gateway
# ---------------------------------------------------------------------------

class GameConnection(threading.Thread):
    def __init__(self, conn: socket.socket, remote: str, port: int,
                 state: ServerState):
        super().__init__(daemon=True, name=f"game-{port}-{remote}")
        self.conn = conn
        self.remote = remote
        self.port = port
        self.state = state
        self.key: Optional[bytes] = None
        self.handshook = False
        self.database_request_types: list[int] = []

    def send_packet(self, packet_id: int, sequence: int, body: bytes,
                    encrypt: bool, status: int = 0) -> None:
        frame = make_frame(packet_id, status, sequence, body, self.key, encrypt)
        self.conn.sendall(frame)

    def run(self) -> None:
        self.state.log(f"TCP {self.port} connection from {self.remote}")
        try:
            self.conn.settimeout(600)
            while not self.state.stop_event.is_set():
                header = recv_exact(self.conn, 4)
                if header is None:
                    break
                length = struct.unpack(">I", header)[0]
                if length < 12 or length > MAX_FRAME:
                    self.state.log(
                        f"TCP {self.port} {self.remote} invalid frame length {length}; closing"
                    )
                    break
                data = recv_exact(self.conn, length)
                if data is None:
                    break
                self.handle_frame(data)
        except (ConnectionResetError, ConnectionAbortedError, socket.timeout,
                OSError) as exc:
            self.state.log(f"TCP {self.port} {self.remote} connection ended: {exc!r}")
        except Exception as exc:  # keep one bad connection from killing the server
            self.state.log(f"TCP {self.port} {self.remote} handler error: {exc!r}")
        finally:
            try:
                self.conn.close()
            except OSError:
                pass
            self.state.log(f"TCP {self.port} {self.remote} closed")

    def handle_frame(self, data: bytes) -> None:
        digest, packet_id, status, sequence, wire_body = parse_frame(data)
        body = wire_body
        encrypted = False

        # Ping is deliberately not encrypted by the client's decoder.  For every
        # other packet after connect, try AES first; fall back to plaintext so a
        # malformed/unexpected frame is still logged instead of dropping the link.
        if self.handshook and packet_id != 6 and wire_body:
            if self.key is not None and len(wire_body) % 16 == 0:
                try:
                    body = aes_decrypt(self.key, wire_body)
                    encrypted = True
                except Exception:
                    body = wire_body
            elif not wire_body:
                body = b""
        elif self.handshook and packet_id == 6:
            body = wire_body

        self.state.log_packet(self.port, self.remote, packet_id, status,
                              sequence, body, encrypted)

        if packet_id == 7:  # connect
            if not wire_body:
                self.state.log(f"TCP {self.port} {self.remote} connect without body")
                return
            try:
                self.key = derive_key(wire_body)
            except ValueError as exc:
                self.state.log(f"TCP {self.port} {self.remote} bad connect: {exc}")
                return
            self.handshook = True
            # Echo the exact 8 plaintext bytes; the client derives the key from them.
            self.send_packet(7, sequence, wire_body, encrypt=False)
            self.state.log(
                f"TCP {self.port} {self.remote} connect accepted; "
                f"AES key={self.key.hex()}"
            )
            return

        if packet_id == 3:  # getPatchContainer -> result code + PatchContainerProto
            # The response body starts with an application-level int32 result.
            # The client interprets those first four bytes as the result code;
            # sending protobuf bytes there makes them appear as an error number.
            # 00 00 00 00 means success; the remaining empty protobuf means
            # there are no patch files.
            self.send_packet(3, sequence, EMPTY_PATCH_CONTAINER_BODY, encrypt=True)
            self.state.log(
                f"TCP {self.port} {self.remote} getPatchContainer answered "
                f"result=0, empty manifest (wire body={EMPTY_PATCH_CONTAINER_BODY.hex(' ')})"
            )
            return

        if packet_id == 5:  # checkVersion -> 8-byte long
            # Content channels (8993/8995) check the patch/content version.
            # Logic channels (8992/8994) use this value as the expected CRC32
            # of the DatabaseProto assembled after packet 50015.
            is_content_channel = self.port in self.state.content_ports
            version_value = (
                self.state.content_check_version
                if is_content_channel else self.state.check_version
            )
            self.send_packet(5, sequence, struct.pack(">q", version_value),
                             encrypt=True)
            if is_content_channel:
                detail = "content channel version"
            else:
                detail = "bootstrap DatabaseProto CRC32 (settings + championship + vinyl blocks + avatars)"
            self.state.log(
                f"TCP {self.port} {self.remote} checkVersion answered with "
                f"{version_value} (0x{version_value & 0xFFFFFFFF:08X}; {detail})"
            )
            return

        if packet_id == 1803:  # checkBan -> length-prefixed CheckBanResponseProto
            # fB1.r() first reads a 4-byte big-endian message length. Sending
            # an empty packet body makes Netty throw:
            # readerIndex(0) + length(4) exceeds writerIndex(0).
            self.send_packet(1803, sequence, CHECK_BAN_OK_BODY, encrypt=True)
            self.state.log(
                f"TCP {self.port} {self.remote} checkBan answered OK "
                f"(protobuf_len={len(CHECK_BAN_OK_PROTO)}, "
                f"wire body={CHECK_BAN_OK_BODY.hex(' ')})"
            )
            return

        if packet_id == 50015:  # database -> count + typed, length-prefixed table blobs
            request_types: list[int] = []
            try:
                request_types = parse_hash_data_request_types(body)
                if request_types:
                    self.database_request_types = list(dict.fromkeys(request_types))
            except ValueError as exc:
                self.state.log(
                    f"TCP {self.port} {self.remote} database request parse warning: {exc}"
                )

            if self.state.db_response is not None:
                response_body = self.state.db_response
                response_mode = "custom db-response override"
            elif request_types:
                # Return the requested map categories. The current bootstrap
                # request contains all 85 known categories.
                response_body = BOOTSTRAP_DATABASE_MAP_RESPONSE
                response_mode = (
                    "85 sections with settings, championship leagues 1..8, "
                    "avatar base/frame ID 1, and initialized vinyl-market blocks (default + bestsellers)"
                )
            else:
                # An empty HashDataProto requests no categories. Do not replay
                # the full database: the client sends this as a separate
                # follow-up and expects an empty count-prefixed map response.
                response_body = struct.pack(">I", 0)
                response_mode = "empty response (client requested 0 categories)"

            self.send_packet(50015, sequence, response_body, encrypt=True)
            req_count = len(request_types)
            remembered_count = len(self.database_request_types)
            self.state.log(
                f"TCP {self.port} {self.remote} database answered {response_mode}; "
                f"request_types={req_count}, remembered_types={remembered_count}, "
                f"response_bytes={len(response_body)}, "
                f"database_crc32=0x{BOOTSTRAP_DATABASE_CRC32:08X}, "
                f"settings_proto_bytes={len(SETTINGS_DATABASE_PROTO)}, "
                f"championship_proto_bytes={len(CHAMPIONSHIP_DATABASE_PROTO)}, "
                f"avatars_proto_bytes={len(AVATARS_DATABASE_PROTO)}, "
                f"vinyl_market_blocks_proto_bytes={len(VINYL_MARKET_BLOCKS_DATABASE_PROTO)} "
                f"(avatar_base={AVATAR_BASE_ID}, frame={AVATAR_FRAME_ID})"
            )
            return

        if packet_id == 535:  # client/server clock synchronization
            # ct2.h(fB1) reads one 64-bit server timestamp via fB1.u().
            server_time_ms = int(time.time() * 1000)
            response_body = struct.pack(">Q", server_time_ms)
            self.send_packet(535, sequence, response_body, encrypt=True)
            self.state.log(
                f"TCP {self.port} {self.remote} time sync answered: "
                f"server_time_ms={server_time_ms}"
            )
            return

        if packet_id == 1408:  # tutorial progress/state update
            # The client sends a single 32-bit tutorial step. Its response
            # parser reads a 32-bit value; never leave this request unanswered.
            if len(body) == 4:
                tutorial_step = struct.unpack(">i", body)[0]
                response_body = struct.pack(">i", tutorial_step)
                self.send_packet(1408, sequence, response_body, encrypt=True)
                self.state.log(
                    f"TCP {self.port} {self.remote} tutorial packet 1408 "
                    f"answered: step={tutorial_step}"
                )
            else:
                self.send_packet(1408, sequence, struct.pack(">i", 0), encrypt=True)
                self.state.log(
                    f"TCP {self.port} {self.remote} tutorial packet 1408 "
                    f"invalid length={len(body)}; returned default step=0"
                )
            return

        if packet_id == 206:  # get tutorial UserCarProto by base car ID
            # The profile sent by this server has an empty garage. Returning a
            # fabricated UserCarProto here is unsafe: OG2.r1() resolves its
            # base_id through VD.a(base_id), then C0259Mn.D1() dereferences
            # multiple component catalogs. A base_id-only catalog entry is
            # not a valid car and crashes the Android client.
            if len(body) != 4:
                self.state.log(
                    f"TCP {self.port} {self.remote} packet 206 invalid request "
                    f"length={len(body)}; expected 4-byte base_id"
                )
                self.send_packet(206, sequence, b"", encrypt=True, status=1)
                return
            base_id = struct.unpack(">i", body)[0]
            # OG2.r1() unconditionally parses UserCarProto.number (field 34).
            # An empty UserCarProto gives a default CarNumberProto with region=0;
            # the RU plate formatter indexes region-1 and crashes at r22.d().
            # Supply a structurally valid local plate (RU, region 1, number 1)
            # and a non-zero car ID instead of returning an empty message.
            car_number_proto = b"".join((
                _protobuf_int32_field(1, 1),  # car_id
                _protobuf_int32_field(2, 1),  # region: RU table starts at 1
                _protobuf_int32_field(3, 1),  # number
            ))
            user_car_proto = b"".join((
                _protobuf_int32_field(1, 1),  # UserCarProto.id
                _protobuf_int32_field(2, base_id),
                _protobuf_bytes_field(34, car_number_proto),  # number
                _protobuf_bytes_field(35, build_tutorial_car_settings_proto()),  # settings
            ))
            response_body = struct.pack(">I", len(user_car_proto)) + user_car_proto
            self.send_packet(206, sequence, response_body, encrypt=True)
            self.state.log(
                f"TCP {self.port} {self.remote} packet 206 answered with "
                f"valid length-prefixed UserCarProto for requested_base_id={base_id}; "
                f"catalog_base_id={TUTORIAL_CAR_BASE_ID}, car_id=1, RU region=1, plate_number=1"
            )
            return

        if packet_id == 6:  # ping -> plaintext empty body
            self.send_packet(6, sequence, b"", encrypt=False)
            return

        if packet_id == 9003:  # one-way startup command; client registers no callback
            self.state.log(
                f"TCP {self.port} {self.remote} one-way packet 9003 received; "
                "no response expected by client"
            )
            return

        if packet_id == 9011:  # getFriendRequests -> empty repeated-message list
            # Client callback iterates while at least 4 bytes remain and parses
            # one FriendRequestProto from each remaining buffer. An empty body
            # therefore represents zero friend requests and still completes
            # the request callback (status remains OK).
            self.send_packet(9011, sequence, EMPTY_FRIEND_REQUESTS_RESPONSE,
                             encrypt=True)
            self.state.log(
                f"TCP {self.port} {self.remote} getFriendRequests answered: "
                "empty list (0 records)"
            )
            return

        if packet_id == 990045:  # EventCommandProto.scheduleInfo
            # The client callback uses fB1.r(), which first reads a 4-byte
            # big-endian protobuf length. Prefix the selected ResultProto;
            # its scheduleInfoResult contains an empty EventInfoContainerProto.
            self.send_packet(990045, sequence,
                             EMPTY_EVENT_SCHEDULE_RESULT_BODY, encrypt=True)
            self.state.log(
                f"TCP {self.port} {self.remote} event schedule request answered: "
                f"no active event (length-prefixed ResultProto={EMPTY_EVENT_SCHEDULE_RESULT_BODY.hex(' ')})"
            )
            return

        if packet_id == 1910:  # InitRequest -> InitResponse with a local test profile
            self.state.save_capture(self.port, packet_id, body)
            try:
                response_body, profile = build_init_response(body, self.state.active_account)
            except Exception as exc:
                self.state.log(
                    f"TCP {self.port} {self.remote} InitRequest parse/build failed: {exc!r}; "
                    "sending no response"
                )
                return
            self.send_packet(1910, sequence, response_body, encrypt=True)
            self.state.log(
                f"TCP {self.port} {self.remote} InitResponse sent: "
                f"user_id={profile['user_id']} nickname={profile['nickname']!r} "
                f"lang={profile['lang']!r} timezone={profile['time_zone_id']!r} "
                f"platform={profile['client_platform']!r} "
                f"protobuf_bytes={profile['protobuf_bytes']} "
                f"wire_body_bytes={profile['body_bytes']} encrypted=True; "
                f"chat_rooms={profile['chat_rooms']} "
                f"avatar_base={AVATAR_BASE_ID} frame={AVATAR_FRAME_ID}; "
                "new-player profile with empty garage"
            )
            return

        # Unknown/unimplemented packet: log only.  Do not send a random reply:
        # the client's request table keys replies by packet id and sequence.
        self.state.log(
            f"TCP {self.port} {self.remote} packet {packet_id} left unanswered"
        )


class GameServer(threading.Thread):
    def __init__(self, port: int, state: ServerState):
        super().__init__(daemon=True, name=f"listen-{port}")
        self.port = port
        self.state = state
        self.sock: Optional[socket.socket] = None

    def run(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.state.host, self.port))
        sock.listen(16)
        sock.settimeout(0.5)
        self.sock = sock
        self.state.log(f"TCP listening on {self.state.host}:{self.port}")
        while not self.state.stop_event.is_set():
            try:
                conn, addr = sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            GameConnection(conn, f"{addr[0]}:{addr[1]}", self.port,
                           self.state).start()
        try:
            sock.close()
        except OSError:
            pass
        self.state.log(f"TCP listener {self.port} stopped")

    def stop(self) -> None:
        try:
            if self.sock is not None:
                self.sock.close()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_ports(value: str) -> list[int]:
    ports = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        if "-" in item:
            start, end = item.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(item))
    return ports


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Drag Streets local test server")
    parser.add_argument("--host", default="127.0.0.1",
                        help="bind address (use 0.0.0.0 for a real LAN device)")
    parser.add_argument("--auth-port", type=int, default=8080)
    parser.add_argument("--ports", default="8992-8995",
                        help="game TCP ports, e.g. 8992,8993,8994,8995")
    parser.add_argument(
        "--check-version", type=int, default=BOOTSTRAP_DATABASE_CRC32,
        help=("8-byte long returned on logic ports (8992/8994); default is "
              "CRC32 of the local bootstrap DatabaseProto (required settings, championship, vinyl-block and avatar tables)"),
    )
    parser.add_argument(
        "--content-check-version", type=int, default=0,
        help="8-byte long returned on content ports (8993/8995); default 0",
    )
    parser.add_argument("--no-answer-init", action="store_true",
                        help="debug option: capture InitRequest (1910) without answering")
    parser.add_argument("--db-response", default=None,
                        help="optional file containing a raw custom database-map "
                             "response body for packet 50015; default sends all "
                             "85 database categories, with required settings, championship leagues 1..8, avatar base/frame ID 1, and populated vinyl-market blocks")
    args = parser.parse_args()

    # The client validates the CRC of the reconstructed DatabaseProto. This value
    # is solved against the exact 85-field proto, including vinyl blocks (field 65).
    # Returning that exact value makes AU.c trust the stale local cache and skip
    # packet 50015 entirely, even though the server has repaired database data.
    # Never allow the known stale CRC to be advertised as the server version.
    if (args.check_version & 0xFFFFFFFF) == 0xC0F869C7:
        print(
            "WARNING: supplied --check-version equals the client's stale cache "
            "CRC 0xC0F869C7; overriding it to the current bootstrap CRC "
            f"0x{BOOTSTRAP_DATABASE_CRC32:08X} to force packet 50015."
        , flush=True)
        args.check_version = BOOTSTRAP_DATABASE_CRC32

    db_response = None
    if args.db_response:
        with open(args.db_response, "rb") as fh:
            db_response = fh.read()

    ports = parse_ports(args.ports)
    # The gateway uses paired logic/content listeners: 8992/8993 and 8994/8995.
    # Derive content roles from the configured list so alternate test ports work.
    content_ports = {port + 1 for port in ports if port % 2 == 0 and port + 1 in ports}
    state = ServerState(here, args.check_version, args.content_check_version,
                        content_ports, not args.no_answer_init, db_response, args.host)
    state.log(f"ACTIVE SERVER FILE: {os.path.abspath(__file__)}")
    state.log(f"ACTIVE SERVER ARGV: {sys.argv!r}")
    state.log("InitRequest mode: " + ("capture only" if args.no_answer_init else "local test profile response"))
    state.log(
        "database bootstrap: packet 50015 -> 85 sections; map types settings=41, "
        "championship=64, vinyl_market_blocks=65, avatars=86; protobuf fields championship=64, vinyl_market_blocks=65, avatars=86; "
        "settings currentHoliday/currentSeason; championship leagues 1..8; vinyl blocks default+bestsellers; avatars base/frame id=1 "
        f"(response_bytes={len(BOOTSTRAP_DATABASE_MAP_RESPONSE)}; "
        f"settings_proto_bytes={len(SETTINGS_DATABASE_PROTO)}, "
        f"championship_proto_bytes={len(CHAMPIONSHIP_DATABASE_PROTO)}, "
        f"avatars_proto_bytes={len(AVATARS_DATABASE_PROTO)}, "
        f"vinyl_market_blocks_proto_bytes={len(VINYL_MARKET_BLOCKS_DATABASE_PROTO)}), "
        f"DatabaseProto CRC32=0x{BOOTSTRAP_DATABASE_CRC32:08X}; "
        f"logic checkVersion=0x{args.check_version & 0xFFFFFFFF:08X}; "
        f"content checkVersion={args.content_check_version}; "
        f"content ports={sorted(content_ports)}"
    )

    auth = AuthServer((args.host, args.auth_port), AuthHandler, state)
    auth_thread = threading.Thread(target=auth.serve_forever, daemon=True,
                                   name="auth-http")
    auth_thread.start()
    state.log(f"HTTP auth listening on http://{args.host}:{args.auth_port}/v1/auth")

    servers = []
    for port in ports:
        server = GameServer(port, state)
        server.start()
        servers.append(server)

    state.log("ready. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        state.log("stopping...")
    finally:
        state.stop_event.set()
        auth.shutdown()
        auth.server_close()
        for server in servers:
            server.stop()
        for server in servers:
            server.join(timeout=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
