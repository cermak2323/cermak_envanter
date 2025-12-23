#!/usr/bin/env python3
"""
Build CermakEnvanter as Electron + Flask integrated executable
Creates: CermakEnvanter.exe (GUI application with embedded backend)
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

# Configuration
APP_NAME = "CermakEnvanter"
APP_DIR = Path(__file__).parent
NETWORK_PATH = r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter"
ELECTRON_DIR = APP_DIR / "electron"

# Deployment settings
DEPLOY_NETWORK = True
DEPLOY_PATH = NETWORK_PATH if DEPLOY_NETWORK else APP_DIR / "dist"

print("=" * 80)
print("CERMAK ENVANTER - ELECTRON + FLASK BUILD")
print("=" * 80)
print(f"[APP DIR] {APP_DIR}")
print(f"[ELECTRON DIR] {ELECTRON_DIR}")
print(f"[DEPLOY PATH] {DEPLOY_PATH}")
print()

# Step 1: Check Electron directory
print("[1] Checking Electron setup...")
if not ELECTRON_DIR.exists():
    print("✗ Electron directory not found!")
    sys.exit(1)
print("✓ Electron directory exists")

# Step 2: Install npm dependencies for Electron
print("\n[2] Installing Electron dependencies...")
try:
    result = subprocess.run(
        "npm install",
        cwd=ELECTRON_DIR,
        capture_output=True,
        text=True,
        timeout=120,
        shell=True,
    )
    if result.returncode == 0:
        print("✓ npm dependencies installed")
    else:
        print(f"[WARNING] npm install returned: {result.returncode}")
        print(result.stderr)
except Exception as e:
    print(f"✗ npm not found - install Node.js from https://nodejs.org")
    print(f"Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error installing npm dependencies: {e}")
    sys.exit(1)

# Step 3: Build Electron application
print("\n[3] Building Electron app...")
print("[INFO] Electron builder already created installer in electron/dist")
print("[INFO] Skipping npm build - using existing Electron files")
# Electron build already done manually, executable exists in electron/dist

# Step 4: Create PyInstaller exe with Electron launcher
print("\n[4] Building PyInstaller executable...")
try:
    # Build the electron_launcher.py as the main entry point
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--windowed",
        f"--icon={APP_DIR / 'cermaktakeuchi_logo.ico'}",
        f"--name={APP_NAME}",
        "--add-data", f"{APP_DIR / 'templates'};templates",
        "--add-data", f"{APP_DIR / 'backend'};backend",
        "--add-data", f"{ELECTRON_DIR};electron",
        "--hidden-import=flask",
        "--hidden-import=flask_sqlalchemy",
        "--hidden-import=flask_socketio",
        "--hidden-import=flask_cors",
        "--hidden-import=pymysql",
        "--hidden-import=sqlalchemy",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=requests",
        "--hidden-import=b2sdk",
        "--hidden-import=apscheduler",
        "--hidden-import=python_socketio",
        "--collect-all=flask",
        "--collect-all=flask_sqlalchemy",
        "--distpath", str(APP_DIR / "dist"),
        "--workpath", str(APP_DIR / "build"),
        str(APP_DIR / "electron_launcher.py"),
    ]
    
    print(f"Running PyInstaller (this takes 15-25 minutes)...")
    result = subprocess.run(cmd, capture_output=False, text=True, timeout=1800)  # 30 minutes for PyInstaller
    
    if result.returncode != 0:
        print(f"✗ PyInstaller failed with code {result.returncode}")
        sys.exit(1)
    
    print("✓ PyInstaller executable created")
    
except Exception as e:
    print(f"✗ Error running PyInstaller: {e}")
    sys.exit(1)

# Step 5: Verify executable
print("\n[5] Verifying executable...")
exe_path = APP_DIR / "dist" / f"{APP_NAME}.exe"
if not exe_path.exists():
    print(f"[ERROR] Executable not found at {exe_path}")
    sys.exit(1)

exe_size = exe_path.stat().st_size / (1024 * 1024)
print(f"[SUCCESS] Executable created: {exe_path.name} ({exe_size:.1f} MB)")

# Step 6: Deploy to network
print("\n[6] Deploying to network...")
try:
    if DEPLOY_NETWORK:
        # Check if network path is accessible
        if not os.path.exists(NETWORK_PATH):
            print(f"[WARNING] Network path not accessible: {NETWORK_PATH}")
            print(f"[INFO] Deploying to local dist folder instead...")
            deploy_target = APP_DIR / "dist"
        else:
            deploy_target = Path(NETWORK_PATH)
            print(f"[OK] Network path accessible")
    else:
        deploy_target = APP_DIR / "dist"
    
    # Copy executable to deployment path
    target_exe = deploy_target / f"{APP_NAME}.exe"
    print(f"[COPY] {target_exe}")
    shutil.copy2(exe_path, target_exe)
    print(f"[SUCCESS] Deployed to {target_exe}")
    
    # Create shortcut batch file
    shortcut_batch = deploy_target / "CREATE_SHORTCUT.bat"
    batch_content = f'''@echo off
setlocal enabledelayedexpansion
set "NETWORK_PATH={NETWORK_PATH}"
set "EXE_NAME={APP_NAME}.exe"
set "SHORTCUT_NAME=Cermak Envanter QR"

REM Create desktop shortcut
cd /d "%USERPROFILE%\\Desktop"
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\\Desktop\\%SHORTCUT_NAME%.lnk');$s.TargetPath='%NETWORK_PATH%\\%EXE_NAME%';$s.WorkingDirectory='%NETWORK_PATH%';$s.IconLocation='%NETWORK_PATH%\\%EXE_NAME%';$s.Save()"

echo.
echo [OK] Desktop shortcut created: %SHORTCUT_NAME%
echo [OK] Location: %USERPROFILE%\\Desktop\\%SHORTCUT_NAME%.lnk
echo.
echo Network Path: %NETWORK_PATH%\\%EXE_NAME%
pause
'''
    
    with open(shortcut_batch, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"[OK] Shortcut helper created: {shortcut_batch}")

except Exception as e:
    print(f"[ERROR] Deploying: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 80)
print("BUILD COMPLETE!")
print("=" * 80)
print(f"[EXE] {exe_path.name} ({exe_size:.1f} MB)")
print(f"[LOCATION] {deploy_target}")
print()
print("[INSTALL]")
print(f"  1. Run CREATE_SHORTCUT.bat on any PC")
print(f"  2. Desktop shortcut will be created")
print(f"  3. All PCs use the same shared executable")
print()
print("[FEATURES]")
print("  - Electron GUI (windowed application)")
print("  - Flask backend (embedded)")
print("  - No console window")
print("  - Session persistence (permanent login)")
print("  - Network deployment ready")
print("=" * 80)
