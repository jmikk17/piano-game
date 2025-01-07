# -*- mode: python ; coding: utf-8 -*-

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[
                ('audio/', 'audio/'),
                ('graphics/', 'graphics/'),
                ('songs/', 'songs/'),
             ],
             hiddenimports=[
                'pygame',
                'game',
                'gamestate',
                'menu',
                'music_engine',
                'cfg',
                'auxil',
                'error',
                'test'
             ],
             excludes=[
                'numpy',  # Not needed unless you're doing array operations
                'OpenGL', # Not needed for basic Pygame
                '_winreg', # Windows registry stuff
                'termios', # Terminal IO stuff
                'java', # Java-related
                'tkinter', # GUI toolkit you're not using
             ],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='YourGameName',  # Change this to your desired game name
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )