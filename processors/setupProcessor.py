"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
import platform
import shutil
import sys
import zipfile

# Adapt the following variables for processor adaptation
win_src_zip = 'lep-3.17-win64.zip'
win_proc_dir_name = 'lep-3.17-win64'

lin_src_zip = ''
lin_proc_dir_name = ''

osx_src_zip = ''
osx_proc_dir_name = ''

# No changes should be needed below upon version change
proc_src_path_name = ''
proc_tgt_path_name = ''

curr_path = os.path.dirname(os.path.realpath(__file__))

if platform.system() == "Windows":
    proc_src_path_name = os.path.join(curr_path, win_src_zip)
    proc_tgt_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'Processors',
                                      win_proc_dir_name)
elif platform.system() == 'Linux':
    proc_src_path_name = os.path.join(curr_path, lin_src_zip)
    proc_tgt_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'Processors',
                                      lin_proc_dir_name)
elif platform.system() == "Darwin":
    proc_src_path_name = os.path.join(curr_path, osx_src_zip)
    proc_tgt_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'Processors',
                                      osx_proc_dir_name)
else:
    print('OS not supported')
    sys.exit(1)

print('Removing old processor')
print(f'Dir {proc_tgt_path_name}')

if os.path.isdir(proc_tgt_path_name):
    shutil.rmtree(proc_tgt_path_name)

print('Extracting processor')
with zipfile.ZipFile(proc_src_path_name, 'r') as zip_ref:
    zip_ref.extractall(proc_tgt_path_name)
