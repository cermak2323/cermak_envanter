# TSPL Barcode Printer Integration - Kurulum ve Kullanım

## Genel Bakış

Sistem artık **TSPL (Thermal Printer Command Language)** desteğine sahiptir. Bu, QR kodların sadece PNG dosyası olarak değil, aynı zamanda doğrudan thermal barcode yazıcıdan çıktı alınmasını sağlar.

### Özellikleri:
- ✅ QR kod PNG dosya oluşturması (mevcut, aynı şekilde devam eder)
- ✅ TSPL thermal barcode yazıcıdan direkt yazdırma
- ✅ Batch yazdırma (birden fazla QR bir seferde)
- ✅ Test bağlantı ve test yazdırması
- ✅ Admin paneli üzerinden konfigürasyon
- ✅ Windows ve Linux uyumlu

---

## Kurulum Adımları

### 1. TSPL Printer Modülü Zaten Kurulu
Dosyalar sizin proje klasöründe mevcuttur:
- `tspl_printer.py` - TSPL printer driver
- `static/js/tspl-printer-helper.js` - Frontend helper
- `.env.tspl.example` - Environment örneği

### 2. Environment Değişkenleri Ayarla

`.env` dosyanıza (veya `.env.tspl.example`'den kopyalayarak) aşağıdakileri ekleyin:

```env
# TSPL Barcode Printer Host (yazıcı IP adresi)
# localhost = USB bağlı yazıcı
# 192.168.x.x = Network yazıcı
TSPL_PRINTER_HOST=localhost

# TSPL Barcode Printer Port (default: 9100)
TSPL_PRINTER_PORT=9100

# TSPL desteğini etkinleştir
# true = Aktif (QR'lar yazıcıdan çıktı alacak)
# false = Pasif (sadece PNG oluşturulacak)
TSPL_ENABLED=false
```

### 3. Thermal Barcode Printer Kurulumu

#### Windows'ta:
```bash
# USB Yazıcı
# Cihaz Yöneticisi'nde yazıcıyı bulun ve direkt USB port'a bağlayın
# Port: localhost:9100

# Network Yazıcı
# Yazıcının IP adresini belirleyin (öğretici tarafından verilecek)
# Örnek: TSPL_PRINTER_HOST=192.168.1.100
```

#### Linux'ta:
```bash
# USB Yazıcı
# /dev/usb/* portunu belirleyin
sudo ls -l /dev/usb/

# Network Yazıcı
# Yazıcının IP adresini kullanın
ping 192.168.x.x
```

---

## Kullanım

### Option 1: Web API ile QR Üretme ve TSPL Yazdırma

#### POST `/generate_qr/<part_code>`

**İstek Örneği:**
```json
{
  "quantity": 10,
  "print_to_tspl": true
}
```

**Yanıt:**
```json
{
  "success": true,
  "message": "10 adet QR kod retildi",
  "generated": [
    {
      "qr_id": "Y129513-14532_1",
      "qr_number": 1,
      "qr_image_url": "/qr_image/Y129513-14532/Y129513-14532_1"
    }
  ],
  "tspl_results": [
    {
      "qr_id": "Y129513-14532_1",
      "success": true,
      "message": "QR Y129513-14532_1 printed successfully"
    }
  ]
}
```

### Option 2: Frontend JavaScript Kullanma

HTML dosyanıza ekleyin:
```html
<script src="/static/js/tspl-printer-helper.js"></script>
```

**Kullanım Örneği:**
```javascript
// QR üretme ve TSPL'ye yazdırma
await generateQRWithTSPL('Y129513-14532', 10, true);

// Sadece QR üretme (TSPL'siz)
await generateQRWithTSPL('Y129513-14532', 10, false);

// Yazıcı durumunu kontrol et
await tsplPrinter.checkStatus();

// Manual yazdırma
await tsplPrinter.printQR('Y129513-14532_1', 1);

// Batch yazdırma
await tsplPrinter.printBatch(['Y129513-14532_1', 'Y129513-14532_2']);
```

### Option 3: Direct API Endpoints

#### Test Yazdırması
```bash
curl -X POST http://localhost:5002/api/tspl/test-print \
  -H "Content-Type: application/json" \
  -d '{
    "qr_id": "TEST_QR_001",
    "part_code": "TEST_CODE",
    "part_name": "Test Part"
  }'
```

#### Yazıcı Durumu
```bash
curl http://localhost:5002/api/tspl/status
```

#### Tek QR Yazdırma
```bash
curl -X POST http://localhost:5002/api/tspl/print-qr/Y129513-14532_1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 1}'
```

#### Batch Yazdırma
```bash
curl -X POST http://localhost:5002/api/tspl/print-batch \
  -H "Content-Type: application/json" \
  -d '{
    "qr_ids": ["Y129513-14532_1", "Y129513-14532_2", "Y129513-14532_3"]
  }'
```

---

## TSPL Komutları (Teknik Detaylar)

Sistem otomatik olarak aşağıdaki TSPL komutlarını üretir:

```tspl
SIZE 100 MM, 150 MM          # Etiket boyutu
GAP 3 MM, 0 MM               # Etiketler arası boşluk
CODEPAGE UTF-8               # Karakter kodlaması
CLS                          # Tamponu temizle
TEXT 8,10,"2",0,1,1,"CERMAK" # Başlık
BARCODE 10,25,QR,6,A,0,"..."  # QR kod
TEXT 10,145,"0",0,1,1,"Y129513-14532"  # Parça kodu
TEXT 10,160,"0",0,1,1,"Parça Adı"      # Parça adı
TEXT 10,175,"0",0,1,1,"Y129513-14532_1" # QR ID
PRINT 1                      # Yazdır (1 kopya)
```

### Etiket Özellikleri:
- **Boyut**: 100mm x 150mm (A6 termal etiket)
- **QR Kod**: 6 (versiyon auto), M hata toleransı
- **Font**: Arial/Liberation Sans (Linux uyumlu)
- **Encoding**: UTF-8 (Türkçe karakterler desteklenir)

---

## Sorun Giderme

### "Printer not connected"
1. Yazıcı IP/Port ayarlarını kontrol edin
2. Ağ bağlantısını test edin: `ping 192.168.x.x`
3. USB yazıcı için: `TSPL_PRINTER_HOST=localhost` kullanın

### "TSPL_ENABLED" false gösteriyor
1. `.env` dosyasında `TSPL_ENABLED=true` olduğundan emin olun
2. App'i yeniden başlatın
3. Log'lara bakın: `logs/app.log`

### Thermal Printer Tanınmıyor (Windows)
1. Cihaz Yöneticisi'nde (Device Manager) "Universal Serial Bus devices" altında kontrol edin
2. Yazıcı manufacturer driver'ını indirin ve kurun
3. Yazıcı komut dilinin TSPL olduğundan emin olun

### Türkçe Karakterler Yazmıyor
1. `.env`'de `CODEPAGE UTF-8` kullanıldığından emin olun
2. Yazıcı firmware güncellemesini kontrol edin
3. Font seçimini yazıcı ayarlarında kontrol edin

---

## API Referansı

### GET `/api/tspl/status`
Yazıcı durumunu kontrol et
```json
{
  "success": true,
  "enabled": true,
  "connected": true,
  "printer_host": "localhost",
  "printer_port": 9100
}
```

### POST `/api/tspl/test-print`
Test yazdırması yap
```json
{
  "qr_id": "TEST_001",
  "part_code": "TEST",
  "part_name": "Test Part"
}
```

### POST `/api/tspl/print-qr/<qr_id>`
Tek QR yazdır
```json
{"quantity": 1}
```

### POST `/api/tspl/print-batch`
Batch yazdır
```json
{"qr_ids": ["QR_1", "QR_2", "QR_3"]}
```

### GET `/api/tspl/config` (Admin)
Konfigürasyon görüntüle

### POST `/api/tspl/config` (Admin)
Konfigürasyon güncelle

---

## Önemli Notlar

⚠️ **PNG Dosyası Hala Oluşturulur**
- TSPL yazıcı etkinleştirilse bile PNG dosyası her zaman oluşturulur
- Bu, yazıcı hatası durumunda fallback sağlar

⚠️ **Ağ Gecikmeleri**
- Batch yazdırması sırasında her QR için ~100-500ms gecikme olabilir
- Büyük batch'ler için `print_batch` kullanın

⚠️ **Yazıcı Kapasitesi**
- Çoğu thermal yazıcı aynı anda 10-20 etiket işleyebilir
- Daha büyük job'lar için işi parçala

---

## Geliştirme Notları

### TSPL Printer Sınıfı (Python)
```python
from tspl_printer import TSPLPrinter, get_tspl_manager

# Direkt kullanım
printer = TSPLPrinter(host='192.168.1.100', port=9100)
printer.connect()
printer.print_qr(qr_id='Y129513-14532_1', ...)
printer.disconnect()

# Manager üzerinden
manager = get_tspl_manager()
success, msg = manager.print_qr_code(qr_id='Y129513-14532_1', ...)
```

### Custom TSPL Komutları
```python
# Özel TSPL etiketi oluştur
tspl = printer.generate_tspl_qr(
    qr_data='CUSTOM_DATA',
    qr_id='CUSTOM_QR_001',
    part_code='CUSTOM_CODE',
    part_name='Custom Part',
    quantity=5,
    label_width=100,
    label_height=150
)
```

---

## İletişim & Support

Sorularınız veya sorunlarınız varsa:
1. Logs kontrol edin: `logs/app.log`
2. Admin panelinden test yazdırması yapın
3. API'yi curl ile test edin

---

**Son Güncelleme:** Aralık 2025
**Versiyon:** 1.0
