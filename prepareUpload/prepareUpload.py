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
answ = input('Default= n ')

if answ == 'y':
    os.system('python ../developerDoc/buildDevDoc.py')
    

print()
print('*****************************************************')
print('Update user help? [y/ n]')
answ = input('Default= y ')

if answ != 'n':
    os.system('python ../userHelp/buildUserHelp.py')  


print()
print('*****************************************************')
print('Reset processor directory? [y/ n]')
answ = input('Default= y ')

if answ != 'n':
    os.system('python ../processors/setupProcessor.py')


print()
print('*****************************************************')
print('Setup version number')
os.system('python ./prepareVersionNumbers.py')


print()
print('*****************************************************')
print('Create new installer package? [y/ n]')
answ = input('Default= n ')

if answ == 'y':
    if platform.system() == "Windows":
        os.system('python ../distribution/build_win64_package.py')
    elif platform.system() == ('Linux'):
        os.system('python ../distribution/build_lin_package.py')
    elif platform.system() == ('Darwin'):
        os.system('python ../distribution/build_osx_package.py')
    else:
        print('OS not supported currently.')

print()