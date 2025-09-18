# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['exam_system_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('single_choice.json', '.'),
        ('multiple_choice.json', '.'),
        ('judgment.json', '.'),
        ('README.md', '.'),
        ('GUI使用说明.md', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='人工智能考试练习系统',
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
    icon=None,
)
