@echo off
REM CERMAK ENVANTER - SERVER WINDOWS SERVICE KURULUM
REM Bu script sunucu'da ADMIN olarak çalıştırılmalı

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo CERMAK ENVANTER - FLASK SERVER KURULUM
echo ================================================================================
echo.

REM Check if running as admin
for /f "tokens=1" %%A in ('whoami /priv ^| find "SeDebugPrivilege"') do set admin=%%A
if not "%admin%"=="SeDebugPrivilege" (
    echo [ERROR] Bu script ADMIN olarak çalıştırılmalı!
    echo.
    pause
    exit /b 1
)

echo [OK] Admin privileges kontrol edild.
echo.

REM Define paths
set PYTHON_PATH=C:\Python311\python.exe
set CERMAK_PATH=C:\CermakEnvanter
set APP_PY=%CERMAK_PATH%\app.py
set VENV_PATH=%CERMAK_PATH%\venv

echo [INFO] Kontrol ediliyor...
echo [INFO] Python: %PYTHON_PATH%
echo [INFO] App: %APP_PY%
echo.

REM Check Python installation
if not exist "%PYTHON_PATH%" (
    echo [ERROR] Python bulunmadı: %PYTHON_PATH%
    echo.
    echo Çözüm: Python 3.11+ yükle
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python bulundu: %PYTHON_PATH%

REM Check app.py
if not exist "%APP_PY%" (
    echo [ERROR] app.py bulunmadı: %APP_PY%
    echo.
    echo Çözüm: CermakEnvanter dosyalarını C:\CermakEnvanter\ kopyala
    echo.
    pause
    exit /b 1
)
echo [OK] app.py bulundu

REM Create venv if not exists
if not exist "%VENV_PATH%" (
    echo.
    echo [SETUP] Virtual environment oluşturuluyor...
    "%PYTHON_PATH%" -m venv "%VENV_PATH%"
    if !errorlevel! neq 0 (
        echo [ERROR] venv oluşturulamadı
        pause
        exit /b 1
    )
    echo [OK] Virtual environment oluşturuldu
)

REM Install requirements
echo.
echo [SETUP] Python paketleri yükleniyor...
"%VENV_PATH%\Scripts\pip.exe" install -r "%CERMAK_PATH%\requirements.txt" --upgrade
if !errorlevel! neq 0 (
    echo [ERROR] Paketler yüklenemedi
    pause
    exit /b 1
)
echo [OK] Paketler yüklendi

REM Create run_flask_service.bat
echo.
echo [SETUP] Flask service batch script oluşturuluyor...
(
    echo @echo off
    echo cd /d C:\CermakEnvanter
    echo C:\CermakEnvanter\venv\Scripts\python.exe app.py
) > "%CERMAK_PATH%\run_flask_service.bat"
echo [OK] run_flask_service.bat oluşturuldu

REM Test Flask startup
echo.
echo [TEST] Flask başlatılıyor... (5 saniye)
start /b /wait "%CERMAK_PATH%\run_flask_service.bat"
timeout /t 5 /nobreak

REM Create Windows Task
echo.
echo [SETUP] Windows Task Scheduler'da görev oluşturuluyor...
schtasks /create ^
    /tn "CermakEnvanterFlask" ^
    /tr "C:\CermakEnvanter\run_flask_service.bat" ^
    /sc onstart ^
    /ru SYSTEM ^
    /f
if !errorlevel! equ 0 (
    echo [OK] Task oluşturuldu
) else (
    echo [WARNING] Task zaten var mı? Devam ediyorum...
)

REM Add Firewall rule
echo.
echo [SETUP] Firewall kuralı ekleniyor...
netsh advfirewall firewall add rule ^
    name="Flask Cermak Envanter" ^
    dir=in ^
    action=allow ^
    protocol=tcp ^
    localport=5002 ^
    profile=any ^
    enable=yes
if !errorlevel! equ 0 (
    echo [OK] Firewall kuralı eklendi
) else (
    echo [INFO] Firewall kuralı zaten var mı?
)

echo.
echo ================================================================================
echo [SUCCESS] KURULUM TAMAMLANDI!
echo ================================================================================
echo.
echo FLASK SERVISI DURUM:
echo   - Otomatik start: Evet (Windows Task)
echo   - Port: 5002
echo   - Adres: http://0.0.0.0:5002
echo.
echo SONRAKI ADIMLAR:
echo   1. Sunucuyu yeniden başlat (veya Task'ı manuel start et)
echo   2. Tüm client PC'lerde CermakEnvanter.exe çalıştır
echo   3. Giriş yap ve kullanmaya başla!
echo.
echo KONTROL:
echo   - http://192.168.0.57:5002/health (browser'da test et)
echo   - Komut satırı: curl http://192.168.0.57:5002/health
echo.
pause
