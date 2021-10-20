# -*- mode: python ; coding: utf-8 -*-

from sys import platform

block_cipher = None

data_files_to_add = [
						('logger.conf', '.' ),
						('translations', 'translations' ),
						('userHelp', 'userHelp' ),
						('Windows\\favicon.ico', 'Windows'),
						('Windows\\appIcon.ico', 'Windows')
					]

processor_w64 = [ 	
						('Processors\\lep-3.16-win64', 'Processors\\lep-3.16-win64' ),
					]
					
processor_lin64 = [ 	
						('Processors\\lep-3.16-lin64', 'Processors\\lep-3.16-lin64' ),
					]

if platform.startswith('win'):
	data_files_to_add += processor_w64
elif platform.startswith('linux'):
	data_files_to_add += processor_lin64

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
          console=True,
		  icon='Windows\\appIcon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='lepg')
