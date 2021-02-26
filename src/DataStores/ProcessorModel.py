# https://doc.qt.io/qtforpython/overviews/sql-model.html
# https://www.datacamp.com/community/tutorials/inner-classes-python
'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to the authors of:

https://doc.qt.io/qtforpython/overviews/sql-model.html

https://www.datacamp.com/community/tutorials/inner-classes-python
'''
import logging
import math
import re

from PyQt5.QtCore import QFile, QTextStream, QObject, pyqtSignal, QSortFilterProxyModel, QRegExp
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
        self.anchPoints_M = self.AnchorPointsModel()
        self.lightC_M = self.LightConfModel()
        self.lightD_M = self.LightDetModel()
        self.skinTens_M = self.SkinTensionModel()
        self.skinTensParams_M = self.SkinTensionParamsModel()
        self.sewAll_M = self.SewingAllowancesModel()
        
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
        logging.debug(self.__className+'.readFile: Brand name')
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.BrandNameCol ), self.remTabSpaceQuot(line) )

        # Wing name
        logging.debug(self.__className+'.readFile: Wing name')
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.WingNameCol), self.remTabSpaceQuot(line) )
        
        # Draw scale
        logging.debug(self.__className+'.readFile: Draw scale')
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.DrawScaleCol), self.remTabSpace( line ) )
        
        # Wing scale
        logging.debug(self.__className+'.readFile: Wing scale')
        line = stream.readLine()
        # self.setSingleVal('WingScale', self.remTabSpace( stream.readLine() ) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.WingScaleCol), self.remTabSpace( stream.readLine() ) )
        
        # Number of cells
        logging.debug(self.__className+'.readFile: Number of cells')
        line = stream.readLine()
        # self.setSingleVal('NumCells', self.remTabSpace( stream.readLine() ) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.NumCellsCol), self.remTabSpace( stream.readLine() ) )
        
        # Number of Ribs
        logging.debug(self.__className+'.readFile: Number of ribs')
        line = stream.readLine()
        # self.setSingleVal('NumRibs', self.remTabSpace( stream.readLine() ) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.NumRibsCol), self.remTabSpace( stream.readLine() ) )

        # Alpha max and parameter
        logging.debug(self.__className+'.readFile: Alpha max and parameter')
        line = stream.readLine()
        values =  self.splitLine( stream.readLine() )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaMaxTipCol), values[0] )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaModeCol), values[1] )
        if len(values) > 2: 
            self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaMaxCentCol), values[2] )
        else:
            self.wing_M.setData(self.wing_M.index(0, self.WingModel.AlphaMaxCentCol), '' )
        
        # Paraglider type and parameter
        logging.debug(self.__className+'.readFile: Paraglider type and parameter')
        line = stream.readLine()
        values =  self.splitLine( stream.readLine() )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.ParaTypeCol), self.remTabSpaceQuot( values[0]) )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.ParaParamCol), values[1])
        
        # Rib geometric parameters
        logging.debug(self.__className+'.readFile: Rib geometric parameters')
        # Rib    x-rib    y-LE    y-TE    xp    z    beta    RP    Washin
        line = stream.readLine()
        line = stream.readLine()

        for i in range( 0, self.wing_M.halfNumRibs ):
            values =  self.splitLine( stream.readLine() )
            for y in range(0, 9):
                self.rib_M.setData(self.rib_M.index(i, y), values[y] )
        
        ##############################
        # 2. AIRFOILS
        logging.debug(self.__className+'.readFile: Airfoils')
        for i in range(4):
            line = stream.readLine()
        
        for i in range( 0, self.wing_M.halfNumRibs ):
            values =  self.splitLine( stream.readLine() )
            for y in range(0, 8):
                self.airf_M.setData(self.airf_M.index(i, y), values[y] )
        
        ##############################
        # 3. ANCHOR POINTS
        logging.debug(self.__className+'.readFile: Anchor points')
        # Just overreading the lines for temporary testing
        for i in range(4):
            line = stream.readLine()
            
        for i in range( 0, self.wing_M.halfNumRibs ):
            values =  self.splitLine( stream.readLine() )
            for y in range(0, 8):
                self.anchPoints_M.setData(self.anchPoints_M.index(i, y), values[y] )
            
        ##############################
        # 4. RIB HOLES
        logging.debug(self.__className+'.readFile: Rib holes')
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int(self.remTabSpace( stream.readLine() ))
        self.lightC_M.setNumConfigs( numConfigs )
        for i in range( 0, numConfigs ):
            ini = int(self.remTabSpace( stream.readLine()))
            fin = int(self.remTabSpace( stream.readLine()))
            self.lightC_M.updateConfigRow(i+1, ini, fin)
            
            numConfigLines = int(self.remTabSpace( stream.readLine() ))
            self.lightD_M.setNumDetailRows(i+1, numConfigLines )
            
            # ConfigNum, orderNum, LightTyp, DistLE, DisChord, HorAxis, VertAxis, RotAngle, Opt1
            for l in range(0, numConfigLines):
                values =  self.splitLine( stream.readLine() )
                self.lightD_M.updateDetRow(i+1, l+1, float(values[0]), \
                                        float(values[1]), \
                                        float(values[2]), \
                                        float(values[4]), \
                                        float(values[5]), \
                                        float(values[6]), \
                                        float(values[7]))

        ##############################
        # 5. SKIN TENSION
        logging.debug(self.__className+'.readFile: Skin tension')
        for i in range(4):
            line = stream.readLine()
        
        for l in range(0, 6 ):
            values =  self.splitLine( stream.readLine() )
            self.skinTens_M.updateRow(l+1, values[0], values[1], values[2], values[3])

        val = self.remTabSpace( stream.readLine() )
        self.skinTensParams_M.setData(self.skinTensParams_M.index(0, ProcessorModel.SkinTensionParamsModel.StrainMiniRibsCol), val )        
                          
        values = self.splitLine( stream.readLine() )
        self.skinTensParams_M.setData(self.skinTensParams_M.index(0, ProcessorModel.SkinTensionParamsModel.NumPointsCol), values[0] )
        self.skinTensParams_M.setData(self.skinTensParams_M.index(0, ProcessorModel.SkinTensionParamsModel.CoeffCol), values[0] )
        
        ##############################
        # 6. SEWING ALLOWANCES
        logging.debug(self.__className+'.readFile: Sewing allowances')
        for i in range(3):
            line = stream.readLine()
            
        for l in range(0, 2 ):
                values =  self.splitLine( stream.readLine() )
                self.sewAll_M.updateRow(l+1, values[0], values[1], values[2])
        
        values = self.splitLine( stream.readLine() )
        self.sewAll_M.updateRow(3, values[0])
        values = self.splitLine( stream.readLine() )
        self.sewAll_M.updateRow(4, values[0])
        
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
        :class: Provides a SqlTableModel holding all data related to the wing itself. 
        '''
        __className = 'WingModel'

        BrandNameCol = 0
        ''':attr: number of the brand name column'''
        WingNameCol = 1
        ''':attr: number of the wing name column'''
        DrawScaleCol = 2
        ''':attr: number of the draw scale column'''
        WingScaleCol = 3
        ''':attr: number of the wing scale column'''
        NumCellsCol = 4
        ''':attr: number of the number of cells column'''
        NumRibsCol = 5
        ''':attr: number of the number of ribs column'''
        AlphaModeCol = 6
        ''':attr: number of the alpha type column'''
        AlphaMaxCentCol = 7
        ''':attr: number of the alpha max angle in center column'''
        AlphaMaxTipCol = 8
        ''':attr: number of the alpha max angle on wingtip column'''
        ParaTypeCol = 9
        ''':attr: number of the paraglider type column'''
        ParaParamCol = 10
        ''':attr: number of the column holding the parameter attached to paraglider type'''
        
        halfNumRibs = 0
        ''':attr: the number of different ribs needed to build the wing. This is more or less the half number of total ribs.'''

        def createWingTable(self): 
            '''
            :method: Creates initially the empty wing table
            '''   
            logging.debug(self.__className+'.createWingTable')
                
            query = QSqlQuery()
            query.exec("DROP TABLE if exists Wing;")
            query.exec("create table if not exists Wing ("
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
                    "ParaParam INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
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
            self.anchPoints_M = ProcessorModel.AnchorPointsModel()
            self.airf_M = ProcessorModel.AirfoilsModel()
            self.lightC_M = ProcessorModel.LightConfModel()
            self.dataChanged.connect(self.syncData)
             
        def syncData(self, q):
            '''
            :method: If NumRibs is changed we must keep halfNumRibs and Ribs table in sync. This method will calculate \
                the current number of half ribs and calls the method to setup the model accordingly. If NumLightConf is changed \ 
                the NumLightConf Model must be keept in sync.
            '''
            logging.debug(self.__className+'.syncData')
            
            if q.column() == self.NumRibsCol:
                numRibs = self.index(0, self.NumRibsCol).data()
                if numRibs.isnumeric():
                    self.halfNumRibs = math.ceil(float(numRibs) / 2)
                    logging.debug(self.__className+'.syncData ' + 'halfNumRibs: ' +str(self.halfNumRibs))
                    
                    self.rib_M.setupRibRows(self.halfNumRibs)
                    self.airf_M.setupRibRows(self.halfNumRibs)
                    self.anchPoints_M.setupRibRows(self.halfNumRibs)

    
    class RibModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to the individual ribs. 
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
            :method: Creates initially the empty rib table.
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
                    "ID INTEGER PRIMARY KEY);")
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
        :class: Provides a SqlTableModel holding all data related to the individual ribs. 
        '''
        __className = 'AirfoilsModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        RibNumCol = 0
        ''':attr: number of the rib number column'''
        AirfNameCol = 1
        ''':attr: number of the rib name column'''
        IntakeStartCol = 2 
        ''':attr: number of the intake start column'''
        IntakeEndCol = 3
        ''':attr: number of the intake end column'''
        OpenCloseCol = 4
        ''':attr: number of the column for the open/ close config'''
        DisplacCol = 5
        ''':attr: number of the column for the displacement'''
        RelWeightCol = 6
        ''':attr: number of the column for the relative weight '''
        rrwCol = 7
        ''':attr: number of the column for the rrw config'''
        
        
        def createAirfoilsTable(self):
            '''
            :method: Creates initially the empty anchor points table
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
                    "ID INTEGER PRIMARY KEY);")
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
            
    class AnchorPointsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to the Anchor points. 
        '''
        __className = 'AnchorPointsModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        RibNumCol = 0
        ''':attr: Number of the rib number column'''
        NumAnchCol = 1
        ''':attr: Number of the column holding the number of anchors'''
        PosACol = 2
        ''':attr: Number the column holding Pos A'''
        PosBCol = 3
        ''':attr: Number the column holding Pos B'''
        PosCCol = 4
        ''':attr: Number the column holding Pos C'''
        PosDCol = 5
        ''':attr: Number the column holding Pos D'''
        PosECol = 6
        ''':attr: Number the column holding Pos E'''
        PosFCol = 7
        ''':attr: Number the column holding Pos F'''
        
        def createAnchorPointsTable(self):
            '''
            :method: Creates initially the empty anchor points table
            ''' 
            logging.debug(self.__className+'.createAnchorPointsTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists AnchorPoints;")
            query.exec("create table if not exists AnchorPoints ("
                    "RibNum INTEGER,"
                    "NumAnchors INTEGER,"
                    "PosA REAL,"
                    "PosB REAL,"
                    "PosC REAL,"
                    "PosD REAL,"
                    "PosE REAL,"
                    "PosF REAL,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createAnchorPointsTable()
            self.setTable("AnchorPoints")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
    class LightConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the global lightening config parameters 
        '''
        
        numConfigsChanged = pyqtSignal(int)
        '''
        :Signal: emitted in the moment the number of configurations handled by the model ist changed. \
        Param1: new number of configurations. 
        '''
        
        __className = 'LightConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        __numConfigs = 0
        
        InitialRibCol = 0
        ''':attr: number of the column holding the first rib of the config'''
        FinalRibCol = 1 
        ''':attr: number of the column holding the final rib'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''
        
        def createLightConfTable(self):
                '''
                :method: Creates initially the empty LightConf table.
                ''' 
                logging.debug(self.__className+'.createLightConfTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists LightConf;")
                query.exec("create table if not exists LightConf ("
                        "InitialRib INTEGER,"
                        "FinalRib INTEGER,"
                        "ConfigNum INTEGER,"
                        "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createLightConfTable()
            self.setTable("LightConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
        def addConfigRow(self):
            '''
            :method: Adds an individual configuration.
            '''
            logging.debug(self.__className+'.addConfigRow')
            currNumRows = self.rowCount()
                
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("INSERT into LightConf (ConfigNum) Values( :conf);")
            query.bindValue(":conf", currNumRows+1 )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
        
        def updateConfigRow(self, config, initialRib, finalRib):
            logging.debug(self.__className+'.setConfigRow')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE LightConf SET InitialRib= :initial , FinalRib= :final WHERE (ConfigNum = :config);")
            query.bindValue(":initial", initialRib )
            query.bindValue(":final", finalRib )
            query.bindValue(":config", config )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def removeRowsByConfigNum(self, configNum ):
            '''
            :method: Removes an individual configuration.
            :param configNum: Number of the config to be deleted.  
            '''
            logging.debug(self.__className+'.removeRowsByConfigNum')
            
            # TODO: add transaction
            query = QSqlQuery()
            query.prepare("DELETE FROM LightConf where ConfigNum = :num ")
            query.bindValue(":num", str(configNum))
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def setNumConfigs(self, mustNumConfigs):
            '''
            :method: Assures the model will be setup to hold the correct number of configs based on parameters passed. 
            :param mustNumConfigs: Number of configs the model must provide.
            '''
            logging.debug(self.__className+'.setNumConfigs')
            currNumConfigs = self.numConfigs()
            
            diff = abs(mustNumConfigs-currNumConfigs)
            if diff != 0:
                # do it only if really the number has changed
                i = 0
                if mustNumConfigs > currNumConfigs:
                    # add config lines
                    while i < diff:
                        self.addConfigRow()
                        i += 1
                else:
                    # remove config lines
                    while i < diff:
                        self.removeRowsByConfigNum( currNumConfigs-i )
                        i += 1
                
                # emit the change signal
                self.numConfigsChanged.emit( self.numConfigs() )
                
        def numConfigs(self):
            '''
            :method: Use this to check how many configs the model currently holds
            :return: Current number of configs.
            '''     
            return self.rowCount()
                
            
         

    class LightDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to the indivudual lightening config parameters.
        '''
        numDetailsChanged = pyqtSignal(int, int)
        '''
        :Signal: Emitted at the moment the number of data lines in the model is changed. \
        Param 1: the configuration number which has changed \
        Param2: new number of data lines
        '''
        
        __className = 'LightDetModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a confit'''
        LightTypCol = 1 
        ''':attr: num of column for 1..3: hole type info'''
        DistLECol = 2
        ''':attr: num of column for 1..3: distance from LE to hole center in% chord '''
        DisChordCol = 3
        ''':attr: num of column for 1..3: distance from the center of hole to the chord line in% of chord'''
        HorAxisCol = 4
        ''':attr: num of column for 1..2: horizontal axis of the ellipse as% of chord; 3: traingle base as% of chord'''
        VertAxisCol = 5
        ''':attr: num of column for 1..2: ellipse vertical axis as% of chord; 3: triangle heigth as% of chord'''
        RotAngleCol = 6
        ''':attr: num of column 1..3:  for rotation angle of the ellipse'''
        Opt1Col = 7
        ''':attr: num of column 1: na; 2:  central strip width; 3: Radius of the smoothed corners'''
        ConfigNumCol = 8
        ''':attr: num of column for 1..3: config number'''
        
        def createLightDetTable(self):
                '''
                :method: Creates initially the empty lightening details table.
                ''' 
                logging.debug(self.__className+'.createLightDetTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists LightDet;")
                query.exec("create table if not exists LightDet ("
                        "OrderNum INTEGER,"
                        "LightTyp INTEGER,"
                        "DistLE REAL,"
                        "DisChord REAL,"
                        "HorAxis REAL,"
                        "VertAxis REAL,"
                        "RotAngle REAL,"
                        "Opt1 REAL,"
                        "ConfigNum INTEGER,"
                        "ID INTEGER PRIMARY KEY);")
                query.exec("INSERT into LightDet (ConfigNum, OrderNum) Values( '1', '1' );")
                
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createLightDetTable()
            self.setTable("LightDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
        def addDetailRow(self, configNum):
            '''
            :method: Adds a row to the model. Takes care about the initial setup of some row values. 
            :parm configNum: Number of the config for which the row must be added.
            '''
            logging.debug(self.__className+'.addConfigRow')

            currNumRows = self.numDetailRows(configNum)
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("INSERT into LightDet (ConfigNum, OrderNum) Values( :conf, :order);")
            query.bindValue(":conf", str(configNum))
            query.bindValue(":order", str(currNumRows+1))
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def updateDetRow(self, ConfigNum, orderNum, LightTyp, DistLE, DisChord, HorAxis, VertAxis, RotAngle, Opt1):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.setConfigRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            #query.prepare("UPDATE LightDet SET LightTyp= :light, DistLE= :dist, DisChord= :dis, HorAxis= :hor, VertAxis= :vert, RotAngle: rot, Opt= :opt WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.prepare("UPDATE LightDet SET LightTyp= :light, "
                          "DistLE= :dist, DisChord= :dis, HorAxis= :hor, "
                          "VertAxis= :vert, RotAngle= :rot, Opt1= :opt1 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":light", LightTyp )
            query.bindValue(":dist", DistLE )
            query.bindValue(":dis", DisChord )
            query.bindValue(":hor", HorAxis )
            query.bindValue(":vert", VertAxis )
            query.bindValue(":rot", RotAngle )
            query.bindValue(":opt1", Opt1 )
            query.bindValue(":config", ConfigNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly


        def removeLastDetailRow(self, configNum):
            '''
            :method: Removes the last detail row from the model.
            :param configNum: Number of the config for which the row must be deleted.  
            '''
            logging.debug(self.__className+'.removeDetailRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select ConfigNum, OrderNum FROM LightDet WHERE ConfigNum = :conf ORDER BY OrderNum ASC")
            query.bindValue(":conf", str(configNum))
            query.exec()
            orderNum = 0
            while (query.next()):
                orderNum = query.value(1)
            
            if orderNum>0:
                query.prepare("DELETE FROM LightDet WHERE (ConfigNum = :conf AND OrderNum = :order);")
                query.bindValue(":conf", str(configNum))
                query.bindValue(":order", str(orderNum))
                query.exec()
                self.select() # to a select() to assure the model is updated properly
            
            
        def setNumDetailRows(self, configNum, mustNumDetailRows):
            '''
            :method: Assures the model will be setup to hold the correct number of rows based on parameters passed. 
            :param configNum: Number of the config for which the row must be deleted.
            :param mustNumDetailRows: Number of rows the model must provide.
            '''
            logging.debug(self.__className+'.setNumDetails')
            
            currNumDetailRows = self.numDetailRows(configNum)
            diff = abs(mustNumDetailRows-currNumDetailRows)
            
            
            if diff != 0:
                # do it only if really the number has changed
                i = 0
                if mustNumDetailRows > currNumDetailRows:
                    # add config lines
                    while i < diff:
                        self.addDetailRow(configNum)
                        i += 1
                else:
                    # remove config lines
                    while i < diff:
                        self.removeLastDetailRow( configNum )
                        i += 1
                
                # emit the change signal
                self.numDetailsChanged.emit(configNum, self.numDetailRows(configNum))
        
        def numDetailRows(self, configNum):
            '''
            :method: Use this to check how many rows a specific config holds currently.
            :param configNum: Number of the config for which the number of rows must be returned.
            :return: Current number of rows.
            '''
            logging.debug(self.__className+'.getNumDetailLines')
            
            proxyModel = QSortFilterProxyModel()
            proxyModel.setSourceModel(self)
            proxyModel.setFilterKeyColumn(ProcessorModel.LightDetModel.ConfigNumCol)
            proxyModel.setFilterRegExp( QRegExp( str(configNum) ) )
            return proxyModel.rowCount()
    
    class SkinTensionModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to Skin tension. 
        '''
        __className = 'SkinTensionModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        TopDistLECol = 0
        ''':attr: Distance in% of chord on the leading edge of extrados'''
        TopWideCol = 1
        ''':attr: Extrados over-wide corresponding in % of chord'''
        BottDistTECol = 2
        ''':attr: Distance in% of chord on trailing edge'''
        BottWideCol = 3
        ''':attr: Intrados over-wide corresponding in% of chord'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Skin tension table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists SkinTension;")
            query.exec("create table if not exists SkinTension ("
                    "TopDistLE REAL,"
                    "TopWide REAL,"
                    "BottDistTE REAL,"
                    "BottWide REAL,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SkinTension")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            self.addRows(-1, 6)
        
        def updateRow(self, row, topDistLE, topWide, bottDistTE, bottWide):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: add transaction
            query = QSqlQuery()
            query.prepare("UPDATE SkinTension SET TopDistLE= :topDis, TopWide= :topWide, BottDistTE= :bottDis, BottWide= :bottWide  WHERE (ID = :id);")
            query.bindValue(":topDis", topDistLE )
            query.bindValue(":topWide", topWide )
            query.bindValue(":bottDis", bottDistTE )
            query.bindValue(":bottWide", bottWide )
            query.bindValue(":id", row )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

    class SkinTensionParamsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the three individual params of the Skin tension setup. 
        '''
        __className = 'SkinTensionParamsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        StrainMiniRibsCol = 0
        ''':attr: Parameter to control the mini ribs'''
        NumPointsCol = 1
        ''':attr: Number of points'''
        CoeffCol = 2
        ''':attr: The coefficient'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Skin tension params table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists SkinTensionParams;")
            query.exec("create table if not exists SkinTensionParams ("
                    "StrainMiniRibs REAL,"
                    "NumPoints Integer,"
                    "Coeff REAL,"
                    "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into SkinTensionParams (StrainMiniRibs, NumPoints, Coeff,  ID) Values( '0.0114', '1000', '1.0', 1 );")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SkinTensionParams")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
    class SewingAllowancesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Sewing allowances parameters. 
        '''
        __className = 'SewingAllowancesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        EdgeSeamCol = 0
        ''':attr: Number of the col holding the Edge seem values'''
        LeSeemCol = 1
        ''':attr: Number of the col holding the LE seem values'''
        TeSeemCol = 2
        ''':attr: Number of the col holding the TE seem values'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Sewing allowances table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists SewingAllowances;")
            query.exec("create table if not exists SewingAllowances ("
                    "EdgeSeam Integer,"
                    "LESeem Integer,"
                    "TESeem Integer,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SewingAllowances")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            self.addRows(-1, 4)
        
        def updateRow(self, row, edgeSeam, leSeem=0, teSeem=0):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: add transaction
            query = QSqlQuery()
            query.prepare("UPDATE SewingAllowances SET EdgeSeam= :edgeSeam, LESeem= :lESeem, TESeem= :tESeem WHERE (ID = :id);")
            query.bindValue(":edgeSeam", edgeSeam )
            query.bindValue(":lESeem", leSeem )
            query.bindValue(":tESeem", teSeem )
            query.bindValue(":id", row )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
        