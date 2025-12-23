# Ubuntu Server Yazıcı Kurulum Rehberi

## Yazıcı Bağlantısı

### 1. USB Yazıcı Cihazını Kontrol Edin

```bash
# USB cihazlarını listele
lsusb

# Detaylı bilgi
lsusb -v | grep -A 10 "Thermal"

# /dev cihazlarını kontrol et
ls -la /dev/usb/
ls -la /dev/lp*
```

### 2. Yazıcı Cihazını Bulun

TSPL yazıcısı genellikle `/dev/usb/lp0` adresinde olur. Kontrol edin:

```bash
# Yazıcı cihazını bulma
find /dev -name "lp*" 2>/dev/null
```

### 3. İzin Ayarları

**Seçenek A: sudo ile çalıştırma**
```bash
sudo python3 app.py
```

**Seçenek B: udev kuralı oluştur (kalıcı çözüm)**

```bash
# udev kural dosyası oluştur
sudo nano /etc/udev/rules.d/99-tspl-printer.rules
```

Aşağıdaki satırı ekle:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="XXXX", ATTRS{idProduct}=="YYYY", MODE="0666"
SUBSYSTEM=="usb_device", ATTRS{idVendor}=="XXXX", ATTRS{idProduct}=="YYYY", MODE="0666"
```

Cihaz ID'sini bul:
```bash
lsusb | grep -i "thermal\|printer"
# Çıkış örneği: Bus 001 Device 005: ID 0471:0019 Philips Electronics
# Burada 0471 = idVendor, 0019 = idProduct
```

Kuralı uygula:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 4. İzni Kontrol Et

```bash
# Yazma izni var mı kontrol et
ls -la /dev/usb/lp0
# Çıkış: crw-rw-rw- ... /dev/usb/lp0 (altı 666 olmalı)
```

## Python Kütüphaneleri

```bash
# Gerekli paketleri kur (varsa)
pip3 install -r requirements.txt
```

## Yazıcı Modülünü Kullanma

### tspl_printer.py
Düşük seviye TSPL komutları gönderir. Doğrudan USB'ye bağlı TSPL yazıcısını kontrol eder.

**Özellikler:**
- USB üzerinden RAW komut gönderme
- QR kod yazdırma
- Barkod yazdırma
- Metin yazdırma
- Çizgi ve şekil çizimi
- Etiket boyutu ve boşluk ayarı
- Koyuluk ve hız ayarı

**Örnek Kullanım:**
```python
from tspl_printer import TSPLPrinter

printer = TSPLPrinter(device_path="/dev/usb/lp0")

if printer.connected:
    printer.initialize()
    printer.set_darkness(10)
    
    # QR kodu yazdır
    printer.print_qrcode(
        qr_data="ENVANTER_123456",
        x=10, y=10,
        size=8,
        eccl="H"  # Yüksek hata düzeltme
    )
    
    # Etiket yazdır
    printer.print_label(label_count=1)
```

### printer_integration.py
Yüksek seviye yazdırma işlemleri ve yönetim.

**PrinterManager Singleton Kullanımı:**
```python
from printer_integration import get_printer_manager

manager = get_printer_manager()

# QR etiketi yazdır
manager.print_qr_label(
    qr_data="ENVANTER_123456",
    label_text="Ürün Adı",
    quantity=1
)

# Barkod etiketi yazdır
manager.print_barcode_label(
    barcode_data="1234567890",
    label_text="Stok Kodu",
    quantity=5
)

# Kombinasyon etiketi
manager.print_combined_label(
    qr_data="ENVANTER_123456",
    barcode_data="1234567890",
    title="Ürün Etiketi",
    quantity=1
)

# Durum kontrol
status = manager.get_status()
print(f"Yazıcı: {status['status']}")
```

## App.py Entegrasyonu

Flask/Django uygulamanıza ekleyin:

```python
from printer_integration import get_printer_manager

# Rota örneği (Flask)
@app.route('/print-qr/<qr_code>')
def print_qr(qr_code):
    manager = get_printer_manager()
    success = manager.print_qr_label(
        qr_data=qr_code,
        label_text="Envanter",
        quantity=1
    )
    return {'status': 'ok' if success else 'error'}
```

## Sorun Çözme

### Yazıcı Bulunamadı
```bash
# 1. Cihazı kontrol et
ls -la /dev/usb/

# 2. USB bağlantısını kontrol et
lsusb

# 3. Sistem çekirdeği mesajlarını kontrol et
dmesg | tail -20
```

### İzin Hatası
```bash
# Sudo ile çalıştır
sudo python3 app.py

# VEYA udev kuralını ayarla (yukarıdaki 3. adım)
```

### Yazıcı Başlamıyor
```bash
# Yazıcının reset yapması gerekebilir
echo -ne "SIZE 100mm,150mm\r\n" > /dev/usb/lp0
```

### Test Et
```bash
python3 -c "from printer_integration import get_printer_manager; \
m = get_printer_manager(); \
print(m.get_status()); \
m.test_print()"
```

## Önemli Notlar

⚠️ **Windows Kodu:**
- Windows tarafında değişiklik yok
- Sadece Linux/Ubuntu dosyaları eklendi

✓ **USB Bağlantısı:**
- Yazıcı USB ile bağlı
- CUPS, ağ yazıcı, sürücü YOK
- RAW TSPL komutları doğrudan /dev/usb/lp0'a gönderiliyor

✓ **İzinler:**
- Sudo veya udev kuralları ile çalışır
- Üretime udev kuralı önerilir

## Kontrol Listesi Dağıtım Öncesi

- [ ] `/dev/usb/lp0` var mı kontrol et
- [ ] İzin ayarlarını yapılandır
- [ ] Test yazdırma yap
- [ ] app.py'de printer_integration import et
- [ ] Hata kaydı ayarını kontrol et
- [ ] TSPL yazıcı dokümantasyonunu oku (parametreler)
