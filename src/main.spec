# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['paste_printer\\main.py'],
             pathex=['C:\\Users\\Johannes\\iCloudDrive\\Uni\\CSE\\Year 3\\Advanced Prototyping\\APP\\3D print, use, disolve, repeat\\GCode Modifier\\src'],
             binaries=[],
             datas=[('paste_printer/resources/icons/*', 'paste_printer/resources/icons'), ('paste_printer/resources/gcode/0.6/*', 'paste_printer/resources/gcode/0.6'), ('paste_printer/resources/gcode/0.8/*', 'paste_printer/resources/gcode/0.8'), ('paste_printer/resources/gcode/1.5/*', 'paste_printer/resources/gcode/1.5'), ('paste_printer/resources/fonts/*', 'paste_printer/resources/fonts'), ('paste_printer/resources/settings/*', 'paste_printer/resources/settings')],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
