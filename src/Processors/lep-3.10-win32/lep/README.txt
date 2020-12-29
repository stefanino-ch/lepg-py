LEparagliding-3.10
(2020-05-02)

Compiled using cygwin in a Windows 10 64bit with AMD processor (still not tested using Intel x64):
(wiht only some warnings messages)

gfortran -std=legacy leparagliding.f

If you don't have Cygwin with fortran compilers (gfortran, f77, fort77, ...),
then use the following dll's in same folder as lep-3.10-win64.exe:

cygwin1.dll
cyggcc_s-seh-1.dll
cyggfortran-3.dll
cygquadmath-0.dll

If you have compiled the code yourself, then remove all the dll's
