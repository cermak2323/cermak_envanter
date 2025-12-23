@echo off
REM Cermak Envanter - Electron Launcher
REM Simple double-click to run

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   CERMAK ENVANTER - Electron Launcher                         ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    echo Install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo Starting system...
echo.

REM Run the launcher
python electron_launcher.py

if errorlevel 1 (
    echo.
    echo Error occurred. Check the console output above.
    pause
)
