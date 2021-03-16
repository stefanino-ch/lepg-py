'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import logging

from PyQt5.QtCore import QObject, QFile, QTextStream, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from Singleton.Singleton import Singleton
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from ConfigReader.ConfigReader import ConfigReader

class PreProcessorStore(QObject, metaclass=Singleton):
    '''
    :class: Does take care about the data handling for the PreProcessor.
        - Reads and writes the data files
        - Holds as a central point all temporary data during program execution
    
    Is implemented as a **Singleton**. Even if it is instantiated multiple times all data will be the same for all instances. 
    '''
    dataStatusUpdate = pyqtSignal(str,str)
    '''
    :signal:  Sent out as soon a file was opened or saved
        The first string indicates the class name
        The second string indicates 
        - if a file was opened
        - if a file was saved
        - Filename and Path has been changed
    '''
    __className = 'PreProcessorStore'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    
    __simpleData ={
        'FileNamePath' :  '' ,
        'FileVersion' : '', 
        'WingName' : '',
        'LE_type' : '1',
        'LE_a1' : '',
        'LE_b1' : '',
        'LE_x1' : '',
        'LE_x2' : '',
        'LE_xm' : '',
        'LE_c01' : '',
        'LE_ex1' : '',
        'LE_c02' : '',
        'LE_ex2' : '',
        'TE_type' : '1',
        'TE_a1' : '',
        'TE_b1' : '',
        'TE_x1' : '',
        'TE_xm' : '',
        'TE_c0' : '',
        'TE_y0' : '',
        'TE_exp' : '',
        'Vault_type' : '1',
        'Vault_a1' : '',
        'Vault_b1' : '',
        'Vault_x1' : '',
        'Vault_c1' : '',
        'CellDistT' : '',
        'CellDistCoeff' : '',
        'CellNum' : ''
    }
    '''
    :attr: Variables used across the class
    '''
    
    __Vault_t2_dta = [[0,0],[0,0],[0,0],[0,0]]
    '''
    :attr: Vault data handled by the class
    '''
    
    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug('PreProcessorStore.__init__')
        super().__init__()
        self.dws = DataWindowStatus()
        self.dws.registerSignal(self.dataStatusUpdate)
    
    def isValid( self, fileName ):
        '''
        :method: Checks if a file can be opened and contains a valid title and known version number.
        :param fileName: the name of the file to be checked
        '''
        logging.debug('PreProcessorStore.isValid')
        try:
            inFile = QFile(fileName)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(inFile)
        except:
            logging.error('File cannot be opened ' + fileName )
            return False
        
        titleOK = False
        versionOK = False
        lineCounter = 0
        
        while (stream.atEnd() != True) and not (titleOK and versionOK) and lineCounter < 4:
            line = stream.readLine()
            if line.find('1.5') >= 0:
                self.setSingleVal('FileVersion', '1.5')
                versionOK = True

            if line.find('GEOMETRY PRE-PROCESSOR') >= 0:
                titleOK = True
            lineCounter += 1

        inFile.close()
        
        if not ( (versionOK and titleOK) ):
            logging.error('Result of PreProc Version check %s', versionOK)
            logging.error('Result of PreProc Title check %s', titleOK)
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('File read error'))
            msgBox.setText(_('File seems not to be a valid PreProc File! \nVersion detected: ')+ str(versionOK)+ _('\nTitle detected: ')+ str(titleOK))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            
            self.setSingleVal('FileNamePath', '')
            self.setSingleVal('FileVersion', '')
        return versionOK and titleOK
    
    def openFile(self):
        '''
        :method: Checks for unapplied/ unsaved data, and appropriate handling. Does the File Open dialog handling. 
        '''
        # Make sure there is no unsaved/ unapplied data
        if not (self.dws.getWindowDataStatus('PreProcDataEdit') and self.dws.getFileStatus('PreProcFile')):
            # There is unsaved/ unapplied data, show a warning
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_("Unsaved or unapplied data"))
            msgBox.setText(_("You have unsaved or unapplied data. \n\nPress OK to open the new file and overwrite the changes.\nPress Cancel to abort. "))
            msgBox.setIcon(QMessageBox.Warning)        
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            answer = msgBox.exec()            
            
            if answer == QMessageBox.Cancel:
                # User wants to abort
                return

        fileName = QFileDialog.getOpenFileName(
                        None,
                        _('Open PreProc file'),
                        "",
                        "Pre Proc Files (*.txt);;All Files (*)")

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the dialog  
            # an empty tuple is retured
            if self.isValid(fileName[0]):
                self.setFileName(fileName[0])
                self.readFile()
            
    def saveFile(self):
        '''
        :method: Checks if there is already a valid file name, if not it asks for it. Starts afterwards the writing process.  
        '''
        logging.debug('PreProcessorStore.saveFile')
        
        filename = self.getFileName()
        if filename != '':
            # We do have already a valid filename
            self.writeFile()
        else:
            # Ask first for the filename
            fileName = QFileDialog.getSaveFileName(
                        None,
                        _('Save PreProc file'),
                        "",
                        "Geometry Files (*.txt);;All Files (*)")
            
            if fileName != ('', ''):
                # User has really selected a file, if it would have aborted the dialog  
                # an empty tuple is retured
                self.setFileName(fileName[0])
                self.writeFile()
            
    def saveFileAs(self):
        '''
        :method: Asks for a new filename. Starts afterwards the writing process.  
        '''
        logging.debug('PreProcessorStore.saveFileAs')
        
        # Ask first for the filename
        fileName = QFileDialog.getSaveFileName(
                    None,
                    _('Save PreProc file as'),
                    "",
                    "Geometry Files (*.txt);;All Files (*)")
        
        if fileName != ('', ''):
                # User has really selected a file, if it would have aborted the dialog  
                # an empty tuple is retured
                self.setFileName(fileName[0])
                self.writeFile()
    
    def readFile(self):
        '''
        :method: Reads the data file and saves the data in the internal varibles. 
        :warning: Filename and Path must be set first!
        '''
        logging.debug(self.__className+'.readFile')
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
        self.setSingleVal('LE_c01', line[1])
        
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
  
    def writeFile(self, forProc=False):
        '''
        :method: Writes all the values into a data file. 
        :warning: Filename must have been set already before, unless the file shall be written for the PreProcessor.
        :param forProc: Set this to True if the file must be saved in the directory where the PreProcessor resides
        '''
        separator = '**********************************\n'
        
        logging.debug(self.__className+'.writeFile')
        
        if forProc == False:
            # Regular file write into a file specified by the user
            outFile = QFile(self.getSingleVal('FileNamePath'))
        else:
            # Special file write into the directory where the PreProcessor resides
            config = ConfigReader()
            pathName = os.path.join(config.getPreProcDirectory(), 'pre-data.txt')
            
            # Delete old file first
            if os.path.exists(pathName):
                logging.debug(self.__className+'.writeFile remove old file')
                os.remove(pathName)
            else:
                logging.debug(self.__className+'.writeFile no PreProc file in place')
            
            outFile = QFile(pathName)
        
        if not outFile.open(QFile.ReadWrite | QFile.Text):
            logging.error(self.__className+'.writeFile '+ outFile.errorString()) 
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle("File save error")
            msgBox.setText('File can not be saved: '+ outFile.errorString( ))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return 
        
        ## File is open, start writing
        stream = QTextStream(outFile)
        stream.setCodec('UTF-8')

        stream << separator
        stream << 'LEPARAGLIDING\n'
        stream << 'GEOMETRY PRE-PROCESSOR     v1.5\n'
        stream << separator
        stream << self.getSingleVal('WingName') << '\n'
        stream << separator
        stream << '* 1. Leading edge parameters\n'
        stream << separator
        stream << self.getSingleVal('LE_type') << '\n'
        stream << 'a1= ' << self.getSingleVal('LE_a1') << '\n'
        stream << 'b1= ' << self.getSingleVal('LE_b1') << '\n'
        stream << 'x1= ' << self.getSingleVal('LE_x1') << '\n'
        stream << 'x2= ' << self.getSingleVal('LE_x2') << '\n'
        stream << 'xm= ' << self.getSingleVal('LE_xm') << '\n'
        stream << 'c01= ' << self.getSingleVal('LE_c01') << '\n'
        stream << 'ex1= ' << self.getSingleVal('LE_ex1') << '\n'
        stream << 'c02= ' << self.getSingleVal('LE_c02') << '\n'
        stream << 'ex2= ' << self.getSingleVal('LE_ex2') << '\n'
        
        stream << separator
        stream << '* 2. Trailing edge parameters\n'
        stream << separator
        stream << self.getSingleVal('TE_type') << '\n'
        stream << 'a1= ' << self.getSingleVal('TE_a1') << '\n'
        stream << 'b1= ' << self.getSingleVal('TE_b1') << '\n'
        stream << 'x1= ' << self.getSingleVal('TE_x1') << '\n'
        stream << 'xm= ' << self.getSingleVal('TE_xm') << '\n'
        stream << 'c0= ' << self.getSingleVal('TE_c0') << '\n'
        stream << 'y0= ' << self.getSingleVal('TE_y0') << '\n'
        stream << 'exp= ' << self.getSingleVal('TE_exp') << '\n'
        
        stream << separator
        stream << '* 3. Vault\n'
        stream << separator
        if self.getSingleVal('Vault_type') == '1':
            # Write Vault type 1
            stream << self.getSingleVal('Vault_type') << '\n'
            stream << 'a1= ' << self.getSingleVal('Vault_a1') << '\n'
            stream << 'b1= ' << self.getSingleVal('Vault_b1') << '\n'
            stream << 'x1= ' << self.getSingleVal('Vault_x1') << '\n'
            stream << 'c1= ' << self.getSingleVal('Vault_c1') << '\n'
        else:
            # Write Vault type 2
            stream << self.getSingleVal('Vault_type') << '\n'
            stream << self.getVault_t2_dta(0, 0) << '\t' << self.getVault_t2_dta(0, 1) << '\n'
            stream << self.getVault_t2_dta(1, 0) << '\t' << self.getVault_t2_dta(1, 1) << '\n'
            stream << self.getVault_t2_dta(2, 0) << '\t' << self.getVault_t2_dta(2, 1) << '\n'
            stream << self.getVault_t2_dta(3, 0) << '\t' << self.getVault_t2_dta(3, 1) << '\n'
         
        stream << separator
        stream << '* 4. Cells distribution\n'
        stream << separator   
        stream << self.getSingleVal('CellDistT') << '\n'
        stream << self.getSingleVal('CellDistCoeff') << '\n'
        stream << self.getSingleVal('CellNum') << '\n'
        
        stream.flush()
        outFile.close()
        
        if forProc == False:
            # Then we need to set the right file version
            self.setSingleVal('FileVersion', '1.5')
        
            # Make flags in order
            self.dataStatusUpdate.emit(self.__className,'Open')
            
    def setFileName( self, fileName ):
        '''
        :method: Does set the File Name the data store shall work with. 
        :param fileName: String containing full path and filename
        '''
        if fileName != '':
            self.setSingleVal('FileNamePath', fileName)
            
    def getFileName( self ):
        '''
        :method: Returns the name of the file name member.
        '''
        return self.getSingleVal('FileNamePath')
    
    def setSingleVal(self, parameter, value):
        '''
        :method: Does set a single value in the data store.
        :param parameter: the name of the parameter to be set. Refer to *__simpleData* for the valid parameter names.
        :param value: the value to be set.
        '''
        self.__simpleData[parameter] = value
        self.dataStatusUpdate.emit(self.__className, parameter)
        
    def getSingleVal(self, parameter):
        '''
        :method: Reads a single parameter from the data store
        :param parameter: Name of the parameter to be read. Refer to *__simpleData* for the valid parameter names.
        :returns: the value of the parameter, an empty string if the parameter was not found.
        ''' 
        return self.__simpleData.get(parameter)

    def setVault_t2_dta(self, row, col, val):
        '''
        :method: Sets the vault data in the data store. Data is organized in a matrix. 
        :param row: number of the row to be set
        :param col: number of the column to be set 
        :param val: the value to be set
        '''
        self.__Vault_t2_dta[row][col] = val
        self.dataStatusUpdate.emit(self.__className, 'Vault_t2_dta')
        
    def getVault_t2_dta(self, row, col):
        '''
        :method: Reads vault data from the data store. Data is organized in a matrix. 
        :param row: number of the row to be read
        :param col: number of the column to be read 
        :returns: the value of the parameter, an empty string if the parameter was not found.
        '''
        return self.__Vault_t2_dta[row][col]
    