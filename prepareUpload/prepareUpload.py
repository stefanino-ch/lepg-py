'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''

import os

print('*****************************************************')
print('Executing all steps to prepare a complete upload ....')
print('*****************************************************')
print()
answ = input('Update developer doc? [y/ n]')

if answ != 'n':
    os.system('python ../developerDoc/buildDevDoc.py ')
    
print()   
answ = input("Update user help? [y/ n] ")

if answ != 'n':
    os.system('python ../userHelp/buildUserHelp.py ')   
    
# TODO: add code to prepare the complete executable
    