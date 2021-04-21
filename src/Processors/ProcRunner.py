'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
import os
import platform

from ConfigReader.ConfigReader import ConfigReader
from subprocess import Popen,PIPE

class ProcRunner():
    '''
    :class: Does take care about the data handling for the executables for processing. 
    '''
    __className = 'ProcRunner'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    
    def __init__(self, procOutW):
        '''
        :method: Constructor
        :param procOutW: The instance of the window where the output of the processor shall be written to
        '''
        logging.debug(self.__className+'.__init__')
        
        self.userInfo = procOutW
        self.confR = ConfigReader()
        
        
    def runPreProc(self):
        '''
        :method: Does all the needed setups to run the pre processor.
        '''
        logging.debug(self.__className+'.runPreProc')
        
        setPath = 'cd ' + self.confR.getPreProcDirectory()
        cmd = self.confR.getPreProcPathName()
            
        args = [setPath, cmd]
        self.run_command(args)
        
    def preProcConfigured(self):
        '''
        :method: Checks if 
                    - the configured pre proc path name string is >0 chars
                    - the file the configured proc path name points really to a file
        :returns: True if both checks above are valid, False else
        ''' 
        logging.debug(self.__className+'.preProcConfigured')
        
        pathName = self.confR.getPreProcPathName()
        
        if len(pathName) > 0:
            if os.path.isfile(pathName) == True:
                return True
            else:
                return False
        else:
            return False

    def runProc(self):
        '''
        :method: Does all the needed setups to run the processor.
        '''
        logging.debug(self.__className+'.runProc')
        
        setPath = 'cd ' + self.confR.getProcDirectory()
        cmd = self.confR.getProcPathName()
            
        args = [setPath, cmd]
        self.run_command(args)
        
    def procConfigured(self):
        '''
        :method: Checks if 
                    - the configured proc path name string is >0 chars
                    - the file the configured proc path name points really to a file
        :returns: True if both checks above are valid, False else
        ''' 
        logging.debug(self.__className+'.procConfigured')
        
        pathName = self.confR.getProcPathName()
        
        if len(pathName) > 0:
            if os.path.isfile(pathName) == True:
                return True
            else:
                return False
        else:
            return False
    
    def run_command(self, cmds):
        '''
        :method: Does finally execute all the commands to run the processor.
        :param cmds: A list of commands to be executed
        '''
        
        for cmd in cmds:
            logging.debug(self.__className+'.run_command '+ cmd )
                
        # TODO: add here other OS as needed
        if platform.system() == "Windows":
            process = Popen('cmd.exe', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False, encoding='utf8')
        elif platform.system() == "Linux":
            # TODO: Fully test Linux option
            process = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False, encoding='utf8')
        else:
            logging.error("Sorry, your operating system is not supported yet")
            return
            
        for cmd in cmds:
            process.stdin.write(cmd + "\n")
        process.stdin.close()
        
        while True:
            output = process.stdout.readline() + process.stderr.readline()
            
            if output == '' and process.poll() is not None:
                self.userInfo.appendText(_('proc_terminating_msg'))
                break
            
            if output:
                logging.debug(self.__className+'.run_command '+ output.strip() )
                self.userInfo.appendText(output.strip())
                
        return
        
        
