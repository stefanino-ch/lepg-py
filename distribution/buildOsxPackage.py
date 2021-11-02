'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import re
import shutil

# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
def readOwnVersion(pathFile):
    verstrline = open(pathFile, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
        return(verstr)
    else:
        print("Unable to find version string in %s." % (pathFile,))
        sys.exit()

print()

dirpath = os.path.dirname(os.path.realpath(__file__))

print('Removing old packages')
pathName = os.path.join(dirpath, 'dist-osx/')
if os.path.isdir(pathName):
    shutil.rmtree(pathName)

# create dist-osx directory
os.makedirs(pathName, exist_ok=True)

print('Executing pyinstaller')

os.chdir(dirpath)
os.system('pyinstaller --noconfirm \
            --distpath dist-osx \
            --clean \
            ../src/lepg.spec')

# os.system('pyinstaller --noconfirm \
            # --distpath dist-Lin64 \
            # --clean \
            # ../src/lepg.spec')

# reading current version number
versFile = os.path.join(dirpath, '../src/__init__.py')
vers = readOwnVersion(versFile)

# setup config file
destPathName = os.path.join(dirpath, 'dist-osx/lepg/configFile.txt')

print()
print('Setup config file')
print('Create package for which branch? ')
print('s: stable; l: latest')
answ = input('Default= s ')

if answ != 'l':
    version = "stable"
    sourcePathName = os.path.join(dirpath, 'stable-configFile.txt')
else:
    version = "latest"
    sourcePathName = os.path.join(dirpath, 'latest-configFile.txt')


shutil.copyfile(sourcePathName, destPathName)
print()
print('Creating new package')
os.system('python -m zipfile -c dist-osx/lepg-osx-V'+vers+'-'+version+'.zip dist-osx/lepg/')
print('done')
print()
