'''


@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import QObject, pyqtSignal

from Singleton.Singleton import Singleton

class DataWindowStatus(QObject, metaclass=Singleton):
    statusUpdated = pyqtSignal(str)
   
    # means data has been applied or saved
    __windowDataStatus ={
        'PreProcDataEdit' : '1' ,
    }
    
    __fileDataStatus ={
        'PreProcFile' :  '1' ,
        'LepFile' : '1'
    }
    
    __windowList ={}

    def __init__(self):
        logging.debug('DataWindowStatus.__init__')
        super().__init__()
    
    def registerSignal(self, signal):
        print('registerSignal')
        signal.connect(self.signalReceived)
    
    def unregisterSignal(self, signal):
        signal.disconnect(self.signalReceived)
    
    def signalReceived(self, name, action):
        if name in self.__fileDataStatus:
            if action == 'Open':
                self.__fileDataStatus[name] = 1
                self.__windowDataStatus['PreProcDataEdit'] = 1
            elif action == 'Save':
                self.__fileDataStatus[name] = 1
        
        if name in self.__windowDataStatus:
            if action == 'edit':
                self.__windowDataStatus[name] = 0
                self.statusUpdated.emit(name)
            
            elif action == 'Apply':
                self.__windowDataStatus[name] = 1
                self.statusUpdated.emit(name)
                
                # As we have written to the file we must update the status accordingly
                if name == 'PreProcDataEdit':
                    self.__fileDataStatus['PreProcFile'] = 0
                    self.statusUpdated.emit('PreProcFile')
                else: 
                    self.__fileDataStatus['LepFile'] = 0
                    self.statusUpdated.emit('LepFile')
            
            elif action == 'Ok':
                self.__windowDataStatus[name] = 1
                self.statusUpdated.emit(name)
                
                # As we have written to the file we must update the status accordingly
                if name == 'PreProcDataEdit':
                    self.__fileDataStatus['PreProcFile'] = 0
                    self.statusUpdated.emit('PreProcFile')
                else:
                    self.__fileDataStatus['LepFile'] = 0
                    self.statusUpdated.emit('LepFile')
            
            elif action == 'Cancel':
                self.__windowDataStatus[name] = 1
                self.statusUpdated.emit(name)
        
    def getWindowDataStatus(self, name):
        return self.__windowDataStatus.get(name)
    
    def getWindowDataStatusChar(self, name):
        if self.__windowDataStatus.get(name) == 0:
            return('C')
        else:
            return('S')
        
    def windowExists(self, window):
        if window in self.__windowList:
            return self.__windowList.get(window)
        else:
            return False
    
    def registerWindow(self, window):
        self.__windowList[window] = True
        
    def unregisterWindow(self, window):
        if window in self.__windowList:
            self.__windowList[window] = False
