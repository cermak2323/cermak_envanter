# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\rsade\\Desktop\\Yeni klasör (2)\\EnvanterQR\\EnvanterQR\\setup_and_run.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\rsade\\Desktop\\Yeni klasör (2)\\EnvanterQR\\EnvanterQR\\templates', 'templates'), ('C:\\Users\\rsade\\Desktop\\Yeni klasör (2)\\EnvanterQR\\EnvanterQR\\static', 'static')],
    hiddenimports=['flask', 'flask_sqlalchemy', 'flask_socketio', 'qrcode', 'PIL', 'pandas', 'openpyxl', 'reportlab'],
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
    name='EnvanterQR',
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
)
