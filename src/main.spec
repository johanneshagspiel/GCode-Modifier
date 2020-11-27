# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main\\main.py'],
             pathex=['C:\\Users\\Johannes\\iCloudDrive\\Uni\\CSE\\Year 3\\Advanced Prototyping\\APP\\3D print, use, disolve, repeat\\Github\\src'],
             binaries=[],
             datas=[('main/resources/icons/*', 'main/resources/icons'), ('main/resources/gcode/*', 'main/resources/gcode'), ('main/resources/fonts/*', 'main/resources/fonts')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
