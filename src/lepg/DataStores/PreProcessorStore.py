'''
Does take care about the data handling for the PreProcessor. 

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''

from PyQt5.QtCore import QObject, QFile, QTextStream, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from Singleton.Singleton import Singleton
import logging
from DataWindowStatus.DataWindowStatus import DataWindowStatus

class PreProcessorStore(QObject, metaclass=Singleton):
    '''
    Does take care about the data handling for the PreProcessor. 
        - Reads and writes the data files
        - Holds as a central point all temporary data during program execution

    Class is implemented as a Singleton. Even if it is instantiated multiple times
    all data will be the same for all instances. 
    
    @signal dataStatusUpdate :  Sent out as soon a file was opened or saved
                                The first string indicates the class name
                                The second string indicates 
                                    - if a file was opened
                                    - if a file was saved
                                    - Filename and Path has been changed
    '''
    dataStatusUpdate = pyqtSignal(str,str)
    __className = 'PreProcessorStore'
    
    # Variables used across the class
    __simpleData ={
        'FileNamePath' :  '' ,
        'FileVersion' : '', 
        'WingName' : '',
        'LE_type' : '',
        'LE_a1' : '',
        'LE_b1' : '',
        'LE_x1' : '',
        'LE_x2' : '',
        'LE_xm' : '',
        'LE_c0' : '',
        'LE_ex1' : '',
        'LE_c02' : '',
        'LE_ex2' : '',
        'TE_type' : '',
        'TE_a1' : '',
        'TE_b1' : '',
        'TE_x1' : '',
        'TE_xm' : '',
        'TE_c0' : '',
        'TE_y0' : '',
        'TE_exp' : '',
        'Vault_type' : '',
        'Vault_a1' : '',
        'Vault_b1' : '',
        'Vault_x1' : '',
        'Vault_c1' : '',
        'CellDistT' : '',
        'CellDistCoeff' : '',
        'CellNum' : ''
    }
    
    __Vault_t2_dta = [[0,0],[0,0],[0,0],[0,0]]
    
    def __init__(self):
        '''
        '''
        logging.debug('PreProcessorStore.__init__')
        super().__init__()
        self.dws = DataWindowStatus()
        self.dws.registerSignal(self.dataStatusUpdate)
        
    
    def isValid( self, fileName ):
        '''
        Checks if a file can be opened and contains a valid title and known version number.
        '''
        logging.debug('PreProcessorStore.isValid')
        try:
            inFile = QFile(fileName)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(inFile)
        except:
            logging.error('File cannot be opened ' + fileName )
            return False
        
        self.titleOK = False
        self.versionOK = False
        
        while (stream.atEnd() != True) and not (self.titleOK and self.versionOK):
            line = stream.readLine()
            if line.find('1.5') >= 0:
                self.setSingleVal('FileVersion', '1.5')
                self.versionOK = True

            if line.find('GEOMETRY PRE-PROCESSOR') >= 0:
                self.titleOK = True

        inFile.close()
        
        if not (self.versionOK and self.titleOK):
            logging.error('Result of PreProc Version check %s', self.versionOK)
            logging.error('Result of PreProc Title check %s', self.titleOK)
            self.setSingleVal('FileNamePath', '')

            self.setSingleVal('FileVersion', '')
            # TODO: add a error dialog here
        
        return self.versionOK and self.titleOK
    
    def openFile(self):
        '''
        Checks for unapplied/ unsaved data, and appropriate handling. 
        Does the File Open dialog. 
        '''
        
        # Make sure there is no unsaved/ unapplied data
        if not (self.dws.getWindowDataStatus('PreProcDataEdit') and self.dws.getFileStatus('PreProcFile')):
            # There is unsaved/ unapplied data, show a warning
            if self.showReallyOpenNewDialog() == QMessageBox.Cancel:
                # User wants to abort
                return
        # Ask first for the filename
        fileName, _filter =QFileDialog.getOpenFileName(
                        None,
                        _('Open PreProc file'),
                        "",
                        "Geometry Files (*.txt);;All Files (*)")

        # TODO: file open must also set flags in Data Status
        if self.isValid(fileName):
            self.setFileName(fileName)
            self.readFile()
            
    def saveFile(self):
        logging.debug('PreProcessorStore.saveFile')
        
        filename = self.getFileName()
        
        if filename != '':
            # We do have already a valid filename
            self.writeFile()
        else:
            # Ask first for the filename
            fileName, _filter =QFileDialog.getSaveFileName(
                        None,
                        _('Save PreProc file'),
                        "",
                        "Geometry Files (*.txt);;All Files (*)")
            
            self.setFileName(fileName)
            self.writeFile()
            
    def saveFileAs(self):
        logging.debug('PreProcessorStore.saveFileAs')
        
        # Ask first for the filename
        fileName, _filter =QFileDialog.getSaveFileName(
                    None,
                    _('Save PreProc file as'),
                    "",
                    "Geometry Files (*.txt);;All Files (*)")
        
        self.setFileName(fileName)
        self.writeFile()
        
            
    def showReallyOpenNewDialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Unsaved or unapplied data")
        msgBox.setText("You have unsaved or unapplied data. \n\nPress OK to open the new file and overwrite the changes.\nPress Cancel to abort. ")
        msgBox.setIcon(QMessageBox.Warning)
        
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msgBox.exec()
    
    def readFile(self):
        '''
        Reads the data file and saves the data in the internal varibles.
        Filename and Path must be set first!
        '''
        inFile = QFile(self.getSingleVal('FileNamePath'))
        inFile.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(inFile)

        # Overread file header
        self.counter = 0
        while self.counter < 2:
            line = stream.readLine()
            if line.find('***************') >= 0:
                self.counter += 1
        
        # *** under file header
        self.setSingleVal('WingName', stream.readLine())
        
        # header of section one
        logging.debug('PreProcessorStore.readFile Section1 Header')
        x = 1
        while x <= 3:
            x += 1
            line = stream.readLine()
        
        #section one values
        logging.debug('PreProcessorStore.readFile Section 1 Data')
        self.setSingleVal('LE_type',stream.readLine())
        
        line = stream.readLine().split()
        self.setSingleVal('LE_a1', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('LE_b1', line[1])

        line = stream.readLine().split()
        self.setSingleVal('LE_x1', line[1])

        line = stream.readLine().split()
        self.setSingleVal('LE_x2', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('LE_xm', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('LE_c0', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('LE_ex1', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('LE_c02', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('LE_ex2', line[1])

        # header of section two
        logging.debug('PreProcessorStore.readFile Section 2 Header')
        x = 1
        while x <= 3:
            x += 1
            line = stream.readLine()
        
        #section two values
        logging.debug('PreProcessorStore.readFile Section 2 Data')
        self.setSingleVal('TE_type', stream.readLine())
        
        line = stream.readLine().split()
        self.setSingleVal('TE_a1', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('TE_b1', line[1])

        line = stream.readLine().split()
        self.setSingleVal('TE_x1', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('TE_xm', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('TE_c0', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('TE_y0', line[1])
        
        line = stream.readLine().split()
        self.setSingleVal('TE_exp', line[1])
        
        ###############
        # header of section three
        logging.debug('PreProcessorStore.readFile Section 3 Header')
        x = 1
        while x <= 3:
            x += 1
            line = stream.readLine()
            
        #section three values
        logging.debug('PreProcessorStore.readFile Section 3 Data')
        self.setSingleVal('Vault_type', stream.readLine())
        
        if self.getSingleVal('Vault_type') == '1':
            logging.debug('PreProcessorStore.readFile Vault Type 1')
            # vault type 1
            line = stream.readLine().split()
            self.setSingleVal('Vault_a1', line[1])
            
            line = stream.readLine().split()
            self.setSingleVal('Vault_b1', line[1])
            
            line = stream.readLine().split()
            self.setSingleVal('Vault_x1', line[1])
            
            line = stream.readLine().split()
            self.setSingleVal('Vault_c1', line[1]) 
            
        else:
            logging.debug('PreProcessorStore.readFile Vault Type 2')
            # vault type 2
            line = stream.readLine().split()
            self.setVault_t2_dta(0, 0, line[0])
            self.setVault_t2_dta(0, 1, line[1])
            
            line = stream.readLine().split()
            self.setVault_t2_dta(1, 0, line[0])
            self.setVault_t2_dta(1, 1, line[1])
        
            line = stream.readLine().split()
            self.setVault_t2_dta(2, 0, line[0])
            self.setVault_t2_dta(2, 1, line[1])
            
            line = stream.readLine().split()
            self.setVault_t2_dta(3, 0, line[0])
            self.setVault_t2_dta(3, 1, line[1])
        
        ###############
        # header of section four
        logging.debug('PreProcessorStore.readFile Section 4 Header')
        x = 1
        while x <= 3:
            x += 1
            line = stream.readLine()
            
        #section four values
        logging.debug('PreProcessorStore.readFile Section 4 Data')
        self.setSingleVal('CellDistT', stream.readLine())
        self.setSingleVal('CellDistCoeff', stream.readLine())
        self.setSingleVal('CellNum', stream.readLine())

        inFile.close()
        self.dataStatusUpdate.emit(self.__className,'Open')
  
    def writeFile( self):
        '''
        '''
#         if self.isValid( self.fileName ):
#             fileName = self.fileName + ".bak"
#             file = open( fileName, 'w' )
#             #file.write( text )
#             file.close()
        return
            
    def setFileName( self, fileName ):
        '''
        Does set the File Name the data store shall work with. 
        
        @param fileName: String containing full path and filename
        @param openFile: If set to True the file will be opened immediately the path and filename was set  
        
        '''
        if fileName != '':
            self.setSingleVal('FileNamePath', fileName)
            
    def getFileName( self ):
        '''
        Returns the name of the file name member.
        '''
        return self.getSingleVal('FileNamePath')
    
    def setSingleVal(self, parameter, value):
        self.__simpleData[parameter] = value
        self.dataStatusUpdate.emit(self.__className, parameter)
        
    def getSingleVal(self, parameter):
        return self.__simpleData.get(parameter)

    def setVault_t2_dta(self, x, y, v):
        self.__Vault_t2_dta[x][y] = v
        self.dataStatusUpdate.emit(self.__className, 'Vault_t2_dta')
        
    def getVault_t2_dta(self, x, y, v):
        return self.__Vault_t2_dta[x][y]
    