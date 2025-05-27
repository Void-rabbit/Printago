# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(['desktop_app.py'],
             pathex=['.'],
             binaries=[],
             datas=[],  # Initialize datas; PySide2 data added below.
                        # Flask-related 'templates' and 'static' are removed.
                        # JSON data files are also removed as the desktop app should manage its own data.
             hiddenimports=[
                 'PySide2.QtCore', 
                 'PySide2.QtGui', 
                 'PySide2.QtWidgets',
                 'requests', # Explicitly add 'requests' as it's used by bambu_cloud_client
                 'bambu_cloud_client', # Ensure this is included if not automatically detected
                 # Do NOT include 'app' or 'flask' here if desktop_app.py is standalone
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=['flask', 'werkzeug', 'jinja2', 'bcrypt', 'app', 'run'], # Attempt to exclude Flask and related modules
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# Collect data files for PySide2 (e.g., Qt plugins, translations)
a.datas += collect_data_files('PySide2', include_py_files=True)

# Include the QSS stylesheet for the dark theme
a.datas += [('static/css/dark_theme.qss', 'static/css')]


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [], 
          name='PrintagoManager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True, # Keep True for debugging the packaged app
          windowed=False, # Paired with console=True for now
          icon=None) 

# For macOS, to create an app bundle (optional):
# app_bundle = BUNDLE(exe,
#              name='PrintagoManager.app',
#              icon=None, # Path to .icns file for macOS
#              bundle_identifier=None)
