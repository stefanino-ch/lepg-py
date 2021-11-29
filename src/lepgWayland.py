import os
import subprocess

# https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
# https://www.codegrepper.com/code-examples/shell/check+if+i+have+wayland
# https://stackoverflow.com/questions/41198523/sourcing-a-file-to-set-environment-variables-from-within-a-python-script

# Wayland needs special environment setting to run lepg
# Check environment an make sure wayland settings apply if needed

retVal = subprocess.check_output(['echo $XDG_SESSION_TYPE'], shell=True, text=True)
if 'wayland' in retVal:
    # os.system('export QT_QPA_PLATFORM="xcb"')
    # os.system('source ./shellSetup.sh')
    os.environ['QT_QPA_PLATFORM'] = "xcb"

os.system('./lepg')



