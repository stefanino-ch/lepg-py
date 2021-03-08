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

from PyQt5.QtCore import Qt, QFile, QTextStream, QObject, pyqtSignal
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
        self.marks_M = self.MarksModel()
        self.globAoA_M = self.GlobAoAModel()
        self.lines_M = self.LinesModel()
        self.brakes_M = self.BrakesModel()
        self.brakeL_M = self.BrakeLengthModel()
        self.ramif_M = self.RamificationModel()
        self.hVvHRibs_M = self.HvVhRibsModel()
        
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
        counter = 0
        while counter < 4:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1
        
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
            self.lightD_M.setNumRowsForConfig(i+1, 0 )
            self.lightD_M.setNumRowsForConfig(i+1, numConfigLines )
            
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
        logging.debug(self.__className+'.readFile: Seewing allowances')
        for i in range(3):
            line = stream.readLine()
            
        for l in range(0, 2 ):
                values =  self.splitLine( stream.readLine() )
                self.sewAll_M.updateRow(l+1, values[0], values[1], values[2])
        
        values = self.splitLine( stream.readLine() )
        self.sewAll_M.updateRow(3, values[0])
        values = self.splitLine( stream.readLine() )
        self.sewAll_M.updateRow(4, values[0])
        
        ##############################
        # 7. MARKS
        logging.debug(self.__className+'.readFile: Marks')
        for i in range(3):
            line = stream.readLine()
            
        values = self.splitLine( stream.readLine() )
        self.marks_M.updateRow(values[0], values[1], values[1])
        
        ##############################
        # 8. Global angle of attack estimation
        logging.debug(self.__className+'.readFile: Global AoA')
        for i in range(3):
            line = stream.readLine()
            
        line = stream.readLine()
        self.globAoA_M.setData(self.globAoA_M.index(0, self.GlobAoAModel.FinesseCol), self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.globAoA_M.setData(self.globAoA_M.index(0, self.GlobAoAModel.CentOfPressCol), self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.globAoA_M.setData(self.globAoA_M.index(0, self.GlobAoAModel.CalageCol), self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.globAoA_M.setData(self.globAoA_M.index(0, self.GlobAoAModel.RisersCol), self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.globAoA_M.setData(self.globAoA_M.index(0, self.GlobAoAModel.LinesCol), self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.globAoA_M.setData(self.globAoA_M.index(0, self.GlobAoAModel.KarabinersCol), self.remTabSpace( stream.readLine() ) )
        
        ##############################
        # 9. SUSPENSION LINES DESCRIPTION
        logging.debug(self.__className+'.readFile: Lines')
        for i in range(3):
            line = stream.readLine()
        
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.LinesConcTypeCol ), self.remTabSpace( stream.readLine() ) )
        
        numConfigs = int(self.remTabSpace( stream.readLine()))
        
        for i in range( 0, numConfigs ):
            numConfigLines = int( self.remTabSpace( stream.readLine() ) )
            self.lines_M.setNumRowsForConfig(i+1, 0 )
            self.lines_M.setNumRowsForConfig(i+1, numConfigLines )
             
            for l in range(0, numConfigLines):
                values =  self.splitLine( stream.readLine() )
                self.lines_M.updateLineRow(i+1, l+1, \
                                        values[0], \
                                        values[1], \
                                        values[2], \
                                        values[3], \
                                        values[4], \
                                        values[5], \
                                        values[6], \
                                        values[7], \
                                        values[8], \
                                        values[9], \
                                        values[10] )
        
        ##############################
        # 10. BRAKES
        logging.debug(self.__className+'.readFile: Brakes')
        for i in range(3):
            line = stream.readLine()
        
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.BrakeLengthCol ), self.remTabSpace( stream.readLine() ) )
        
        # delete existing data
        self.brakes_M.setNumRowsForConfig(1, 0 )
        
        # read new data
        numConfigLines = int( self.remTabSpace( stream.readLine() ) )
        self.brakes_M.setNumRowsForConfig(1, numConfigLines )
        
        for l in range(0, numConfigLines):
            values =  self.splitLine( stream.readLine() )
            self.brakes_M.updateBrakeRow(1, l+1, \
                                        values[0], \
                                        values[1], \
                                        values[2], \
                                        values[3], \
                                        values[4], \
                                        values[5], \
                                        values[6], \
                                        values[7], \
                                        values[8], \
                                        values[9], \
                                        values[10] )   
        
        line = stream.readLine()
        
        for c in range(0, 2):
            values =  self.splitLine( stream.readLine() )
            
            for p in range (0, 5):
                self.brakeL_M.setData(self.brakeL_M.index(0, p + (c*5) ), values[p] )

        ##############################
        # 11. Ramification lengths
        logging.debug(self.__className+'.readFile: Ramification')
        for i in range(3):
            line = stream.readLine()
        
        values =  self.splitLine( stream.readLine() )
        self.ramif_M.updateDataRow(1, 1, values[0], values[1], 0)
        
        values =  self.splitLine( stream.readLine() )
        self.ramif_M.updateDataRow(1, 2, values[0], values[1], values[2])
                    
        values =  self.splitLine( stream.readLine() )
        self.ramif_M.updateDataRow(1,3, values[0], values[1], 0)
            
        values =  self.splitLine( stream.readLine() )
        self.ramif_M.updateDataRow(1, 4, values[0], values[1], values[2])

        ##############################
        # 12. H V and VH ribs (Mini Ribs)
        logging.debug(self.__className+'.readFile: H V and VH ribs (Mini Ribs)')
        for i in range(3):
            line = stream.readLine()
        
        numConfigLines = int(self.remTabSpace( stream.readLine() ) )
        
        values =  self.splitLine( stream.readLine() )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.xSpacingCol ), values[0] )
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.ySpacingCol ), values[1] )
        
        # delete existing data
        self.hVvHRibs_M.setNumRowsForConfig(1, 0 )
        # read new data
        self.hVvHRibs_M.setNumRowsForConfig(1, numConfigLines )
        
        for l in range(0, numConfigLines):
            values =  self.splitLine( stream.readLine() )
            if (values[1] == '6') or (values[1] == '16'):
                self.hVvHRibs_M.updateDataRow(1, l+1, \
                                        values[0], \
                                        values[1], \
                                        values[2], \
                                        values[3], \
                                        values[4], \
                                        values[5], \
                                        values[6], \
                                        values[7], \
                                        values[8], \
                                        values[9], \
                                        values[10], \
                                        values[11])
            else:
                self.hVvHRibs_M.updateDataRow(1, l+1, \
                                        values[0], \
                                        values[1], \
                                        values[2], \
                                        values[3], \
                                        values[4], \
                                        values[5], \
                                        values[6], \
                                        values[7], \
                                        values[8], \
                                        values[9])
    
        
        ##############################
        # Cleanup
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

    class BrakesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the lines parameters. 
        '''
        __className = 'BrakesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a confit'''
        NumBranchesCol = 1
        ''':attr: Number of the col holding the number of branches'''
        BranchLvlOneCol = 2
        ''':attr: Number of the col holding the branching level 1 value'''
        OrderLvlOneCol = 3
        ''':attr: Number of the col holding order at level 1 value'''
        LevelOfRamTwoCol = 4
        ''':attr: Number of the col holding level of ramification 2 value'''
        OrderLvlTwoCol = 5
        ''':attr: Number of the col holding order at level 2 value'''
        LevelOfRamThreeCol = 6
        ''':attr: Number of the col holding level of ramification 3 value'''
        OrderLvlThreeCol = 7
        ''':attr: Number of the col holding order at level 3 value'''
        BranchLvlFourCol = 8
        ''':attr: Number of the col holding branching level 4 value'''
        OrderLvlFourCol = 9
        ''':attr: Number of the col holding order at level 4 value'''
        AnchorLineCol = 10
        ''':attr: Number of the col holding the  anchor line (1 = A, 2 = B, 3 = C, 4 = c 5 = D, 6 = brake) value'''
        AnchorRibNumCol = 11
        ''':attr: Number of the col holding the anchor rib number value'''
        ConfigNumCol = 12
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Lines table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists Brakes;")
            query.exec("create table if not exists Brakes ("
                    "OrderNum INTEGER,"
                    "NumBranches INTEGER,"
                    "BranchLvlOne INTEGER,"
                    "OrderLvlOne INTEGER,"
                    "LevelOfRamTwo INTEGER,"
                    "OrderLvlTwo INTEGER,"
                    "LevelOfRamThree INTEGER,"
                    "OrderLvlThree INTEGER,"
                    "BranchLvlFour INTEGER,"
                    "OrderLvlFour INTEGER,"
                    "AnchorLine INTEGER,"
                    "AnchorRibNum INTEGER,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into Brakes (OrderNum, ConfigNum, ID) Values( '1', '1', '1' );")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Brakes")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))                    
            self.setHeaderData(1, Qt.Horizontal, _("num Branches"))
            self.setHeaderData(2, Qt.Horizontal, _("Branch lvl 1"))
            self.setHeaderData(3, Qt.Horizontal, _("Order lvl 1"))
            self.setHeaderData(4, Qt.Horizontal, _("Ramif lvl2"))
            self.setHeaderData(5, Qt.Horizontal, _("Order lvl 2"))
            self.setHeaderData(6, Qt.Horizontal, _("Ramif lvl3"))
            self.setHeaderData(7, Qt.Horizontal, _("Order lvl 3"))
            self.setHeaderData(8, Qt.Horizontal, _("Branch lvl 4"))
            self.setHeaderData(9, Qt.Horizontal, _("Order lvl 4"))
            self.setHeaderData(10, Qt.Horizontal, _("Anchor"))
            self.setHeaderData(11, Qt.Horizontal, _("An. Rib num"))
        
        def updateBrakeRow(self, configNum, orderNum, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateLineRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE Brakes SET "
                          "NumBranches= :i1, "
                          "BranchLvlOne= :i2, "
                          "OrderLvlOne= :i3, "
                          "LevelOfRamTwo= :i4, "
                          "OrderLvlTwo= :i5, "
                          "LevelOfRamThree= :i6, "
                          "OrderLvlThree= :i7, "
                          "BranchLvlFour= :i8, "
                          "OrderLvlFour= :i9, "
                          "AnchorLine= :i10, "
                          "AnchorRibNum= :i11 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":i1", i1 )
            query.bindValue(":i2", i2 )
            query.bindValue(":i3", i3 )
            query.bindValue(":i4", i4 )
            query.bindValue(":i5", i5 )
            query.bindValue(":i6", i6 )
            query.bindValue(":i7", i7 )
            query.bindValue(":i8", i8 )
            query.bindValue(":i9", i9 )
            query.bindValue(":i10", i10 )
            query.bindValue(":i11", i11 )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

    class BrakeLengthModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Marks parameters. 
        '''
        __className = 'BrakeLengthModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        s1Col = 0
        ''':attr: Number of the col holding the s1 value'''
        s2Col = 1
        ''':attr: Number of the col holding the s2 value'''
        s3Col = 2
        ''':attr: Number of the col holding the s3 value'''
        s4Col = 3
        ''':attr: Number of the col holding the s4 value'''
        s5Col = 4
        ''':attr: Number of the col holding the s5 value'''
        d1Col = 5
        ''':attr: Number of the col holding the d1 value'''
        d2Col = 6
        ''':attr: Number of the col holding the d2 value'''
        d3Col = 7
        ''':attr: Number of the col holding the d3 value'''
        d4Col = 8
        ''':attr: Number of the col holding the d4 value'''
        d5Col = 9
        ''':attr: Number of the col holding the d5 value'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Brake length table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists BrakeLenght;")
            query.exec("create table if not exists BrakeLenght ("
                    "s1 INTEGER,"
                    "s2 INTEGER,"
                    "s3 INTEGER,"
                    "s4 INTEGER,"
                    "s5 INTEGER,"
                    "d1 INTEGER,"
                    "d2 INTEGER,"
                    "d3 INTEGER,"
                    "d4 INTEGER,"
                    "d5 INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into BrakeLenght (ID) Values( '1' );")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("BrakeLenght")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(0, Qt.Horizontal, _("s1 [%]"))
            self.setHeaderData(1, Qt.Horizontal, _("s2 [%]"))
            self.setHeaderData(2, Qt.Horizontal, _("s3 [%]"))
            self.setHeaderData(3, Qt.Horizontal, _("s4 [%]"))
            self.setHeaderData(4, Qt.Horizontal, _("s5 [%]"))
            self.setHeaderData(5, Qt.Horizontal, _("d1 [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("d2 [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("d3 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("d4 [cm]"))
            self.setHeaderData(9, Qt.Horizontal, _("d5 [cm]"))

    
            
    class GlobAoAModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the global AoA parameters. 
        '''
        __className = 'GlobAoAModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        FinesseCol = 0
        ''':attr: Number of the col holding the finesse value'''
        CentOfPressCol = 1
        ''':attr: Number of the col holding the center of pressure value'''
        CalageCol = 2
        ''':attr: Number of the col holding the calage value'''
        RisersCol = 3
        ''':attr: Number of the col holding the risers length value'''
        LinesCol = 4
        ''':attr: Number of the col holding the lines length value'''
        KarabinersCol = 5 
        ''':attr: Number of the col holding the karabiners length value'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty GlobalAoA table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists GlobalAoA;")
            query.exec("create table if not exists GlobalAoA ("
                    "Finesse REAL,"
                    "CentOfPress INTEGER,"
                    "Calage INTEGER,"
                    "Risers INTEGER,"
                    "Lines INTEGER,"
                    "Karabiners INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into GlobalAoA (ID) Values( '1' );")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("GlobalAoA")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(0, Qt.Horizontal, _("Finesse [deg]"))
            self.setHeaderData(1, Qt.Horizontal, _("Center of Pressure [%chord]"))
            self.setHeaderData(2, Qt.Horizontal, _("Calage [%chord]"))
            self.setHeaderData(3, Qt.Horizontal, _("Risers [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("Lines [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("Karabiners [cm]"))
    
    class HvVhRibsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the lines parameters. 
        '''
        __className = 'HvVhRibsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a confit'''
        RibNumCol = 1
        ''':attr: Number of the col holding the rib num for which the setup is valid'''
        TypeCol = 2
        ''':attr: Number of the col holding the rib type info'''
        IniRibCol = 3
        ''':attr: Number of the col holding initial rib of the configuration'''
        ParamACol = 4
        ''':attr: Number of the col holding param A'''
        ParamBCol = 5
        ''':attr: Number of the col holding param B'''
        ParamCCol = 6
        ''':attr: Number of the col holding param C'''
        ParamDCol = 7
        ''':attr: Number of the col holding param D'''
        ParamECol = 8
        ''':attr: Number of the col holding param E'''
        ParamFCol = 9
        ''':attr: Number of the col holding param F'''
        ParamGCol = 10
        ''':attr: Number of the col holding param G'''
        ParamHCol = 11
        ''':attr: Number of the col holding param H'''
        ParamICol = 12
        ''':attr: Number of the col holding param I'''
        ConfigNumCol = 13
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Lines table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists HvVhRibs;")
            query.exec("create table if not exists HvVhRibs ("
                    "OrderNum INTEGER,"
                    "RibNum INTEGER,"
                    "Type INTEGER,"
                    "IniRib INTEGER,"
                    "ParamA INTEGER,"
                    "ParamB INTEGER,"
                    "ParamC INTEGER,"
                    "ParamD REAL,"
                    "ParamE REAL,"
                    "ParamF REAL,"
                    "ParamG REAL,"
                    "ParamH REAL,"
                    "ParamI REAL,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("HvVhRibs")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))                    
            self.setHeaderData(1, Qt.Horizontal, _("Rib num"))
            self.setHeaderData(2, Qt.Horizontal, _("Type"))
            self.setHeaderData(3, Qt.Horizontal, _("Ini Rib"))
            self.setHeaderData(4, Qt.Horizontal, _("Param A"))
            self.setHeaderData(5, Qt.Horizontal, _("Param B"))
            self.setHeaderData(6, Qt.Horizontal, _("Param C"))
            self.setHeaderData(7, Qt.Horizontal, _("Param D"))
            self.setHeaderData(8, Qt.Horizontal, _("Param E"))
            self.setHeaderData(9, Qt.Horizontal, _("Param F"))
            self.setHeaderData(10, Qt.Horizontal, _("Param G"))
            self.setHeaderData(11, Qt.Horizontal, _("Param H"))
            self.setHeaderData(12, Qt.Horizontal, _("Param I"))
        
        def updateDataRow(self, configNum, orderNum, ribNum, typ, iniRib, paramA, paramB, paramC, paramD, paramE, paramF, paramG, paramH=0, paramI=0):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateLineRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE HvVhRibs SET "
                          "RibNum= :ribNum, "
                          "Type= :typ, "
                          "IniRib= :iniRib, "
                          "ParamA= :paramA, "
                          "ParamB= :paramB, "
                          "ParamC= :paramC, "
                          "ParamD= :paramD, "
                          "ParamE= :paramE, "
                          "ParamF= :paramF, "
                          "ParamG= :paramG, "
                          "ParamH= :paramH, "
                          "ParamI= :paramI "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":ribNum", ribNum )
            query.bindValue(":typ", typ )
            query.bindValue(":iniRib", iniRib )
            query.bindValue(":paramA", paramA )
            query.bindValue(":paramB", paramB )
            query.bindValue(":paramC", paramC )
            query.bindValue(":paramD", paramD )
            query.bindValue(":paramE", paramE )
            query.bindValue(":paramF", paramF )
            query.bindValue(":paramG", paramG )
            query.bindValue(":paramH", paramH )
            query.bindValue(":paramI", paramI )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

            
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
        # numDetailsChanged = pyqtSignal(int, int)
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

        def updateDetRow(self, configNum, orderNum, LightTyp, DistLE, DisChord, HorAxis, VertAxis, RotAngle, Opt1):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateDetRow')
            
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
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
       
    class LinesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the lines parameters. 
        '''
        __className = 'LinesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        NumBranchesCol = 1
        ''':attr: Number of the col holding the number of branches'''
        BranchLvlOneCol = 2
        ''':attr: Number of the col holding the branching level 1 value'''
        OrderLvlOneCol = 3
        ''':attr: Number of the col holding order at level 1 value'''
        LevelOfRamTwoCol = 4
        ''':attr: Number of the col holding level of ramification 2 value'''
        OrderLvlTwoCol = 5
        ''':attr: Number of the col holding order at level 2 value'''
        LevelOfRamThreeCol = 6
        ''':attr: Number of the col holding level of ramification 3 value'''
        OrderLvlThreeCol = 7
        ''':attr: Number of the col holding order at level 3 value'''
        BranchLvlFourCol = 8
        ''':attr: Number of the col holding branching level 4 value'''
        OrderLvlFourCol = 9
        ''':attr: Number of the col holding order at level 4 value'''
        AnchorLineCol = 10
        ''':attr: Number of the col holding the  anchor line (1 = A, 2 = B, 3 = C, 4 = c 5 = D, 6 = brake) value'''
        AnchorRibNumCol = 11
        ''':attr: Number of the col holding the anchor rib number value'''
        ConfigNumCol = 12
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Lines table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists Lines;")
            query.exec("create table if not exists Lines ("
                    "OrderNum INTEGER,"
                    "NumBranches INTEGER,"
                    "BranchLvlOne INTEGER,"
                    "OrderLvlOne INTEGER,"
                    "LevelOfRamTwo INTEGER,"
                    "OrderLvlTwo INTEGER,"
                    "LevelOfRamThree INTEGER,"
                    "OrderLvlThree INTEGER,"
                    "BranchLvlFour INTEGER,"
                    "OrderLvlFour INTEGER,"
                    "AnchorLine INTEGER,"
                    "AnchorRibNum INTEGER,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Lines")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))                    
            self.setHeaderData(1, Qt.Horizontal, _("num Branches"))
            self.setHeaderData(2, Qt.Horizontal, _("Branch lvl 1"))
            self.setHeaderData(3, Qt.Horizontal, _("Order lvl 1"))
            self.setHeaderData(4, Qt.Horizontal, _("Ramif lvl2"))
            self.setHeaderData(5, Qt.Horizontal, _("Order lvl 2"))
            self.setHeaderData(6, Qt.Horizontal, _("Ramif lvl3"))
            self.setHeaderData(7, Qt.Horizontal, _("Order lvl 3"))
            self.setHeaderData(8, Qt.Horizontal, _("Branch lvl 4"))
            self.setHeaderData(9, Qt.Horizontal, _("Order lvl 4"))
            self.setHeaderData(10, Qt.Horizontal, _("Anchor"))
            self.setHeaderData(11, Qt.Horizontal, _("An. Rib num"))
        
        def updateLineRow(self, configNum, orderNum, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateLineRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE Lines SET "
                          "NumBranches= :i1, "
                          "BranchLvlOne= :i2, "
                          "OrderLvlOne= :i3, "
                          "LevelOfRamTwo= :i4, "
                          "OrderLvlTwo= :i5, "
                          "LevelOfRamThree= :i6, "
                          "OrderLvlThree= :i7, "
                          "BranchLvlFour= :i8, "
                          "OrderLvlFour= :i9, "
                          "AnchorLine= :i10, "
                          "AnchorRibNum= :i11 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":i1", i1 )
            query.bindValue(":i2", i2 )
            query.bindValue(":i3", i3 )
            query.bindValue(":i4", i4 )
            query.bindValue(":i5", i5 )
            query.bindValue(":i6", i6 )
            query.bindValue(":i7", i7 )
            query.bindValue(":i8", i8 )
            query.bindValue(":i9", i9 )
            query.bindValue(":i10", i10 )
            query.bindValue(":i11", i11 )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
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
                        self.addRowForConfig( currNumConfigs +1 +i )
                        i += 1
                else:
                    # remove config lines
                    while i < diff:
                        self.removeRowForConfig( currNumConfigs-i )
                        i += 1
                
                # emit the change signal
                self.numConfigsChanged.emit( self.numConfigs() )

    class MarksModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Marks parameters. 
        '''
        __className = 'MarksModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        MarksSpCol = 0
        ''':attr: Number of the col holding the marks spacing value'''
        PointRadCol = 1
        ''':attr: Number of the col holding the point radius value'''
        PointDisplCol = 2
        ''':attr: Number of the col holding the points displacement value'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Marks table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists Marks;")
            query.exec("create table if not exists Marks ("
                    "MarksSp REAL,"
                    "PointRad REAL,"
                    "PointDispl REAL,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Marks")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(0, Qt.Horizontal, _("Marks Spacing [cm]"))
            self.setHeaderData(1, Qt.Horizontal, _("Point Radius [cm]"))
            self.setHeaderData(2, Qt.Horizontal, _("Point Displacement [cm]"))
            
            self.addRows(-1, 1)
        
        def updateRow(self, marksSp, pointRad, pointDispl):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: add transaction
            query = QSqlQuery()
            query.prepare("UPDATE Marks SET MarksSp= :marksSp, PointRad= :pointRad, PointDispl= :pointDispl WHERE (ID = :id);")
            query.bindValue(":marksSp", marksSp )
            query.bindValue(":pointRad", pointRad )
            query.bindValue(":pointDispl", pointDispl )
            query.bindValue(":id", 1 )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

    class RamificationModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the ramification parameters. 
        '''
        __className = 'RamificationModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        RowsCol = 1
        ''':attr: Number of the col holding the number of rows'''
        ThirdToSailCol = 2
        ''':attr: Number of the col holding the distance branching third to sail (l3)'''
        FourthToSailCol = 3
        ''':attr: Number of the col holding the distance beginning of fourth branching to sail (l2)'''
        ConfigNumCol = 4
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Ramification table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists Ramification;")
            query.exec("create table if not exists Ramification ("
                    "OrderNum INTEGER,"
                    "Rows INTEGER,"
                    "ThirdToSail INTEGER,"
                    "FourthToSail INTEGER,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Ramification")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(1, Qt.Horizontal, _("Rows"))
            self.setHeaderData(2, Qt.Horizontal, _("Third to sail [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("Fourth to sail [cm]"))
            
            self.setNumRowsForConfig(1,4)
 
        def updateDataRow(self, configNum, orderNum, rows, thirdToSail, fourthToSail):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateDataRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE Ramification SET "
                          "Rows= :rows, "
                          "ThirdToSail= :thirdToSail, "
                          "FourthToSail= :fourthToSail "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":rows", rows )
            query.bindValue(":thirdToSail", thirdToSail )
            query.bindValue(":fourthToSail", fourthToSail )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
           
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
            
            self.setHeaderData(0, Qt.Horizontal, _("Edge seem [mm]"))
            self.setHeaderData(1, Qt.Horizontal, _("LE seem [mm]"))
            self.setHeaderData(2, Qt.Horizontal, _("TE seem [mm]"))
            
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
        LinesConcTypeCol = 11
        ''':attr: number of the column holding the lines concept type'''
        BrakeLengthCol = 12
        ''':attr: number of the column holding the lenthg of the brake lines'''
        xSpacingCol = 13
        ''':attr: number of the column holding xSpacing for the HvVh Ribs'''
        ySpacingCol = 14
        ''':attr: number of the column holding ySpacing for the HvVh Ribs'''
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
                    "LinesConcType INTEGER,"
                    "Brakelength INTEGER,"
                    "xSpacing REAL,"
                    "ySpacing REAL, "
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
