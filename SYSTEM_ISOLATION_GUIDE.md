# 🛡️ SİSTEM İZOLASYON KILAVUZU

## ✅ İKİ BAĞIMSIZ SİSTEM

### 1️⃣ **ENVANTER SİSTEMİ** (İnventory System)
**Veritabanı Tabloları:**
- `part_codes` - Parça bilgileri (3,983 parça)
- `qr_codes` - QR kodları (9,212+ kod)
- `scanned_qr` - Sayım işlemleri
- `count_sessions` - Sayım oturumları

**Erişim Yolları:**
- `/parts` - Parça listesi görüntüleme
- `/part/<id>` - Parça detayları
- `/generate_qr/<part_code>` - QR kod oluşturma (MANUEL)
- `/count` - QR kod sayımı

**Admin Yönetimi:**
- `/admin` - Admin paneli
- `/upload_parts` - **SADECE** part_codes tablosuna yazar

---

### 2️⃣ **SİPARİŞ SİSTEMİ** (Order System - TAMAMEN AYRILAN)
**Veritabanı Tabloları:**
- `order_system_stock` - Sipariş parçaları
- `order_list` - Sipariş listesi
- `delivery_history` - Teslimat geçmişi

**Erişim Yolları:**
- `/order_system/` - Sipariş sistem menüsü
- `/order_system/upload_stock` - Excel stok yükleme
- `/order_system/create_orders` - Manuel sipariş oluşturma

**Önemli:** `order_system.py` **ASLA** `part_codes` veya `qr_codes` tablosuna dokunmaz!

---

## 🔒 KORUMA MEKANIZMALARI

### 📌 Layer 1: Database Level (Veritabanı Düzeyinde)
```
part_codes ←→ Foreign Key ←→ qr_codes
                    ↓
          (Sıkı bağlantı)
          
order_system_stock ←→ ❌ BAĞLANTISI YOK
```

### 📌 Layer 2: Application Level (Uygulama Düzeyinde)

#### ✅ `/upload_parts` (Admin - Envanter)
```python
# SADECE bu tabloları kullanan kod:
- INSERT INTO part_codes (part_code, part_name, ...)
- UPDATE part_codes SET part_name = ...
- SELECT FROM part_codes

# ASLA değiştirilmez:
❌ qr_codes
❌ order_system_stock
❌ scanned_qr
```

#### ✅ `/order_system/api/upload_stock` (Sipariş)
```python
# SADECE bu tabloları kullanan kod:
- INSERT INTO order_system_stock (...)
- UPDATE order_system_stock SET ...
- DELETE FROM order_list (eski siparişler)

# ASLA değiştirilmez:
❌ part_codes
❌ qr_codes
❌ count_sessions
❌ scanned_qr
```

#### ✅ `/generate_qr/<part_code>` (Envanter)
```python
# SADECE:
- part_codes'dan oku
- qr_codes'a ekle
- Dosya sistemine kaydet

# ASLA değiştirilmez:
❌ order_system_stock
❌ order_list
```

---

## ⚠️ RİSK ANALIZI

| Risk | Olasılık | Etki | Önlem |
|------|----------|------|-------|
| Excel'de çok sayıda parça yükleme | Yüksek | Normal ✅ | Doğru format kontrol |
| Mevcut parçalar yanlışlıkla silinme | Düşük | Ciddi ❌ | DELETE yok, sadece UPDATE |
| QR kodları yanlışlıkla silinme | Çok Düşük | Ciddi ❌ | Ayrı sistem, manuel silme |
| Sipariş sistemi envantere zarar verme | Çok Düşük | Ciddi ❌ | Tamamen izole |

---

## ✅ GÜVENLİ EXCEL YÜKLEME TALIMATLARI

### Envanter Sistemi (/admin)
**Format:**
| part_code | part_name |
|-----------|-----------|
| Y129A00-55730 | YAKIT SU AYIRICI FİLTRE |
| 14201-10950 | ALT KAPI BALAMA KLIPLERI |

**Sonuç:**
- ✅ Yeni parçalar eklenir
- ✅ Mevcut parçalar güncellenir
- ✅ Başka şey değiştirilmez
- ✅ QR kodlar korunur

### Sipariş Sistemi (/order_system/upload_stock)
**Format:**
| Parça Kodu | Parça Adı | Stok | Kritik stok | Beklenen stok | Tedarikçi | Birim Fiyatı |
|-----------|-----------|-----|-----------|--------------|----------|------------|
| Y129A00-55730 | YAKIT SU AYIRICI FİLTRE | 100 | 20 | 150 | Supplier1 | 25.50 |

**Sonuç:**
- ✅ Stok bilgileri güncellenir
- ✅ Sipariş parçaları yönetilir
- ✅ Envanter sistemi dokunulmaz

---

## 🔄 SİSTEM AKIŞI

```
ENVANTER SİSTEMİ AKIŞI:
┌─────────────────────────────────────┐
│ 1. Admin Excel Yükle (/admin)       │
│    ↓                                 │
│ 2. part_codes tablosuna ekle/güncelle
│    ↓                                 │
│ 3. Parça Detay Sayfasında Manuel     │
│    QR Oluştur (/generate_qr)        │
│    ↓                                 │
│ 4. QR Kodlarla Sayım Yap (/count)   │
└─────────────────────────────────────┘

SİPARİŞ SİSTEMİ AKIŞI:
┌─────────────────────────────────────┐
│ 1. Excel Yükle (/order_system)      │
│    ↓                                 │
│ 2. order_system_stock'a kaydet      │
│    ↓                                 │
│ 3. Sipariş Listesi Oluştur          │
│    (/order_system/create_orders)    │
└─────────────────────────────────────┘
```

---

## 🧪 TEST KONTROL LİSTESİ

```
□ Admin panelinden 10 yeni parça yükle
  ✅ Kontrol: /parts'ta görünüyor mu?
  ✅ Kontrol: part_codes tablosuna yazıldı mı?
  
□ Yeni parçanın QR kodlarını oluştur (50 adet)
  ✅ Kontrol: /generate_qr_image'de çıkıyor mu?
  ✅ Kontrol: qr_codes tablosuna yazıldı mı?
  ✅ Kontrol: order_system_stock etkilendi mi? (HAYIR OLMALI)

□ Sipariş sisteminden Excel yükle
  ✅ Kontrol: order_system_stock'a yazıldı mı?
  ✅ Kontrol: part_codes etkilendi mi? (HAYIR OLMALI)

□ Sayım başlat ve QR tara
  ✅ Kontrol: scanned_qr'a yazıldı mı?
  ✅ Kontrol: part_codes etkilendi mi? (HAYIR OLMALI)
```

---

## 📋 TEKNIK DETAYLAR

### Database Foreign Keys
```sql
-- BAĞLANTILI:
ALTER TABLE qr_codes ADD CONSTRAINT fk_qr_part
  FOREIGN KEY (part_code_id) REFERENCES part_codes(id);

-- BAĞLANTILI DEĞİL:
-- order_system_stock ← part_codes (INTENTIONAL)
-- order_list ← order_system_stock (internal only)
```

### Application Isolation Points
```python
# order_system.py
- SADECE: pymysql.connect() ile kendi bağlantısı
- SADECE: DB_CONFIG['database'] = 'flaskdb'
- SADECE: order_system_stock, order_list, delivery_history

# app.py (Envanter)
- SQLAlchemy ORM kullanır
- PartCode model ← part_codes
- QRCode model ← qr_codes
```

---

## 🎯 ÖZET

| Sistem | Veritabanı | Excel Upload | QR Yönetimi | Durum |
|--------|-----------|--------------|------------|-------|
| Envanter | part_codes, qr_codes | ✅ Safe | ✅ Manuel | **KORUNMUŞ** |
| Sipariş | order_system_stock, order_list | ✅ Safe | ❌ Yok | **KORUNMUŞ** |

**Sonuç:** İki sistem tamamen bağımsız ve birbirinden güvenli.

---

## 📞 İŞLEM REHBERI

### Scenario 1: "Tüm parçaları baştan yükleme yapacağım"
1. Excel hazırla (part_code, part_name)
2. `/admin` → "Parça Listesi Yükle"
3. ✅ Mevcut parçalar güncellenir, QR kodlar korunur
4. Yeni parçalara QR kodlarını `/parts` → "Detay" → "QR Oluştur"'dan yarat

### Scenario 2: "Sipariş sistemine Excel yükleyeceğim"
1. Excel hazırla (Parça Kodu, Parça Adı, Stok, vs)
2. `/order_system/upload_stock` 
3. ✅ Sadece stok bilgileri güncellenir
4. `/order_system/create_orders`'dan sipariş listesi oluştur

### Scenario 3: "Sayım yapmak istiyorum"
1. `/count` → Yeni sayım oturumu oluştur
2. QR kod tara (scanner + web)
3. ✅ scanned_qr'a kayıt edilir
4. Rapor indir

---

**Güncelleme Tarihi:** 16 Aralık 2025
**Sistem Durumu:** ✅ TAMAMEN İZOLE EDİLMİŞ VE KORUNMUŞ
