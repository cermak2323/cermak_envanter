# TSPL Barcode Printer - Hızlı Başlangıç Kılavuzu

## ⚡ 5 Adımda Başlama

### 1️⃣ Environment'ı Ayarla
```.env dosyasına ekle:
TSPL_PRINTER_HOST=localhost    # USB: localhost, Network: 192.168.x.x
TSPL_PRINTER_PORT=9100
TSPL_ENABLED=true
```

### 2️⃣ Uygulamayı Yeniden Başlat
```bash
# Uygulamayı durdurup yeniden başlat
python app.py
```

### 3️⃣ Admin Paneline Git
```
URL: http://192.168.10.27:5002/admin/tspl
```

### 4️⃣ Bağlantı Test Et
```
Admin panelinde "Test Connection" butonuna tıkla
```

### 5️⃣ QR Üret ve Yazdır
```
- Parts sayfasında QR kod üret
- "Print to TSPL" seçeneğini işaretle
- Yazdır!
```

---

## 🔗 Önemli URL'ler

| Fonksiyon | URL |
|-----------|-----|
| Admin Panel | `/admin/tspl` |
| Status API | `/api/tspl/status` |
| Test Print | `/api/tspl/test-print` |
| QR Print | `/api/tspl/print-qr/{qr_id}` |
| Batch Print | `/api/tspl/print-batch` |

---

## 📱 Curl Örnekleri

### Status Kontrol
```bash
curl http://192.168.10.27:5002/api/tspl/status
```

### Test Yazdır
```bash
curl -X POST http://192.168.10.27:5002/api/tspl/test-print \
  -H "Content-Type: application/json" \
  -d '{
    "qr_id": "TEST_001",
    "part_code": "TEST",
    "part_name": "Test"
  }'
```

### QR Üret + Yazdır
```bash
curl -X POST http://192.168.10.27:5002/generate_qr/Y129513-14532 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 5,
    "print_to_tspl": true
  }'
```

---

## 🎨 JavaScript Kullanım

```javascript
// 1. Helper'ı yükle
<script src="/static/js/tspl-printer-helper.js"></script>

// 2. Status kontrol et
await tsplPrinter.checkStatus();

// 3. QR üret ve yazdır
await generateQRWithTSPL('Y129513-14532', 10, true);

// 4. Test yazdır
await tsplPrinter.testPrint();

// 5. Batch yazdır
await tsplPrinter.printBatch(['QR_1', 'QR_2', 'QR_3']);
```

---

## ⚙️ Yazıcı Ayarları

| Ayar | Değer | Not |
|------|-------|-----|
| Protocol | TSPL | Thermal Printer Command Language |
| Port | 9100 | Standard TSPL portu |
| Bağlantı | TCP/IP | Network veya USB |
| Etiket | 100x150 mm | A6 thermal |
| DPI | 203 | Barcode scanner standardı |
| Encoding | UTF-8 | Türkçe desteklenir |

---

## 🔧 Sorun Giderme

### ❌ "Printer not connected"
```
✓ Host/Port ayarlarını kontrol et
✓ Yazıcı IP'sine ping at: ping 192.168.x.x
✓ USB yazıcı: localhost kullan
✓ Network yazıcı: IP adresini gir
```

### ❌ "TSPL_ENABLED false"
```
✓ .env'de TSPL_ENABLED=true olduğunu kontrol et
✓ Uygulamayı yeniden başlat
✓ Logs'u kontrol et: logs/app.log
```

### ❌ "Test print fails"
```
✓ Yazıcıyı yeniden başlat
✓ Port setini kontrol et (netstat -an)
✓ Firewall kurallarını kontrol et
✓ Yazıcı driver'ını güncelleştir
```

---

## 📊 Status Yanıtları

### ✅ Başarılı
```json
{
  "success": true,
  "connected": true,
  "enabled": true,
  "printer_host": "localhost",
  "printer_port": 9100
}
```

### ❌ Başarısız
```json
{
  "success": false,
  "connected": false,
  "error": "Connection timeout"
}
```

---

## 💡 İpuçları

1. **PNG Hep Oluşturulur**: TSPL yazıcı kapalı olsa bile PNG dosyası kaydedilir
2. **Batch Daha Hızlı**: 100+ QR için batch yazdırma kullan
3. **Test Önce**: Production'da kullanmadan test print yap
4. **Logs Kontrol Et**: Sorun varsa `/logs/app.log`'a bak
5. **Config Reboot**: TSPL_ENABLED değişkendikten sonra yeniden başlat

---

## 🚀 Örnek İş Akışı

```
1. Admin Panel → /admin/tspl
   ↓
2. "Test Connection" tıkla
   ↓
3. "Test Print" ile label yazdır
   ↓
4. Parts → QR kod üret
   ↓
5. Quantity: 10 gir
   ↓
6. "Print to TSPL" işaretle
   ↓
7. Generate!
   ↓
8. PNG dosyaları + TSPL çıktısı ✓
```

---

## 📞 Support

### Resmi Dokümantasyon
- `/TSPL_SETUP_GUIDE.md` - Detaylı kurulum
- `/TSPL_IMPLEMENTATION_SUMMARY.md` - Teknik detaylar
- `/test_tspl_integration.py` - Test örnekleri

### Hızlı Kontrol
```bash
# Test scripti çalıştır
python test_tspl_integration.py 1    # Status check
python test_tspl_integration.py 2    # Test print
python test_tspl_integration.py 3    # Generate + Print
```

---

## 🎯 Checklist

- [ ] `.env` dosyası güncellendi
- [ ] Uygulamayı yeniden başlattı
- [ ] Admin paneline gitti (`/admin/tspl`)
- [ ] Bağlantı test etti
- [ ] Test print yaptı
- [ ] QR üretip yazdırdı
- [ ] PNG dosyası kaydedildiğini kontrol etti

✅ Tamamlandı!

---

**Versiyon**: 1.0  
**Güncelleme**: Aralık 2025  
**Durum**: Production Ready ✓
