'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import platform

print('*****************************************************')
print('Executing all steps to prepare a complete upload ....')
print('*****************************************************')
print()
print('*****************************************************')
print('Update developer doc? [y/ n]')
answ = input('Default= y ')

if answ != 'n':
    os.system('python ../developerDoc/buildDevDoc.py')
    

print()
print('*****************************************************')
print('Update user help? [y/ n]')
answ = input('Default= y ')

if answ != 'n':
    os.system('python ../userHelp/buildUserHelp.py')  
    
print()
print('*****************************************************')
print('Update version number? [y/ n]')
answ = input('Default= n ')

if answ == 'y':
    os.system('python ./prepareVersionNumbers.py')

print()
print('*****************************************************')
print('Create new installer package? [y/ n]')
answ = input('Default= n ')

if answ == 'y':
    if platform.system() == "Windows":
        os.system('python ../distribution/buildW64Package.py')
    elif platform.system() == ('Linux'):
        os.system('python ../distribution/buildLinuxPackage.py')
    else:
        print('OS not supported currently.')