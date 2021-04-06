'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''

from __future__ import annotations
import os
import configparser

from PyQt5.QtCore import QObject
from Singleton.Singleton import Singleton

class ConfigReader(QObject, metaclass=Singleton):
    '''
    :class: Does all the necessary work to read and save global program configurations. 
    '''
    def __init__(self):
        '''
        :method: Constructor
        '''
        # Variables and instances used across the class
        self.__configFileNamePath = ""
        self.__language = ""
        self.__preProcDirectory  = ""
        self.__lepDirectory = ""
        self.__preProcPathName = ""
        self.__procPathName = ""
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
        '''
        :method: Reads all values from the config file. Does apply hardcoded defaults if a key/ value pair does not exist in the file. 
        ''' 
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
                self.__lepDirectory = self.__parser.get('Defaults','ProcDirectory')
            except:
                # Value does not exist
                self.__lepDirectory = ""
                
            try:
                self.__preProcPathName = self.__parser.get('Defaults','PreProcPathName')
            except:
                # Value does not exist
                self.__preProcPathName = ""
                
            try:
                self.__procPathName = self.__parser.get('Defaults','ProcPathName')
            except:
                # Value does not exist
                self.__procPathName = ""    
                
            openFile.close()
            
    def writeConfigFileContent(self):
        '''
        :method: Write all configuration options in the config file 
    
        Options changed during program execution must be written back with set.. methods prior to write the config file.
        Usually you won't need to call this method, as every set.. method does trigger immediately a write operation as well.
        '''
        cfgfile = open(self.__configFilePathName,'w')
        self.__parser.set('Defaults','Language',self.__language)
        self.__parser.set('Defaults','PreProcDirectory',self.__preProcDirectory)
        self.__parser.set('Defaults','ProcDirectory',self.__lepDirectory)
        self.__parser.set('Defaults','PreProcPathName',self.__preProcPathName)
        self.__parser.set('Defaults','ProcPathName',self.__procPathName)
        self.__parser.write(cfgfile)
        cfgfile.close()
        
        
    def getLanguage(self):
        '''
        :method: Returns language info e.g. en
        '''
        return self.__language
    
    def setLanguage(self, lang):
        '''
        :method: Set the language info
        :param lang: language string e.g. en, de
        '''
        self.__language = lang
        self.writeConfigFileContent()
    
    def getPreProcDirectory(self):
        '''
        :method: Returns the directory where the PreProcecssor resides
        '''
        return self.__preProcDirectory
    
    def setPreProcDirectory(self, param):
        '''
        :method: Set the PreProcessor directory
        :param lang: Directory string
        '''    
        self.__preProcDirectory = param
        self.writeConfigFileContent()
        
    def getProcDirectory(self):
        '''
        :method: Returns the directory where the Procecssor resides
        '''
        return self.__lepDirectory
    
    def setProcDirectory(self, param): 
        '''
        :method: Set the Processor directory
        :param lang: Directory string
        '''   
        self.__lepDirectory = param
        self.writeConfigFileContent()
        
    def getPreProcPathName(self):
        '''
        :method: Return the path/ and name string for the PreProcessor
        '''
        return self.__preProcPathName
    
    def setPreProcPathName(self, param): 
        '''
        :method: Sets the path/ and name string for the pre processor 
        :param param: Full path and name of the pre processor executable
        '''
        self.__preProcPathName = param
        
        # At the same time we set also the path only information        
        directory = os.path.dirname(os.path.abspath(param))
        self.setPreProcDirectory(directory)
        
    def getProcPathName(self):
        '''
        :method: Return the path/ and name string for the Processor
        '''
        return self.__procPathName
    
    def setProcPathName(self, param):    
        '''
        :method: Set the path/ and name string for the lep processor 
        :param param: Full path and name of the Processor executable
        '''
        self.__procPathName = param 
        
        # At the same time we set also the path only information        
        directory = os.path.dirname(os.path.abspath(param))
        self.setProcDirectory(directory)
