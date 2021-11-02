# -*- mode: python ; coding: utf-8 -*-

from sys import platform
import os

dirpath = os.path.dirname(os.path.abspath("__file__"))
pathex_path = [os.path.join(dirpath, '..','src')]

block_cipher = None

data_files_to_add = [
					('logger.conf', '.' ),
					('translations', 'translations' ),
					('userHelp', 'userHelp' ),
					(os.path.join('Windows','appIcon.ico'), 'Windows')
					]

processor_w64 = [
			    (os.path.join('Processors',
				'lep-3.16-win64'),
				os.path.join('Processors',
			    'lep-3.16-win64'))
				]
					
processor_lin64 = [ 	
				  (os.path.join('Processors',
				  'lep-3.16-lin64'),
				  os.path.join('Processors',
			      'lep-3.16-lin64'))
				  ]
					
processor_osx = [	
				(os.path.join('Processors',
				'lep-3.16-osx'),
				os.path.join('Processors',
				'lep-3.16-osx'))
				] 

if platform.startswith('win'):
	data_files_to_add += processor_w64
elif platform.startswith('linux'):
	data_files_to_add += processor_lin64
elif platform.startswith('darwin'):
	data_files_to_add += processor_osx
	
a = Analysis(['lepg.py'],
             pathex=pathex_path,
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
		  icon= os.path.join('Windows', 'appIcon.ico'))

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='lepg')
