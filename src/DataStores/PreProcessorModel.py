'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
import logging

from PyQt5.QtCore import Qt, QFile, QTextStream, QObject, pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Singleton.Singleton import Singleton
from DataStores.SqlTableModel import SqlTableModel

from ConfigReader.ConfigReader import ConfigReader
from DataStores.Database import Database

from DataStores.FileHelpers import FileHelpers

class PreProcessorModel(QObject, metaclass=Singleton):
    '''
    :class: Does take care about the data handling for the pre-processor.
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
    __className = 'PreProcessorModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    __fileNamePath = ''
    '''
    :attr: full path and name of the data file currently in use
    '''
    __fileVersion = ''
    '''
    :attr: version number of the file currently in use
    '''
    
    def __init__(self, parent=None): # @UnusedVariable
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+ '.__init__')
         
        self.db = Database()
        self.db.openConnection()
        
        super().__init__()
        
        self.fh = FileHelpers()

        self.leadingE_M = self.LeadingEdgeModel()
        self.trailingE_M = self.TrailingEdgeModel()
        self.vault_M = self.VaultModel()
        self.gen_M = self.GenModel()
        self.cellsDistr_M = self.CellsDistrModel()

    def setFileName( self, fileName ):
        '''
        :method: Does set the file name the data store shall work with. 
        :param fileName: String containing full path and filename
        '''
        self.__fileNamePath = fileName
        self.dataStatusUpdate.emit(self.__className, 'FileNamePath')
            
    def getFileName( self ):
        '''
        :method: Returns the name of the file name member.
        '''
        return self.__fileNamePath
    
    def setFileVersion( self, fileVersion ):
        '''
        :method: Does set the file version the data store shall work with. 
        :param fileVersion: String containing the version number
        '''
        self.__fileVersion = fileVersion
        self.dataStatusUpdate.emit(self.__className, 'FileVersion')
            
    def getFileVersion( self ):
        '''
        :method: Returns the version info of the data file currently in use
        '''
        return self.__fileVersion
    
    def isValid( self, fileName ):
        '''
        :method: Checks if a file can be opened and contains a valid title and known version number.
        :param fileName: the name of the file to be checked
        '''
        logging.debug(self.__className+ '.isValid')
        try:
            inFile = QFile(fileName)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(inFile)
        except:
            logging.error( self.__className + 'File cannot be opened ' + fileName )
            return False
        
        titleOK = False
        versionOK = False
        lineCounter = 0
        
        while (stream.atEnd() != True) and not (titleOK and versionOK) and lineCounter < 4:
            line = stream.readLine()
            if line.find('1.5') >= 0:
                self.setFileVersion('1.6')
                versionOK = True
            elif line.find('1.6') >= 0:
                self.setFileVersion('1.6')
                versionOK = True

            if line.find('GEOMETRY PRE-PROCESSOR') >= 0:
                titleOK = True
            lineCounter += 1

        inFile.close()
        
        if not ( (versionOK and titleOK) ):
            logging.error(self.__className+ ' Result of PreProc file version check %s', versionOK)
            logging.error(self.__className+ ' Result of PreProc file title check %s', titleOK)
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('File read error'))
            msgBox.setText(_('File seems not to be a valid PreProcessor File! \nVersion detected: ')+ str(versionOK)+ _('\nTitle detected: ')+ str(titleOK))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            
            self.setFileName('')
            self.setFileVersion('')

        return versionOK and titleOK
    
    def openFile(self):
        '''
        :method: Checks for unapplied/ unsaved data, and appropriate handling. Does the File Open dialog handling. 
        '''
        logging.debug(self.__className+ '.openFile')
        # Make sure there is no unsaved/ unapplied data
#         if not (self.dws.getWindowDataStatus('PreProcDataEdit') and self.dws.getFileStatus('PreProcFile')):
#             # There is unsaved/ unapplied data, show a warning
#             msgBox = QMessageBox()
#             msgBox.setWindowTitle(_("Unsaved or unapplied data"))
#             msgBox.setText(_("You have unsaved or unapplied data. \n\nPress OK to open the new file and overwrite the changes.\nPress Cancel to abort. "))
#             msgBox.setIcon(QMessageBox.Warning)        
#             msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#             answer = msgBox.exec()            
#             
#             if answer == QMessageBox.Cancel:
#                 # User wants to abort
#                 return

        fileName = QFileDialog.getOpenFileName(
                        None,
                        _('Open Pre-Proc file'),
                        "",
                        "Pre-Proc Files (*.txt);;All Files (*)")

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
        logging.debug(self.__className+ '.saveFile')
        
        fileName = self.getFileName() 
        if len(fileName) != 0:
            # We do have already a valid filename
            self.writeFile()
        else:
            # Ask first for the filename
            fileName = QFileDialog.getSaveFileName(
                        None,
                        _('Save Pre-Processor file'),
                        "",
                        "Pre-Proc Files (*.txt);;All Files (*)")
            
            if fileName != ('', ''):
                # User has really selected a file, if it would have aborted the dialog  
                # an empty tuple is retured
                self.setFileName(fileName[0])
                self.writeFile()
            
    def saveFileAs(self):
        '''
        :method: Asks for a new filename. Starts afterwards the writing process.  
        '''
        logging.debug(self.__className+ '.saveFileAs')
        
        # Ask first for the filename
        fileName = QFileDialog.getSaveFileName(
                    None,
                    _('Save Pre-Processor file as'),
                    "",
                    "Pre-Proc Files (*.txt);;All Files (*)")
        
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
        
        inFile = QFile( self.getFileName() )
        inFile.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(inFile)

        ##############################
        # 1. Geometry
        # Overread file header
        counter = 0
        while counter < 2:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1
        
        # Wing Name
        self.gen_M.setNumConfigs(0)
        
        logging.debug(self.__className+'.readFile: Wing name')
        self.gen_M.setNumRowsForConfig(1, 1)
        name = stream.readLine()
        self.gen_M.updateRow(1,1, name )
        
        # 1. Leading edge
        logging.debug(self.__className+'.readFile: Leading edge')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()
            
        one = self.fh.remTabSpaceQuot(stream.readLine())
        two = self.fh.splitLine( stream.readLine() )
        thr = self.fh.splitLine( stream.readLine() )
        fou = self.fh.splitLine( stream.readLine() )
        fiv = self.fh.splitLine( stream.readLine() )
        six = self.fh.splitLine( stream.readLine() )
        sev = self.fh.splitLine( stream.readLine() )
        eig = self.fh.splitLine( stream.readLine() )
        nin = self.fh.splitLine( stream.readLine() )
        ten = self.fh.splitLine( stream.readLine() )
        
        self.leadingE_M.setNumConfigs(0)
        self.leadingE_M.setNumConfigs(1)
        self.leadingE_M.updateRow(1, 1, one, two[1], thr[1], fou[1], fiv[1], six[1], sev[1], eig[1], nin[1], ten[1] )
        
        # 2. Trailing edge
        logging.debug(self.__className+'.readFile: Trailing edge')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()
            
        one = self.fh.remTabSpaceQuot(stream.readLine())
        two = self.fh.splitLine( stream.readLine() )
        thr = self.fh.splitLine( stream.readLine() )
        fou = self.fh.splitLine( stream.readLine() )
        fiv = self.fh.splitLine( stream.readLine() )
        six = self.fh.splitLine( stream.readLine() )
        sev = self.fh.splitLine( stream.readLine() )
        eig = self.fh.splitLine( stream.readLine() )
        
        self.trailingE_M.setNumConfigs(0)
        self.trailingE_M.setNumConfigs(1)
        self.trailingE_M.updateRow(1, 1, one, two[1], thr[1], fou[1], fiv[1], six[1], sev[1], eig[1] )
        
        # 3. Vault
        logging.debug(self.__className+'.readFile: vault')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()
            
        self.vault_M.setNumConfigs(0)
        self.vault_M.setNumConfigs(1)
        vtype = int( self.fh.remTabSpaceQuot(stream.readLine()) )
        
        one = self.fh.splitLine( stream.readLine() )
        two = self.fh.splitLine( stream.readLine() )
        thr = self.fh.splitLine( stream.readLine() )
        fou = self.fh.splitLine( stream.readLine() )
        
        if vtype == 1:
            self.vault_M.updateRow(1, 1, vtype, one[1], two[1], thr[1], fou[1], 0, 0, 0, 0, 0, 0, 0, 0)
            
        else:
            self.vault_M.updateRow(1, 1, vtype, 0, 0, 0, 0, one[0], two[0], thr[0], fou[0], one[1], two[1], thr[1], fou[1])
            
        # 4. Cells distribution
        logging.debug(self.__className+'.readFile: Cells')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()
        
        self.cellsDistr_M.setNumConfigs(0)
        
        distrT = int( self.fh.remTabSpaceQuot(stream.readLine()) )
                
        if distrT == 1:
            self.cellsDistr_M.setNumRowsForConfig(1, 1)
            numCells = self.fh.remTabSpaceQuot(stream.readLine())
            self.cellsDistr_M.updateRow(1, 1, distrT, 0, 0, numCells)
            
        elif (distrT  == 2) or (distrT == 3):
            self.cellsDistr_M.setNumRowsForConfig(1, 1)
            coef = self.fh.remTabSpaceQuot(stream.readLine())
            numCells = self.fh.remTabSpaceQuot(stream.readLine())
            self.cellsDistr_M.updateRow(1, 1, distrT, coef, 0, numCells)
            
        elif distrT == 4:
            numCells = int( self.fh.remTabSpaceQuot(stream.readLine()) )
            self.cellsDistr_M.setNumRowsForConfig(1, numCells)
            
            for l in range (0, numCells):
                width = self.fh.splitLine(stream.readLine())
                self.cellsDistr_M.updateRow(1, l+1, distrT, 0, width[1], numCells)
            
        ##############################
        # Cleanup
        inFile.close() 

    def writeFile(self, forProc=False):
        '''
        :method: Writes all the values into a data file. 
        :warning: Filename must have been set already before, unless the file shall be written for the PreProcessor.
        :param forProc: Set this to True if the file must be saved in the directory where the PreProcessor resides
        '''
        
        separator = '***************************************************\n'
        
        logging.debug(self.__className+'.writeFile')
        
        # check if the file already exists
        filePathName = self.getFileName()
        if os.path.isfile(filePathName):
            # file exists -> delete it
            os.remove(filePathName)
        
        if forProc == False:
            # Regular file write into a file specified by the user
            outFile = QFile(filePathName)
        else:
            # Special file write into the directory where the PreProcessor resides
            config = ConfigReader()
            pathName = os.path.join(config.getPreProcDirectory(), 'pre-data.txt')
            
            # Delete old file first
            if os.path.exists(pathName):
                logging.debug(self.__className+'.writeFile remove old file')
                os.remove(pathName)
            else:
                logging.debug(self.__className+'.writeFile no Proc file in place')
            
            outFile = QFile(pathName)
        
        if not outFile.open(QFile.ReadWrite | QFile.Text):
            logging.error(self.__className+'.writeFile '+ outFile.errorString()) 
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_("File save error"))
            msgBox.setText(_('File can not be saved: ')+ outFile.errorString( ))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return 
        
        ## File is open, start writing
        stream = QTextStream(outFile)
        stream.setCodec('UTF-8')

        stream << separator
        stream << 'LEPARAGLIDING\n'
        stream << 'GEOMETRY PRE-PROCESSOR         V1.6\n'
        stream << separator
        
        values = self.gen_M.getRow(1, 1)
        stream << '%s\n' %(self.fh.chkStr(values(0),''))
        
        stream << separator
        stream << '* 1. Leading edge parameters\n'
        stream << separator
        values = self.leadingE_M.getRow(1, 1)
        stream << '%s\n'        %(self.fh.chkNum(values(0),1))
        stream << 'a1= %s\n'    %(self.fh.chkNum(values(1)))
        stream << 'b1= %s\n'    %(self.fh.chkNum(values(2)))
        stream << 'x1= %s\n'    %(self.fh.chkNum(values(3)))
        stream << 'x2= %s\n'    %(self.fh.chkNum(values(4)))
        stream << 'xm= %s\n'    %(self.fh.chkNum(values(5)))
        stream << 'c0= %s\n'    %(self.fh.chkNum(values(6)))
        stream << 'ex1= %s\n'   %(self.fh.chkNum(values(7)))
        stream << 'c02= %s\n'   %(self.fh.chkNum(values(8)))
        stream << 'ex2= %s\n'   %(self.fh.chkNum(values(9)))
        
        stream << separator
        stream << '* 2. Trailing edge parameters\n'
        stream << separator
        values = self.trailingE_M.getRow(1, 1)
        stream << '%s\n'        %(self.fh.chkNum(values(0),1))
        stream << 'a1= %s\n'    %(self.fh.chkNum(values(1)))
        stream << 'b1= %s\n'    %(self.fh.chkNum(values(2)))
        stream << 'x1= %s\n'    %(self.fh.chkNum(values(3)))
        stream << 'xm= %s\n'    %(self.fh.chkNum(values(4)))
        stream << 'c0= %s\n'    %(self.fh.chkNum(values(5)))
        stream << 'y0= %s\n'    %(self.fh.chkNum(values(6)))
        stream << 'exp= %s\n'   %(self.fh.chkNum(values(7)))

        stream << separator
        stream << '* 3. Vault\n'
        stream << separator
        
        values = self.vault_M.getRow(1, 1)
        stream << '%s\n' %(self.fh.chkNum(values(0),1))

        try:
            if int( values(0) ) ==1:
                stream << 'a1= %s\n' %values(1)
                stream << 'b1= %s\n' %values(2)
                stream << 'x1= %s\n' %values(3)
                stream << 'c1= %s\n' %values(4)
            else:
                stream << '%s\t%s\n' %(values(5), values(9))
                stream << '%s\t%s\n' %(values(6), values(10))
                stream << '%s\t%s\n' %(values(7), values(11))
                stream << '%s\t%s\n' %(values(8), values(12))
        except:
            stream << 'a1= 0\n'
            stream << 'b1= 0\n'
            stream << 'x1= 0\n'
            stream << 'c1= 0\n'
            
        
        stream << separator
        stream << '* 4. Cells distribution\n'
        stream << separator
        values = self.cellsDistr_M.getRow(1, 1)
        stream << '%s\n' %(self.fh.chkNum(values(0),1))
        
        try:
            if int( values(0) ) ==1:
                stream << '%s\n' %values(3)
                
            elif int( values(0) ) ==2 or int( values(0) ) ==3:
                stream << '%s\n' %values(1)
                stream << '%s\n' %values(3)
            
            elif int( values(0) ) ==4:
                stream << '%s\n' %values(3)
                
                for l in range (0, int(values(3))):
                    values = self.cellsDistr_M.getRow(1, l+1)
                    stream << '%s\t%s\n' %(l+1, values(2))
        except:
            stream << '0\n'
        
        stream.flush()
        outFile.close()
        
        if forProc == False:
            # Then we need to set the right file version
            self.setFileVersion('3.10')
        
            # Make flags in order
            #self.dataStatusUpdate.emit(self.__className,'Open')
     
    class CellsDistrModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all for cells distribution.
        '''
        __className = 'CellsDistrModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        DistrTypeCol = 1 
        CoefCol = 2
        WidthCol = 3
        NumCellsCol = 4
        ConfigNumCol = 5
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("PreProcCellsDistr")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(0, Qt.Horizontal, _("Cell Num"))
            self.setHeaderData(2, Qt.Horizontal, _("Coef"))
            self.setHeaderData(3, Qt.Horizontal, _("Width"))
            self.setHeaderData(4, Qt.Horizontal, _("Num cells"))
            
            self.setNumRowsForConfig(1, 1)
        
        def createTable(self):
            '''
            :method: Creates initially the table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists PreProcCellsDistr;")
            query.exec("create table if not exists PreProcCellsDistr ("
                    "OrderNum INTEGER, "
                    "DistrType INTEGER, "
                    "Coef REAL, "
                    "Width REAL, "
                    "NumCells INTEGER, "
                    "ConfigNum INTEGER, "
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, distrT, coef, width, numCells):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')

            query = QSqlQuery()
            query.prepare("UPDATE PreProcCellsDistr SET "
                            "DistrType = :distrT, "
                            "Coef = :coef, "
                            "Width = :width, "
                            "NumCells = :numCells "
                            "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":distrT", distrT )
            query.bindValue(":coef", coef )
            query.bindValue(":width", width )
            query.bindValue(":numCells", numCells )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a config and order number
            :param configNum: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: values read from internal database
            '''
            logging.debug(self.__className+'.getRow')

            query = QSqlQuery()
            query.prepare("Select " 
                            "DistrType, "
                            "Coef, "
                            "Width, "
                            "NumCells "
                            "FROM PreProcCellsDistr WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            return query.value
        
        def updateType(self, configNum, orderNum, distrT):
            logging.debug(self.__className+'.updateType')

            query = QSqlQuery()
            query.prepare("UPDATE PreProcCellsDistr SET "
                            "DistrType= :typeN "
                            "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", distrT )
            
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getType(self, configNum, orderNum):
            '''
            :method: reads type value back from the internal database for a config and order number
            :param configNum: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: type value
            '''
            logging.debug(self.__className+'.getType')

            query = QSqlQuery()
            query.prepare("Select " 
                            "DistrType "
                            "FROM PreProcCellsDistr WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            
            if query.value(0) == '':
                return 1
            else: 
                return query.value(0)


    class GenModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the general data 
        '''
        __className = 'GenModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        WingNameCol = 1
        ConfigNumCol = 2
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("PreProcGen")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(1, Qt.Horizontal, _("Wing name"))
            
            self.setNumRowsForConfig(1, 1)
        
        def createTable(self):
            '''
            :method: Creates initially the table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists PreProcGen;")
            query.exec("create table if not exists PreProcGen ("
                    "OrderNum INTEGER, "
                    "WingN TEXT, "
                    "ConfigNum INTEGER, "
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, wingN):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')

            query = QSqlQuery()
            query.prepare("UPDATE PreProcGen SET "
                            "WingN = :wingN "
                            "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":wingN", wingN )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a config and order number
            :param configNum: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: values read from internal database
            '''
            logging.debug(self.__className+'.getRow')

            query = QSqlQuery()
            query.prepare("Select " 
                            "WingN "
                            "FROM PreProcGen WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            return query.value


    class LeadingEdgeModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data for leading edge definition 
        '''
        __className = 'LeadingEdgeModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        TypeCol = 1
        aOneCol = 2 
        bOneCol = 3
        xOneCol = 4
        xTwoCol = 5
        xmCol = 6
        cZeroOneCol = 7
        exOneCol = 8 
        cZeroTwoCol = 9 
        exTwoCol = 10
        ConfigNumCol = 11
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("LeadingEdge")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(1, Qt.Horizontal, _("Type"))
            self.setHeaderData(2, Qt.Horizontal, _("a1 [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("b1 [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("x1 [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("x2 [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("xm [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("c01 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("ex1 [coef]"))
            self.setHeaderData(9, Qt.Horizontal, _("c02 [coef]"))
            self.setHeaderData(10, Qt.Horizontal, _("ex2 [coef]"))
            
            self.setNumRowsForConfig(1, 1)
        
        def createTable(self):
            '''
            :method: Creates initially the table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists LeadingEdge;")
            query.exec("create table if not exists LeadingEdge ("
                    "OrderNum INTEGER, "
                    "Type INTEGER, "
                    "aOne REAL, "
                    "bOne REAL, "
                    "xOne INTEGER, "
                    "xTwo INTEGER, "
                    "xm INTEGER, "
                    "cZeroOne INTEGER, "
                    "exOne REAL, "
                    "cZeroTwo INTEGER, "
                    "exTwo REAL, "
                    "ConfigNum INTEGER, "
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, typeNum, aOne, bOne, xOne, xTwo, xm, cZeroOne, exOne, cZeroTwo, exTwo):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')

            query = QSqlQuery()
            query.prepare("UPDATE LeadingEdge SET "
                            "Type= :typeN, "
                            "aOne= :aOne, "
                            "bOne= :bOne, "
                            "xOne= :xOne, "
                            "xTwo= :xTwo, "
                            "xm= :xm, "
                            "cZeroOne= :cZeroOne, "
                            "exOne= :exOne, "
                            "cZeroTwo= :cZeroTwo, "
                            "exTwo= :exTwo "
                            "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", typeNum )
            query.bindValue(":aOne", aOne )
            query.bindValue(":bOne", bOne )
            query.bindValue(":xOne", xOne )
            query.bindValue(":xTwo", xTwo )
            query.bindValue(":xm", xm )
            query.bindValue(":cZeroOne", cZeroOne )
            query.bindValue(":exOne", exOne )
            query.bindValue(":cZeroTwo", cZeroTwo )
            query.bindValue(":exTwo", exTwo )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a config and order number
            :param configNum: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: values read from internal database
            '''
            logging.debug(self.__className+'.getRow')

            query = QSqlQuery()
            query.prepare("Select " 
                            "Type, "
                            "aOne, "
                            "bOne, "
                            "xOne, "
                            "xTwo, "
                            "xm, "
                            "cZeroOne, "
                            "exOne, "
                            "cZeroTwo, "
                            "exTwo "
                            "FROM LeadingEdge WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            return query.value


    class TrailingEdgeModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data for trailing edge definition
        '''
        __className = 'TrailingEdgeModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        TypeCol = 1
        aOneCol = 2 
        bOneCol = 3
        xOneCol = 4
        xmCol = 5
        cZeroCol = 6
        yZeroCol = 7 
        expCol = 8
        ConfigNumCol = 9
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("TrailingEdge")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(1, Qt.Horizontal, _("Type"))
            self.setHeaderData(2, Qt.Horizontal, _("a1 [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("b1 [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("x1 [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("xm [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("c0 [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("y0 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("exp [coef]"))
            
            self.setNumRowsForConfig(1, 1)
        
        def createTable(self):
            '''
            :method: Creates initially the table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists TrailingEdge;")
            query.exec("create table if not exists TrailingEdge ("
                    "OrderNum INTEGER, "
                    "Type INTEGER, "
                    "aOne REAL, "
                    "bOne REAL, "
                    "xOne INTEGER, "
                    "xm INTEGER, "
                    "cZero REAL, "
                    "yZero REAL, "
                    "exp REAL, "
                    "ConfigNum INTEGER, "
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, typeNum, aOne, bOne, xOne, xm, cZero, yZero, exp):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')

            query = QSqlQuery()
            query.prepare("UPDATE TrailingEdge SET "
                            "Type= :typeN, "
                            "aOne= :aOne, "
                            "bOne= :bOne, "
                            "xOne= :xOne, "
                            "xm= :xm, "
                            "cZero= :cZero, "
                            "yZero= :yZero, "
                            "exp= :exp "
                            "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", typeNum )
            query.bindValue(":aOne", aOne )
            query.bindValue(":bOne", bOne )
            query.bindValue(":xOne", xOne )
            query.bindValue(":xm", xm )
            query.bindValue(":cZero", cZero )
            query.bindValue(":yZero", yZero )
            query.bindValue(":exp", exp )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a config and order number
            :param configNum: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: values read from internal database
            '''
            logging.debug(self.__className+'.getRow')

            query = QSqlQuery()
            query.prepare("Select " 
                            "Type, "
                            "aOne, "
                            "bOne, "
                            "xOne, "
                            "xm, "
                            "cZero, "
                            "yZero, "
                            "exp "
                            "FROM TrailingEdge WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            return query.value

        
    class VaultModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data for the vault definition
        '''
        __className = 'VaultModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol= 0
        TypeCol= 1
        aOneCol= 2
        bOneCol= 3
        xOneCol= 4
        cOneCol= 5
        rOneRACol= 6 
        rTwoRACol= 7
        rThrRACol= 8
        rFouRACol= 9
        aOneRACol= 10
        aTwoRACol= 11
        aThrRACol= 12
        aFouRACol= 13
        ConfigNumCol = 14
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Vault")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(2, Qt.Horizontal, _("a1 [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("b1 [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("x1 [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("c1 [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("r1 [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("r2 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("r3 [cm]"))
            self.setHeaderData(9, Qt.Horizontal, _("r4 [cm]"))
            self.setHeaderData(10, Qt.Horizontal, _("a1 [deg]"))
            self.setHeaderData(11, Qt.Horizontal, _("a2 [deg]"))
            self.setHeaderData(12, Qt.Horizontal, _("a3 [deg]"))
            self.setHeaderData(13, Qt.Horizontal, _("a4 [deg]"))
            
            self.setNumRowsForConfig(1, 1)
        
        def createTable(self):
            '''
            :method: Creates initially the table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists Vault;")
            query.exec("create table if not exists Vault ("
                    "OrderNum INTEGER, "
                    "Type INTEGER, "
                    "aOne REAL, "
                    "bOne REAL, "
                    "xOne REAL, "
                    "cOne REAL, "
                    "rOneRA REAL, "
                    "rTwoRA REAL, "
                    "rThrRA REAL, "
                    "rFouRA REAL, "
                    "aOneRA REAL, "
                    "aTwoRA REAL, "
                    "aThrRA REAL, "
                    "aFouRA REAL, "
                    "ConfigNum INTEGER, "
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, typeNum, aOne, bOne, xOne, cOne, rOneRA, rTwoRA, rThrRA, rFouRA, aOneRA, aTwoRA, aThreRA, aFouRA):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')

            query = QSqlQuery()
            query.prepare("UPDATE Vault SET "
                            "Type= :typeN, "
                            "aOne= :aOne, "
                            "bOne= :bOne, "
                            "xOne= :xOne, "
                            "cOne= :cOne, "
                            "rOneRA= :rOneRA, "
                            "rTwoRA= :rTwoRA, "
                            "rThrRA= :rThrRA, "
                            "rFouRA= :rFouRA, "
                            "aOneRA= :aOneRA, "
                            "aTwoRA= :aTwoRA, "
                            "aThrRA= :aThreRA, "
                            "aFouRA= :aFouRA  "
                            "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", typeNum )
            query.bindValue(":aOne", aOne )
            query.bindValue(":bOne", bOne )
            query.bindValue(":xOne", xOne )
            query.bindValue(":cOne", cOne )
            
            query.bindValue(":rOneRA", rOneRA )
            query.bindValue(":rTwoRA", rTwoRA )
            query.bindValue(":rThrRA", rThrRA )
            query.bindValue(":rFouRA", rFouRA )
            
            query.bindValue(":aOneRA", aOneRA )
            query.bindValue(":aTwoRA", aTwoRA )
            query.bindValue(":aThreRA", aThreRA )
            query.bindValue(":aFouRA", aFouRA )
            
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a config and order number
            :param configNum: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: values read from internal database
            '''
            logging.debug(self.__className+'.getRow')

            query = QSqlQuery()
            query.prepare("Select " 
                            "Type, "
                            "aOne, "
                            "bOne, "
                            "xOne, "
                            "cOne, "
                            "rOneRA, "
                            "rTwoRA, "
                            "rThrRA, "
                            "rFouRA, "
                            "aOneRA, "
                            "aTwoRA, "
                            "aThrRA, "
                            "aFouRA "
                            "FROM Vault WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            return query.value
        
        def updateType(self, configNum, orderNum, typeNum):
            logging.debug(self.__className+'.updateType')

            query = QSqlQuery()
            query.prepare("UPDATE Vault SET "
                            "Type= :typeN "
                            "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", typeNum )
            
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getType(self, configNum, orderNum):
            '''
            :method: reads type value back from the internal database for a config and order number
            :param configNum: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: type value
            '''
            logging.debug(self.__className+'.getType')

            query = QSqlQuery()
            query.prepare("Select " 
                            "Type "
                            "FROM Vault WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            return query.value(0)
