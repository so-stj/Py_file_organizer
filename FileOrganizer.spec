# -*- mode: python ; coding: utf-8 -*-
"""
FileOrganizer PyInstaller Specification File
This file configures how PyInstaller should build the executable

Version: 1.2.0
Features: Custom separation destination selection, multilingual support
"""

block_cipher = None

# Analysis phase: collect all necessary files and dependencies
a = Analysis(
    ['main.py'],  # Main entry point
    pathex=['src', '.'],  # Python path for imports
    binaries=[],  # Additional binary files
    datas=[('src', 'src')],  # Include entire src directory
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'pathlib',
        'json',
        'os',
        'shutil',
        're',
        'datetime',
        'threading',
        'typing',
        'sys',
        'traceback',
        'src',
        'src.config',
        'src.config.config_manager',
        'src.core',
        'src.core.file_organizer_core',
        'src.utils',
        'src.utils.logger',
        'src.gui',
        'src.gui.language_dialog',
        'src.gui.settings_window',
        'src.gui.file_type_dialog',
        'src.gui.separation_destination_dialog',
        'src.main_app'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'torch',
        'tensorflow',
        'sklearn',
        'seaborn',
        'plotly',
        'bokeh',
        'dash',
        'flask',
        'django',
        'fastapi',
        'sqlalchemy',
        'pymongo',
        'redis',
        'celery',
        'requests',
        'urllib3',
        'beautifulsoup4',
        'selenium',
        'pytest',
        'unittest'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FileOrganizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUIアプリなのでコンソールを表示しない
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico'  # アイコンファイルがある場合はコメントアウトを外す
)
