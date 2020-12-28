REM Simple script which starts the document creator and copies the help files 
REM into the correct place within the lepg source tree. 

REM Stefan Feuz; http://www.laboratoridenvol.com
REM General Public License GNU GPL 3.0

REM Remove already existing html files to force a new build
rmdir /s /q .\build\doctrees
rmdir /s /q .\build\html

REM Start Sphinx
call make.bat html
