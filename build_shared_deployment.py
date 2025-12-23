#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CermakEnvanter Executable Builder
Shared Folder Deployment - Network Access
STATIC klasörüne DOKUNMAZ (zaten network'te)
Direkt \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter klasörüne deploy eder
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Renkli çıktı
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def print_ok(msg):
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {msg}")

def print_info(msg):
    print(f"{Colors.YELLOW}[*]{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[!]{Colors.RESET} {msg}")

print(f"""{Colors.GREEN}
════════════════════════════════════════════════════════════
   CERMAK ENVANTER - EXECUTABLE BUILDER
   Network Shared Deployment
════════════════════════════════════════════════════════════
{Colors.RESET}""")

app_dir = Path(__file__).parent.resolve()
dist_dir = app_dir / "dist"
build_dir = app_dir / "build"

# Shared folder path
shared_deploy = Path(r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter")

print_info(f"Source: {app_dir}")
print_info(f"Deploy Target: {shared_deploy}")

# [1] Network erişim kontrolü
print(f"\n{Colors.YELLOW}[1] Network Access Check...{Colors.RESET}")
try:
    if not shared_deploy.exists():
        print_error(f"Network path not accessible: {shared_deploy}")
        print_error("Making directory locally: dist/")
        shared_deploy = dist_dir
    else:
        print_ok("Network path accessible")
except Exception as e:
    print_error(f"Network check failed: {e}")
    print_info("Will build locally to dist/")
    shared_deploy = dist_dir

# [2] Cleanup
print(f"\n{Colors.YELLOW}[2] Cleaning Previous Builds...{Colors.RESET}")
if build_dir.exists():
    shutil.rmtree(build_dir)
    print_ok(f"Removed {build_dir}")

if dist_dir.exists():
    shutil.rmtree(dist_dir)
    print_ok(f"Removed {dist_dir}")

# [3] PyInstaller check
print(f"\n{Colors.YELLOW}[3] Checking Dependencies...{Colors.RESET}")
try:
    import PyInstaller
    print_ok("PyInstaller found")
except ImportError:
    print_info("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyinstaller"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print_ok("PyInstaller installed")

# [4] Build command - ONE-FILE MODE
print(f"\n{Colors.YELLOW}[4] Building Executable (--onefile mode)...{Colors.RESET}")
print_info("This may take 5-15 minutes...")

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",                          # Single executable
    "--windowed",                         # GUI mode - NO console window (Windows only)
    "--icon=cermaktakeuchi_logo.ico",
    "--add-data", f"{app_dir / 'templates'};templates",
    "--add-data", f"{app_dir / 'backend'};backend",
    # IMPORTANT: DO NOT add static - it's on network
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
    "--hidden-import=werkzeug",
    "--hidden-import=jinja2",
    "--hidden-import=apscheduler",
    "--hidden-import=apscheduler.schedulers.background",
    "--name=CermakEnvanter",
    str(app_dir / "app.py")
]

try:
    # Run with live output
    result = subprocess.run(cmd, cwd=str(app_dir))
    if result.returncode != 0:
        print_error("Build failed")
        sys.exit(1)
    print_ok("Build completed")
except Exception as e:
    print_error(f"Build error: {e}")
    sys.exit(1)

# [5] Verify exe
print(f"\n{Colors.YELLOW}[5] Verifying Build Output...{Colors.RESET}")
exe_path = dist_dir / "CermakEnvanter.exe"

if exe_path.exists():
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print_ok(f"Executable created: {exe_path.name}")
    print_ok(f"Size: {size_mb:.1f} MB")
else:
    print_error("Executable not found")
    sys.exit(1)

# [6] Deploy to network/shared folder
print(f"\n{Colors.YELLOW}[6] Deploying to Network...{Colors.RESET}")

try:
    # Create deploy directory if needed
    shared_deploy.mkdir(parents=True, exist_ok=True)
    
    # Copy exe to shared folder
    deploy_exe = shared_deploy / "CermakEnvanter.exe"
    print_info(f"Copying to {deploy_exe}...")
    shutil.copy2(exe_path, deploy_exe)
    print_ok(f"Deployed successfully")
    
    # Create shortcut helper batch
    batch_file = shared_deploy / "CREATE_SHORTCUT.bat"
    batch_content = f"""@echo off
REM Create desktop shortcut for CermakEnvanter
set SHORTCUT_PATH=%USERPROFILE%\\Desktop\\CermakEnvanter.lnk
set TARGET_EXE={deploy_exe}
set WORK_DIR={shared_deploy}

echo Creating shortcut on Desktop...
powershell -Command ^
  "$WshShell = New-Object -ComObject WScript.Shell; " ^
  "$Shortcut = $WshShell.CreateShortcut('{deploy_exe.parent / 'CermakEnvanter.lnk'}'); " ^
  "$Shortcut.TargetPath = '{deploy_exe}'; " ^
  "$Shortcut.WorkingDirectory = '{shared_deploy}'; " ^
  "$Shortcut.IconLocation = '{deploy_exe}'; " ^
  "$Shortcut.Save()"

echo.
echo Shortcut created on Desktop!
echo Double-click to start CermakEnvanter
pause
"""
    with open(batch_file, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    print_ok(f"Created shortcut helper: {batch_file.name}")
    
except Exception as e:
    print_error(f"Deployment error: {e}")
    sys.exit(1)

# [7] Summary
print(f"""
{Colors.GREEN}════════════════════════════════════════════════════════════
   BUILD COMPLETE ✓
════════════════════════════════════════════════════════════
{Colors.RESET}

📁 Executable: {deploy_exe}
📊 Size: {size_mb:.1f} MB
🌐 Deployment: {shared_deploy}

{Colors.YELLOW}INSTALLATION INSTRUCTIONS:{Colors.RESET}

1. Run CREATE_SHORTCUT.bat on any PC to create Desktop shortcut
   OR manually create shortcut to: {deploy_exe}

2. All PCs will use the same shared executable
3. Static files served from network (no Chrome needed)
4. Database: Network shared folder

{Colors.GREEN}Ready for deployment!{Colors.RESET}
""")
