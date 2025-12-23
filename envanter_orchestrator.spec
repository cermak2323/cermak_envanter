# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['backend\\startup_orchestrator.py'],
    pathex=[],
    binaries=[],
    datas=[('backend', 'backend'), ('.env.default', '.'), ('templates', 'templates'), ('static', 'static'), ('models.py', '.'), ('db_config.py', '.'), ('app.py', '.')],
    hiddenimports=['flask', 'flask_socketio', 'sqlalchemy', 'psycopg2', 'apscheduler', 'engineio.async_drivers.threading'],
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
    name='envanter_orchestrator',
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
