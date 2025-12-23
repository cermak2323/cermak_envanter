# CERMAK ENVANTER - DEPLOYMENT REHBERI

## 🚀 HIZLI BAŞLAMA

### **SUNUCU KURULUM (Bir kere)**

1. **Dosyaları sunucuya kopyala:**
   ```
   C:\CermakEnvanter\
   ├── app.py
   ├── models.py
   ├── templates\
   ├── static\
   ├── instance\
   ├── requirements.txt
   └── SETUP_FLASK_SERVICE.bat (bu dosya)
   ```

2. **Kurulum script'ini çalıştır (ADMIN):**
   ```
   SETUP_FLASK_SERVICE.bat
   ```
   
   Bu ne yapar?
   - ✓ Python venv oluşturur
   - ✓ Gerekli paketleri yükler
   - ✓ Flask'ı Windows Service yapıştırır
   - ✓ Firewall kuralını açar (port 5002)
   - ✓ Sunucuyu yeniden başlatma önerir

3. **Sunucuyu yeniden başlat**
   - Flask otomatik başlayacak (port 5002)

4. **Test et:**
   ```
   http://192.168.0.57:5002/health
   ```
   - 200 OK dönerse başarılı!

---

### **CLIENT KURULUM (Her PC'de)**

1. **Network'ten exe indir:**
   ```
   \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\CermakEnvanter.exe
   ```

2. **Kurulum script'ini çalıştır:**
   ```
   SETUP_CLIENT.bat
   ```
   
   Bu ne yapar?
   - ✓ Desktop shortcut oluşturur
   - ✓ Network path'i kontrol eder
   - ✓ İlk açılış hazırlanır

3. **Desktop shortcut'ına tıkla:**
   - Electron GUI açılır
   - Flask server'a bağlanır
   - Giriş formu gösterilir

---

## 📋 KURULUM DETAYLARI

### Sunucu Mimarisi

```
SUNUCU (Windows Server / PC)
├── Flask App (port 5002)
│   ├── Database: MySQL 192.168.0.57:3306
│   ├── Templates: render
│   └── API: /api/*, /health, /login, etc.
└── Windows Service: CermakEnvanterFlask
    └── Auto-start at boot

CLIENT PC (Any Windows PC)
├── CermakEnvanter.exe
│   ├── Electron GUI
│   └── → Connects to http://192.168.0.57:5002
└── Desktop Shortcut
    └── → \\DCSRV\...\CermakEnvanter.exe

NETWORK SHARE (\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter)
├── CermakEnvanter.exe (client download)
├── static/
│   ├── portal_video.mp4
│   ├── qr_codes/ (all QR files)
│   ├── css/
│   ├── js/
│   └── ...
└── SETUP_CLIENT.bat
```

### Network Akışı

```
User Desktop:
  1. Tıkla: "Cermak Envanter QR" shortcut
  2. Exe başlar: CermakEnvanter.exe
  3. Electron GUI opens
  4. Server'a bağlan: http://192.168.0.57:5002
  5. Login page göster
  6. Giriş yap
  7. System ready!
  
  ↓↓↓
  
Server (192.168.0.57):
  - Flask running on port 5002
  - Handles: API, login, QR scan, reports
  - Database: MySQL 192.168.0.57:3306
  - Static files: \\DCSRV\...\static
```

---

## ⚙️ KONFIGÜRASYON

### Server IP Değiştir (isteğe bağlı)

Eğer Flask server IP farklıysa:

**Dosya:** `electron/main.js` (satır 8-9)
```javascript
const FLASK_URL = `http://192.168.0.57:${FLASK_PORT}`; // Bu satırı değiştir
```

Örneğin sunucu IP 10.0.0.50 ise:
```javascript
const FLASK_URL = `http://10.0.0.50:${FLASK_PORT}`;
```

Sonra Electron'u rebuild et:
```
cd electron
npm run build
```

### Database

App.py otomatik kontrol eder:
- MySQL 192.168.0.57:3306
- Database: flaskdb
- Credentials: app.py satır ~150'de

### Static Folder

Network path: `\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static`
- Tüm QR kodları burada
- CSS/JS/resimler burada
- Excel reports burada

---

## ✓ KONTROL LİSTESİ

### Sunucu Hazırlandı mı?

- [ ] Python 3.11+ yüklü
- [ ] `SETUP_FLASK_SERVICE.bat` çalıştırıldı
- [ ] Flask çalışıyor (port 5002)
- [ ] `http://192.168.0.57:5002/health` → 200 OK
- [ ] Firewall port 5002 açık
- [ ] MySQL bağlantısı çalışıyor
- [ ] Network path erişilebilir

### Client Hazırlandı mı?

- [ ] `CermakEnvanter.exe` indirildi
- [ ] `SETUP_CLIENT.bat` çalıştırıldı
- [ ] Desktop shortcut var
- [ ] Network erişimi var (test: ping DCSRV)
- [ ] Exe çalıştırıldı test edildi

### İlk Çalıştırma

- [ ] Server çalışıyor
- [ ] Client shortcut'ını tıkla
- [ ] Electron GUI açılır
- [ ] Login formu gösterilir
- [ ] Giriş yap (admin/@R9t$L7e!xP2w)
- [ ] Sistem açılır

---

## 🐛 SORUN GIDERME

### "Exe çalıştırılamadı"
```
Çözüm: Network erişimi kontrol et
  ping \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter
```

### "Flask server'a bağlanamıyor"
```
Çözüm 1: Firewall
  netsh advfirewall firewall show rule name="Flask Cermak Envanter"

Çözüm 2: Flask çalışıyor mu?
  http://192.168.0.57:5002/health (browser test)

Çözüm 3: Network
  ping 192.168.0.57
  tracert 192.168.0.57
```

### "Database hatası"
```
Çözüm: MySQL bağlantısı
  Sunucu'da app.py'ı çalıştırıp log'a bak
  Error message'da hangi satır hata yapmış?
```

### "Giriş yapamıyor"
```
Çözüm: Credentials
  admin / @R9t$L7e!xP2w
  
  Değiştirilmişse:
  Sunucu'da database kontrol et:
    SELECT * FROM envanter_users LIMIT 1;
```

---

## 📞 DESTEK

Sorunlar için:
1. `app.py` output'unu kontrol et (sunucu console)
2. Browser console'u aç (F12)
3. Network tab'ında request/response kontrol et
4. Firewall/antivirus kurallarını kontrol et

---

## ÖZET

| Bileşen | Nerede | Durum |
|---------|-------|-------|
| Flask Server | C:\CermakEnvanter\ (sunucu) | Windows Service (auto-start) |
| Client GUI | CermakEnvanter.exe | Portable, network'ten indir |
| Static Files | \\DCSRV\...\static | Network share |
| Database | 192.168.0.57:3306 | MySQL |
| Port | 5002 | Firewall açık |

**Kurulum sonrası:**
- User shortcut'ına tıklar
- Exe başlar → Flask bağlanır → Giriş yapıp kullanır
- Basit, hızlı, merkezi!

