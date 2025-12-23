#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnvanterQR Setup Script
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

print("""
[*] ENVANTERQR v1.0 INSTALLER
[*] Setup starting... Please wait!
""")

# Get application directory
app_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(app_dir))

print(f"[*] App Directory: {app_dir}")

# Step 1: Check Python version
print("\n[1] Checking Python Version...")
python_version = sys.version_info
if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
    print(f"[!] ERROR: Python 3.8+ required (Installed: {python_version.major}.{python_version.minor})")
    sys.exit(1)
print(f"[OK] Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")

# Step 2: Check if pip is available
print("\n[2] Checking Pip...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[OK] Pip Found and Ready")
except Exception as e:
    print(f"[!] ERROR: Pip not available: {e}")
    sys.exit(1)

# Step 3: Upgrade pip
print("\n[3] Upgrading Pip...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[OK] Pip Upgraded")
except Exception as e:
    print(f"[!] Pip upgrade failed (continuing): {e}")

# Step 4: Install requirements
print("\n[4] Installing Required Packages...")
requirements_file = app_dir / "requirements.txt"

if not requirements_file.exists():
    print(f"[!] ERROR: {requirements_file} not found")
    sys.exit(1)

packages = [
    "flask>=3.1.2",
    "flask-sqlalchemy>=3.1.1",
    "flask-socketio>=5.5.1",
    "openpyxl>=3.1.5",
    "pandas>=2.3.3",
    "pillow>=12.0.0",
    "python-socketio>=5.14.2",
    "qrcode[pil]>=8.2",
    "python-dotenv>=1.0.0",
    "eventlet>=0.35.2",
    "gunicorn>=21.2.0",
    "reportlab>=4.0.0"
]

installed = 0
failed = 0

for i, package in enumerate(packages, 1):
    try:
        pkg_name = package.split('>=')[0]
        print(f"   [{i}/{len(packages)}] {pkg_name}...", end=" ", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("OK")
        installed += 1
    except Exception as e:
        print(f"FAIL")
        failed += 1

print(f"\n[OK] Packages Installed: {installed} success, {failed} errors")

if failed > 3:
    print(f"[!] WARNING: Many packages failed. Check internet connection.")
    sys.exit(1)

# Step 5: Check if required files exist
print("\n[5] Checking System Files...")
required_files = ["app.py", "models.py", "config.py"]
for f in required_files:
    if not (app_dir / f).exists():
        print(f"[!] ERROR: {f} not found")
        sys.exit(1)
print(f"[OK] All required files present")

# Step 6: Create necessary directories
print("\n[6] Creating Required Directories...")
dirs_to_create = ["instance", "static/qrcodes", "static/exports", "backups", "templates"]
for d in dirs_to_create:
    dir_path = app_dir / d
    dir_path.mkdir(parents=True, exist_ok=True)
print(f"[OK] Directories Ready")

# Step 7: Test import
print("\n[7] Testing System Modules...")
try:
    from app import app
    print("[OK] Flask Application Loaded Successfully")
except ImportError as e:
    print(f"[!] ERROR: {e}")
    print("[*] Please contact system administrator")
    sys.exit(1)

# Step 8: Get Flask port
port = 5000
print(f"\n[8] Starting Web Server...")
print(f"[*] Address: http://localhost:{port}")
print(f"[*] Admin: http://localhost:{port}/admin")

time.sleep(2)

print("""
[*] SETUP COMPLETE - SYSTEM STARTING
[*] Please keep the browser window open!
[*] To stop: Press Ctrl+C
""")

# Open browser
try:
    webbrowser.open(f"http://localhost:{port}")
    print("[OK] Browser Opened")
except:
    print("[!] Browser could not open automatically - please open manually")

# Start Flask app
try:
    from app import app
    print(f"\n[*] Flask starting...")
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
except KeyboardInterrupt:
    print("\n\n[*] System stopped")
    sys.exit(0)
except Exception as e:
    print(f"\n[!] ERROR: {e}")
    sys.exit(1)
