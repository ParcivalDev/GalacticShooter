# GalacticShooter.spec
from PyInstaller.utils.hooks import collect_all

a = Analysis(
    ['GalacticShooter.py'],
    pathex=[],  
    binaries=[],
    datas=[
    ('assets/start.png', 'assets'),
    ('assets/game_over.png', 'assets'),
    ('assets/laser.png', 'assets'),
    ('assets/fondo_espacio.jpg', 'assets'),
    ('assets/player.png', 'assets'),
    ('assets/enemigo.jpg', 'assets'),
    ('assets/life_heart.png', 'assets'),
    ('assets/explosion.png', 'assets'),
    ('assets/hysteria.ogg', 'assets'),
    ('assets/collision.ogg', 'assets'),
    ('assets/explosion.ogg', 'assets'),
    ('assets/laser_shot.ogg', 'assets')
],

    hiddenimports=[],
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
    name='GalacticShooter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Cambiar a True si quieres la consola abierta
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
