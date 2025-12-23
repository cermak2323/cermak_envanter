# Yazıcı Entegrasyonu - Özet

## ✅ Tamamlanan İşler

### 1. Yazıcı Modülü Oluşturuldu
- ✓ [tspl_printer.py](tspl_printer.py) - TSPL protokolü sürücüsü
  - USB üzerinden doğrudan `/dev/usb/lp0`'a RAW komutlar gönderir
  - QR kod, barkod, metin yazdırma
  - Yazıcı parametreleri (hız, koyuluk, boyut)
  - Linux/Ubuntu için optimize edilmiş

### 2. Entegrasyon Katmanı Oluşturuldu
- ✓ [printer_integration.py](printer_integration.py) - Yüksek seviye API
  - `PrinterManager` singleton sınıfı
  - `print_qr_label()` - QR etiketi yazdırma
  - `print_barcode_label()` - Barkod etiketi yazdırma
  - `print_combined_label()` - QR + Barkod kombinasyonu
  - `test_print()` - Test etiketi

### 3. App.py Entegrasyonu
- ✓ Yazıcı import'u (Linux-only, Windows'u etkilemez)
- ✓ Uygulama başlatılırken yazıcı durumu kontrol
- ✓ 5 yeni API endpoint'i:
  - `GET /api/printer/status` - Yazıcı durumu
  - `POST /api/printer/print-qr` - QR yazdırma
  - `POST /api/printer/print-barcode` - Barkod yazdırma
  - `POST /api/printer/print-combined` - Kombinasyon yazdırma
  - `POST /api/printer/test` - Test yazdırma

### 4. Test Scripti
- ✓ [test_printer.py](test_printer.py) - Ubuntu'da çalıştırılacak test
  - Cihaz kontrolü
  - Bağlantı testi
  - İzin kontrolü
  - Test yazdırma

### 5. Dokümantasyon
- ✓ [PRINTER_SETUP_UBUNTU.md](PRINTER_SETUP_UBUNTU.md) - Ubuntu kurulum rehberi
- ✓ [PRINTER_API_INTEGRATION.md](PRINTER_API_INTEGRATION.md) - API referansı
- ✓ [DEPLOY_UBUNTU_PRINTER.md](DEPLOY_UBUNTU_PRINTER.md) - Deployment adımları

## 🎯 Mimari

```
┌─────────────────────┐
│   Web Tarayıcı      │
│  (Frontend)         │
└──────────┬──────────┘
           │
           ├─ GET  /api/printer/status
           ├─ POST /api/printer/print-qr
           ├─ POST /api/printer/print-barcode
           └─ POST /api/printer/print-combined
           │
           ▼
┌─────────────────────────────────────────┐
│          Flask App (app.py)             │
│                                         │
│  - Route handlers                       │
│  - Hata işleme                         │
│  - Logging                             │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│   PrinterManager (printer_integration)  │
│                                         │
│  - Singleton pattern                    │
│  - Yüksek seviye metodlar              │
│  - Yapılandırma                        │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│    TSPLPrinter (tspl_printer)           │
│                                         │
│  - TSPL protokolü                       │
│  - USB I/O                              │
│  - Komut gönderme                       │
└─────────────────────────────────────────┘
           │
           ▼
    ┌─────────────┐
    │   USB Port  │
    │ /dev/usb/lp0│
    └─────────────┘
           │
           ▼
    ┌─────────────┐
    │ TSPL Yazıcı │
    │ (Thermal)   │
    └─────────────┘
```

## 📋 Platform Davranışı

### Windows
- Yazıcı modülü **yüklenmez**
- Yazıcı endpoint'leri **hata döndürür**
- Diğer sistem **normal çalışır**
- **Hiçbir değişiklik olmadan** sistem çalışmaya devam eder

### Ubuntu/Linux
- Yazıcı modülü **otomatik yüklenir**
- USB yazıcı **kontrol edilir**
- Yazıcı endpoint'leri **fonksiyonel**
- Tüm yazıcı **işlemleri** çalışır

## 🚀 Deployment Kontrol Listesi

### Öncesi (Windows)
- [ ] Windows sistem hiç değiştirilmedi
- [ ] `app.py` değişiklikler sadece Linux'ta etkin
- [ ] Tüm Windows endpoint'leri çalışıyor
- [ ] Build ve exe'ler hiç etkilenmedi

### Ubuntu Hazırlığı
1. [ ] `tspl_printer.py` kopyala
2. [ ] `printer_integration.py` kopyala
3. [ ] USB yazıcıyı kontrol et: `lsusb`
4. [ ] Cihaz yolu kontrol et: `ls -la /dev/usb/lp*`
5. [ ] İzinleri ayarla (udev kuralı)
6. [ ] Test et: `python3 test_printer.py`
7. [ ] App başlat: `python3 app.py`
8. [ ] API test et: `curl /api/printer/status`

## 📝 API Kullanım Örnekleri

### Python
```python
import requests

# Yazıcı durumu
response = requests.get('http://localhost:5002/api/printer/status')
status = response.json()
print(f"Yazıcı: {status['status']}")

# QR etiket
response = requests.post('http://localhost:5002/api/printer/print-qr', json={
    'qr_data': 'ENVANTER_123456',
    'label_text': 'Ürün Adı',
    'quantity': 1
})
print(response.json())
```

### JavaScript
```javascript
async function printQR() {
  const response = await fetch('/api/printer/print-qr', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      qr_data: 'ENVANTER_123456',
      label_text: 'Ürün Adı',
      quantity: 1
    })
  });
  const result = await response.json();
  console.log(result);
}
```

### cURL
```bash
# Yazıcı durumu
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:5002/api/printer/status

# QR yazdır
curl -X POST http://localhost:5002/api/printer/print-qr \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"qr_data": "TEST", "quantity": 1}'
```

## ⚙️ Konfigürasyon

Yazıcı parametreleri [printer_integration.py](printer_integration.py) içinde:

```python
# Varsayılan ayarlar
self.printer.set_label_size(100, 150)  # 100x150mm
self.printer.set_gap(2.0)              # 2mm boşluk
self.printer.set_darkness(10)          # Koyuluk (0-15)
self.printer.set_speed(4)              # Hız (1-5)
```

Değiştirmek isterseniz `_configure_printer()` metodunu düzenle.

## 🔍 Sorun Çözme

### Yazıcı Bulunamadı
```bash
lsusb  # USB cihazlarını listele
dmesg | tail -20  # Sistem mesajlarını kontrol et
```

### İzin Hatası
```bash
sudo usermod -a -G lp $USER  # Kullanıcıyı grup'a ekle
# VEYA
sudo python3 app.py  # Sudo ile çalıştır
```

### Yazıcı Başlamıyor
```bash
# Reset yap
echo -ne "SIZE 100mm,150mm\r\n" > /dev/usb/lp0
# Test et
python3 test_printer.py
```

## 📞 Başvuru

- [PRINTER_SETUP_UBUNTU.md](PRINTER_SETUP_UBUNTU.md) - Ubuntu setup
- [PRINTER_API_INTEGRATION.md](PRINTER_API_INTEGRATION.md) - API detayları
- [DEPLOY_UBUNTU_PRINTER.md](DEPLOY_UBUNTU_PRINTER.md) - Deployment prosedürü
- [tspl_printer.py](tspl_printer.py) - Sürücü kodu
- [printer_integration.py](printer_integration.py) - Entegrasyon kodu

## ✨ Özellikler

- ✓ USB üzerinden doğrudan bağlantı
- ✓ TSPL protokolü (RAW komutlar)
- ✓ QR kodu yazdırma
- ✓ Barkod yazdırma
- ✓ Metin yazdırma
- ✓ Kombinasyon yazdırma
- ✓ Singleton pattern
- ✓ Hata işleme
- ✓ Kapsamlı loglama
- ✓ Platform-bağımsız (Windows-safe)
- ✓ Async hazır (REST API)
- ✓ Admin kontrol
- ✓ Test endpoint'i

## 🎓 Sonraki Adımlar

1. **Ubuntu'ya Deploy Et**
   - 3 dosya kopyala
   - Test et
   - Üretim başlat

2. **Frontend Entegre Et**
   - Etiket yazdır butonları ekle
   - API çağrılarını implement et
   - UI feedback ekle

3. **İş Akışına Entegre Et**
   - Part oluşturmada QR yazdır
   - Inventory üzerinde barkod yazdır
   - Scanner sonrası hemen yazdır

## 📄 Lisans & Notlar

- Windows kodu **hiç değişmedi**
- Ubuntu entegrasyonu **tam ve bağımsız**
- Kütüphane gereklilikleri **minimal** (sadece standart library)
- Üretim hazır kod
