#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CermakEnvanter Network Deployment Builder
Derliyorduk: \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter
Tüm PC'ler buradan çalışacak (kısayol ile)
Static klasörüne dokunmaz - zaten network'te var
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

print("""
[*] CERMAKENVANTER - NETWORK DEPLOYMENT BUILDER
[*] Target: \\\\DCSRV\\tahsinortak\\CermakDepo\\CermakEnvanter
[*] Mode: One-directory (network shared)
[*] Static: Will NOT be touched (already on network)
""")

app_dir = Path(__file__).parent.resolve()
network_deploy_dir = Path(r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter")
dist_dir = app_dir / "dist_network"
build_dir = app_dir / "build_network"

print(f"\n[1] Checking network access...")
if network_deploy_dir.exists():
    print(f"    [OK] Network path accessible: {network_deploy_dir}")
else:
    print(f"    [!] WARNING: Network path not accessible")
    print(f"    [!] Will build locally to: {dist_dir}")
    network_deploy_dir = dist_dir
    network_deploy_dir.mkdir(parents=True, exist_ok=True)

print(f"\n[2] Cleaning old builds...")
if build_dir.exists():
    shutil.rmtree(build_dir)
    print(f"    [OK] {build_dir} deleted")

# Check PyInstaller
print(f"\n[3] Checking PyInstaller...")
try:
    import PyInstaller
    print(f"    [OK] PyInstaller installed")
except ImportError:
    print(f"    [*] Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyinstaller"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"    [OK] PyInstaller installed")

# Build executable - ONE-DIR mode (NOT one-file)
print(f"\n[4] Building executable (one-dir mode)...")
print(f"    [*] This may take 5-10 minutes...")

# Prepare hiddenimports
hiddenimports = [
    'flask', 'flask_sqlalchemy', 'flask_socketio', 'engineio.async_drivers.threading',
    'qrcode', 'PIL', 'pandas', 'openpyxl', 'reportlab',
    'pymysql', 'pymysql.cursors', 'sqlalchemy.dialects.mysql.pymysql',
    'b2sdk', 'b2sdk.v2', 'werkzeug', 'jinja2', 'click',
    'apscheduler', 'apscheduler.schedulers.background',
    'mysql', 'mysql.connector'
]

# Build command with one-dir mode
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onedir",  # One-directory mode (NOT --onefile)
    "--console",
    "--icon=cermaktakeuchi_logo.ico",
    "--add-data", f"{app_dir / 'templates'};templates",
    "--add-data", f"{app_dir / 'backend'};backend",
    # DO NOT add static - it's on network
    "--distpath", str(dist_dir),
    "--buildpath", str(build_dir),
]

# Add hidden imports
for imp in hiddenimports:
    cmd.extend(["--hidden-import", imp])

cmd.extend([
    "--name=CermakEnvanter",
    "--clean",
    str(app_dir / 'app.py')
])

try:
    result = subprocess.run(cmd, cwd=str(app_dir), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] ERROR: {result.stderr}")
        sys.exit(1)
    print(f"    [OK] Build completed")
except Exception as e:
    print(f"[!] ERROR: {e}")
    sys.exit(1)

# Check if exe was created
exe_path = dist_dir / "CermakEnvanter" / "CermakEnvanter.exe"
if exe_path.exists():
    print(f"\n[5] Checking build output...")
    print(f"    [OK] Executable created: {exe_path}")
    
    # Get directory size
    total_size = 0
    for item in (dist_dir / "CermakEnvanter").rglob('*'):
        if item.is_file():
            total_size += item.stat().st_size
    size_mb = total_size / (1024 * 1024)
    print(f"    [OK] Build size: {size_mb:.1f} MB")
    
    # Deploy to network
    print(f"\n[6] Deploying to network...")
    deploy_path = network_deploy_dir / "CermakEnvanter"
    
    if deploy_path.exists():
        print(f"    [*] Removing old version: {deploy_path}")
        shutil.rmtree(deploy_path)
    
    print(f"    [*] Copying to network: {deploy_path}")
    shutil.copytree(dist_dir / "CermakEnvanter", deploy_path)
    print(f"    [OK] Deployment successful!")
    
    print(f"\n[OK] BUILD COMPLETE!")
    print(f"    Path: {deploy_path}")
    print(f"    Size: {size_mb:.1f} MB")
    print(f"""
[*] DEPLOYMENT INSTRUCTIONS:
[*] 1. On each PC, create shortcut to:
[*]    {deploy_path}/CermakEnvanter.exe
[*] 2. Place shortcut on Desktop or Start Menu
[*] 3. All PCs will use the same shared version
[*] 4. Static files will be served from network
[*] 5. No need for Chrome - exe runs standalone
    """)
    
    # Create batch file for shortcut creation
    batch_path = network_deploy_dir / "CREATE_SHORTCUTS.bat"
    exe_path_str = str(deploy_path / "CermakEnvanter.exe")
    deploy_path_str = str(deploy_path)
    batch_content = f"""@echo off
REM Create desktop shortcuts for all users
echo Creating shortcut...

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\\CermakEnvanter.lnk'); $Shortcut.TargetPath = '{exe_path_str}'; $Shortcut.WorkingDirectory = '{deploy_path_str}'; $Shortcut.IconLocation = '{exe_path_str}'; $Shortcut.Save()"

echo Shortcut created on Desktop!
pause
"""
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    print(f"[*] Created shortcut helper: {batch_path}")
    
else:
    print(f"[!] ERROR: Executable could not be created")
    sys.exit(1)
