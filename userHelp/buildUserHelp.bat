REM Simple script which starts the document creator and copies the help files 
REM into the correct place within the lepg source tree. 

REM Stefan Feuz; http://www.laboratoridenvol.com
REM General Public License GNU GPL 3.0

foliant make site

xcopy /s /y userHelp.mkdocs ..\src\lepg\userHelp\