# 🎯 TAKEUCHI PARÇA YÖNETIM SİSTEMİ - HIZLI BAŞLANGIÇ

## 🚀 Sistem Harita

```
┌─────────────────────────────────────────────────────┐
│        TAKEUCHI PARÇA YÖNETİMİ MODÜLÜ              │
└─────────────────────────────────────────────────────┘
         │
         ├─ 🔧 Ana Menü (/takeuchi)
         │   ├─ ➕ Parça Ekle
         │   └─ ✅ Parça Kontrol
         │
         ├─ ⚙️ Admin Paneli (/takeuchi/admin)
         │   ├─ 📥 Excel Yükleme
         │   ├─ 📊 İstatistikler
         │   ├─ 📋 Geçici Siparişler
         │   └─ 📦 Parça Listesi
         │
         └─ 🔐 API Endpointleri (/api/takeuchi/...)
             ├─ POST /admin/upload-parts
             ├─ GET /admin/parts-list
             ├─ POST /admin/create-order
             └─ ...11 toplam endpoint
```

## 📋 ADIM ADIM KULLANIM

### AŞAMA 1: Excel Dosyasını Hazırla

**Şablon Indirme:**
```
1. /takeuchi/admin adresine git
2. "📋 Şablon İndir" butonuna tıkla
3. takeuchi_parca_template.xlsx indirilecek
```

**Veya Manuel Oluştur:**
```
Excel dosyasında 5 sütun:
┌──────────────┬────────────────┬─────────────────┬────────────┬─────────────┐
│ Parça Kodu   │ Parça Adı      │ Değişen Kod     │ Build Out  │ Fiyat (TL)  │
├──────────────┼────────────────┼─────────────────┼────────────┼─────────────┤
│ TP001        │ Motor Parçası  │ ALT-TP001      │ MOTOR-12   │ 1500.00     │
│ TP002        │ Piston         │ ALT-TP002      │ PISTON-8   │ 250.00      │
│ TP003        │ Segment        │ ALT-TP003      │ SEG-16     │ 75.00       │
└──────────────┴────────────────┴─────────────────┴────────────┴─────────────┘
```

### AŞAMA 2: Dosyayı Yükle

**Seçenek A - Sürükle-Bırak:**
```
1. Admin paneli açık
2. "📥 Excel dosyasını buraya sürükleyin" alanına dosyayı sürükle
3. Otomatik yüklenir
```

**Seçenek B - Tıkla ve Seç:**
```
1. Admin paneli açık
2. "📁 Dosya Seç" butonuna tıkla
3. Bilgisayardan dosya seç
4. Yüklemeyi başlat
```

### AŞAMA 3: Sonuç Kontrol Et

```
✅ Başarılı Yükleme:
   - Kaç parça yüklendiyse gösterilir
   - Parça tablosu otomatik yenilenir
   - Hata var mı gösterilir

❌ Hata Durumunda:
   - Hata mesajı gösterilir
   - Hangi satırda sorun olduğu belirtilir
   - Sayfa yenilemeyi deneyin
```

## 🎯 KULLANIM SENARYOLARI

### Senaryo 1: İlk Kez Parça Yükleme

```
1. Admin Paneline Git: /takeuchi/admin
2. Excel Dosyasını Hazırla (şablon indir veya manuel)
3. Sürükle-Bırak ile Yükle
4. Sonuç Kontrolü Et
5. Başarılı! ✅ Parçalar artık kullanılabilir
```

### Senaryo 2: Parça Bilgilerini Güncelle

```
1. Excel'de mevcut parçaları aç
2. Fiyatı değiştir (örn: 150 → 180)
3. Admin Paneline git
4. Dosyayı tekrar yükle
5. Sistem otomatik günceller
6. Eski 150 → Yeni 180 ✅
```

### Senaryo 3: Yeni Parçalar Ekle

```
1. Excel şablonuna yeni satırlar ekle
2. 10-20 yeni parça ekle
3. Yükle
4. Tüm parçalar listelenir
5. Hepsi sipariş için hazır ✅
```

## 📊 ADMIN PANELİ KULLANIMI

### İstatistikler Kartı

```
┌─────────────────────────────────────────┐
│ 📊 Sistem İstatistikleri                │
├─────────────────────────────────────────┤
│ ┌──────────┬──────────┬──────────────┐  │
│ │   10     │    45    │     120      │  │
│ │ Geçici   │ Toplam   │ Yüklü        │  │
│ │ Siparişler│ Parçalar│ Parçalar     │  │
│ └──────────┴──────────┴──────────────┘  │
│                                         │
│ 🔄 İstatistikleri Yenile               │
└─────────────────────────────────────────┘
```

### Excel Yükleme Bölümü

```
┌─────────────────────────────────────────┐
│ 📥 Parça Yükle (Excel)                  │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │           📄                        │ │
│ │  Excel dosyasını buraya sürükleyin │ │
│ │         veya tıklayarak seçin       │ │
│ │    Desteklenen: .xlsx, .xls         │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌──────────────────────────────────┐   │
│ │ 📁 Dosya Seç │ 📋 Şablon İndir  │   │
│ └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Parça Listesi Tablosu

```
Parça Kodu │ Parça Adı    │ Değişen Kod │ Build Out │ Fiyat  │ Tarih
───────────┼──────────────┼─────────────┼───────────┼────────┼──────
TP001      │ Motor        │ ALT-001    │ MOTOR-12 │ 1500₺  │ 21.12
TP002      │ Piston       │ ALT-002    │ PISTON-8 │ 250₺   │ 21.12
TP003      │ Segment      │ ALT-003    │ SEG-16   │ 75₺    │ 21.12
```

## 🔄 API TESTLERI

### Excel Yükleme Testi

```bash
curl -X POST http://localhost:5002/api/takeuchi/admin/upload-parts \
  -F "file=@template.xlsx" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Başarılı Yanıt:**
```json
{
  "success": true,
  "imported_count": 3,
  "total_rows": 3,
  "error_rows": []
}
```

### Parça Listesi Testi

```bash
curl -X GET http://localhost:5002/api/takeuchi/admin/parts-list \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Yanıt:**
```json
{
  "success": true,
  "parts": [
    {
      "id": 1,
      "part_code": "TP001",
      "part_name": "Motor",
      "alternative_code": "ALT-001",
      "build_out": "MOTOR-12",
      "cost_price": 1500.0,
      "created_at": "2025-12-21T20:00:00"
    }
  ],
  "total": 1
}
```

## ⚙️ SİSTEM AYARLARI

### URL ADRESLERI

```
Ana Menü:        http://192.168.10.27:5002/takeuchi
Parça Ekle:      http://192.168.10.27:5002/takeuchi/add
Parça Kontrol:   http://192.168.10.27:5002/takeuchi/check
Admin Paneli:    http://192.168.10.27:5002/takeuchi/admin
```

### VERİTABANI TABLOSU

```
Tablo Adı              │ Amaç
───────────────────────┼──────────────────────────────
takeuchi_parts         │ Parça Kataloğu (EXCEL'DEN)
takeuchi_part_orders   │ Resmi Siparişler
takeuchi_order_items   │ Sipariş Kalemleri
takeuchi_temp_orders   │ Geçici Siparişler
takeuchi_temp_order_items │ Geçici Kalemler
```

## 🔒 İZİNLER VE GÜVENLİK

### Erişim Seviyeleri

```
┌──────────────────────────────────────┐
│ Admin Kullanıcı                      │
├──────────────────────────────────────┤
│ ✅ Excel yükleyebilir                │
│ ✅ Parça listesini görebilir         │
│ ✅ Siparişleri oluşturabilir         │
│ ✅ Tüm admin işlevlerine erişim      │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ Normal Kullanıcı                     │
├──────────────────────────────────────┤
│ ✅ Parça ekleyebilir                 │
│ ✅ Siparişleri kontrol edebilir      │
│ ❌ Excel yükleyemez                  │
│ ❌ Admin paneline giriş yasak        │
└──────────────────────────────────────┘
```

## 🐛 SORA SORULAN SORULAR

### S: Excel'de 1000 parça varsa hepsi yüklenir mi?
**C:** Evet! Yükleme sırasında:
- 💾 Veritabanı bağlantısı kontrol edilir
- ✅ Her satır valide edilir
- ⚡ Hızlı şekilde işlenir
- 📊 Sonuç raporu verilir

### S: Parça zaten yüklü ise ne olur?
**C:** İki seçenek:
- **Güncelle:** Tüm alanlar yeni verilerle güncellenir
- **Bildir:** Kaç parçanın güncellendiği raporlanır

### S: Hata olursa tüm dosya başarısız mı olur?
**C:** Hayır! Satır satır işlenir:
- ✅ Geçerli satırlar yüklenir
- ⚠️ Hatalı satırlar atlanır
- 📋 Hata raporu gösterilir

### S: Mevcut parça sistemi etkilenir mi?
**C:** HAYIR! Tamamen izole sistem:
- ✅ Başka tablolarla ilişkisi yok
- ✅ Mevcut siparişler etkilenmez
- ✅ QR kod sistemi etkilenmez

---

**DURUM:** ✅ ÜRETIME HAZIR

Herhangi bir soru veya sorun için admin ile iletişime geçin.
