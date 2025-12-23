# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:\\Users\\rsade\\Desktop\\Yeni klasör\\EnvanterQR\\EnvanterQR\\templates', 'templates'), ('C:\\Users\\rsade\\Desktop\\Yeni klasör\\EnvanterQR\\EnvanterQR\\backend', 'backend'), ('C:\\Users\\rsade\\Desktop\\Yeni klasör\\EnvanterQR\\EnvanterQR\\electron', 'electron')]
binaries = []
hiddenimports = ['flask', 'flask_sqlalchemy', 'flask_socketio', 'flask_cors', 'pymysql', 'sqlalchemy', 'pandas', 'openpyxl', 'requests', 'b2sdk', 'apscheduler', 'python_socketio']
tmp_ret = collect_all('flask')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('flask_sqlalchemy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\rsade\\Desktop\\Yeni klasör\\EnvanterQR\\EnvanterQR\\electron_launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CermakEnvanter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\rsade\\Desktop\\Yeni klasör\\EnvanterQR\\EnvanterQR\\cermaktakeuchi_logo.ico'],
)
