REM Simple script which starts the document creator and copies the help files 
REM into the correct place within the lepg source tree. 

REM Stefan Feuz; http://www.laboratoridenvol.com
REM General Public License GNU GPL 3.0

REM Remove old help files in _build
rmdir /s /q .\_build\doctrees
rmdir /s /q .\_build\html

REM Start Sphinx
call make.bat html

REM Remove old help files in source tree
rmdir /s /q ..\src\userHelp\

REM Copy new files
xcopy /s /y _build\html\*.* ..\src\userHelp\

REM delete unnecessary files. 
del ..\src\userHelp\.buildinfo
