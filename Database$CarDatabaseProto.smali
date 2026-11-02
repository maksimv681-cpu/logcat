.class public final Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
.super Lcom/google/protobuf/GeneratedMessageLite;
.source "SourceFile"

# interfaces
.implements Lmobi/square/sr/android/wo1;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;
    }
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Lcom/google/protobuf/GeneratedMessageLite<",
        "Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;",
        "Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;",
        ">;",
        "Lmobi/square/sr/android/wo1;"
    }
.end annotation


# static fields
.field private static final DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

.field public static final FOUNDPLACES_FIELD_NUMBER:I = 0x2

.field public static final ITEMS_FIELD_NUMBER:I = 0x1

.field private static volatile PARSER:Lmobi/square/sr/android/GD1;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Lmobi/square/sr/android/GD1<",
            "Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;",
            ">;"
        }
    .end annotation
.end field


# instance fields
.field private foundPlaces_:Lcom/google/protobuf/z$k;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Lcom/google/protobuf/z$k<",
            "Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;",
            ">;"
        }
    .end annotation
.end field

.field private items_:Lcom/google/protobuf/z$k;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Lcom/google/protobuf/z$k<",
            "Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .registers 2

    .line 1
    new-instance v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 2
    .line 3
    invoke-direct {v0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;-><init>()V

    .line 4
    .line 5
    .line 6
    sput-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 7
    .line 8
    const-class v1, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 9
    .line 10
    invoke-static {v1, v0}, Lcom/google/protobuf/GeneratedMessageLite;->registerDefaultInstance(Ljava/lang/Class;Lcom/google/protobuf/GeneratedMessageLite;)V

    .line 11
    .line 12
    .line 13
    return-void
.end method

.method private constructor <init>()V
    .registers 2

    .line 1
    invoke-direct {p0}, Lcom/google/protobuf/GeneratedMessageLite;-><init>()V

    .line 2
    .line 3
    .line 4
    invoke-static {}, Lcom/google/protobuf/GeneratedMessageLite;->emptyProtobufList()Lcom/google/protobuf/z$k;

    .line 5
    .line 6
    .line 7
    move-result-object v0

    .line 8
    iput-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 9
    .line 10
    invoke-static {}, Lcom/google/protobuf/GeneratedMessageLite;->emptyProtobufList()Lcom/google/protobuf/z$k;

    .line 11
    .line 12
    .line 13
    move-result-object v0

    .line 14
    iput-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 15
    .line 16
    return-void
.end method

.method public static synthetic access$28100()Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 1

    .line 1
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 2
    .line 3
    return-object v0
.end method

.method public static synthetic access$28200(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;ILmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V
    .registers 3

    .line 1
    invoke-direct {p0, p1, p2}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->setItems(ILmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$28300(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V
    .registers 2

    .line 1
    invoke-direct {p0, p1}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->addItems(Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$28400(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;ILmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V
    .registers 3

    .line 1
    invoke-direct {p0, p1, p2}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->addItems(ILmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$28500(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;Ljava/lang/Iterable;)V
    .registers 2

    .line 1
    invoke-direct {p0, p1}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->addAllItems(Ljava/lang/Iterable;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$28600(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;)V
    .registers 1

    .line 1
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->clearItems()V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$28700(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;I)V
    .registers 2

    .line 1
    invoke-direct {p0, p1}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->removeItems(I)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$28800(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;ILmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V
    .registers 3

    .line 1
    invoke-direct {p0, p1, p2}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->setFoundPlaces(ILmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$28900(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V
    .registers 2

    .line 1
    invoke-direct {p0, p1}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->addFoundPlaces(Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$29000(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;ILmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V
    .registers 3

    .line 1
    invoke-direct {p0, p1, p2}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->addFoundPlaces(ILmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$29100(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;Ljava/lang/Iterable;)V
    .registers 2

    .line 1
    invoke-direct {p0, p1}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->addAllFoundPlaces(Ljava/lang/Iterable;)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$29200(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;)V
    .registers 1

    .line 1
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->clearFoundPlaces()V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method public static synthetic access$29300(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;I)V
    .registers 2

    .line 1
    invoke-direct {p0, p1}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->removeFoundPlaces(I)V

    .line 2
    .line 3
    .line 4
    return-void
.end method

.method private addAllFoundPlaces(Ljava/lang/Iterable;)V
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/Iterable<",
            "+",
            "Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;",
            ">;)V"
        }
    .end annotation

    .line 1
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureFoundPlacesIsMutable()V

    .line 2
    .line 3
    .line 4
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 5
    .line 6
    invoke-static {p1, v0}, Lcom/google/protobuf/a;->addAll(Ljava/lang/Iterable;Ljava/util/List;)V

    .line 7
    .line 8
    .line 9
    return-void
.end method

.method private addAllItems(Ljava/lang/Iterable;)V
    .registers 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/Iterable<",
            "+",
            "Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;",
            ">;)V"
        }
    .end annotation

    .line 1
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureItemsIsMutable()V

    .line 2
    .line 3
    .line 4
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 5
    .line 6
    invoke-static {p1, v0}, Lcom/google/protobuf/a;->addAll(Ljava/lang/Iterable;Ljava/util/List;)V

    .line 7
    .line 8
    .line 9
    return-void
.end method

.method private addFoundPlaces(ILmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V
    .registers 4

    .line 4
    invoke-virtual {p2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 5
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureFoundPlacesIsMutable()V

    .line 6
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    invoke-interface {v0, p1, p2}, Ljava/util/List;->add(ILjava/lang/Object;)V

    return-void
.end method

.method private addFoundPlaces(Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V
    .registers 3

    .line 1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureFoundPlacesIsMutable()V

    .line 3
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    invoke-interface {v0, p1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    return-void
.end method

.method private addItems(ILmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V
    .registers 4

    .line 4
    invoke-virtual {p2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 5
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureItemsIsMutable()V

    .line 6
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    invoke-interface {v0, p1, p2}, Ljava/util/List;->add(ILjava/lang/Object;)V

    return-void
.end method

.method private addItems(Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V
    .registers 3

    .line 1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureItemsIsMutable()V

    .line 3
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    invoke-interface {v0, p1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    return-void
.end method

.method private clearFoundPlaces()V
    .registers 2

    .line 1
    invoke-static {}, Lcom/google/protobuf/GeneratedMessageLite;->emptyProtobufList()Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    .line 4
    move-result-object v0

    .line 5
    iput-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 6
    .line 7
    return-void
.end method

.method private clearItems()V
    .registers 2

    .line 1
    invoke-static {}, Lcom/google/protobuf/GeneratedMessageLite;->emptyProtobufList()Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    .line 4
    move-result-object v0

    .line 5
    iput-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 6
    .line 7
    return-void
.end method

.method private ensureFoundPlacesIsMutable()V
    .registers 3

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0}, Lcom/google/protobuf/z$k;->o()Z

    .line 4
    .line 5
    .line 6
    move-result v1

    .line 7
    if-nez v1, :cond_e

    .line 8
    .line 9
    invoke-static {v0}, Lcom/google/protobuf/GeneratedMessageLite;->mutableCopy(Lcom/google/protobuf/z$k;)Lcom/google/protobuf/z$k;

    .line 10
    .line 11
    .line 12
    move-result-object v0

    .line 13
    iput-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 14
    .line 15
    :cond_e
    return-void
.end method

.method private ensureItemsIsMutable()V
    .registers 3

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0}, Lcom/google/protobuf/z$k;->o()Z

    .line 4
    .line 5
    .line 6
    move-result v1

    .line 7
    if-nez v1, :cond_e

    .line 8
    .line 9
    invoke-static {v0}, Lcom/google/protobuf/GeneratedMessageLite;->mutableCopy(Lcom/google/protobuf/z$k;)Lcom/google/protobuf/z$k;

    .line 10
    .line 11
    .line 12
    move-result-object v0

    .line 13
    iput-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 14
    .line 15
    :cond_e
    return-void
.end method

.method public static getDefaultInstance()Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 1

    .line 1
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 2
    .line 3
    return-object v0
.end method

.method public static newBuilder()Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;
    .registers 1

    .line 1
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-virtual {v0}, Lcom/google/protobuf/GeneratedMessageLite;->createBuilder()Lcom/google/protobuf/GeneratedMessageLite$b;

    move-result-object v0

    check-cast v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;

    return-object v0
.end method

.method public static newBuilder(Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;
    .registers 2

    .line 2
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-virtual {v0, p0}, Lcom/google/protobuf/GeneratedMessageLite;->createBuilder(Lcom/google/protobuf/GeneratedMessageLite;)Lcom/google/protobuf/GeneratedMessageLite$b;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;

    return-object p0
.end method

.method public static parseDelimitedFrom(Ljava/io/InputStream;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 1
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0}, Lcom/google/protobuf/GeneratedMessageLite;->parseDelimitedFrom(Lcom/google/protobuf/GeneratedMessageLite;Ljava/io/InputStream;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseDelimitedFrom(Ljava/io/InputStream;Lcom/google/protobuf/r;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 2
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0, p1}, Lcom/google/protobuf/GeneratedMessageLite;->parseDelimitedFrom(Lcom/google/protobuf/GeneratedMessageLite;Ljava/io/InputStream;Lcom/google/protobuf/r;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Lcom/google/protobuf/f;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/google/protobuf/A;
        }
    .end annotation

    .line 3
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Lcom/google/protobuf/f;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Lcom/google/protobuf/f;Lcom/google/protobuf/r;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/google/protobuf/A;
        }
    .end annotation

    .line 4
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0, p1}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Lcom/google/protobuf/f;Lcom/google/protobuf/r;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Lcom/google/protobuf/g;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 9
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Lcom/google/protobuf/g;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Lcom/google/protobuf/g;Lcom/google/protobuf/r;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 10
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0, p1}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Lcom/google/protobuf/g;Lcom/google/protobuf/r;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Ljava/io/InputStream;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 7
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Ljava/io/InputStream;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Ljava/io/InputStream;Lcom/google/protobuf/r;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 8
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0, p1}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Ljava/io/InputStream;Lcom/google/protobuf/r;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Ljava/nio/ByteBuffer;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/google/protobuf/A;
        }
    .end annotation

    .line 1
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Ljava/nio/ByteBuffer;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom(Ljava/nio/ByteBuffer;Lcom/google/protobuf/r;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/google/protobuf/A;
        }
    .end annotation

    .line 2
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0, p1}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;Ljava/nio/ByteBuffer;Lcom/google/protobuf/r;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom([B)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/google/protobuf/A;
        }
    .end annotation

    .line 5
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;[B)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parseFrom([BLcom/google/protobuf/r;)Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;
    .registers 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/google/protobuf/A;
        }
    .end annotation

    .line 6
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    invoke-static {v0, p0, p1}, Lcom/google/protobuf/GeneratedMessageLite;->parseFrom(Lcom/google/protobuf/GeneratedMessageLite;[BLcom/google/protobuf/r;)Lcom/google/protobuf/GeneratedMessageLite;

    move-result-object p0

    check-cast p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    return-object p0
.end method

.method public static parser()Lmobi/square/sr/android/GD1;
    .registers 1
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Lmobi/square/sr/android/GD1<",
            "Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;",
            ">;"
        }
    .end annotation

    .line 1
    sget-object v0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 2
    .line 3
    invoke-virtual {v0}, Lcom/google/protobuf/GeneratedMessageLite;->getParserForType()Lmobi/square/sr/android/GD1;

    .line 4
    .line 5
    .line 6
    move-result-object v0

    .line 7
    return-object v0
.end method

.method private removeFoundPlaces(I)V
    .registers 3

    .line 1
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureFoundPlacesIsMutable()V

    .line 2
    .line 3
    .line 4
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 5
    .line 6
    invoke-interface {v0, p1}, Ljava/util/List;->remove(I)Ljava/lang/Object;

    .line 7
    .line 8
    .line 9
    return-void
.end method

.method private removeItems(I)V
    .registers 3

    .line 1
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureItemsIsMutable()V

    .line 2
    .line 3
    .line 4
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 5
    .line 6
    invoke-interface {v0, p1}, Ljava/util/List;->remove(I)Ljava/lang/Object;

    .line 7
    .line 8
    .line 9
    return-void
.end method

.method private setFoundPlaces(ILmobi/sr/common/proto/compiled/Database$FoundPlacesProto;)V
    .registers 4

    .line 1
    invoke-virtual {p2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureFoundPlacesIsMutable()V

    .line 5
    .line 6
    .line 7
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 8
    .line 9
    invoke-interface {v0, p1, p2}, Ljava/util/List;->set(ILjava/lang/Object;)Ljava/lang/Object;

    .line 10
    .line 11
    .line 12
    return-void
.end method

.method private setItems(ILmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;)V
    .registers 4

    .line 1
    invoke-virtual {p2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    .line 2
    .line 3
    .line 4
    invoke-direct {p0}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->ensureItemsIsMutable()V

    .line 5
    .line 6
    .line 7
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 8
    .line 9
    invoke-interface {v0, p1, p2}, Ljava/util/List;->set(ILjava/lang/Object;)Ljava/lang/Object;

    .line 10
    .line 11
    .line 12
    return-void
.end method


# virtual methods
.method public final dynamicMethod(Lcom/google/protobuf/GeneratedMessageLite$g;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    .registers 5

    .line 1
    const/4 p2, 0x1

    .line 2
    sget-object p3, Lmobi/square/sr/android/n80;->a:[I

    .line 3
    .line 4
    invoke-virtual {p1}, Ljava/lang/Enum;->ordinal()I

    .line 5
    .line 6
    .line 7
    move-result p1

    .line 8
    aget p1, p3, p1

    .line 9
    .line 10
    const/4 p3, 0x0

    .line 11
    packed-switch p1, :pswitch_data_64

    .line 12
    .line 13
    .line 14
    new-instance p1, Ljava/lang/UnsupportedOperationException;

    .line 15
    .line 16
    invoke-direct {p1}, Ljava/lang/UnsupportedOperationException;-><init>()V

    .line 17
    .line 18
    .line 19
    throw p1

    .line 20
    :pswitch_13
    return-object p3

    .line 21
    :pswitch_14
    invoke-static {p2}, Ljava/lang/Byte;->valueOf(B)Ljava/lang/Byte;

    .line 22
    .line 23
    .line 24
    move-result-object p1

    .line 25
    return-object p1

    .line 26
    :pswitch_19
    sget-object p1, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->PARSER:Lmobi/square/sr/android/GD1;

    .line 27
    .line 28
    if-nez p1, :cond_34

    .line 29
    .line 30
    const-class p2, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 31
    .line 32
    monitor-enter p2

    .line 33
    :try_start_20
    sget-object p1, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->PARSER:Lmobi/square/sr/android/GD1;

    .line 34
    .line 35
    if-nez p1, :cond_30

    .line 36
    .line 37
    new-instance p1, Lcom/google/protobuf/GeneratedMessageLite$c;

    .line 38
    .line 39
    sget-object p3, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 40
    .line 41
    invoke-direct {p1, p3}, Lcom/google/protobuf/GeneratedMessageLite$c;-><init>(Lcom/google/protobuf/GeneratedMessageLite;)V

    .line 42
    .line 43
    .line 44
    sput-object p1, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->PARSER:Lmobi/square/sr/android/GD1;

    .line 45
    .line 46
    goto :goto_30

    .line 47
    :catchall_2e
    move-exception p1

    .line 48
    goto :goto_32

    .line 49
    :cond_30
    :goto_30
    monitor-exit p2

    .line 50
    return-object p1

    .line 51
    :goto_32
    monitor-exit p2
    :try_end_33
    .catchall {:try_start_20 .. :try_end_33} :catchall_2e

    .line 52
    throw p1

    .line 53
    :cond_34
    return-object p1

    .line 54
    :pswitch_35
    sget-object p1, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 55
    .line 56
    return-object p1

    .line 57
    :pswitch_38
    const/4 p1, 0x4

    .line 58
    new-array p1, p1, [Ljava/lang/Object;

    .line 59
    .line 60
    const-string p3, "items_"

    .line 61
    .line 62
    const/4 v0, 0x0

    .line 63
    aput-object p3, p1, v0

    .line 64
    .line 65
    const-class p3, Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;

    .line 66
    .line 67
    aput-object p3, p1, p2

    .line 68
    .line 69
    const-string p2, "foundPlaces_"

    .line 70
    .line 71
    const/4 p3, 0x2

    .line 72
    aput-object p2, p1, p3

    .line 73
    .line 74
    const-class p2, Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;

    .line 75
    .line 76
    const/4 p3, 0x3

    .line 77
    aput-object p2, p1, p3

    .line 78
    .line 79
    const-string p2, "\u0001\u0002\u0000\u0000\u0001\u0002\u0002\u0000\u0002\u0000\u0001\u001b\u0002\u001b"

    .line 80
    .line 81
    sget-object p3, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->DEFAULT_INSTANCE:Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 82
    .line 83
    invoke-static {p3, p2, p1}, Lcom/google/protobuf/GeneratedMessageLite;->newMessageInfo(Lcom/google/protobuf/K;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 84
    .line 85
    .line 86
    move-result-object p1

    .line 87
    return-object p1

    .line 88
    :pswitch_57
    new-instance p1, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;

    .line 89
    .line 90
    invoke-direct {p1, p3}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto$a;-><init>(Lmobi/square/sr/android/n80;)V

    .line 91
    .line 92
    .line 93
    return-object p1

    .line 94
    :pswitch_5d
    new-instance p1, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;

    .line 95
    .line 96
    invoke-direct {p1}, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;-><init>()V

    .line 97
    .line 98
    .line 99
    return-object p1

    .line 100
    nop

    .line 101
    :pswitch_data_64
    .packed-switch 0x1
        :pswitch_5d
        :pswitch_57
        :pswitch_38
        :pswitch_35
        :pswitch_19
        :pswitch_14
        :pswitch_13
    .end packed-switch
.end method

.method public getFoundPlaces(I)Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;
    .registers 3

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0, p1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 4
    .line 5
    .line 6
    move-result-object p1

    .line 7
    check-cast p1, Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;

    .line 8
    .line 9
    return-object p1
.end method

.method public getFoundPlacesCount()I
    .registers 2

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0}, Ljava/util/List;->size()I

    .line 4
    .line 5
    .line 6
    move-result v0

    .line 7
    return v0
.end method

.method public getFoundPlacesList()Ljava/util/List;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lmobi/sr/common/proto/compiled/Database$FoundPlacesProto;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    return-object v0
.end method

.method public getFoundPlacesOrBuilder(I)Lmobi/square/sr/android/o80;
    .registers 3

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0, p1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 4
    .line 5
    .line 6
    move-result-object p1

    .line 7
    check-cast p1, Lmobi/square/sr/android/o80;

    .line 8
    .line 9
    return-object p1
.end method

.method public getFoundPlacesOrBuilderList()Ljava/util/List;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "+",
            "Lmobi/square/sr/android/o80;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->foundPlaces_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    return-object v0
.end method

.method public getItems(I)Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;
    .registers 3

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0, p1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 4
    .line 5
    .line 6
    move-result-object p1

    .line 7
    check-cast p1, Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;

    .line 8
    .line 9
    return-object p1
.end method

.method public getItemsCount()I
    .registers 2

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0}, Ljava/util/List;->size()I

    .line 4
    .line 5
    .line 6
    move-result v0

    .line 7
    return v0
.end method

.method public getItemsList()Ljava/util/List;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lmobi/sr/common/proto/compiled/BaseCarContainer$BaseCarProto;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    return-object v0
.end method

.method public getItemsOrBuilder(I)Lmobi/square/sr/android/Rn;
    .registers 3

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    invoke-interface {v0, p1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    .line 4
    .line 5
    .line 6
    move-result-object p1

    .line 7
    check-cast p1, Lmobi/square/sr/android/Rn;

    .line 8
    .line 9
    return-object p1
.end method

.method public getItemsOrBuilderList()Ljava/util/List;
    .registers 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "+",
            "Lmobi/square/sr/android/Rn;",
            ">;"
        }
    .end annotation

    .line 1
    iget-object v0, p0, Lmobi/sr/common/proto/compiled/Database$CarDatabaseProto;->items_:Lcom/google/protobuf/z$k;

    .line 2
    .line 3
    return-object v0
.end method
