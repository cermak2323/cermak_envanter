@echo off
REM CermakEnvanter - No Console Launcher
REM PowerShell üzerinden gizli console ile Flask başlatır

powershell -NoProfile -WindowStyle Hidden -Command "Start-Process '\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\CermakEnvanter.exe' -WindowStyle Hidden"

REM Kapat (Flask arka planda çalışmaya devam edecek)
exit /b 0
