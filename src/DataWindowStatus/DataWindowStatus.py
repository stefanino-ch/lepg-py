'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import QObject, pyqtSignal

from Singleton.Singleton import Singleton

class DataWindowStatus(QObject, metaclass=Singleton):
    '''
    :class: Central place where the data status will be tracked.

    Class is implemented as a **Singleton**. Even if it is instantiated multiple times all data will be the same for all instances. 
    
      
    '''
    statusUpdated = pyqtSignal(str)
    '''
    :signal:  sent out as soon a data or window status changes
                A string indicates either
                - the window name 
                - the PreProc file
                - the ProcFile 
                status has changed.
                **1** means data has been applied or saved
    '''
    
    __windowDataStatus ={
        'PreProcDataEdit' : '1' ,
        'WingOutlineViewer' : '1',
        'ProcBasicData' : '1',
        'ProcGeometry' : '1',
        'ProcAirfoils' : '1'
    }
    '''
    :attr: List of all windows taken care of
    '''
    
    __fileDataStatus ={
        'PreProcFile' :  '1' ,
        'ProcFile' : '1'
    }
    '''
    :attr: List of all files taken care of
    '''
    
    __instanciatedWindowList ={}
    '''
    :attr: Helps to remember which windows have already been opened before
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug('DataWindowStatus.__init__')
        super().__init__()
    
    def registerSignal(self, signal):
        '''
        :method: Each new sender must been registered first.
        '''
        signal.connect(self.signalReceived)
    
    def unregisterSignal(self, signal):
        '''
        :method: At the moment a sender does not exist anymore: unregister also its signal
        '''
        signal.disconnect(self.signalReceived)
    
    def signalReceived(self, name, action):
        '''
        :method: Called at the moment a signal was received. Does all the signal handling.
        :param name: Name of the signal emitter
        :param action: The action which is reported by the emitter
        '''
        # File actions
        if action == 'Open':
            if name == 'PreProcessorStore':
                self.__fileDataStatus['PreProcFile'] = 1 
                self.statusUpdated.emit('PreProcFile')
                                
                self.__windowDataStatus['PreProcDataEdit'] = 1
                self.statusUpdated.emit('PreProcDataEdit')
            if name == 'ProcessorStore':
                self.__fileDataStatus['ProcFile'] = 1 
                self.statusUpdated.emit('ProcFile')
                                
                self.__windowDataStatus['ProcDataEdit'] = 1
                self.statusUpdated.emit('ProcDataEdit')
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
                self.__fileDataStatus['ProcFile'] = 0
                self.statusUpdated.emit('ProcFile')
        
        elif action == 'Ok':
            self.__windowDataStatus[name] = 1
            self.statusUpdated.emit(name)
            
            # As we have written to the file we must update the status accordingly
            if name == 'PreProcDataEdit':
                self.__fileDataStatus['PreProcFile'] = 0
                self.statusUpdated.emit('PreProcFile')
            else:
                self.__fileDataStatus['ProcFile'] = 0
                self.statusUpdated.emit('ProcFile')
        
        elif action == 'Cancel':
            self.__windowDataStatus[name] = 1
            self.statusUpdated.emit(name)
        
    def getWindowDataStatus(self, name):
        '''
        :method: Ask for the status of a specific window.
        :returns: **0** if the window contains data which has not yet been applied. **1** if a apply was pressed and and no values has been changed since then.
        '''
        return self.__windowDataStatus.get(name)
    
    def getWindowDataStatusChar(self, name):
        '''
        :method: Ask for the status of a specific window.
        :returns: **C** if the window contains data which has not yet been applied. **S** if a apply was pressed and and no values has been changed since then.
        '''
        if self.__windowDataStatus.get(name) == 0:
            return('C')
        else:
            return('S')
        
    def getFileStatus(self, name):
        '''
        :method: Ask for the status of a specific file.
        :returns: **0** if a file has been Changed but not yet saved. **1** if a file has been saved and no values has been changed since then.
        '''
        return self.__fileDataStatus.get(name)
    
    def getFileStatusChar(self, name):
        '''
        :method: Ask for the status of a specific file.
        :returns: **C** if a file has been Changed but not yet saved. **S** if a file has been saved and no values has been changed since then.
        ''' 
        if self.__fileDataStatus.get(name) == 0:
            return('C')
        else:
            return('S')
        
    def windowExists(self, window):
        '''
        :method: Checks if a window has already been instanciated. 
        :param window: Name of the window to check for it's existence
        :returns: True/ False: depending on window has been registered/ unregistered
        '''
        if window in self.__instanciatedWindowList:
            return self.__instanciatedWindowList.get(window)
        else:
            return False
    
    def registerWindow(self, window):
        '''
        :method: Windows which are instanciated shall be registered here. This is part of the work to avoid multiple windows of the same name are open. 
        :param window: window name to be register
        '''
        self.__instanciatedWindowList[window] = True
        
    def unregisterWindow(self, window):
        '''
        :method: Windows which are closed shall be unregistered here. This is part of the work to avoid multiple windows of the same name are open. 
        :param window: window name to be unregistered
        '''
        if window in self.__instanciatedWindowList:
            self.__instanciatedWindowList[window] = False
