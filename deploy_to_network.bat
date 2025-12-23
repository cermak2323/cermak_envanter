@echo off
REM CermakEnvanter - Ağ Üzerinden Konuşlandırma
REM Bu script exe'yi network klasörüne kopyalar ve kısayol oluşturur

setlocal enabledelayedexpansion

set "SOURCE_EXE=%CD%\dist\CermakEnvanter.exe"
set "NETWORK_PATH=\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter"
set "DEPLOY_EXE=%NETWORK_PATH%\CermakEnvanter.exe"

echo ════════════════════════════════════════════════════════════
echo    CERMAK ENVANTER - NETWORK DEPLOYMENT
echo ════════════════════════════════════════════════════════════
echo.

REM [1] Exe kontrol
if not exist "%SOURCE_EXE%" (
    echo [!] ERROR: exe bulunamadi: %SOURCE_EXE%
    echo      Lutfen once build_shared_deployment.py calistirin
    pause
    exit /b 1
)

echo [*] Source EXE: %SOURCE_EXE%
echo [*] Deploy Target: %DEPLOY_EXE%
echo.

REM [2] Network erişim
echo [*] Network erisimi kontrol ediliyor...
if not exist "%NETWORK_PATH%" (
    echo [!] ERROR: Network klasoru erisime acik degil
    echo      %NETWORK_PATH%
    pause
    exit /b 1
)
echo [+] Network klasoru OK

REM [3] Kopyala
echo [*] EXE network'e kopylanıyor...
copy /Y "%SOURCE_EXE%" "%DEPLOY_EXE%" >nul 2>&1
if errorlevel 1 (
    echo [!] Kopyalama hatalı
    pause
    exit /b 1
)
echo [+] EXE kopyalandi: %DEPLOY_EXE%
echo.

echo ════════════════════════════════════════════════════════════
echo    BASARILI - Deployment Tamamlandi
echo ════════════════════════════════════════════════════════════
echo.
echo EXE Konumu: %DEPLOY_EXE%
echo.
echo SONRAKI ADIM:
echo   1. Masaüstüne kısayol oluştur (CREATE_SHORTCUT.bat)
echo   2. Diğer PC'lerde aynı kısayolu oluştur
echo.
pause
