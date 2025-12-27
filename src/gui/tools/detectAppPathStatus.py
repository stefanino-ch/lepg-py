import os
import sys

def detect_app_path_status():
    # Additional code needed due to pyinstaller.
    # determine if application is a script file or frozen exe
    # https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller#404750
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
        running_mode = 'Frozen/executable'
    else:
        try:
            file_full_path = os.path.realpath(__file__)
            application_path = os.path.dirname(file_full_path)
            running_mode = "Non-interactive (e.g. 'python myapp.py')"
        except NameError:
            application_path = os.getcwd()
            running_mode = 'Interactive'

    application_path = os.path.realpath(os.path.join(application_path, '..', '..'))

    return running_mode, application_path

