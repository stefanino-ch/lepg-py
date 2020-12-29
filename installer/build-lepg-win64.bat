REM Simple script which starts the pyinstaller tool to build an install package.  

REM Stefan Feuz; http://www.laboratoridenvol.com
REM General Public License GNU GPL 3.0

REM *****************
REM Build new package
REM *****************
pyinstaller --noconfirm ^
 			--distpath dist-W64 ^
            ../src/lepg.spec 


REM *****************
REM zip it
REM *****************

REM Remove old archive
del %cd%\dist-W64\lepg-w64.*

REM Create new archives
"%ProgramFiles%\7-Zip\7z.exe" a -v20m -tzip %cd%/dist-W64/lepg-w64.zip  %cd%/dist-W64/lepg
