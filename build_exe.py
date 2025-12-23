#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CermakEnvanter Executable Builder
Converts app.py to CermakEnvanter.exe
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

print("""
[*] CERMAKENVANTER - EXECUTABLE BUILDER
[*] Building executable from app.py
""")

app_dir = Path(__file__).parent.resolve()
dist_dir = app_dir / "dist"
build_dir = app_dir / "build"

print(f"\n[1] Cleaning directories...")
if dist_dir.exists():
    shutil.rmtree(dist_dir)
    print(f"    [OK] {dist_dir} deleted")

if build_dir.exists():
    shutil.rmtree(build_dir)
    print(f"    [OK] {build_dir} deleted")

# Install PyInstaller
print(f"\n[2] Checking PyInstaller...")
try:
    import PyInstaller
    print(f"    [OK] PyInstaller installed")
except ImportError:
    print(f"    [*] Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyinstaller"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"    [OK] PyInstaller installed")

# Build executable
print(f"\n[3] Building executable (this may take a few minutes)...")
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--console",
    "--icon=cermaktakeuchi_logo.ico",
    "--add-data", f"{app_dir / 'templates'};templates",
    "--add-data", f"{app_dir / 'static'};static",
    "--hidden-import=flask",
    "--hidden-import=flask_sqlalchemy",
    "--hidden-import=flask_socketio",
    "--hidden-import=engineio.async_drivers.threading",
    "--hidden-import=qrcode",
    "--hidden-import=PIL",
    "--hidden-import=pandas",
    "--hidden-import=openpyxl",
    "--hidden-import=reportlab",
    "--hidden-import=pymysql",
    "--hidden-import=pymysql.cursors",
    "--hidden-import=sqlalchemy.dialects.mysql.pymysql",
    "--hidden-import=b2sdk",
    "--hidden-import=b2sdk.v2",
    "--name=CermakEnvanter",
    f"{app_dir / 'app.py'}"
]

# Clean empty command arguments
cmd = [arg for arg in cmd if arg]

try:
    result = subprocess.run(cmd, cwd=str(app_dir), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] ERROR: {result.stderr}")
        sys.exit(1)
    print(f"    [OK] Executable built")
except Exception as e:
    print(f"[!] ERROR: {e}")
    sys.exit(1)

# Check if exe was created
exe_path = dist_dir / "CermakEnvanter.exe"
if exe_path.exists():
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"\n[OK] BUILD SUCCESSFUL!")
    print(f"    File: {exe_path}")
    print(f"    Size: {size_mb:.1f} MB")
    print(f"\n[*] Exe Directory: {dist_dir}")
    print(f"    Double-click CermakEnvanter.exe and start!")
else:
    print(f"[!] ERROR: Executable could not be created")
    sys.exit(1)

print(f"""
[*] BUILD COMPLETE
[*] File Location: {str(exe_path)}
[*] INSTALLATION:
[*] 1. Copy CermakEnvanter.exe to a folder
[*] 2. Double-click - system will start automatically
[*] 3. All requirements will install automatically
[*] 4. Browser will open at http://localhost:5000
""")
