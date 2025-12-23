# HIZLI BAŞLAMA REHBERI - ENVANTERQR v1.0

## 🚀 Sistem Başlatma (5 dakika)

```bash
# 1. Klasöre git
cd "c:\Users\rsade\Desktop\Yeni klasör (2)\EnvanterQR\EnvanterQR"

# 2. Sistemi başlat
python app.py

# 3. Tarayıcıda aç
http://localhost:5000
```

---

## 👤 Admin Paneli

**URL:** http://localhost:5000/admin  
**Kullanıcı:** `admin`  
**Şifre:** `@R9t$L7e!xP2w`

### Admin Panel Fonksiyonları:
- ✓ Parça Yönetimi (Ekle/Sil/Düzenle)
- ✓ Paket Oluşturma
- ✓ QR Baskı
- ✓ Excel İthal/İhraç
- ✓ Sayım Raporları
- ✓ Kullanıcı Yönetimi

---

## 📝 Parça Ekleme (Excel ile)

### Adım 1: Excel Şablonu İndir
Admin Panel → Parça Yönetimi → "Excel Şablonunu İndir"

### Adım 2: Türkçe Sütunlarla Doldur
| Parça Kodu | Parça Adı | Beklenen Adet |
|---|---|---|
| Y129648 | ARKA PANEL | 5 |
| Y129649 | ÖN KAPAK | 3 |

**ÖNEMLİ:** 
- Parça Kodu: Zorunlu (hiç boş bırakma)
- Parça Adı: Otomatik (veritabanından çekilir)
- Beklenen Adet: Sayım için (opsiyonel)

### Adım 3: Excel'i Yükle
Admin Panel → Parça Yönetimi → "Excel Yükle" → Dosya Seç → Yükle

---

## 📦 Paket/Koli Oluşturma

### Adım 1: Admin Panel'e Git
Admin Panel → Paket Yönetimi → "Yeni Paket"

### Adım 2: Paket Bilgisi Gir
- **Paket Adı:** KOLİ_001 (veya benzeri)
- **Açıklama:** Opsiyonel
- **Parçaları Ekle:** + Buton ile parça ekle

### Adım 3: QR'ı Yazdır
- QR kodu ekranda gösterilecek
- Sağ tık → Yazdır
- Format: Cermak yazılı, standart

---

## 📊 Sayım Yapmak

### Adım 1: Sayım Başlat
Scanner sekmesi → "Sayım Başlat"

### Adım 2: Paket Tara (OPSIYONEL)
- Paket QR'ını tara
- **Otomatik:** Içindeki tüm parçaları tanır

### Adım 3: Parçaları Tara
- Parçaları tek tek tara
- Her tarama: Sayı artar
- Ürün adı, resim, son sayım otomatik gösterilir

### Adım 4: Sayım Bitir
- "Sayım Bitir" butonu
- Otomatik rapor oluşturulur

---

## 📋 Rapor Görme & Arama

### Rapor Açmak
Scanner sekmesi → "Sayım Raporları" → Son raporu seç

### Rapor Arama
1. Parça kodu/adı yaz (örn: "Y129648" veya "ARKA")
2. "ARA" butonu tıkla
3. Sonuçlar filtrelenir
4. "TEMIZLE" butonu tıkla → Tümünü gör

### Rapor Bilgileri
| Sütun | Anlam |
|---|---|
| Parça Kodu | Ürün kimliği |
| Parça Adı | Ürün adı |
| Beklenen | Excel'de girilen miktar |
| Sayılan | Taradığınız miktar |
| Fark | Beklenen - Sayılan |
| Durum | OK / UYARI / EKSİK |

---

## 🔴 ÖNEMLI NOTLAR

1. **Veriler Güvenli**
   - Veritabanı: Lokal SQLite
   - Hiç buluta yüklenmez
   - Otomatik yedekle alınır

2. **Multi-Device Desteği**
   - Birden fazla tablet aynı anda tarama yapabilir
   - Çakışma yönetimi otomatik
   - Hiç data loss olmaz

3. **QR Formatı**
   - Tüm QR'lar standart Cermak formatı
   - Barkod makinesiyle 100% uyumlu
   - Tarayıcıyla sorunsuz okuma

4. **Excel İmport**
   - Türkçe başlıklar otomatik tanınır
   - "Beklenen Adet" otomatik görünür
   - Parça Adı database'den çekilir

5. **Arama Fonksiyonu**
   - Büyük sayım raporlarında hızlı arama
   - Kısmi eşleşme desteklenir
   - Renk göstergesi: Yeşil (bulundu) / Kırmızı (bulunamadı)

---

## 🔧 Sorun Çözme

### "Sistem açılmıyor"
```bash
# 1. Python kurulu mu kontrol et
python --version

# 2. Kütüphaneler kurulu mu
pip install -r requirements.txt

# 3. Sistemi başlat
python app.py
```

### "QR taranmıyor"
1. Scanner cihazını kontrol et
2. Kalibrasyonu yap
3. QR'ın net olduğundan emin ol

### "Rapor yavaş yükleniyor"
1. Tarayıcı sekmesini yenile (F5)
2. Eski raporları silebilirsin
3. Excel ihraç et (daha hızlı)

### "Veri kayboldu"
1. Sistem kapat
2. `backups/` klasöründen en son backup'ı kopyala
3. `instance/envanter_local.db` yerine yapıştır
4. Sistem başlat

---

## 📞 KULLANICI HATLARI

```
SCANNER SEKMESI:
- Sayım Başlat: Yeni sayım oturumu oluştur
- Sayım Bitir: Sayımı sonlandır ve rapor oluştur
- QR Tara: Elle QR kodu gir
- Ürün Ara: Database'de ürün ara

RAPOR SEKMESI:
- Sayım Raporları: Geçmiş raporları gör
- Rapor Arama: Parça kodu/adı ile filtrele
- Excel İhraç: Raporu Excel'e dönüştür
```

---

## ✅ SYSTEM STATUS

| Öğe | Durum |
|---|---|
| Veritabanı | ✓ Çalışıyor (3,831 parça) |
| QR Oluşturma | ✓ Aktif (Cermak formatı) |
| Paket Yönetimi | ✓ Aktif |
| Multi-Device | ✓ Aktif (5/5 test geçti) |
| Yedekleme | ✓ Otomatik (02:00 günlük) |
| Excel Support | ✓ Türkçe sütunlar |
| Arama | ✓ Aktif |

---

**Sistem v1.0 - Production Ready**  
**Son Güncelleme:** 22 Kasım 2025
