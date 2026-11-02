package mobi.sr.common.proto.compiled;

import com.google.protobuf.A;
import com.google.protobuf.GeneratedMessageLite;
import com.google.protobuf.z;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.util.List;
import mobi.square.sr.android.GD1;
import mobi.square.sr.android.Rn;
import mobi.square.sr.android.n80;
import mobi.square.sr.android.o80;
import mobi.square.sr.android.wo1;
/* loaded from: C:\Users\MaX\AppData\Local\Temp\opencode\dragstreets\dex\classes3.dex */
public final class Database$CarDatabaseProto extends GeneratedMessageLite<Database$CarDatabaseProto, a> implements wo1 {
    private static final Database$CarDatabaseProto DEFAULT_INSTANCE;
    public static final int FOUNDPLACES_FIELD_NUMBER = 2;
    public static final int ITEMS_FIELD_NUMBER = 1;
    private static volatile GD1<Database$CarDatabaseProto> PARSER;
    private z.k<BaseCarContainer$BaseCarProto> items_ = GeneratedMessageLite.emptyProtobufList();
    private z.k<Database$FoundPlacesProto> foundPlaces_ = GeneratedMessageLite.emptyProtobufList();

    /* loaded from: C:\Users\MaX\AppData\Local\Temp\opencode\dragstreets\dex\classes3.dex */
    public static final class a extends GeneratedMessageLite.b<Database$CarDatabaseProto, a> implements wo1 {
        public /* synthetic */ a(n80 n80Var) {
            this();
        }

        public a E(Database$FoundPlacesProto database$FoundPlacesProto) {
            t();
            ((Database$CarDatabaseProto) ((GeneratedMessageLite.b) this).b).addFoundPlaces(database$FoundPlacesProto);
            return this;
        }

        public a F(BaseCarContainer$BaseCarProto baseCarContainer$BaseCarProto) {
            t();
            ((Database$CarDatabaseProto) ((GeneratedMessageLite.b) this).b).addItems(baseCarContainer$BaseCarProto);
            return this;
        }

        public a() {
            super(Database$CarDatabaseProto.DEFAULT_INSTANCE);
        }
    }

    static {
        Database$CarDatabaseProto database$CarDatabaseProto = new Database$CarDatabaseProto();
        DEFAULT_INSTANCE = database$CarDatabaseProto;
        GeneratedMessageLite.registerDefaultInstance(Database$CarDatabaseProto.class, database$CarDatabaseProto);
    }

    private Database$CarDatabaseProto() {
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void addAllFoundPlaces(Iterable<? extends Database$FoundPlacesProto> iterable) {
        ensureFoundPlacesIsMutable();
        com.google.protobuf.a.addAll(iterable, this.foundPlaces_);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void addAllItems(Iterable<? extends BaseCarContainer$BaseCarProto> iterable) {
        ensureItemsIsMutable();
        com.google.protobuf.a.addAll(iterable, this.items_);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void addFoundPlaces(Database$FoundPlacesProto database$FoundPlacesProto) {
        database$FoundPlacesProto.getClass();
        ensureFoundPlacesIsMutable();
        this.foundPlaces_.add(database$FoundPlacesProto);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void addItems(BaseCarContainer$BaseCarProto baseCarContainer$BaseCarProto) {
        baseCarContainer$BaseCarProto.getClass();
        ensureItemsIsMutable();
        this.items_.add(baseCarContainer$BaseCarProto);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void clearFoundPlaces() {
        this.foundPlaces_ = GeneratedMessageLite.emptyProtobufList();
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void clearItems() {
        this.items_ = GeneratedMessageLite.emptyProtobufList();
    }

    private void ensureFoundPlacesIsMutable() {
        z.k<Database$FoundPlacesProto> kVar = this.foundPlaces_;
        if (!kVar.o()) {
            this.foundPlaces_ = GeneratedMessageLite.mutableCopy(kVar);
        }
    }

    private void ensureItemsIsMutable() {
        z.k<BaseCarContainer$BaseCarProto> kVar = this.items_;
        if (!kVar.o()) {
            this.items_ = GeneratedMessageLite.mutableCopy(kVar);
        }
    }

    public static Database$CarDatabaseProto getDefaultInstance() {
        return DEFAULT_INSTANCE;
    }

    public static a newBuilder() {
        return (a) DEFAULT_INSTANCE.createBuilder();
    }

    public static Database$CarDatabaseProto parseDelimitedFrom(InputStream inputStream) throws IOException {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseDelimitedFrom(DEFAULT_INSTANCE, inputStream);
    }

    public static Database$CarDatabaseProto parseFrom(ByteBuffer byteBuffer) throws A {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, byteBuffer);
    }

    public static GD1<Database$CarDatabaseProto> parser() {
        return DEFAULT_INSTANCE.getParserForType();
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void removeFoundPlaces(int i) {
        ensureFoundPlacesIsMutable();
        this.foundPlaces_.remove(i);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void removeItems(int i) {
        ensureItemsIsMutable();
        this.items_.remove(i);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void setFoundPlaces(int i, Database$FoundPlacesProto database$FoundPlacesProto) {
        database$FoundPlacesProto.getClass();
        ensureFoundPlacesIsMutable();
        this.foundPlaces_.set(i, database$FoundPlacesProto);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void setItems(int i, BaseCarContainer$BaseCarProto baseCarContainer$BaseCarProto) {
        baseCarContainer$BaseCarProto.getClass();
        ensureItemsIsMutable();
        this.items_.set(i, baseCarContainer$BaseCarProto);
    }

    public final Object dynamicMethod(GeneratedMessageLite.g gVar, Object obj, Object obj2) {
        GeneratedMessageLite.c cVar;
        switch (n80.a[gVar.ordinal()]) {
            case 1:
                return new Database$CarDatabaseProto();
            case 2:
                return new a(null);
            case 3:
                return GeneratedMessageLite.newMessageInfo(DEFAULT_INSTANCE, "\u0001\u0002\u0000\u0000\u0001\u0002\u0002\u0000\u0002\u0000\u0001\u001b\u0002\u001b", new Object[]{"items_", BaseCarContainer$BaseCarProto.class, "foundPlaces_", Database$FoundPlacesProto.class});
            case 4:
                return DEFAULT_INSTANCE;
            case 5:
                GD1<Database$CarDatabaseProto> gd1 = PARSER;
                if (gd1 == null) {
                    synchronized (Database$CarDatabaseProto.class) {
                        try {
                            cVar = PARSER;
                            if (cVar == null) {
                                cVar = new GeneratedMessageLite.c(DEFAULT_INSTANCE);
                                PARSER = cVar;
                            }
                        } catch (Throwable th) {
                            throw th;
                        }
                    }
                    return cVar;
                }
                return gd1;
            case 6:
                return (byte) 1;
            case 7:
                return null;
            default:
                throw new UnsupportedOperationException();
        }
    }

    public Database$FoundPlacesProto getFoundPlaces(int i) {
        return (Database$FoundPlacesProto) this.foundPlaces_.get(i);
    }

    public int getFoundPlacesCount() {
        return this.foundPlaces_.size();
    }

    public List<Database$FoundPlacesProto> getFoundPlacesList() {
        return this.foundPlaces_;
    }

    public o80 getFoundPlacesOrBuilder(int i) {
        return (o80) this.foundPlaces_.get(i);
    }

    public List<? extends o80> getFoundPlacesOrBuilderList() {
        return this.foundPlaces_;
    }

    public BaseCarContainer$BaseCarProto getItems(int i) {
        return (BaseCarContainer$BaseCarProto) this.items_.get(i);
    }

    public int getItemsCount() {
        return this.items_.size();
    }

    public List<BaseCarContainer$BaseCarProto> getItemsList() {
        return this.items_;
    }

    public Rn getItemsOrBuilder(int i) {
        return (Rn) this.items_.get(i);
    }

    public List<? extends Rn> getItemsOrBuilderList() {
        return this.items_;
    }

    public static a newBuilder(Database$CarDatabaseProto database$CarDatabaseProto) {
        return (a) DEFAULT_INSTANCE.createBuilder(database$CarDatabaseProto);
    }

    public static Database$CarDatabaseProto parseDelimitedFrom(InputStream inputStream, com.google.protobuf.r rVar) throws IOException {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseDelimitedFrom(DEFAULT_INSTANCE, inputStream, rVar);
    }

    public static Database$CarDatabaseProto parseFrom(ByteBuffer byteBuffer, com.google.protobuf.r rVar) throws A {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, byteBuffer, rVar);
    }

    public static Database$CarDatabaseProto parseFrom(com.google.protobuf.f fVar) throws A {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, fVar);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void addFoundPlaces(int i, Database$FoundPlacesProto database$FoundPlacesProto) {
        database$FoundPlacesProto.getClass();
        ensureFoundPlacesIsMutable();
        this.foundPlaces_.add(i, database$FoundPlacesProto);
    }

    /* JADX INFO: Access modifiers changed from: private */
    public void addItems(int i, BaseCarContainer$BaseCarProto baseCarContainer$BaseCarProto) {
        baseCarContainer$BaseCarProto.getClass();
        ensureItemsIsMutable();
        this.items_.add(i, baseCarContainer$BaseCarProto);
    }

    public static Database$CarDatabaseProto parseFrom(com.google.protobuf.f fVar, com.google.protobuf.r rVar) throws A {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, fVar, rVar);
    }

    public static Database$CarDatabaseProto parseFrom(byte[] bArr) throws A {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, bArr);
    }

    public static Database$CarDatabaseProto parseFrom(byte[] bArr, com.google.protobuf.r rVar) throws A {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, bArr, rVar);
    }

    public static Database$CarDatabaseProto parseFrom(InputStream inputStream) throws IOException {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, inputStream);
    }

    public static Database$CarDatabaseProto parseFrom(InputStream inputStream, com.google.protobuf.r rVar) throws IOException {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, inputStream, rVar);
    }

    public static Database$CarDatabaseProto parseFrom(com.google.protobuf.g gVar) throws IOException {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, gVar);
    }

    public static Database$CarDatabaseProto parseFrom(com.google.protobuf.g gVar, com.google.protobuf.r rVar) throws IOException {
        return (Database$CarDatabaseProto) GeneratedMessageLite.parseFrom(DEFAULT_INSTANCE, gVar, rVar);
    }
}
