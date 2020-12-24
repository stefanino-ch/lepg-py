REM Simple script which starts the pyinstaller tool to build an install package.  

REM Stefan Feuz; http://www.laboratoridenvol.com
REM General Public License GNU GPL 3.0

REM *****************
REM Build new package
REM *****************

pyinstaller --noconfirm ^
 			--distpath dist-W64 ^
            ../src/lepg/lepg.spec 
