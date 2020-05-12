'''
Does all the handling aroung the Pre-Processor  

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
import logging
import platform

from ConfigReader.ConfigReader import ConfigReader
from subprocess import Popen,PIPE

class ProcRunner():
    
    '''
    classdocs
    '''
    __className = 'ProcRunner'

    def __init__(self, procOutW):
        '''
        Constructor
        
        @param procOutW: The instance of the window where the output of the processor shall be written to 
        '''
        self.userInfo = procOutW
        logging.debug(self.__className+'.__init__')
        
    def runPreProc(self):
        '''
        Does all the needed setups to run the processor.
        '''
        logging.debug(self.__className+'.run')
        
        config = ConfigReader()
        
        setPath = 'cd ' + config.getPreProcDirectory()
        cmd = config.getPreProcPathName()
            
        args = [setPath, cmd]
        self.run_command(args)

    
    def run_command(self, cmds):
        '''
        Does finally execute all the commands to run the processor.
        
        @param cmds: A list of commands to be executed
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
            output = process.stdout.readline()
            
            if output == '' and process.poll() is not None:
                self.userInfo.appendText(_('proc_terminating_msg'))
                break
            
            if output:
                logging.debug(self.__className+'.run_command '+ output.strip() )
                self.userInfo.appendText(output.strip())
                
        return
        
        