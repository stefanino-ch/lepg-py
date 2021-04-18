'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''

import requests
import re

class VersionCheck():
    '''
    :class: Connects to the main Github page of the project. 
                Searches there for the *latestVersion* and reads the version info assigned.
    '''
    
    __alreadyConnected__ = False
    ''':attr: is set to true at the moment a request to the remote was executed successfully. '''
    
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
        pass
    
    def __getVersion(self):
        '''
        :method: Executes the request to the remote page, does set the internal variables according to the result. 
        '''
        try:
            self.req = requests.get('https://github.com/stefanino-ch/updateTester', timeout=5)
            
        except requests.ConnectionError as e:
            self.__errorInfo__ = 'Connection Error: %s' %(str(e))
        except requests.Timeout as e:
            self.__errorInfo__ = 'Timeout Error: %s' %(str(e))
        except requests.RequestException as e:
            self.__errorInfo__ = 'General Error: %s' %(str(e))
        except KeyboardInterrupt:
            self.__errorInfo__ = 'Manual abort'
        else:
            if self.req.status_code == 200:
                self.__alreadyConnected__ = True
                
                remoteVersline = self.req.text
                VSRE = r"latestVersion = ['\"]([^'\"]*)['\"]"
                mo = re.search(VSRE, remoteVersline)
                if mo:
                    self.__validVersFound__ = True
                    self.__remoteVersion__ = mo.group(1) 

    
    def remoteVersionFound(self):
        '''
        :method: Use this to check if there is remote version info available. 
        :returns: True if a valid version string was found, False else.
        '''
        if self.__alreadyConnected__ == False:
            self.__getVersion()

        return self.__validVersFound__
        
         
    def getRemoteVersion(self):
        '''
        :method: Get the version string from the remote version. 
        :returns: The version string if one was found, an empty string else.  
        '''
        if self.__alreadyConnected__ == False:
            self.__getVersion()

        return self.__remoteVersion__
        
    def getErrorInfo(self):
        '''
        :method: In case no remote version info was found you can use this method to get the last error msg.  
        :returns: The error msg string if the error could be evaluated, an empty string else if there was no error.  
        '''
        return self.__errorInfo__
    