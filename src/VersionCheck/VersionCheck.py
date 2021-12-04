'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''

import platform
import requests
import re


class VersionCheck():
    '''
    :class: Connects to the main Github page of the project.
                Searches there for the *latestVersion* and reads the
                version info assigned.
    '''
    # https://stackoverflow.com/questions/14120502/how-to-download-and-write-a-file-from-github-using-requests
    __branchToCheck = ''
    __stableBranch = ('https://raw.githubusercontent.com/stefanino-ch/'
                      'lepg-py/stable/README.md')
    __latestBranch = ('https://raw.githubusercontent.com/stefanino-ch/'
                      'lepg-py/latest/README.md')

    __alreadyConnected__ = False
    ''':attr: is set to true at the moment a request to the remote was
              executed successfully. '''

    __validVersFound__ = False
    ''':attr: is set to true at the moment a version string was found. '''

    __remoteVersion__ = ''
    ''':attr: saves the version string found on the remote page. '''

    __errorInfo__ = ''
    ''':attr: saves the error string in case of problems. '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        self.__branchToCheck = self.__stableBranch

    def __getVersion(self):
        '''
        :method: Executes the request to the remote page, does set the
                 internal variables according to the result.
        '''
        try:
            self.req = requests.get(self.__branchToCheck, timeout=5)

        except requests.ConnectionError as e:
            self.__errorInfo__ = 'Connection Error: %s' % str(e)
        except requests.Timeout as e:
            self.__errorInfo__ = 'Timeout Error: %s' % str(e)
        except requests.RequestException as e:
            self.__errorInfo__ = 'General Error: %s' % str(e)
        except KeyboardInterrupt:
            self.__errorInfo__ = 'Manual abort'
        else:
            if self.req.status_code == 200:
                self.__alreadyConnected__ = True

                remoteVersline = self.req.text

                if platform.system() == "Windows":
                    VSRE = r"Latest_Windows_Version = ['\"]([^'\"]*)['\"]"
                elif platform.system() == ('Linux'):
                    VSRE = r"Latest_Linux_Version = ['\"]([^'\"]*)['\"]"

                mo = re.search(VSRE, remoteVersline)
                if mo:
                    self.__validVersFound__ = True
                    self.__remoteVersion__ = mo.group(1)

    def setBranch(self, branch):
        '''
        :method: Allows to check what branch shall be checked for updates
        :param branch: Name of the branch. Valid names are stable and latest.
        '''
        if branch == 'stable':
            self.__branchToCheck = self.__stableBranch
        else:
            self.__branchToCheck = self.__latestBranch

    def remoteVersionFound(self):
        '''
        :method: Use this to check if there is remote version info available.
        :returns: True if a valid version string was found, False else.
        '''
        if self.__alreadyConnected__ is False:
            self.__getVersion()

        return self.__validVersFound__

    def getRemoteVersion(self):
        '''
        :method: Get the version string from the remote version.
        :returns: The version string if one was found, an empty string else.
        '''
        if self.__alreadyConnected__ is False:
            self.__getVersion()

        return self.__remoteVersion__

    def getErrorInfo(self):
        '''
        :method: In case no remote version info was found you can use this
                 method to get the last error msg.
        :returns: The error msg string if the error could be evaluated, an
                  empty string else if there was no error.
        '''
        return self.__errorInfo__
