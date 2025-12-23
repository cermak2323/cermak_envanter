# Ubuntu Deploy Hazırlık - Yazıcı Entegrasyonu

## Hızlı Özet

Yazıcı entegrasyonu Windows'u etkilemez. Ubuntu'ya yalnızca şu 3 dosya eklenmeli:

1. `tspl_printer.py` - TSPL sürücüsü
2. `printer_integration.py` - Entegrasyon katmanı
3. `app.py` - App.py zaten güncellendi

## Deploy Adımları

### Adım 1: Dosyaları Ubuntu'ya Kopyala

```bash
# SSH ile Ubuntu sunucuya bağlan
ssh user@192.168.0.XX

# App dizinine git
cd /path/to/EnvanterQR

# Dosyaları kopyala (Windows'tan)
# PowerShell'den:
scp tspl_printer.py user@192.168.0.XX:/path/to/EnvanterQR/
scp printer_integration.py user@192.168.0.XX:/path/to/EnvanterQR/
```

### Adım 2: USB Yazıcıyı Kontrol Et

```bash
# 1. USB cihazlarını listele
lsusb

# 2. /dev cihazlarını kontrol et
ls -la /dev/usb/lp*
ls -la /dev/lp*

# 3. Detaylı bilgi
dmesg | grep -i "usb\|printer" | tail -10
```

Yazıcı `/dev/usb/lp0` veya `/dev/lp0` adresinde olmalı.

### Adım 3: İzin Ayarla

**Seçenek A: sudo ile çalıştırma (Hızlı Test)**
```bash
sudo python3 app.py
```

**Seçenek B: udev kuralı (Üretim Önerilir)**

```bash
# 1. Yazıcı cihaz bilgisini al
lsusb | grep -i "printer\|thermal"
# Çıkış örneği: Bus 001 Device 005: ID 0471:0019 ...

# 2. Cihaz ID'lerini not et: idVendor=0471, idProduct=0019

# 3. udev kuralı oluştur
sudo nano /etc/udev/rules.d/99-tspl-printer.rules
```

Aşağıdaki satırları ekle (cihaz ID'lerini kendi değerlerin ile değiştir):
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0471", ATTRS{idProduct}=="0019", MODE="0666"
SUBSYSTEM=="usb_device", ATTRS{idVendor}=="0471", ATTRS{idProduct}=="0019", MODE="0666"
```

Kaydet (Ctrl+O, Enter, Ctrl+X)

```bash
# 4. Kuralı uygula
sudo udevadm control --reload-rules
sudo udevadm trigger

# 5. İzni kontrol et
ls -la /dev/usb/lp0
# crw-rw-rw- oluşmalı (666 izin)
```

### Adım 4: Test Et

```bash
# Yazıcı test scripti çalıştır
python3 test_printer.py

# Çıkış örneği:
# ==================================================
# TSPL Yazıcı Test - Ubuntu
# ==================================================
# 1️⃣  Cihaz Kontrolü
# ✓ Cihaz bulundu: /dev/usb/lp0
# ✓ Yazma izni var
# 2️⃣  Yazıcı Bağlantısı
# ✓ Yazıcı bağlandı
#   Durum: Hazır
# ...
```

### Adım 5: App'i Başlat

```bash
# Normal başlatma (udev kuralı var ise)
python3 app.py

# Çıkış örneği:
# [PRINTER] ✓ USB Yazıcı Hazır - /dev/usb/lp0
# ==================================================
#  CERMAK ENVANTER QR SİSTEMİ v2.0
# ==================================================
#  Dashboard:      http://0.0.0.0:5002
#  ...
#  Printer:        USB TSPL Ready (/dev/usb/lp0)
# ==================================================
```

### Adım 6: API Test Et

```bash
# Yazıcı durumunu kontrol et
curl -X GET http://localhost:5002/api/printer/status

# Test etiketi yazdır (Admin token gerekli)
curl -X POST http://localhost:5002/api/printer/test \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_TOKEN"

# Yanıt:
# {"success": true, "message": "Test etiketi başarıyla yazdırıldı"}
```

## Sorun Çözme

### Problem: Cihaz Bulunamadı

```bash
# 1. Yazıcı USB'ye bağlı mı?
lsusb

# 2. Sistem tarafından tanındı mı?
dmesg | tail -20

# 3. Alternatif cihaz yolları
find /dev -name "lp*" 2>/dev/null
find /dev -name "usb*" 2>/dev/null

# 4. Yazıcı sıfırla
echo -ne "SIZE 100mm,150mm\r\n" | sudo tee /dev/lp0 > /dev/null
```

### Problem: İzin Hatası (Permission Denied)

```bash
# 1. Geçerli kullanıcıyı grup'a ekle
sudo usermod -a -G lp $USER
sudo usermod -a -G lpadmin $USER

# 2. Oturum kapat, yeniden aç
exit
ssh user@192.168.0.XX

# 3. Veya sudo ile çalıştır
sudo python3 app.py
```

### Problem: Yazıcı Bağlandı ama Yazdırmadı

```bash
# 1. Yazıcı durumunu kontrol et
python3 test_printer.py

# 2. Test etiketi gönder
echo -ne "SIZE 100mm,150mm\r\nTEXT 10 10 \"1\" 1 0\nTest\r\nPRINT 1 1\r\n" | \
  sudo tee /dev/usb/lp0 > /dev/null

# 3. Yazıcı loglarını kontrol et
dmesg | tail -10

# 4. TSPL komutlarını doğrula
# Yazıcı dokümantasyonuna bak
```

### Problem: App Yazıcı Algılamıyor

```bash
# 1. Platform kontrol
python3 -c "import platform; print(platform.system())"
# Çıkış: Linux

# 2. Import kontrol
python3 -c "from printer_integration import get_printer_manager; print('OK')"

# 3. Loglama
tail -f logs/app.log | grep PRINTER
```

## Başarı Kontrol Listesi

- [ ] Dosyalar Ubuntu'ya kopyalandı
- [ ] Yazıcı `/dev/usb/lp0` veya `/dev/lp0`'da bulundu
- [ ] İzinler ayarlandı (udev kuralı)
- [ ] `python3 test_printer.py` başarılı çalıştı
- [ ] `python3 app.py` başlatıldı ve "[PRINTER] ✓" mesajı görüldü
- [ ] `/api/printer/status` isteği başarılı yanıt verdi
- [ ] Test etiketi başarıyla yazdırıldı
- [ ] Hata logları temiz
- [ ] Windows kodu hiç değiştirilmedi

## Kalıcı Çalıştırma (Production)

### Systemd Service Oluştur

```bash
# Service dosyası oluştur
sudo nano /etc/systemd/system/envanter-app.service
```

İçeriği:
```ini
[Unit]
Description=Cermak Envanter QR System
After=network.target mysql.service

[Service]
Type=simple
User=appuser
WorkingDirectory=/home/appuser/EnvanterQR
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 /home/appuser/EnvanterQR/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Service'i etkinleştir ve başlat
sudo systemctl daemon-reload
sudo systemctl enable envanter-app.service
sudo systemctl start envanter-app.service

# Durum kontrol
sudo systemctl status envanter-app.service

# Logları izle
sudo journalctl -u envanter-app.service -f
```

## Yazıcı Bakım

```bash
# Yazıcı loglarını kontrol
tail -f logs/app.log | grep PRINTER

# İstatistik
grep "PRINTER" logs/app.log | wc -l

# Hata logları
grep -i "PRINTER.*error" logs/app.log
```

## Entegrasyon Noktaları

Frontend'de yazıcı buton'ları eklemek isterseniz:

1. **Part Details Sayfası**: "Etiket Yazdır" butonu
2. **Inventory Page**: Toplu yazdırma
3. **QR Scanner**: Scan sonrası hemen yazdır
4. **Admin Panel**: Yazıcı durumu ve test

Örnek HTML:
```html
<button onclick="printQRLabel()">📄 Etiket Yazdır</button>

<script>
async function printQRLabel() {
  const response = await fetch('/api/printer/print-qr', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    },
    body: JSON.stringify({
      qr_data: 'TEST_QR_123',
      label_text: 'Test Etiketi',
      quantity: 1
    })
  });
  const result = await response.json();
  alert(result.success ? result.message : result.error);
}
</script>
```
