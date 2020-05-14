'''
Takes care about reading and saving the program configuration.

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''

from __future__ import annotations
import os
import configparser

#from typing import Optional

class ConfigReaderMeta(type):
    ''' 
    The meta class for the ConfigReader
    
    As the configuration options are used across the whole program
    this was implemented as a singleton to avoid data mismatches.
    '''
    
    _instance: Optional[ConfigReader] = None
    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance

class ConfigReader(metaclass=ConfigReaderMeta):
    '''
    Does all the necessary work to read and save global program configurations. 
    '''
    def __init__(self):
        # Variables and instances used across the class
        self.__configFileNamePath = ""
        self.__language = ""
        self.__preProcDirectory  = ""
        self.__lepDirectory = ""
        self.__preProcPathName = ""
        self.__lepPathName = ""
        self.__parser = configparser.ConfigParser()
        
        # Detect the current application path
        self.__configFilePathName = os.path.join(os.getcwd(), 'configFile.txt')
        
        if os.path.exists(self.__configFilePathName):
            self.readConfigFileContent()
        elif IOError:
            # Just create an empty file
            cfgfile = open(self.__configFilePathName,'w')
            cfgfile.close()
            self.readConfigFileContent()

    def readConfigFileContent(self):
        with open(self.__configFilePathName, 'r+') as openFile:
            self.__parser.read_file(openFile)
            
            if not self.__parser.has_section('Defaults'):
                self.__parser.add_section('Defaults')
            
            try:
                self.__language = self.__parser.get('Defaults','Language')
            except:
                # Value does not exist
                self.__language = "en"
            
            try:
                self.__preProcDirectory = self.__parser.get('Defaults','PreProcDirectory')
            except:
                # Value does not exist
                self.__preProcDirectory = ""
                
            try:
                self.__lepDirectory = self.__parser.get('Defaults','LepDirectory')
            except:
                # Value does not exist
                self.__lepDirectory = ""
                
            try:
                self.__preProcPathName = self.__parser.get('Defaults','PreProcPathName')
            except:
                # Value does not exist
                self.__preProcPathName = ""
                
            try:
                self.__lepPathName = self.__parser.get('Defaults','LepPathName')
            except:
                # Value does not exist
                self.__lepPathName = ""    
                
            openFile.close()
            
    def writeConfigFileContent(self):
        '''
        Write all configuration options in the config file 
    
        Options changed during program execution must be written back with set.. 
        methods prior to write the config file.
        Usually you won't need to call this as every set.. method does 
        trigger immediately a write operation as well.
        '''
        cfgfile = open(self.__configFilePathName,'w')
        self.__parser.set('Defaults','Language',self.__language)
        self.__parser.set('Defaults','PreProcDirectory',self.__preProcDirectory)
        self.__parser.set('Defaults','LepDirectory',self.__lepDirectory)
        self.__parser.set('Defaults','PreProcPathName',self.__preProcPathName)
        self.__parser.set('Defaults','LepPathName',self.__lepPathName)
        self.__parser.write(cfgfile)
        cfgfile.close()
        
        
    def getLanguage(self):
        '''
        Return language info e.g. en
        '''
        return self.__language
    
    def setLanguage(self, param):
        '''
        Set the language info
        
        Keyword arguments:
        param -- language string e.g. en, de
        '''
        self.__language = param
        self.writeConfigFileContent()
    
    def getPreProcDirectory(self):
        return self.__preProcDirectory
    
    def setPreProcDirectory(self, param):    
        self.__preProcDirectory = param
        self.writeConfigFileContent()
        
    def getLepDirectory(self):
        return self.__lepDirectory
    
    def setLepDirectory(self, param):    
        self.__lepDirectory = param
        self.writeConfigFileContent()
        
    def getPreProcPathName(self):
        '''
        Return the path/ and name string for the pre processor
        '''
        return self.__preProcPathName
    
    def setPreProcPathName(self, param): 
        '''
        Sets the path/ and name string for the pre processor 
    
        Keyword arguments:
        param -- full path and name of the pre processor executable
        '''
        self.__preProcPathName = param
        
        # At the same time we set also the path only information        
        directory = os.path.dirname(os.path.abspath(param))
        self.setPreProcDirectory(directory)
        
    def getLepPathName(self):
        '''
        Return the path/ and name string for the lep processor
        '''
        return self.__lepPathName
    
    def setLepPathName(self, param):    
        '''Set the path/ and name string for the lep processor 
            
        Keyword arguments:
        param -- full path and name of the lep processor executable"""
        '''
        self.__lepPathName = param 
        self.writeConfigFileContent()
