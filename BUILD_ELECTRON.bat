@echo off
REM Cermak Envanter - Quick Build and Run Script

setlocal enabledelayedexpansion

set "COLOR_GREEN=[92m"
set "COLOR_YELLOW=[93m"
set "COLOR_RED=[91m"
set "COLOR_RESET=[0m"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   CERMAK ENVANTER - Electron + Flask Build                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_RED%✗ Python not found!%COLOR_RESET%
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
echo %COLOR_GREEN%✓ Python found%COLOR_RESET%

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_YELLOW%⚠ Node.js not found%COLOR_RESET%
    echo Install from https://nodejs.org and add to PATH
    echo Trying to install anyway...
)
echo %COLOR_GREEN%✓ Node.js found%COLOR_RESET%

echo.
echo Checking PyInstaller...
python -m pip show PyInstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install PyInstaller
)
echo %COLOR_GREEN%✓ PyInstaller ready%COLOR_RESET%

echo.
echo ════════════════════════════════════════════════════════════════
echo Select build option:
echo ════════════════════════════════════════════════════════════════
echo 1) Run locally (development)
echo 2) Build executable (network deployment)
echo 3) Run locally with Electron (test GUI)
echo 4) Exit
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting development mode...
    python electron_launcher.py
) else if "%choice%"=="2" (
    echo.
    echo Building executable...
    python build_electron_app.py
    if errorlevel 1 (
        echo %COLOR_RED%Build failed!%COLOR_RESET%
        pause
        exit /b 1
    )
    echo.
    echo %COLOR_GREEN%Build complete!%COLOR_RESET%
    echo.
    echo.exe file is ready for deployment
    pause
) else if "%choice%"=="3" (
    echo.
    echo Starting with Electron GUI...
    cd electron
    npm install
    npm start
    cd ..
) else (
    echo Exiting...
    exit /b 0
)

pause
