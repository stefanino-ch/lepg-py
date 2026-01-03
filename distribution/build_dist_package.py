"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
import platform
import re
import shutil
import sys

# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
def read_own_version(path_file):
    ver_str_line = open(path_file, "rt").read()
    ver_str_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(ver_str_re, ver_str_line, re.M)
    if mo:
        verstr = mo.group(1)
        return verstr
    else:
        print("Unable to find ver_str string in %s." % (path_file,))
        sys.exit()

def main():
    curr_path = os.path.dirname(os.path.realpath(__file__))

    print()

    # Setup system dependent stuff
    match platform.uname()[0]:
        case 'Linux':
            print('Linux system detected')
            dist_string = 'lepg-lin'
        case 'Windows':
            print('Windows system detected')
            dist_string = 'lepg-win'
        case _:
            print('Unable to detect OS')
            dist_string = None
            exit(1)

    dist_folder_name = os.path.join(curr_path, dist_string)

    # Remove old dist folder
    print()
    print('Remov old package')
    if os.path.isdir(dist_folder_name):
        shutil.rmtree(dist_folder_name)

    print('Create new package folder')
    os.makedirs(dist_folder_name, exist_ok=True)

        # Execute pyinstaller
    print('Execute pyinstaller')
    os.chdir(curr_path)
    os.system(f'pyinstaller --noconfirm \
                --distpath {dist_folder_name} \
                --clean \
                ../src/lepg.spec')
    # add --windowed to hide console window
    # add --clean to get rid of old stuff

    # setup config file
    print()
    print('Setup config file')
    print('Create package for which branch? ')
    print('s: stable; l: latest')
    answer = input('Default= s ')

    if answer != 'l':
        version = "stable"
        source_path_name_config_file = os.path.join(curr_path, 'stable-configFile.txt')
    else:
        version = "latest"
        source_path_name_config_file = os.path.join(curr_path, 'latest-configFile.txt')

    dest_path_name_config_file = os.path.join(dist_folder_name, 'lepg', 'configFile.txt')
    shutil.copyfile(source_path_name_config_file, dest_path_name_config_file)

    # read current ver_str number
    path_name_version_file = os.path.join(curr_path, '../src/__init__.py')
    version_string = read_own_version(path_name_version_file)

    print()
    print('Create new package...')
    cmd=f'python -m zipfile -c {dist_string}/{dist_string}-V{version_string}-{version}.zip {dist_string}/lepg/.'
    os.system(cmd)

    print()
    print('... cleanup ...')
    clean_path = os.path.join(dist_folder_name, 'lepg')
    if os.path.isdir(clean_path):
        shutil.rmtree(clean_path)

    print('... done')
    print()

if __name__ == '__main__':
    main()