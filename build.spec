# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 要打包的文件
a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('icons/app_icon.icns', 'icons')],
    hiddenimports=['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# 打包成单文件应用
pyz = PYZ(a.pure)

# 创建可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FlexWorkManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons/app_icon.icns'],  # 应用图标
)

# 创建.app bundle（Mac应用）
app = BUNDLE(
    exe,
    name='FlexWorkManager.app',
    icon='icons/app_icon.icns',
    bundle_identifier='com.yourcompany.flexwork',
    info_plist={
        'CFBundleName': 'FlexWorkManager',
        'CFBundleDisplayName': '灵活用工管理平台',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.yourcompany.flexwork',
        'NSHumanReadableCopyright': '版权所有 © 2024',
        'LSMinimumSystemVersion': '10.13',
        'LSApplicationCategoryType': 'public.app-category.business',
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
    },
)
