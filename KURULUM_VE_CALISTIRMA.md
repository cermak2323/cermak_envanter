# ENVANTERQR KURULUM VE ÇALIŞTIRMA REHBERİ

> Bu sürüm son kullanıcıya **tek bir `setup.exe`** dosyası ile dağıtılır. Kullanıcının Python, Node.js veya ek bağımlılık kurmasına gerek yoktur.

## 1. Sistem Gereksinimleri
- Windows 10/11 (64-bit)
- İnternet erişimi (ilk açılışta B2 senkronizasyonu ve güncelleme için)
- Kurulum için yaklaşık 1.5 GB boş disk alanı
- Backblaze B2 / PostgreSQL erişim bilgileri kurulumdan önce hazırlanmalı (yetkili kişi tarafından sağlanır)

## 2. Hızlı Kurulum (Önerilen)
1. `setup.exe` dosyasını çalıştırın.
2. NSIS sihirbazındaki adımları takip ederek kurulumu tamamlayın. Masaüstü kısayolu otomatik olarak oluşturulur.
3. Kurulum bittiğinde uygulama otomatik başlatılır.

Kurulum paketinin içinde:
- PyInstaller ile derlenmiş `envanter_orchestrator.exe` (Flask backend + APScheduler)
- Electron arayüzü, preload ve statik dosyalar
- Gerekli Python paketleri, B2 SDK, SQLAlchemy ve tüm bağımlılıklar

## 3. İlk Açılışta Çalışan Otomatik Akış
1. **B2 Senkronizasyonu:** Uygulama başlar başlamaz Backblaze B2 ile iki yönlü senkron yapılır. Splash ekranındaki ilerleme çubuğu canlı veriyi `/api/sync/status` üzerinden gösterir.
2. **Güncelleme Kontrolü:** `.env` içinde tanımlanan `UPDATE_METADATA_URL` adresindeki `metadata.json` okunur. Yeni sürüm varsa kullanıcıya popup gösterilir (veya `AUTO_UPDATE=true` ise sessiz güncelleme).
3. **Backend Başlatma:** Flask sunucusu (`envanter_orchestrator.exe`) ayağa kalkar ve `/api/health` endpointi hazır hale gelir.
4. **Electron Arayüzü:** Login ekranı tam ekran açılır; başarılı giriş sonrası ana panel yüklenir.

> Bu sıralama kullanıcı müdahalesi olmadan gerçekleşir. B2 senkronu bitmeden arayüz açılmaz.

## 4. Kullanım Akışı (Günlük Operasyon)
- Login ekranında ADMİN hesabınızla giriş yapın.
- Ana paneldeki **“Manuel Senkron”** butonu ile dilediğiniz an B2 sync tetikleyebilirsiniz.
- APScheduler her 30 dakikada otomatik senkron çalıştırır.
- Güncelleme bulunduğunda popup gelir; onayladığınızda installer indirilir, mevcut oturum kapanır ve kurulum başlar.

## 5. Sık Sorulanlar
- **Senkronizasyon dosya silmez:** Eksik olan dosyaları tamamlar; hiçbir dosya otomatik silinmez.
- **metadata.json erişilebilir olmalı:** `UPDATE_METADATA_URL` halka açık veya VPN üzerinden ulaşılabilir bir konuma işaret etmelidir.
- **Kısayol / Başlangıç:** NSIS kurulumunda “Start Menu” ve “Desktop” kısayolları varsayılan olarak eklenir.

## 6. Splash, İkon ve Özelleştirme
- Splash ekranı ve ana pencere `cermaktakeuchi_logo.ico` kullanır.
- `frontend/electron/main.js` otomatik olarak backend çalışıp `/api/health` OK dönene kadar bekler.
- İsteğe göre `AUTO_UPDATE=true` yapıldığında popup beklenmeden installer indirilip çalıştırılır.

## 7. Geliştirici Modu (Opsiyonel)
Ürünü paketlemek veya geliştirmek isteyen ekip üyeleri için adımlar aşağıdadır. Son kullanıcıların bu işlemleri yapmasına gerek yoktur.

### a) Python ortamı
```powershell
pip install -r requirements.txt
```

### b) Electron bağımlılıkları
```powershell
cd frontend/electron
npm install
cd ../../
```

### c) .env dosyası
```powershell
copy .env.example .env
```
Alanlar:
- `B2_KEY_ID`, `B2_APP_KEY`, `B2_BUCKET_NAME`
- `DATABASE_URL`
- `UPDATE_METADATA_URL`
- `AUTO_UPDATE` (true/false)

### d) Backend sürüm dosyası
`app_version.txt` içindeki sürüm numarası NSIS paketindeki sürümle eşleşmelidir.

### e) Çalıştırma
```powershell
python backend\startup_orchestrator.py --skip-electron
```
Geliştirme sırasında Electron’u ayrı olarak `npm start` ile çalıştırabilirsiniz.

---
Daha fazla bilgi için `README.md`, `EXE_BUILD_INSTRUCTIONS.md` ve kod içi açıklamalara göz atın.
