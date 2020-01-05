'''
Central place where the data status will be tracked. 

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import QObject, pyqtSignal

from Singleton.Singleton import Singleton

class DataWindowStatus(QObject, metaclass=Singleton):
    '''
    Central place where the data status will be tracked.

    Class is implemented as a Singleton. Even if it is instantiated multiple times
    all data will be the same for all instances. 
    
    @signal dataStatusUpdate :  sent out as soon a data or window status changes
                                A string indicates either
                                    - the window name 
                                    - the PreProc file
                                    - the LepFile 
                                status has changed.  
    '''
    statusUpdated = pyqtSignal(str)
   
    # 1 means data has been applied or saved
    
    # List of all windows taken care of
    __windowDataStatus ={
        'PreProcDataEdit' : '1' ,
    }
    
    # List of all files taken care of
    __fileDataStatus ={
        'PreProcFile' :  '1' ,
        'LepFile' : '1'
    }
    
    __instanciatedWindowList ={}

    def __init__(self):
        logging.debug('DataWindowStatus.__init__')
        super().__init__()
    
    def registerSignal(self, signal):
        print('registerSignal')
        signal.connect(self.signalReceived)
    
    def unregisterSignal(self, signal):
        signal.disconnect(self.signalReceived)
    
    def signalReceived(self, name, action):
        # File actions
        if action == 'Open':
            if name == 'PreProcessorStore':
                self.__fileDataStatus['PreProcFile'] = 1 
                self.statusUpdated.emit('PreProcFile')
                                
                self.__windowDataStatus['PreProcDataEdit'] = 1
                self.statusUpdated.emit('PreProcDataEdit')
            else: 
                logging.error('DataWindowStatus.signalReceived Open: unknown name ' + name)
                
        elif action == 'Save':
            if name == 'PreProcessorStore':
                self.__fileDataStatus['PreProcFile'] = 1 
                self.statusUpdated.emit('PreProcFile')                
            else: 
                logging.error('DataWindowStatus.signalReceived Save: unknown name ' + name)
        
        # Edit actions
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
        
    def getFileStatus(self, name):
        return self.__fileDataStatus.get(name)
        
    def windowExists(self, window):
        '''
        Checks if a window has already been instanciated. 
        
        @param window: Name of the window to check for it's existence
        @return: True/ False: depending on window has been registered/ unregistered
        '''
        if window in self.__instanciatedWindowList:
            return self.__instanciatedWindowList.get(window)
        else:
            return False
    
    def registerWindow(self, window):
        '''
        Windows which are instanciated shall be registered here. This is part of the work to avoid 
        multiple windows of the same name are open. 
        
        @param window: window name to be register
        '''
        self.__instanciatedWindowList[window] = True
        
    def unregisterWindow(self, window):
        '''
        Windows which are closed shall be unregistered here. This is part of the work to avoid 
        multiple windows of the same name are open. 
        
        @param window: window name to be unregistered
        '''
        if window in self.__instanciatedWindowList:
            self.__instanciatedWindowList[window] = False
