# -*- mode: python ; coding: utf-8 -*-

import os
import glob

cmd_dir = os.path.join(SPECPATH, 'src/mepo/command')
cmd_list = [os.path.basename(x).split('.')[0] for x in glob.glob(os.path.join(cmd_dir, '*.py'))]
hidden_imports = [f'mepo.command.{x}' for x in cmd_list if '_' not in x] # exclude subcommands
print(f'hidden_imports: {hidden_imports}')

a = Analysis(
    ['src/mepo/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hidden_imports,
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
    [],
    exclude_binaries=True,
    name='mepo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mepo',
)
