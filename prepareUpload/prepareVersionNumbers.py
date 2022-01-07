"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
import platform
import re
import sys


# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
def read_own_version(path_file):
    ver_str_line = open(path_file, "rt").read()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(version_regex, ver_str_line, re.M)
    if mo:
        ver_str = mo.group(1)
        return ver_str
    else:
        print("Unable to find ver_str string in %s." % (path_file,))
        sys.exit()


# https://stackoverflow.com/questions/52952905/python-increment-version-number-by-0-0-1
def increment_version(ver_str):
    ver_str = ver_str.split('.')
    ver_str[2] = str(int(ver_str[2]) + 1)
    return '.'.join(ver_str)


# https://stackoverflow.com/questions/57108712/replace-updated-version-strings-in-files-via-python
def update_own_version(path_file, ver):
    version_regex = re.compile(r"(^_*?version_*?\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    
    with open(path_file, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(
            re.sub(
                version_regex,
                lambda match: "{}{}".format(match.group(1), ver),
                content,
            )
        )
        f.truncate()


def update_remote_version(path_file, ver):
    # version_regex = re.compile(r"(latestVersion\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    if platform.system() == "Windows":
        version_regex = re.compile(r"(Latest_Windows_Version\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    elif platform.system() == 'Linux':
        version_regex = re.compile(r"(Latest_Linux_Version\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    elif platform.system() == 'Darwin':
        version_regex = re.compile(r"(Latest_Mac_Version\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    else:
        print('OS not supported')
        version_regex = ''

    with open(path_file, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(
            re.sub(
                version_regex,
                lambda match: "{}{}".format(match.group(1), ver),
                content,
            )
        )
        f.truncate()


print()
curr_path = os.path.dirname(os.path.realpath(__file__))
versFile = os.path.join(curr_path, '../src/__init__.py')
readmeFile = os.path.join(curr_path, '../README.md')

vers = read_own_version(versFile)

print('The current ver_str is: %s' % vers)
print('Update ver_str number? [y/ n]')
answer = input('Default= n ')
if answer == 'y':
    vers = increment_version(vers)
    update_own_version(versFile, vers)

update_remote_version(readmeFile, vers)

print('Version is now: %s' % vers)
print()
