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
pathName = os.path.join(dirpath, 'dist-W64/')
if os.path.isdir(pathName):
    shutil.rmtree(pathName)
    
# create dist-W64 directory
os.makedirs(pathName, exist_ok=True)

print('Executing pyinstaller')
# execName = os.path.join(dirpath, 'pyinstaller --noconfirm \
                                     # --distpath dist-W64 \
                                    # ../src/lepg.spec')
# os.system(execName)
print(dirpath)
os.chdir(dirpath)
os.system('pyinstaller --noconfirm \
            --distpath dist-W64 \
            ../src/lepg.spec')

# reading current version number
versFile = os.path.join(dirpath, '../src/__init__.py')
vers = readOwnVersion(versFile)

print('Creating new package')
os.system('python -m zipfile -c dist-W64/lepg-W64-V'+vers+'.zip dist-W64/lepg/')
print('done')
print()