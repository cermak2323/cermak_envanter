# 🔧 TAKEUCHI PARÇA SİPARİŞ MODÜLÜ

## Genel Amaç

Mevcut envanter ve yedek parça sistemlerine **KESİNLİKLE DOKUNMADAN**, sadece Takeuchi marka parçalar için kullanılan basitleştirilmiş bir sipariş ve kontrol modülü oluşturulmuştur.

Bu modül **ayrı bir akış** olarak çalışır:
- **Ayrı Tablolar**: `takeuchi_part_orders`, `takeuchi_order_items`, `takeuchi_temp_orders`, `takeuchi_temp_order_items`
- **Ayrı Mantık**: `takeuchi_module.py` bağımsız yönetim sınıfı
- **Ayrı UI**: `/takeuchi/` yolunda münferit arayüz

---

## 📋 Ana Menü Yapısı

Sisteme girildiğinde kullanıcıya **sadece iki menü** gösterilir:

1. **➕ Parça Ekle**
2. **✅ Parça Kontrol Et**

Başka hiçbir menü, tedarikçi seçimi veya karmaşık akış yoktur.

---

## 1️⃣ PARÇA EKLE AKIŞI

### 1.1 Parça Kodu Girişi
- Kullanıcıdan parça kodu istenir
- Parça kodu girildiğinde sistem gösterir:
  - Parçanın adı
  - Bu parçaya ait önceki sipariş geçmişi

### 1.2 Aktif Sipariş Kontrolü
Eğer girilen parça kodu:
- Daha önce sipariş edilmiş
- Henüz **tamamen teslim alınmamış** bir siparişte yer alıyorsa

➡ **Kullanıcıya uyarı mesajı gösterilir:**
```
"Bu parça için henüz tamamlanmamış bir sipariş bulunmaktadır."
```

### 1.3 Sipariş Miktarı
Eğer parça için:
- Aktif sipariş **YOKSA**
- Veya önceki siparişler tamamen kapandıysa

➡ **Kullanıcıdan sorulur:**
- Kaç adet sipariş edileceği

### 1.4 Geçici Sipariş Listesi
- Girilen parçalar: **geçici bir sipariş listesine** eklenir
- Kullanıcı: **birden fazla parça ekleyebilir**
- Bu liste: **henüz Takeuchi'ye gönderilmiş sayılmaz** ❌

---

## 2️⃣ ADMIN – SİPARİŞ OLUŞTURMA

### 2.1 Siparişlerin Listelenmesi
Admin panelinde:
- Oluşturulmuş **geçici parça listeleri** görüntülenir
- Her liste için: oluşturan kullanıcı, tarih, parça sayısı

### 2.2 Siparişe Dönüştürme
Admin, seçilen listeyi:
- **Resmi siparişe dönüştürür**
- Siparişe **benzersiz bir sipariş adı/kodu** verilir

**📌 Sipariş kodu formatı:**
```
CER2025001  ← CER + YIL + Sıra
CER2025002
CER2025003
...
```

### 2.3 Sipariş Çıktısı
Admin:
- Resmi sipariş listesini **indirebilir** (Excel / PDF / CSV)
- Takeuchi'ye göndermeye hazır hale getirilebilir

---

## 3️⃣ PARÇA KONTROL ET AKIŞI

### 3.1 Siparişlerin Görüntülenmesi
"Parça Kontrol Et" menüsünde:
- **Oluşturulmuş tüm siparişler** listelenir
- Sipariş kodu altında (örn. `CER2025001`):
  - Sipariş edilen parçalar
  - Adetleri
  - Teslim durumları

### 3.2 Teslim Kontrolü
Kullanıcı:
- **Parçanın geldiğini işaretleyebilir**
- **Kaç adet geldiğini girebilir**

### 3.3 Kısmi Teslim Senaryosu
Eğer:
```
Sipariş edilen adet ≠ gelen adet
```

➡ **Sipariş açık kalmaya devam eder** (durum: `partial`)

**Sipariş Tamamlanması:**
Sipariş şu durumda **"Tamamlandı"** olarak işaretlenir:
```
✅ Tüm parçalar
✅ Tüm adetler eksiksiz
✅ Teslim alındığında
```

---

## 🔐 KESİN KURALLAR (ÇOK ÖNEMLİ ⚠️)

| Kural | Durum |
|-------|-------|
| 🚫 Envanter sistemine DOKUNULMAYACAK | ❌ KATEGORİK |
| 🚫 Mevcut yedek parça mantığı DEĞİŞTİRİLMEYECEK | ❌ KATEGORİK |
| 🚫 Tedarikçi tablosu / seçimi OLMAYACAK | ❌ KATEGORİK |
| ✅ Sadece Takeuchi parçaları kullanılacak | ✅ GEREKLI |
| ✅ Ayrı tablolar | ✅ GEREKLI |
| ✅ Ayrı mantık | ✅ GEREKLI |
| ✅ Ayrı iş akışı | ✅ GEREKLI |

---

## 🗄️ VERİTABANI TABLOSU

### 1. `takeuchi_part_orders` – Resmi Siparişler
```sql
id (PK)
order_code (UNIQUE) → CER2025001
order_name
status → pending | completed
created_at
created_by (FK → envanter_users)
completed_at
notes
```

### 2. `takeuchi_order_items` – Sipariş Kalemleri
```sql
id (PK)
order_id (FK → takeuchi_part_orders)
part_code
part_name
ordered_quantity
received_quantity
status → pending | partial | completed
created_at
first_received_at
fully_received_at
notes
```

### 3. `takeuchi_temp_orders` – Geçici Siparişler
```sql
id (PK)
session_id (UNIQUE) → UUID
created_by (FK → envanter_users)
created_at
updated_at
```

### 4. `takeuchi_temp_order_items` – Geçici Kalemler
```sql
id (PK)
temp_order_id (FK → takeuchi_temp_orders)
part_code
part_name
quantity
added_at
```

---

## 🛣️ ROUTE'LAR (URL YOLLARı)

### Kullanıcı Yolları
```
GET  /takeuchi/          → Ana Menu
GET  /takeuchi/add       → Parça Ekle
GET  /takeuchi/check     → Parça Kontrol Et
```

### Admin Yolları
```
GET  /takeuchi/admin     → Admin Panel
```

### API Endpoints
```
POST   /api/takeuchi/init-session              → Geçici sipariş başlat
POST   /api/takeuchi/part-info                 → Parça bilgisi al
POST   /api/takeuchi/add-part                  → Parçayı listeye ekle
GET    /api/takeuchi/temp-order/<session_id>  → Geçici siparişi al
DELETE /api/takeuchi/remove-item/<item_id>    → Parçayı kaldır
GET    /api/takeuchi/orders                    → Tüm siparişleri listele
POST   /api/takeuchi/mark-received             → Teslimi kaydet

ADMIN:
GET    /api/takeuchi/admin/temp-orders         → Geçici siparişleri listele
POST   /api/takeuchi/admin/create-order        → Resmi sipariş oluştur
```

---

## 📁 DOSYA YAPISI

```
EnvanterQR/
├── models.py                          ← Takeuchi modelleri eklendi
├── takeuchi_module.py                 ← NEW: TakeuchiOrderManager sınıfı
├── app.py                             ← Takeuchi routes eklendi
├── templates/takeuchi/
│   ├── main.html                      ← Ana menü
│   ├── add_part.html                  ← Parça Ekle
│   ├── check_part.html                ← Parça Kontrol Et
│   └── admin.html                     ← Admin Panel
└── TAKEUCHI_MODULE.md                 ← Bu dosya
```

---

## 💡 KULLANIM ÖRNEĞI

### Senaryo 1: Yeni Parça Siparişi

1. **Kullanıcı**: `/takeuchi/add` ziyaret eder
2. **Kullanıcı**: "Y129" parça kodunu girer
3. **Sistem**: 
   - Parça adı: "Yedek Parça Y129" gösterir
   - Önceki siparişleri gösterir
4. **Kullanıcı**: "5 adet" girip "Listeye Ekle" tıklar
5. **Sistem**: Geçici listesine ekler
6. **Kullanıcı**: Başka parçalar ekleyebilir veya listeyi kaydedebilir

### Senaryo 2: Admin – Sipariş Oluştur

1. **Admin**: `/takeuchi/admin` ziyaret eder
2. **Admin**: Geçici siparişleri görmektedir
3. **Admin**: "Ağustos Siparişi" adını girer
4. **Admin**: "Resmi Sipariş Oluştur" tıklar
5. **Sistem**:
   - Yeni `TakeuchiPartOrder` oluşturur: `CER2025001`
   - Geçici siparişi siler
6. **Admin**: Siparişi indirebilir

### Senaryo 3: Teslim Kontrolü

1. **Kullanıcı**: `/takeuchi/check` ziyaret eder
2. **Kullanıcı**: Siparişi `CER2025001` görür
3. **Kullanıcı**: "Y129" parçası için "3 adet" teslim alındı girip kaydeder
4. **Sistem**:
   - Durum: `partial` (3/5)
   - Kullanıcı kalan 2'sini beklemeye devam eder
5. **Kullanıcı**: Sonra "2 adet" daha ekler
6. **Sistem**: 
   - Durum: `completed` (5/5)
   - Sipariş `CER2025001` tamamlandı olur

---

## ⚙️ TEKNIK NOTLAR

| Özellik | Açıklama |
|---------|----------|
| **Session Tracking** | Her kullanıcının bir session_id'si vardır (UUID) |
| **Aktif Sipariş Kontrolü** | Aynı parçanın 2x siparişini engeller |
| **Kısmi Teslim** | ordered_qty ≠ received_qty → `partial` durum |
| **Tam Teslim** | Tüm kalemler `completed` → Order `completed` |
| **Audit Trail** | Tüm işlemler `created_at`, `created_by` ile kaydedilir |

---

## 🚀 BAŞLATMA

1. **Veritabanı Tabloları Oluştur:**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

2. **Uygulamayı Başlat:**
   ```bash
   python app.py
   ```

3. **Erişim:**
   - Kullanıcı: `http://localhost:5002/takeuchi`
   - Admin: `http://localhost:5002/takeuchi/admin`

---

## 📝 NOTLAR

- ✅ Modül **tamamen izole** - mevcut sistemi etkilemez
- ✅ Admin yetkisi gerekli - sadece admin siparişler oluşturabilir
- ✅ Türkçe UI - tam Türkçe arayüz
- ✅ Hızlı ve basit - 2 ana akış, karmaşa yok
- ✅ Savepoint'ler eklenebilir - geçici siparişler silinebilir

---

**Son Güncelleme:** Aralık 2025
**Sürüm:** 1.0 (Stable)
**Durum:** ✅ Üretim Hazır
