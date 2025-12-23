@echo off
REM CERMAK ENVANTER - CLIENT SHORTCUT KURULUM
REM Tüm client PC'lerde çalıştırılacak

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo CERMAK ENVANTER - CLIENT KURULUM
echo ================================================================================
echo.

set NETWORK_PATH=\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter
set EXE_NAME=CermakEnvanter.exe
set SHORTCUT_NAME=Cermak Envanter QR
set DESKTOP=%USERPROFILE%\Desktop

echo [INFO] Network path kontrol ediliyor...
echo [INFO] Path: %NETWORK_PATH%
echo.

if not exist "%NETWORK_PATH%\%EXE_NAME%" (
    echo [ERROR] Exe bulunmadı: %NETWORK_PATH%\%EXE_NAME%
    echo.
    echo Çözüm: Network path'e %EXE_NAME% kopyalanmış mı?
    echo.
    pause
    exit /b 1
)
echo [OK] Exe bulundu!

echo.
echo [SETUP] Desktop shortcut oluşturuluyor...
echo [SHORTCUT] Adı: %SHORTCUT_NAME%
echo [SHORTCUT] Hedef: %NETWORK_PATH%\%EXE_NAME%
echo.

REM Create shortcut using PowerShell
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%.lnk');$s.TargetPath='%NETWORK_PATH%\%EXE_NAME%';$s.WorkingDirectory='%NETWORK_PATH%';$s.IconLocation='%NETWORK_PATH%\%EXE_NAME%';$s.Save()"

if exist "%DESKTOP%\%SHORTCUT_NAME%.lnk" (
    echo [SUCCESS] Shortcut oluşturuldu!
) else (
    echo [ERROR] Shortcut oluşturulamadı
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo [SUCCESS] KURULUM TAMAMLANDI!
echo ================================================================================
echo.
echo Shortcut konumu: %DESKTOP%\%SHORTCUT_NAME%.lnk
echo.
echo HEMEN BAŞLA:
echo   1. Desktop'ta "%SHORTCUT_NAME%" shortcut'ına çift tıkla
echo   2. Electron GUI açılır
echo   3. Giriş formuna kullanıcı adı ve şifre gir
echo   4. Sistem açılır, sayım başla!
echo.
echo NOT:
echo   - Network erişimi gerekli (\\DCSRV\...)
echo   - Sunucu'da Flask çalışıyor olmalı
echo   - İlk açılış 10-15 saniye sürebilir
echo.
pause
