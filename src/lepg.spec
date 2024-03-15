# -*- mode: python ; coding: utf-8 -*-

# https://www.zacoding.com/en/post/pyinstaller-create-multiple-executables/

from sys import platform
import os

dirpath = os.path.dirname(os.path.abspath("__file__"))
pathex_path = [os.path.join(dirpath, '..','src')]

block_cipher = None

data_files_to_add = [
					('logger.conf', '.' ),
					('translations', 'translations' ),
					('userHelp', 'userHelp' ),
					(os.path.join('gui','elements', 'appIcon.ico'), os.path.join('gui','elements'))
					]

processor_w64 = [
			    (os.path.join('processors',
				'lep-3.23-win64'),
				os.path.join('processors',
			    'lep-3.23-win64'))
				]
					
processor_lin64 = [ 	
				  (os.path.join('processors',
				  'lep-3.23-lin64'),
				  os.path.join('processors',
			      'lep-3.23-lin64'))
				  ]
					
processor_osx = [	
				(os.path.join('processors',
				'lep-3.19-osx'),
				os.path.join('processors',
				'lep-3.19-osx'))
				] 

if platform.startswith('win'):
	data_files_to_add += processor_w64
elif platform.startswith('linux'):
	data_files_to_add += processor_lin64
elif platform.startswith('darwin'):
	data_files_to_add += processor_osx
	
main_a = Analysis(['lepg.py'],
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
             
main_pyz = PYZ(main_a.pure,
               main_a.zipped_data,
               cipher=block_cipher)
          
main_exe = EXE(main_pyz,
               main_a.scripts,
               [],
               exclude_binaries=True,
               name='lepg',
               debug=False,
               bootloader_ignore_signals=False,
               strip=False,
               upx=True,
               console=True,
		       icon= os.path.join('gui', 'elements', 'appIcon.ico'))

#if platform.startswith('win'):
coll = COLLECT(main_exe,
               main_a.binaries,
               main_a.zipfiles,
               main_a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='lepg')

coll = COLLECT(main_exe,
               main_a.binaries,
               main_a.zipfiles,
               main_a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='lepg')
