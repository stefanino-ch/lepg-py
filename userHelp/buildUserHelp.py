'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import shutil

print()
print('******************')
print('Building User help')
print('******************')
print()
print('Removing already existing html files to force a new build...')

dirpath = os.path.dirname(os.path.realpath(__file__))
pathName = os.path.join(dirpath, '_build/doctrees')
srcPath = os.path.join(dirpath, '_build/html')

print('Delete old doc to force a complete build? [y/ n]')
answ = input('Default= n ')

if answ == 'y':
    if os.path.isdir(pathName):
        shutil.rmtree(pathName)
    
    if os.path.isdir(srcPath):
        shutil.rmtree(srcPath)

print()
print('...starting Sphinx...')
pathName = os.path.join(dirpath, 'make.bat html')
os.system(pathName)

print()
print('...removing old help files in source tree...')
tgtPath = os.path.join(dirpath, '../src/userHelp')
if os.path.isdir(tgtPath):
    shutil.rmtree(tgtPath)

print()
print('...copying new files in source tree...')
shutil.copytree(srcPath, tgtPath, ignore=None)

print()
print('...removing unnecessary files...')
tgtFile = os.path.join(dirpath, '../src/userHelp/.buildinfo')
os.remove(tgtFile)

print()
print('...done')
print()
