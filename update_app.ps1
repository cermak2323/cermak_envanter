# Cermak Envanter Güncelleme Scripti
# Bu script mevcut verileri koruyarak uygulamayı günceller

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CERMAK ENVANTER GÜNCELLEME" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kaynak ve hedef dizinler
$source = "c:\Users\rsade\Desktop\Yeni klasör\EnvanterQR\EnvanterQR\frontend\electron\dist\win-unpacked"
$dest = "\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter"

# Çalışan processleri kapat
Write-Host "[1] Çalışan processleri kapatılıyor..." -ForegroundColor Yellow
taskkill /F /IM "Cermak-Envanter.exe" /T 2>$null
taskkill /F /IM "CermakEnvanter.exe" /T 2>$null
Start-Sleep -Seconds 3
Write-Host "    OK - Processler kapatıldı" -ForegroundColor Green

# Korunacak klasörler - BU KLASÖRLER ASLA SİLİNMEZ
$protectedFolders = @(
    "static\qr_codes",
    "static\temp",
    "static\excel",
    "static\reports",
    "static\part_photos",
    "static\exports",
    "static\backups"
)

Write-Host ""
Write-Host "[2] Korunan klasörler kontrol ediliyor..." -ForegroundColor Yellow
foreach ($folder in $protectedFolders) {
    $fullPath = Join-Path $dest $folder
    if (Test-Path $fullPath) {
        $itemCount = (Get-ChildItem $fullPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "    KORUNUYOR: $folder ($itemCount dosya)" -ForegroundColor Green
    } else {
        Write-Host "    OLUŞTURULUYOR: $folder" -ForegroundColor Cyan
        New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
    }
}

# Ana dosyaları güncelle (klasörleri silmeden)
Write-Host ""
Write-Host "[3] Uygulama dosyaları güncelleniyor..." -ForegroundColor Yellow

# Ana exe ve dll'leri kopyala
$mainFiles = @(
    "Cermak-Envanter.exe",
    "*.dll",
    "*.pak",
    "*.dat",
    "*.bin",
    "*.json",
    "*.txt",
    "*.html"
)

foreach ($pattern in $mainFiles) {
    $files = Get-ChildItem -Path $source -Filter $pattern -File -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        Copy-Item -Path $file.FullName -Destination $dest -Force
        Write-Host "    Güncellendi: $($file.Name)" -ForegroundColor Gray
    }
}

# Locales klasörünü güncelle
Write-Host ""
Write-Host "[4] Locales güncelleniyor..." -ForegroundColor Yellow
$localesSource = Join-Path $source "locales"
$localesDest = Join-Path $dest "locales"
if (Test-Path $localesSource) {
    if (!(Test-Path $localesDest)) {
        New-Item -Path $localesDest -ItemType Directory -Force | Out-Null
    }
    Copy-Item -Path "$localesSource\*" -Destination $localesDest -Force
    Write-Host "    OK - Locales güncellendi" -ForegroundColor Green
}

# Resources klasörünü güncelle (backend dahil)
Write-Host ""
Write-Host "[5] Resources güncelleniyor..." -ForegroundColor Yellow
$resourcesSource = Join-Path $source "resources"
$resourcesDest = Join-Path $dest "resources"
if (Test-Path $resourcesSource) {
    if (!(Test-Path $resourcesDest)) {
        New-Item -Path $resourcesDest -ItemType Directory -Force | Out-Null
    }
    # Backend klasörünü tamamen güncelle
    $backendSource = Join-Path $resourcesSource "backend"
    $backendDest = Join-Path $resourcesDest "backend"
    if (Test-Path $backendSource) {
        if (!(Test-Path $backendDest)) {
            New-Item -Path $backendDest -ItemType Directory -Force | Out-Null
        }
        Copy-Item -Path "$backendSource\*" -Destination $backendDest -Force -Recurse
        Write-Host "    OK - Backend güncellendi" -ForegroundColor Green
    }
    # Diğer resources dosyaları
    Get-ChildItem -Path $resourcesSource -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $resourcesDest -Force
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  GÜNCELLEME TAMAMLANDI!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Korunan veriler:" -ForegroundColor Cyan
foreach ($folder in $protectedFolders) {
    $fullPath = Join-Path $dest $folder
    if (Test-Path $fullPath) {
        $itemCount = (Get-ChildItem $fullPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "  OK $folder - $itemCount dosya" -ForegroundColor Green
    }
}
Write-Host ""
Write-Host "Program baslatilabilir:" -ForegroundColor Yellow
Write-Host "$dest\Cermak-Envanter.exe" -ForegroundColor White
Write-Host ""
