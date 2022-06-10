#!/bin/bash
# Replace all NaN (Not a Number) by 0.0 in a Fortran generated DXF file
# 2021-10-30
#
# If your DXF file cannot be opened with Autocad,
# try to repair the DXF file by replacing all NaNs (not a number) with 0.0.
# It can be done with any text editor.
# The noNaN.sh script does this in a more elegant and faster way: ./noNaN.sh 
#
# Si votre fichier DXF ne peut pas être ouvert avec Autocad, 
# essayez de réparer le fichier DXF en remplaçant tous les NaN (pas un nombre) par 0.0. 
# Cela peut être fait avec n'importe quel éditeur de texte. 
# Le script noNaN.sh fait cela de manière plus élégante et plus rapide : ./noNaN.sh

sed -i 's/NaN/0.0/g' leparagliding.dxf
