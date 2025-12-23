# EnvanterQR – Setup.exe Derleme Rehberi

Bu doküman geliştirici ekibin **tek bir Windows `setup.exe`** paketi üretmesi için gerekli adımları anlatır. Son kullanıcıların bu işlemleri yapması gerekmez.

## 1. Ön Koşullar
- Windows 10/11 x64
- Python 3.10+ ve `pip`
- Node.js 18+
- `npm` / `npx`
- NSIS (electron-builder, NSIS target için `makensis` komutunu otomatik çağırır)
- Geçerli `.env` dosyası ve güncel `app_version.txt`

> Bu bağımlılıklar yalnızca geliştirici makinesinde bulunur. Kurulan setup.exe son kullanıcıdan hiçbir ek kurulum istemez.

## 2. PyInstaller ile Backend Derleme
`backend/build_backend.ps1` betiği PyInstaller ayarlarını içerir ve `envanter_orchestrator.exe` üretir.

```powershell
powershell -ExecutionPolicy Bypass -File backend\build_backend.ps1
```

Çıktı: `dist\envanter_orchestrator\envanter_orchestrator.exe`

Bu dosyayı Electron projesine kopyalayın:

```powershell
copy dist\envanter_orchestrator\envanter_orchestrator.exe frontend\electron\resources\envanter_orchestrator.exe
```

## 3. Electron Bağımlılıkları (İlk Kurulum)
```powershell
cd frontend\electron
npm install
```

## 4. NSIS Setup Oluşturma (electron-builder)
ENV değerlerini doğrulayın (`UPDATE_METADATA_URL`, `AUTO_UPDATE` vb.) ve ardından:

```powershell
cd frontend\electron
npm run dist
```

- electron-builder `envanter_orchestrator.exe` dosyasını `extraResources` içinde paketler.
- NSIS hedefi tek bir `EnvanterQR Setup.exe` üretir (`frontend/electron/dist` klasörü).
- İmzalama gerekiyorsa `electron-builder.yml` ya da `package.json` içindeki `build` bölümüne sertifika bilgisi ekleyin.

## 5. Test Adımları
1. Üretilen `EnvanterQR Setup.exe` dosyasını temiz bir Windows VM üzerinde çalıştırın.
2. Kurulum sonunda uygulama otomatik açılır; splash ekranında B2 senkron ilerlemesini takip edin.
3. Login ekranı açılıyorsa kurulum başarılıdır.

## 6. metadata.json Güncelleme
Güncelleme kontrolü şu şemayı bekler:

```json
{
  "version": "1.4.0",
  "changelog": "Yeni splash ekranı ve sessiz güncelleme",
  "installer_download_url": "https://cdn.example.com/envanterqr/EnvanterQR%20Setup.exe"
}
```

Yeni paket yayınlarken:
- `app_version.txt` değerini artırın.
- metadata.json içindeki `version` ve `installer_download_url` alanlarını güncelleyin.
- Dosyayı `UPDATE_METADATA_URL` ile erişilebilir hale getirin.

## 7. Hızlı Komut Özeti
```powershell
# Backend exe
powershell -ExecutionPolicy Bypass -File backend\build_backend.ps1

# Electron NSIS installer
cd frontend\electron
npm run dist
```

Bu adımlar tamamlandığında son kullanıcıya yalnızca `EnvanterQR Setup.exe` dosyası verilir ve kullanıcı hiçbir ek bağımlılık yüklemez.
