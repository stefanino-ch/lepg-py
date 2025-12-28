"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

import os
import webbrowser

from gui.tools.detectAppPathStatus import detect_app_path_status
from gui.tools.detectLanguage import detect_language

def open_user_help_file(file_path_name):
    bundle_dir = os.path.join(detect_app_path_status()[1])
    system_language = detect_language()

    # Check if there are user help files for the detected language
    lang_path = os.path.join(bundle_dir, 'userHelp', system_language)
    if not os.path.isdir(lang_path):
        # There seems to be no help in the current lang.
        # Fallback to the default index.html file
        file_path_name = 'index.html'

    if file_path_name == 'index.html':
        webbrowser.open('file://'
                        + os.path.realpath(os.path.join(bundle_dir,
                                                        'userHelp',
                                                        file_path_name)))
    else:
        webbrowser.open('file://'
                        + os.path.realpath(os.path.join(bundle_dir,
                                                        'userHelp',
                                                        detect_language(),
                                                        file_path_name)))