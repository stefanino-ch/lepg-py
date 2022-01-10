"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
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


print()

curr_path = os.path.dirname(os.path.realpath(__file__))

print('Removing old packages')
pathName = os.path.join(curr_path, 'dist-osx/')
if os.path.isdir(pathName):
    shutil.rmtree(pathName)

# create dist-osx directory
os.makedirs(pathName, exist_ok=True)

print('Executing pyinstaller')

os.chdir(curr_path)
os.system('pyinstaller --noconfirm \
            --distpath dist-osx \
            --clean \
            ../src/lepg.spec')

# os.system('pyinstaller --noconfirm \
#           --distpath dist-Lin64 \
#            --clean \
#            ../src/lepg.spec')

# reading current ver_str number
vers_file = os.path.join(curr_path, '../src/__init__.py')
vers = read_own_version(vers_file)

# setup config file
dest_path_name = os.path.join(curr_path, 'dist-osx/lepg/configFile.txt')

print()
print('Setup config file')
print('Create package for which branch? ')
print('s: stable; l: latest')
answ = input('Default= s ')

if answ != 'l':
    version = "stable"
    sourcePathName = os.path.join(curr_path, 'stable-configFile.txt')
else:
    version = "latest"
    sourcePathName = os.path.join(curr_path, 'latest-configFile.txt')

shutil.copyfile(sourcePathName, dest_path_name)

print()
print('Creating new package')
os.system('python -m zipfile -c dist-osx/lepg-osx-V'
          + vers
          + '-'
          + version
          + '.zip dist-osx/lepg/')

print()
print('Cleanup')
os.system('rm -rf dist-osx/lepg/')

print('done')
print()