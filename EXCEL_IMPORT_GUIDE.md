# Excel'den Hızlı Sipariş Ekle - Kullanım Kılavuzu

## 📋 Özellik Özeti

Excel dosyalarından toplu sipariş oluşturmak için tasarlanmış hızlı sistem.

## 🚀 Nasıl Kullanılır?

### 1. Excel Dosyası Hazırlama

Excel dosyanız şu sütunları içermelidir:

| Parça Kodu | Adet |
|------------|------|
| Y113       | 5    |
| Y129       | 10   |
| Y130       | 3    |
| K003       | 7    |

**Önemli notlar:**
- Sütun başlıkları: "Parça Kodu" ve "Adet" (veya "Kod" / "Miktar")
- İlk satır başlık olmalı
- Parça kodları veritabanında bulunmalı
- Adet değerleri > 0 olmalı

### 2. Sayfaya Erişim

```
http://192.168.10.27:5002/order_system/create_orders_fast
```

### 3. Excel Dosyası Yükleme

1. **"Excel Dosyası Seç"** butonuna tıklayın
2. İngilizce `.xlsx`, `.xls` veya `.csv` dosyasını seçin
3. Sistem otomatik olarak parçaları kontrol edecek

### 4. Sipariş Listesi Adı

- Listesine özel bir ad girin (örn: CER2025001)
- **Otomatik Oluştur** butonuna tıklayarak sistem tarafından oluşturulmasını sağlayabilirsiniz

### 5. Ön İzleme

Sistem şunları gösterecektir:
- ✅ **Yeşil satırlar**: Bulundu ve eklenmeye hazır
- ❌ **Kırmızı satırlar**: Veritabanında bulunamadı

### 6. Siparişlere Ekle

Tüm parçalar kontrol edildikten sonra:
- **"Siparişlere Ekle"** butonuna tıklayın
- Sistem otomatik olarak:
  - Parça adlarını çekecek
  - Tedarikçi bilgisini alacak
  - Birim fiyatını belirleyecek
  - Toplam fiyatı hesaplayacak

## 📊 Örnek Dosya

Sistemde hazır örnek dosya vardır: `sample_order.xlsx`

İndirmek için sayfadaki **"Örnek dosyayı indir"** linkine tıklayın.

## ✨ Özellikleri

- 🔄 **Otomatik Parça Adı Çekme**: Veritabanından otomatik çekilir
- 📋 **Ön İzleme**: Eklemeden önce kontrol edin
- 🔴 **Hata Göstergesi**: Bulunamayan parçaları kırmızı ile işaret et
- ⚡ **Hızlı Toplu Ekleme**: Tüm parçaları bir kez ekle
- 📁 **Birden Fazla Format**: .xlsx, .xls, .csv desteği

## 🐛 Sorun Giderme

### "Parça Bulunamadı" Hatası
- Parça kodlarını kontrol edin
- Veritabanında var olup olmadığını doğrulayın
- Yazılım tamamen doğru olmalıdır (Y113 vs y113)

### "Excel Dosyasında Veri Bulunamadı"
- Dosyanın ilk satırında başlıklar var mı?
- Sütun adları: "Parça Kodu" ve "Adet" mi?
- Boş satırlar atlamayın

### Liste Adı Hatası
- Liste adı boş olamaz
- "Otomatik Oluştur" butonunu kullanabilirsiniz

## 📈 İstatistikler

Başarıyla eklenen siparişleri görmek için:
1. Sayfayı yenileyin (F5)
2. Alt kısımda "Mevcut Siparişleri Seç" bölümünde yeni listeyi görün

## 🔧 Teknik Bilgiler

- **Frontend**: SheetJS (XLSX) kütüphanesi
- **Backend API**: `/order_system/api/add_manual_orders`
- **Veritabanı**: MySQL (order_system_stock tablosu)
- **Desteklenen Dosyalar**: .xlsx, .xls, .csv

---

**Son Güncelleme**: 2025-12-16
**Versiyon**: 1.0
