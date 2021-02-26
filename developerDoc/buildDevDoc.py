'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import shutil

print()
print('**********************')
print('Building Developer doc')
print('**********************')
print()
print('Removing already existing html files to force a new build...')

dirpath = os.path.dirname(os.path.realpath(__file__))

pathName = os.path.join(dirpath, 'build/doctrees')
if os.path.isdir(pathName):
    shutil.rmtree(pathName)

pathName = os.path.join(dirpath, 'build/html')
if os.path.isdir(pathName):
    shutil.rmtree(pathName)

print()
print('...starting Sphinx...')
pathName = os.path.join(dirpath, 'make.bat html')
os.system(pathName)

print()
print('...done')
print()
