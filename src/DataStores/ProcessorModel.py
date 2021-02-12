# https://doc.qt.io/qtforpython/overviews/sql-model.html
# https://www.datacamp.com/community/tutorials/inner-classes-python
'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
import math
import re

from PyQt5.QtCore import QFile, QTextStream, QObject
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Singleton.Singleton import Singleton
from DataStores.SqlTableModel import SqlTableModel

class ProcessorModel(QObject, metaclass=Singleton):
    '''
    :class: Does take care about the data handling for the processor.
        - Reads and writes the data files
        - Holds as a central point all temporary data during program execution
    
    Is implemented as a **Singleton**. Even if it is instantiated multiple times all data will be the same for all instances.
    '''
    __className = 'ProcessorModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    
    def __init__(self, parent=None): # @UnusedVariable
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+ '.__init__')
        self.fileNamePath = ''
        self.fileVersion = ''
        
        # open database
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("processorModel.sqlite")
        if not self.db.open():
            logging.error(self.__className+ '.__init__ cannot open db')
        
        super().__init__()
        # make sure tables are there
        self.rib_M = self.RibModel()
        self.wing_M = self.WingModel()
        self.airf_M = self.AirfoilsModel()
        
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
            if line.find('3.10') >= 0:
                self.fileVersion = '3.10'
                versionOK = True

            if line.find('Input data file') >= 0:
                titleOK = True
            lineCounter += 1

        inFile.close()
        
        if not ( (versionOK and titleOK) ):
            logging.error(self.__className+ ' Result of PreProc Version check %s', versionOK)
            logging.error(self.__className+ ' Result of PreProc Title check %s', titleOK)
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('File read error'))
            msgBox.setText(_('File seems not to be a valid PreProc File! \nVersion detected: ')+ str(versionOK)+ _('\nTitle detected: ')+ str(titleOK))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            
            self.fileNamePath = ''
            self.fileVersion = ''

        return versionOK and titleOK
    
    def setFileName( self, fileName ):
        '''
        :method: Does set the File Name the data store shall work with. 
        :param fileName: String containing full path and filename
        '''
        logging.debug(self.__className+ '.setFileName')
        if fileName != '':
            self.fileNamePath= fileName
    
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
                        _('Open PreProc file'),
                        "",
                        "Pre Proc Files (*.txt);;All Files (*)")

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the dialog  
            # an empty tuple is retured
            if self.isValid(fileName[0]):
                self.setFileName(fileName[0])
                self.readFile()
    
    def readFile(self):
        '''
        :method: Reads the data file and saves the data in the internal varibles.
        :warning: Filename and Path must be set first!
        '''
        logging.debug(self.__className+'.readFile')
        
        inFile = QFile( self.fileNamePath )
        inFile.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(inFile)

        ##############################
        # 1. Geometry
        # Overread file header
        self.counter = 0
        while self.counter < 4:
            line = stream.readLine()
            if line.find('***************') >= 0:
                self.counter += 1
        
        # Brand name
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.BrandNameCol ), self.remTabSpaceQuot(line) )

        # Wing name
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.WingNameCol), self.remTabSpaceQuot(line) )
        
        # Draw scale
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.DrawScaleCol), self.remTabSpace( line ) )
        
        # Wing scale
        line = stream.readLine()
        # self.setSingleVal('WingScale', self.remTabSpace( stream.readLine() ) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.WingScaleCol), self.remTabSpace( stream.readLine() ) )
        
        # Number of cells
        line = stream.readLine()
        # self.setSingleVal('NumCells', self.remTabSpace( stream.readLine() ) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.NumCellsCol), self.remTabSpace( stream.readLine() ) )
        
        # Number of Ribs
        line = stream.readLine()
        # self.setSingleVal('NumRibs', self.remTabSpace( stream.readLine() ) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.NumRibsCol), self.remTabSpace( stream.readLine() ) )

        # Alpha max and parameter
        line = stream.readLine()
        values =  self.splitLine( stream.readLine() )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaMaxTipCol), values[0] )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaModeCol), values[1] )
        if len(values) > 2: 
            self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaMaxCentCol), values[2] )
        else:
            self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaMaxCentCol), '' )
        
        # Paraglider type and parameter
        line = stream.readLine()
        values =  self.splitLine( stream.readLine() )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.ParaTypeCol), self.remTabSpaceQuot( values[0]) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.ParaParamCol), values[1])
        
        # Rib geometric parameters
        # Rib    x-rib    y-LE    y-TE    xp    z    beta    RP    Washin
        line = stream.readLine()
        line = stream.readLine()

        for i in range( 0, self.wing_M.halfNumRibs ):
            values =  self.splitLine( stream.readLine() )
            for y in range(0, 9):
                self.rib_M.setData(self.rib_M.index(i, y), values[y] )
        
        ##############################
        # 2. AIRFOILS
        for i in range(4):
            line = stream.readLine()
        
        for i in range( 0, self.wing_M.halfNumRibs ):
            values =  self.splitLine( stream.readLine() )
            for y in range(0, 8):
                self.airf_M.setData(self.airf_M.index(i, y), values[y] )
        
        
        
        inFile.close() 
       
    def remTabSpace(self, line):
        '''
        :method: Deletes all leaing and trailing edges from a string
        :param Line: The string to be cleaned
        :returns: cleaned string 
        '''
        logging.debug(self.__className+'.remTabSpace')
        value = re.sub(r'^\s+|\s+$', '', line ) 
        return value
    
    def remTabSpaceQuot(self, line):
        '''
        :method: Removes from a string all leading, trailing spaces tabs and quotations
        :param Line: The string to be cleaned
        :returns: cleaned string 
        '''
        logging.debug(self.__className+'.remTabSpaceQuot')
        line = self.remTabSpace(line)
        line = re.sub(r'^\"+|\"+$', '', line )
        return line
    
    def splitLine(self, line):
        '''
        :method: Splits lines with multiple values into a list of values delimiters could be spaces and tabs
        :param line: The line to be split
        :returns: a list of values 
        '''
        logging.debug(self.__className+'.splitLine')
        line = self.remTabSpace(line) # remove leadind and trailing waste
        values = re.split(r'[\t\s]\s*', line)
        return values
    
    class WingModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the wing itself. 
        '''
        __className = 'WingModel'

        BrandNameCol = 1
        ''':attr: number of the brand name column'''
        WingNameCol = 2
        ''':attr: number of the wing name column'''
        DrawScaleCol = 3
        ''':attr: number of the draw scale column'''
        WingScaleCol = 4
        ''':attr: number of the wing scale column'''
        NumCellsCol = 5
        ''':attr: number of the number of cells column'''
        NumRibsCol = 6
        ''':attr: number of the number of ribs column'''
        AlphaModeCol = 7
        ''':attr: number of the alpha type column'''
        AlphaMaxCentCol = 8
        ''':attr: number of the alpha max angle in center column'''
        AlphaMaxTipCol = 9
        ''':attr: number of the alpha max angle on wingtip column'''
        ParaTypeCol = 10
        ''':attr: number of the paraglider type column'''
        ParaParamCol = 11
        ''':attr: number of the column holding the parameter attached to paraglider type'''
        halfNumRibs = 0
        ''':attr: the number of different ribs needed to build the wing. This is more or less the half number of total ribs.'''

        def createWingTable(self): 
            '''
            :method: cereates initially the empty wing table
            '''   
            logging.debug(self.__className+'.createWingTable')
                
            query = QSqlQuery()
            query.exec("DROP TABLE if exists Wing;")
            query.exec("create table if not exists Wing ("
                    "ID INTEGER PRIMARY KEY,"
                    "BrandName TEXT,"
                    "WingName TEXT,"
                    "DrawScale REAL,"
                    "WingScale REAL,"
                    "NumCells INTEGER,"
                    "NumRibs INTEGER,"
                    "AlphaMode INTEGER,"
                    "AlphaMaxCent REAL,"
                    "AlphaMaxTip REAL,"
                    "ParaType TEXT,"
                    "ParaParam INTEGER);")
            query.exec("INSERT into Wing (ID) Values( '1' );")

        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createWingTable()
            self.setTable("Wing")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.rib_M = ProcessorModel.RibModel()
            self.airf_M = ProcessorModel.AirfoilsModel()
            self.dataChanged.connect(self.syncData)
             
        def syncData(self, q):
            '''
            :method: If NumRibs is changed we must keep halfNumRibs and Ribs table in sync. This method will calculate the current number of half ribs and calls the method to setup the model accordingly. 
            '''
            # 
            logging.debug(self.__className+'.syncData')
            
            if q.column() == self.NumRibsCol:
                numRibs = self.index(0, self.NumRibsCol).data()
                if numRibs.isnumeric():
                    self.halfNumRibs = math.ceil(float(numRibs) / 2)
                    logging.debug(self.__className+'.syncData ' + 'halfNumRibs: ' +str(self.halfNumRibs))
                    
                    self.rib_M.setupRibRows(self.halfNumRibs)
                    self.airf_M.setupRibRows(self.halfNumRibs)
    
    class RibModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the individual ribs. 
        '''
        __className = 'RibModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        RibNumCol = 0
        ''':attr: number of the rib number column'''
        xribCol = 1
        ''':attr: number of the column providing rib X coordinate'''
        yLECol = 2
        ''':attr: number of the column providing Y coordinate of the leading edge'''
        yTECol = 3
        ''':attr: number of the column providing Y coordinate of the trailing edge'''
        xpCol = 4
        ''':attr: number of the column providing X' coordinate of the rib in its final position in space'''
        zCol = 5
        ''':attr: number of the column providing Z coordinate of the rib in its final position in space '''
        betaCol = 6
        ''':attr: number of the column providing the angle "beta" of the rib to the vertical (degres)'''
        RPCol = 7
        ''':attr: number of the column providing RP percentage of chord to be held on the relative torsion of the airfoils'''
        WashinCol = 8
        ''':attr: number of the column providing washin in degrees defined manually (if parameter is set to "0")'''
        
        def createRibTable(self):
            '''
            :method: cereates initially the empty rib table
            ''' 
            logging.debug(self.__className+'.createRibTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists Rib;")
            query.exec("create table if not exists Rib ("
                    "RibNum INTEGER,"
                    "xrib REAL,"
                    "yLE REAL,"
                    "yTE REAL,"
                    "xp REAL,"
                    "z REAL,"
                    "beta REAL,"
                    "RP REAL,"
                    "Washin REAL,"
                    "ID INTEGER);")
            query.exec("INSERT into Rib (ID) Values( '1' );")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createRibTable()
            self.setTable("Rib")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)


    class AirfoilsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the individual ribs. 
        '''
        __className = 'AirfoilsModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        RibNumCol = 0
        ''':attr: number of the rib number column'''
        AirfNameCol = 1
        IntakeStartCol = 2 
        IntakeEndCol = 3
        OpenCloseCol = 4
        DisplacCol = 5
        RelWeightCol = 6
        rrwCol = 7
        
        
        def createAirfoilsTable(self):
            '''
            :method: cereates initially the empty rib table
            ''' 
            logging.debug(self.__className+'.createAirfoilsTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists Airfoils;")
            query.exec("create table if not exists Airfoils ("
                    "RibNum INTEGER,"
                    "AirfName TEXT,"
                    "IntakeStart REAL,"
                    "IntakeEnd REAL,"
                    "OpenClose INTEGER,"
                    "Displac REAL,"
                    "RelWeight REAL,"
                    "rrw REAL,"
                    "ID INTEGER);")
            query.exec("INSERT into Airfoils (ID) Values( '1' );")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createAirfoilsTable()
            self.setTable("Airfoils")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
