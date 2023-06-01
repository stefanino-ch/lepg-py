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

dirpath = os.path.dirname(os.path.realpath(__file__))

buildPath = os.path.join(dirpath, '_build')
doctreesPath = os.path.join(dirpath, '_build/doctrees')
htmlPath = os.path.join(dirpath, '_build/html')
dirpath = os.path.dirname(os.path.realpath(__file__))
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

print()
print('...starting Sphinx...')
doctreesPath = os.path.join(dirpath, 'make.bat html')
os.system(doctreesPath)

print()
print('...done')
print()
