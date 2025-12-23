# Yedek Parça Bilgi Sistemi - Kullanım Kılavuzu

## Sistem Özeti
Yedek Parça Bilgi Sistemi, ana envanter sisteminden tamamen bağımsız olarak çalışan bir parça katalog sistemidir.

### Özellikler:
- ✅ Excel ile toplu parça yükleme
- ✅ Parça kodu ve adı ile arama
- ✅ Otomatik EUR/TRY kur dönüşümü (TCMB)
- ✅ Admin sisteminden fotoğraf entegrasyonu
- ✅ Stok takibi (normal, kritik, beklenen)
- ✅ Tedarikçi ve fiyat bilgileri

## Erişim
Sistem Seçim menüsünden veya doğrudan URL ile:
```
http://192.168.10.27:5002/parts_info/
```

## Excel Yükleme

### Gerekli Sütunlar:
Excel dosyanızda aşağıdaki sütunlar **mutlaka** bulunmalıdır:

| Sütun Adı | Açıklama | Örnek |
|-----------|----------|-------|
| Parça Kodu | Benzersiz parça kodu | 19111-01342 |
| Parça Adı | Parçanın adı | Motor Kapağı |
| Stok | Mevcut stok adedi | 15 |
| Tedarikçi | Tedarikçi firma adı | ABC Tedarik |
| Geliş (Euro) | Alış fiyatı (EUR) | 25.50 |
| Tanım | Parça açıklaması | Siyah renk, metal |
| Satış Fiyatı (EUR) | Satış fiyatı (EUR) | 35.00 |

### Opsiyonel Sütunlar:
- **Kritik stok**: Minimum stok seviyesi
- **Beklenen stok**: Sipariş edilen miktar

### Excel Örneği:

```
Parça Kodu    | Parça Adı        | Stok | Kritik stok | Beklenen stok | Tedarikçi    | Geliş (Euro) | Tanım              | Satış Fiyatı (EUR)
19111-01342   | Motor Kapağı     | 15   | 5           | 20            | ABC Tedarik  | 25.50        | Siyah renk, metal  | 35.00
19111-01343   | Yağ Filtresi     | 8    | 10          | 25            | XYZ Parts    | 12.00        | Standart tip       | 18.50
19111-01344   | Fren Balatası    | 3    | 5           | 15            | DEF Motor    | 45.00        | Ön takım           | 65.00
```

## Kullanım Adımları

### 1. Excel Hazırlama
- Excel dosyanızı yukarıdaki formata uygun hazırlayın
- Tüm zorunlu sütunların dolu olduğundan emin olun
- Fiyatları ondalık ayırıcı olarak nokta (.) kullanarak yazın

### 2. Excel Yükleme
- "Excel Yükle" bölümündeki alana tıklayın veya dosyayı sürükleyin
- Sistem otomatik olarak yükleme yapacaktır
- Sonuç mesajında kaç kayıt eklendiği/güncellendiği gösterilir

### 3. Fotoğraf Eşitleme
- Admin sisteminde zaten fotoğrafı olan parçalar varsa
- "Fotoğrafları Eşitle" butonuna tıklayın
- Admin sistemindeki fotoğraflar parts_info'ya kopyalanır

### 4. Arama ve Görüntüleme
- Arama kutusuna parça kodu veya adı yazın
- Enter'a basın veya "Ara" butonuna tıklayın
- "Tümünü Göster" ile tüm parçaları listeleyin

## Kur Bilgisi
Sistem otomatik olarak TCMB'den (Türkiye Cumhuriyet Merkez Bankası) güncel EUR/TRY kurunu çeker ve:
- Alış fiyatlarını TRY'ye çevirir
- Satış fiyatlarını TRY'ye çevirir
- Kur bilgisi sayfanın üst kısmında gösterilir

## Önemli Notlar

### Veri Güvenliği
- ✅ Sistem tamamen bağımsızdır (ayrı tablo: `parts_info`)
- ✅ Ana envanter sistemine dokunmaz
- ✅ Aynı parça kodu ile yükleme yapılırsa mevcut kayıt güncellenir

### Fotoğraflar
- Fotoğraflar admin sisteminden çekilir
- Admin sistemde fotoğraf yoksa boş simge gösterilir
- Manuel fotoğraf yükleme şu an parts_info'da mevcut değil

### Stok Renk Kodları
- 🟢 **Yeşil**: Stok kritik seviyenin üzerinde
- 🟡 **Sarı**: Stok kritik seviyenin altında
- 🔴 **Kırmızı**: Stok bitti (0)

## Sorun Giderme

### "Eksik sütunlar" hatası
- Excel'inizde tüm zorunlu sütunların olduğundan emin olun
- Sütun başlıklarının tam olarak yukarıdaki gibi olduğunu kontrol edin
- Türkçe karakterlere dikkat edin

### Kur güncellenmiyor
- İnternet bağlantınızı kontrol edin
- TCMB sitesine erişim olup olmadığını test edin
- Hata durumunda varsayılan kur (35.00) kullanılır

### Fotoğraflar görünmüyor
- "Fotoğrafları Eşitle" butonuna tıklayın
- Admin sistemde ilgili parçanın fotoğrafının olduğundan emin olun
- Parça kodlarının admin ve parts_info'da aynı olduğunu kontrol edin

## API Endpoints (Geliştiriciler için)

```
GET  /parts_info/                      - Ana sayfa
GET  /api/parts_info/search?q=xxx      - Parça ara
GET  /api/parts_info/get_all           - Tüm parçaları getir
POST /api/parts_info/upload_excel      - Excel yükle
POST /api/parts_info/sync_photos       - Fotoğrafları eşitle
```

## Veritabanı Şeması

```sql
CREATE TABLE parts_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    part_code VARCHAR(100) UNIQUE NOT NULL,
    part_name VARCHAR(255) NOT NULL,
    stock INT DEFAULT 0,
    critical_stock INT DEFAULT 0,
    expected_stock INT DEFAULT 0,
    supplier VARCHAR(255),
    purchase_price_eur DECIMAL(10, 2),
    sale_price_eur DECIMAL(10, 2),
    description TEXT,
    photo_path VARCHAR(500),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Destek
Sorunlar için sistem yöneticinize başvurun.
