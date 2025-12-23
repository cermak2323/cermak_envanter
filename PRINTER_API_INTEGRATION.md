# App.py Yazıcı Entegrasyonu

## Yapılan Değişiklikler

### 1. İmport'lar (app.py satır ~50)
```python
# Yazıcı Entegrasyonu (Linux/Ubuntu için)
try:
    import sys
    if 'linux' in sys.platform.lower() or platform.system().lower() == 'linux':
        from printer_integration import get_printer_manager
        PRINTER_ENABLED = True
    else:
        PRINTER_ENABLED = False
except ImportError:
    PRINTER_ENABLED = False
except Exception:
    PRINTER_ENABLED = False
```

- Sadece Linux/Ubuntu'da yazıcı modülü yüklenir
- Windows'ta `PRINTER_ENABLED = False` kalır
- Hata durumunda yazıcı devre dışı bırakılır

### 2. Yazıcı Başlatması (app.py satır ~155)
```python
# Yazıcı Yöneticisini Başlat (Linux/Ubuntu için)
_printer_manager = None
if PRINTER_ENABLED:
    try:
        _printer_manager = get_printer_manager()
        printer_status = _printer_manager.get_status()
        if printer_status.get('connected'):
            print(f"[PRINTER] ✓ USB Yazıcı Hazır - {printer_status.get('device', '/dev/usb/lp0')}")
        else:
            print(f"[PRINTER] ⚠️  USB Yazıcı Bağlanamadı - Yazıcı devre dışı")
    except Exception as e:
        print(f"[PRINTER] ⚠️  Yazıcı başlatılamadı: {e}")
        _printer_manager = None
else:
    print("[PRINTER] Yazıcı devre dışı (Windows ortamında çalışıyor)")
```

- App başlatılırken yazıcı kontrol edilir
- Bağlı değilse uyarı verilir, app çalışmaya devam eder
- Windows'ta yazıcı devre dışı kalır

### 3. API Endpoints

#### `/api/printer/status` - GET
Yazıcı durumunu kontrol et

```bash
curl -X GET http://localhost:5002/api/printer/status \
  -H "Authorization: Bearer TOKEN"
```

Yanıt:
```json
{
  "success": true,
  "enabled": true,
  "connected": true,
  "status": "Hazır",
  "device": "/dev/usb/lp0"
}
```

#### `/api/printer/print-qr` - POST
QR kodlu etiket yazdır

```bash
curl -X POST http://localhost:5002/api/printer/print-qr \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "qr_data": "ENVANTER_123456",
    "label_text": "Ürün Adı",
    "quantity": 1
  }'
```

Parametreler:
- `qr_data`: QR kod içeriği (zorunlu)
- `label_text`: Etiket üzerindeki metin (opsiyonel)
- `quantity`: Yazdırılacak kopya sayısı (1-100, varsayılan: 1)

#### `/api/printer/print-barcode` - POST
Barkodlu etiket yazdır

```bash
curl -X POST http://localhost:5002/api/printer/print-barcode \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "barcode_data": "1234567890",
    "barcode_type": "CODE128",
    "label_text": "Stok Kodu",
    "quantity": 5
  }'
```

Parametreler:
- `barcode_data`: Barkod verileri (zorunlu)
- `barcode_type`: Barkod türü (varsayılan: CODE128)
- `label_text`: Etiket metni (opsiyonel)
- `quantity`: Kopya sayısı (1-100, varsayılan: 1)

#### `/api/printer/print-combined` - POST
QR + Barkod kombinasyonu yazdır

```bash
curl -X POST http://localhost:5002/api/printer/print-combined \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "qr_data": "ENVANTER_123456",
    "barcode_data": "1234567890",
    "title": "Ürün Etiketi",
    "quantity": 1
  }'
```

#### `/api/printer/test` - POST
Test etiketi yazdır (Admin olması gerekli)

```bash
curl -X POST http://localhost:5002/api/printer/test \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

## Frontend Entegrasyonu

### JavaScript Örneği

```javascript
// Yazıcı durumunu kontrol et
async function checkPrinter() {
  const response = await fetch('/api/printer/status', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    }
  });
  const data = await response.json();
  return data;
}

// QR etiketi yazdır
async function printQRLabel(qrData, labelText = '', quantity = 1) {
  const response = await fetch('/api/printer/print-qr', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    },
    body: JSON.stringify({
      qr_data: qrData,
      label_text: labelText,
      quantity: quantity
    })
  });
  return await response.json();
}

// Barkod etiketi yazdır
async function printBarcodeLabel(barcodeData, labelText = '', quantity = 1) {
  const response = await fetch('/api/printer/print-barcode', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    },
    body: JSON.stringify({
      barcode_data: barcodeData,
      label_text: labelText,
      quantity: quantity
    })
  });
  return await response.json();
}

// Kombinasyon yazdır
async function printCombinedLabel(qrData, barcodeData, title = '', quantity = 1) {
  const response = await fetch('/api/printer/print-combined', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    },
    body: JSON.stringify({
      qr_data: qrData,
      barcode_data: barcodeData,
      title: title,
      quantity: quantity
    })
  });
  return await response.json();
}

// Kullanım örneği
async function printPartLabel(partCode, partName) {
  // Yazıcı durumunu kontrol et
  const status = await checkPrinter();
  
  if (!status.connected) {
    alert('Yazıcı bağlı değil!');
    return;
  }
  
  // QR kodu yazdır
  const result = await printQRLabel(
    `ENVANTER_${partCode}`,
    partName,
    1
  );
  
  if (result.success) {
    alert('Etiket başarıyla yazdırıldı!');
  } else {
    alert(`Yazıcı hatası: ${result.error}`);
  }
}
```

## Hata İşleme

Tüm endpoint'ler hata durumunda aşağıdaki format'ta yanıt verir:

```json
{
  "success": false,
  "error": "Hata açıklaması"
}
```

## Loglama

Tüm yazıcı işlemleri `logs/app.log` dosyasına kaydedilir:

```
[PRINTER] ✓ USB Yazıcı Hazır - /dev/usb/lp0
[PRINTER] QR etiketi yazdırıldı: ENVANTER_123456 x1
[PRINTER] Barkod etiketi yazdırıldı: 1234567890 x5
```

## Önemli Notlar

⚠️ **Windows'ta:**
- Yazıcı endpoint'leri hata döndürür
- `PRINTER_ENABLED = False`
- Diğer tüm sistem normal çalışır

✓ **Ubuntu'da:**
- `tspl_printer.py` ve `printer_integration.py` gerekli
- USB yazıcı `/dev/usb/lp0`'da bağlı olmalı
- İzin ayarları yapılmalı (udev kuralı veya sudo)
- Tüm endpoint'ler fonksiyonel

## Deployment Kontrol Listesi

- [ ] `tspl_printer.py` Ubuntu'ya kopyalandı
- [ ] `printer_integration.py` Ubuntu'ya kopyalandı
- [ ] `app.py` güncellemeleri uygulandı
- [ ] USB yazıcı `/dev/usb/lp0`'da bağlı
- [ ] İzin ayarları yapıldı (udev kuralı)
- [ ] `/api/printer/status` test edildi
- [ ] Test etiketi başarıyla yazdırıldı
- [ ] Hata logları kontrol edildi
