# CERMAK ENVANTER - SERVER KURULUM

## Sunucu Kurulum (Windows Service olarak)

### 1. Server'da Python Yüklü Olmalı
```
Python 3.11+ kurulu olmalı
PIP ile gerekli paketler yüklü
```

### 2. Server'da Flask'ı Windows Service Yap

#### Yöntem 1: NSSM (Non-Sucking Service Manager) ile

1. NSSM indir: https://nssm.cc/download
2. Sunucuya kopyala
3. PowerShell (Admin) açıp:

```powershell
# NSSM path
cd C:\path\to\nssm\win64

# Service oluştur
.\nssm.exe install CermakEnvanterFlask "C:\Python311\python.exe" "C:\CermakEnvanter\app.py"

# Service başlat
.\nssm.exe start CermakEnvanterFlask
```

#### Yöntem 2: Python venv + batch script

1. Server'da folder oluştur:
```
C:\CermakEnvanter\
  ├── app.py
  ├── templates\
  ├── static\
  ├── instance\
  ├── venv\
  └── run_flask_service.bat
```

2. `run_flask_service.bat` oluştur:
```batch
@echo off
cd /d C:\CermakEnvanter
C:\CermakEnvanter\venv\Scripts\python.exe app.py
```

3. Windows Task Scheduler'da scheduled task oluştur:
   - Program: `C:\CermakEnvanter\run_flask_service.bat`
   - Run with highest privileges
   - Run at startup

### 3. Flask Konfigürasyonu

Server'da `app.py` başladığında:
```
Flask runs on 0.0.0.0:5002
Database: MySQL 192.168.0.57:3306
Static: \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static
QR codes: \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static\qr_codes
```

### 4. Client PC'de Kurulum

1. Network'ten `CermakEnvanter.exe` indir
2. Desktop'a shortcut oluştur:
   - Target: `\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\CermakEnvanter.exe`
   - Start in: `\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter`

3. Exe'ye tıkla:
   - Electron GUI açılır
   - Flask server'a bağlanır (192.168.0.57:5002)
   - Giriş formu gösterilir
   - Kullanıma hazır!

### 5. Firewall Kuralları

Server'da port 5002 açık olmalı:
```powershell
# Admin PowerShell'de
New-NetFirewallRule -DisplayName "Flask Cermak Envanter" `
  -Direction Inbound `
  -LocalPort 5002 `
  -Protocol TCP `
  -Action Allow
```

### 6. İlk Kez Başlat Kontrol Listesi

✓ Flask server'da çalışıyor (port 5002)
✓ Database MySQL'e bağlı
✓ Static folder network'te erişilebilir
✓ QR codes cache yüklendi
✓ Firewall 5002 portunu açık
✓ Client PC'de CermakEnvanter.exe
✓ Shortcut desktop'ta
✓ Exe çalıştır → Electron açılır

### 7. Sorun Giderme

**"Flask server'a bağlanamıyor"**
- Server'da Flask çalışıyor mu? `http://192.168.0.57:5002/health` test et
- Firewall kuralı varsa kontrol et
- Network bağlantısı kontrol et

**"Database hatası"**
- MySQL 192.168.0.57:3306 çalışıyor mu?
- Credentials doğru mu?

**"Static folder'a erişemiyor"**
- Network path \\DCSRV accessible mi?
- Permissyonlar doğru mu?

---

## Deployment Özetle

**Server:** C:\CermakEnvanter\ → Flask Windows Service
**Network:** \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\ → Static, QR, Excel
**Client:** CermakEnvanter.exe + Desktop shortcut → GUI only
**Connection:** Client → Server Flask (192.168.0.57:5002) → MySQL

