# -*- mode: python ; coding: utf-8 -*-

from sys import platform

block_cipher = None

data_files_to_add = [
						('configFile.txt', '.'),
						('logger.conf', '.' ),
						('translations', 'translations' ),
						('userHelp', 'userHelp' ),
					]

pre_processor_w32 = [ 	
						('Processors\\pre1_5-w32\\*.*', 'Processors\\pre1_5-w32' ),
						('Processors\\pre1_5-w32\\jpg\\*.*', 'Processors\\pre1_5-w32\\jpg' )
					]

if platform.startswith('win'):
	data_files_to_add += pre_processor_w32

a = Analysis(['lepg.py'],
             pathex=['C:\\Users\\user\\git\\lepg-py\\src'],
             binaries=[],
             datas= data_files_to_add,
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
          name='lepg',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='lepg')
