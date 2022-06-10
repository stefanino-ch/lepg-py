"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
import platform
import subprocess
import sys

from PyQt5.QtWidgets import QApplication

from gui.MainWindow import MainWindow

# https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
# https://www.codegrepper.com/code-examples/shell/check+if+i+have+wayland
# https://stackoverflow.com/questions/41198523/sourcing-a-file-to-set-environment-variables-from-within-a-python-script

# Wayland needs special environment setting to run lepg
# Check environment an make sure wayland settings apply if needed

if platform.system() == 'Linux':
    retVal = subprocess.check_output(['echo $XDG_SESSION_TYPE'], shell=True, text=True)
    if 'wayland' in retVal:
        # os.system('export QT_QPA_PLATFORM="xcb"')
        # os.system('source ./shellSetup.sh')
        os.environ['QT_QPA_PLATFORM'] = "xcb"


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
