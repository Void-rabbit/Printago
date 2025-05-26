# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['run.py'],
             pathex=['.'],  # Ensure the current directory is in the Python path
             binaries=[],
             datas=[
                 ('templates', 'templates'),
                 ('static', 'static'),
                 ('users.json', '.'), # Data files at the root, to be placed in the root of dist
                 ('parts.json', '.'),
                 ('printers.json', '.'),
                 ('print_jobs.json', '.')
             ],
             hiddenimports=['jinja2.ext', 'bcrypt', 'paho'], # Added bcrypt and paho based on project usage
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PrintFarmManager', # Name of the executable
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True, # Start with console=True for easier debugging
          windowed=False # Paired with console=True
          )
