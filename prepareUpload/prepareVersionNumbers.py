'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import platform
import re
import sys

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
    
# https://stackoverflow.com/questions/52952905/python-increment-version-number-by-0-0-1
def incrementVersion(ver):
    ver = ver.split('.')
    ver[2] = str(int(ver[2]) + 1)
    return '.'.join(ver)

# https://stackoverflow.com/questions/57108712/replace-updated-version-strings-in-files-via-python
def updateOwnVersion(pathFile, ver):
    version_regex = re.compile(r"(^_*?version_*?\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    
    with open(pathFile, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(
            re.sub(
                version_regex,
                lambda match: "{}{}".format(match.group(1), ver),
                content,
            )
        )
        f.truncate()
        
def updateRemoteVersion(pathFile, ver):
    # version_regex = re.compile(r"(latestVersion\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    if platform.system() == "Windows":
        version_regex = re.compile(r"(Latest_Windows_Version\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    elif platform.system() == ('Linux'):
        version_regex = re.compile(r"(Latest_Linux_Version\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    with open(pathFile, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(
            re.sub(
                version_regex,
                lambda match: "{}{}".format(match.group(1), ver),
                content,
            )
        )
        f.truncate()

print()
dirpath = os.path.dirname(os.path.realpath(__file__))
versFile = os.path.join(dirpath, '../src/__init__.py')
readmeFile = os.path.join(dirpath, '../README.md')

vers = readOwnVersion(versFile)

print('The current version is: %s' %(vers))   
print('Update version number? [y/ n]')
answ = input('Default= n ')
if answ == 'y':
    vers = incrementVersion(vers)
    updateOwnVersion(versFile, vers)

updateRemoteVersion(readmeFile, vers)

print('Version is now: %s' %(vers))
print()
