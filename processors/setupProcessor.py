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
win_src_zip = 'lep-3.19-win64.zip'
win_proc_dir_name = 'lep-3.19-win64'

lin_src_zip = 'lep-3.19-lin64.zip'
lin_proc_dir_name = 'lep-3.19-lin64'

osx_src_zip = 'lep-3.17-osx.zip'
osx_proc_dir_name = 'lep-3.17-osx'
osx_pre_dir_name = 'pre1.6'
osx_lep_dir_name = 'lep'


# No changes should be needed below upon version change
proc_src_path_name = ''
proc_tgt_path_name = ''

curr_path = os.path.dirname(os.path.realpath(__file__))

if platform.system() == "Windows":
    proc_src_path_name = os.path.join(curr_path, win_src_zip)
    proc_del_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'processors',
                                      win_proc_dir_name)
    proc_zip_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'processors')
elif platform.system() == 'Linux':
    proc_src_path_name = os.path.join(curr_path, lin_src_zip)
    proc_del_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'processors',
                                      lin_proc_dir_name)
    proc_zip_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'processors')

elif platform.system() == "Darwin":
    proc_src_path_name = os.path.join(curr_path, osx_src_zip)
    proc_del_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'processors',
                                      osx_proc_dir_name)
    proc_zip_path_name = os.path.join(curr_path, '..',
                                      'src',
                                      'processors')
    pre_path_name = os.path.join(curr_path, '..',
                                 'src',
                                 'processors',
                                 osx_proc_dir_name,
                                 osx_pre_dir_name)
    lep_path_name = os.path.join(curr_path, '..',
                                 'src',
                                 'processors',
                                 osx_proc_dir_name,
                                 osx_lep_dir_name)
else:
    print('OS not supported')
    sys.exit(1)
print()
print('Removing old processor in %s ...' % proc_del_path_name)

if os.path.isdir(proc_del_path_name):
    shutil.rmtree(proc_del_path_name)

print()
print('... extracting new processor ...')
with zipfile.ZipFile(proc_src_path_name, 'r') as zip_ref:
    zip_ref.extractall(proc_zip_path_name)

if platform.system() == "Darwin":
    print()
    print('... deleting old .o and .out files ...')

    for path in [pre_path_name, lep_path_name]:
        print('... %s ...' % path)
        files = os.listdir(path)
        for item in files:
            if item.endswith(".o") \
                    or item.endswith(".out"):
                os.remove(os.path.join(path, item))

    print()
    print('... copy processor setup script ...')
    script_src_path_name = os.path.join(curr_path, 'lepPrepare.command')
    script_tgt_path_name = os.path.join(curr_path, '..',
                                        'src',
                                        'processors',
                                        osx_proc_dir_name,
                                        'lepPrepare.command')

    shutil.copyfile(script_src_path_name, script_tgt_path_name)

    print()
    print('... make the script executable ...')
    os.chmod(script_tgt_path_name, 0o744)

print()
print('... done')
