"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
import platform
import subprocess
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from gui.MainWindow import MainWindow

# https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
# https://www.codegrepper.com/code-examples/shell/check+if+i+have+wayland
# https://stackoverflow.com/questions/41198523/sourcing-a-file-to-set-environment-variables-from-within-a-python-script

# Wayland needs special environment setting to run lepg
# Check environment and make sure wayland settings apply if needed

basedir = os.path.dirname(__file__)

match platform.system():
    case 'Windows':
        # Special code to get the appIcon also in the taskbar
        try:
            from ctypes import windll  # Only exists on Windows.
            myappid = "stefanino-ch.gliderrank"
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except ImportError:
            pass
    case 'Linux':
        retVal = subprocess.check_output(['echo $XDG_SESSION_TYPE'], shell=True, text=True)
        if 'wayland' in retVal:
            # os.system('export QT_QPA_PLATFORM="xcb"')
            # os.system('source ./shellSetup.sh')
            os.environ['QT_QPA_PLATFORM'] = "xcb"


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, 'gui', 'elements', 'appIcon.ico')))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
