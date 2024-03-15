'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import shutil

import platform

print()
print('******************')
print('Building User help')
print('******************')
print()
print('Removing already existing html files to force a new build...')

dirpath = os.path.dirname(os.path.realpath(__file__))

buildPath = os.path.join(dirpath, '_build')
doctreesPath = os.path.join(dirpath, '_build/doctrees')
htmlPath = os.path.join(dirpath, '_build/html')
staticPath = os.path.join(dirpath, 'source/_static')


print('Delete old doc to force a complete build? [y/ n]')
answ = input('Default= n ')

if answ == 'y':
    if os.path.isdir(doctreesPath):
        shutil.rmtree(doctreesPath)
    
    if os.path.isdir(htmlPath):
        shutil.rmtree(htmlPath)

# Check if _static dir ist there
if not os.path.isdir(staticPath):
    os.mkdir(staticPath)

# Check if _build dir ist there
if not os.path.isdir(buildPath):
    os.mkdir(buildPath)

# Check if _build/html dir ist there
if not os.path.isdir(htmlPath):
    os.mkdir(htmlPath)

print()
print('...starting Sphinx...')
if platform.system() == "Windows":
    doctreesPath = os.path.join(dirpath, 'make.bat html')
    os.system(doctreesPath)
elif platform.system() == 'Linux'\
        or platform.system() == 'Darwin':
    os.chdir(dirpath)
    os.system('python ./make.py')

else:
    print('OS not supported currently.')
    exit(1)

print()
print('...removing old help files in source tree...')
tgtPath = os.path.join(dirpath, '../src/userHelp')
if os.path.isdir(tgtPath):
    shutil.rmtree(tgtPath)

print()
print('...copying new files in source tree...')
shutil.copytree(htmlPath, tgtPath, ignore=None)

print('\nUpdate github.pages tree? [y/ n]')
answ = input('Default= n ')

if answ == 'y':
    print('...removing old help files in github.pages tree...')
    tgtPath = os.path.join(dirpath, '../docs')
    if os.path.isdir(tgtPath):
        shutil.rmtree(tgtPath)

    print()
    print('...copying new files in github.pages tree...')
    shutil.copytree(htmlPath, tgtPath, ignore=None)

print()
print('...removing unnecessary files...')
tgtFile = os.path.join(dirpath, '../src/userHelp/.buildinfo')
if os.path.isfile(tgtFile):
    os.remove(tgtFile)

print()
print('...done')
print()
