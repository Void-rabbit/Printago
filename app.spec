# -*- mode: python ; coding: utf-8 -*-

# This spec file is configured for building the PySide2 desktop application.
# The Flask web components (templates, static files, web-specific JSON data handling)
# might still be bundled if not explicitly excluded or if app.py is imported by desktop_app.py.
# For a pure desktop app, further refinement might be needed to exclude Flask components
# unless the Flask app is intended to run as a backend service.

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(['desktop_app.py'],  # Changed entry point to desktop_app.py
             pathex=['.'],
             binaries=[],
             datas=[],  # Initially empty; PySide2 data is typically handled by hooks or collected explicitly
             hiddenimports=['PySide2.QtCore', 'PySide2.QtGui', 'PySide2.QtWidgets', 'app'], # Essential PySide2 modules, added 'app' if desktop_app imports from it
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# Collect data files for PySide2 (e.g., plugins, translations)
# This is a common way to include necessary Qt platform plugins.
a.datas += collect_data_files('PySide2', include_py_files=True) # include_py_files=True can be important

# If the desktop app still uses the Flask backend for API calls or data,
# and imports 'app.py' or its components, then Flask-related templates/static files
# and JSON data files might be needed.
# This example assumes desktop_app.py might eventually call APIs from app.py,
# or app.py might be refactored into a utility module.
# If app.py (and thus Flask) is needed:
a.hiddenimports.extend(['jinja2.ext', 'bcrypt', 'werkzeug.serving', 'flask']) # Add flask and werkzeug.serving for flask dev server
# The data files for Flask part would be needed if it's run as a backend.
# For a pure desktop app not using Flask server, these would be removed.
a.datas += [
    ('templates', 'templates'),
    ('static', 'static'),
    ('users.json', '.'),
    ('parts.json', '.'),
    ('printers.json', '.'),
    ('print_jobs.json', '.')
]


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [], # Cleared explicit a.binaries, a.zipfiles, a.datas; PyInstaller handles from Analysis
          name='PrintagoManager',  # Updated name for the desktop app
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True, # Start with True for debugging desktop app issues
          windowed=False, # Paired with console=True
          icon=None) # TODO: Add an application icon path here if available (e.g., 'app_icon.ico')

# For macOS, to create an app bundle:
# app_bundle = BUNDLE(exe,
#              name='PrintagoManager.app',
#              icon=None, # Path to .icns file
#              bundle_identifier=None)
