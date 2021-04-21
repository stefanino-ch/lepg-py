'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to the authors of:

https://doc.qt.io/qtforpython/overviews/sql-model.html

https://www.datacamp.com/community/tutorials/inner-classes-python
'''
import os
import logging
import math
import re

from datetime import date

from PyQt5.QtCore import Qt, QFile, QTextStream, QObject, pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Singleton.Singleton import Singleton
from DataStores.SqlTableModel import SqlTableModel

from ConfigReader.ConfigReader import ConfigReader
from DataStores.Database import Database

class ProcessorModel(QObject, metaclass=Singleton):
    '''
    :class: Does take care about the data handling for the processor.
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
    __className = 'ProcessorModel'
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
        self.extradColsConf_M = self.ExtradColsConfModel()
        self.extradColsDet_M = self.ExtradColsDetModel()
        self.intradColsConf_M = self.IntradColsConfModel()
        self.intradColsDet_M = self.IntradColsDetModel()
        self.addRibPts_M = self.AddRibPointsModel()
        self.elLinesCorr_M = self.ElasticLinesCorrModel()
        self.elLinesDef_M = self.ElasticLinesDefModel()
        self.dxfLayNames_M = self.DxfLayerNamesModel()
        self.marksT_M = self.MarksTypesModel()
        self.joncsDef_M = self.JoncsDefModel()
        self.noseMylars_M = self.NoseMylarsModel()
        self.twoDDxf_M = self.TwoDDxfModel()
        self.threeDDxf_M = self.ThreeDDxfModel()
        self.glueVent_M = ProcessorModel.GlueVentModel()
        self.specWingTyp_M = ProcessorModel.SpecWingTipModel()
        self.calageVar_M = ProcessorModel.CalageVarModel()
        self.threeDShConf_M = ProcessorModel.ThreeDShConfModel()
        self.threeDShUpDet_M = ProcessorModel.ThreeDShUpDetModel()
        self.threeDShLoDet_M = ProcessorModel.ThreeDShLoDetModel()
        self.threeDShPr_M = ProcessorModel.ThreeDShPrintModel()
        self.airfThick_M = ProcessorModel.AirfoilThicknessModel()
        self.newSkinTensConf_M = ProcessorModel.NewSkinTensConfModel()
        self.newSkinTensDet_M = ProcessorModel.NewSkinTensDetModel()

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
    
    def isValidPreProcFile( self, fileName ):
        '''
        :method: Checks if a file can be opened and contains a valid title and known version number.
        :param fileName: the name of the file to be checked
        '''
        logging.debug(self.__className+ '.isValidPreProcFile')
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
        
        while (stream.atEnd() != True) and not (titleOK and versionOK) and lineCounter < 10:
            line = stream.readLine()
            if line.find('1.6') >= 0:
                versionOK = True

            if line.find('Auxiliar geometry data') >= 0:
                titleOK = True
            lineCounter += 1

        inFile.close()
        
        if not ( (versionOK and titleOK) ):
            logging.error(self.__className+ ' Result of Pre-Proc out file version check %s', versionOK)
            logging.error(self.__className+ ' Result of Pre-Proc out file title check %s', titleOK)
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('File read error'))
            msgBox.setText(_('File seems not to be a valid Pre-Proc output File! \nVersion detected: ')+ str(versionOK)+ _('\nTitle detected: ')+ str(titleOK))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

        return versionOK and titleOK
    
    def isValidProcFile( self, fileName ):
        '''
        :method: Checks if a file can be opened and contains a valid title and known version number.
        :param fileName: the name of the file to be checked
        '''
        logging.debug(self.__className+ '.isValidProcFile')
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
                self.setFileVersion('3.10')
                versionOK = True
            elif line.find('3.15') >= 0:
                self.setFileVersion('3.15')
                versionOK = True

            if line.find('Input data file') >= 0:
                titleOK = True
            lineCounter += 1

        inFile.close()
        
        if not ( (versionOK and titleOK) ):
            logging.error(self.__className+ ' Result of Proc file version check %s', versionOK)
            logging.error(self.__className+ ' Result of Proc file title check %s', titleOK)
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('File read error'))
            msgBox.setText(_('File seems not to be a valid Processor File! \nVersion detected: ')+ str(versionOK)+ _('\nTitle detected: ')+ str(titleOK))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            
            self.setFileName('')
            self.setFileVersion('')

        return versionOK and titleOK
    
    def importPreProcFile(self):
        '''
        :method: Checks for unapplied/ unsaved data, and appropriate handling. Does the File Open dialog handling. 
        '''
        logging.debug(self.__className+ '.importPreProcFile')
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
                        _('Import Pre-Proc ouptut file'),
                        "",
                        "Pre Proc Files (*.txt);;All Files (*)")

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the dialog  
            # an empty tuple is retured
            if self.isValidPreProcFile(fileName[0]):
                # TODO: delete already existing Processor data
                self.readPreProcFile(fileName[0])
     
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
                        _('Open Proc file'),
                        "",
                        "Pre Proc Files (*.txt);;All Files (*)")

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the dialog  
            # an empty tuple is retured
            if self.isValidProcFile(fileName[0]):
                self.setFileName(fileName[0])
                self.readFile()
                
    def saveFile(self):
        '''
        :method: Checks if there is already a valid file name, if not it asks for it. Starts afterwards the writing process.  
        '''
        logging.debug(self.__className+ '.saveFile')
        
        fileName = self.getFileName() 
        if self.fileName != '':
            # We do have already a valid filename
            self.writeFile()
        else:
            # Ask first for the filename
            fileName = QFileDialog.getSaveFileName(
                        None,
                        _('Save Processor file'),
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
        logging.debug(self.__className+ '.saveFileAs')
        
        # Ask first for the filename
        fileName = QFileDialog.getSaveFileName(
                    None,
                    _('Save Processor file as'),
                    "",
                    "Geometry Files (*.txt);;All Files (*)")
        
        if fileName != ('', ''):
                # User has really selected a file, if it would have aborted the dialog  
                # an empty tuple is retured
                self.setFileName(fileName[0])
                self.writeFile()
                
    def readPreProcFile(self, fileName):
        '''
        :method: Imports the data file created by the pre-processor saves the data in the internal database.
        :param fileName: Path and Filename in one fully qualified string.
        '''
        logging.debug(self.__className+'.readPreProcFile')
        
        inFile = QFile( fileName )
        inFile.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(inFile)

        ##############################
        # overread file header
        counter = 0
        while counter < 5:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1
        
        # overread title
        line = stream.readLine()
        
        # There's no idication about the number of lines
        # We first read all into the memory 
        lineArray = []
        validData = True
        
        while validData:
            line = stream.readLine()
            
            if line.find('***************') >= 0:
                validData = False
            else:
                lineArray.append(line)
        
        # all read now
        numLines = len(lineArray)
        
        self.wing_M.updateNumRibs(numLines*2)
        
        for l in range (0, numLines):
            values = self.splitLine(lineArray[l])
            self.rib_M.updateRow(l+1, values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])
            
        for i in range(2): # @UnusedVariable
            line = stream.readLine()
            
        values = self.splitLine( stream.readLine() )
        self.wing_M.updateNumCells(values[1])
                
        ##############################
        # Cleanup
        inFile.close()
    
    def readFile(self):
        '''
        :method: Reads the data file and saves the data in the internal database.
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
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.WingScaleCol), self.remTabSpace( stream.readLine() ) )
        
        # Number of cells
        logging.debug(self.__className+'.readFile: Number of cells')
        line = stream.readLine()
        self.wing_M.setData(self.wing_M.index(0, self.WingModel.NumCellsCol), self.remTabSpace( stream.readLine() ) )
        
        # Number of Ribs
        logging.debug(self.__className+'.readFile: Number of ribs')
        line = stream.readLine()
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
            self.lightC_M.updateRow(i+1, ini, fin)
            
            numConfigLines = int(self.remTabSpace( stream.readLine() ))
            self.lightD_M.setNumRowsForConfig(i+1, 0 )
            self.lightD_M.setNumRowsForConfig(i+1, numConfigLines )
            
            # ConfigNum, orderNum, LightTyp, DistLE, DisChord, HorAxis, VertAxis, RotAngle, Opt1
            for l in range(0, numConfigLines):
                values =  self.splitLine( stream.readLine() )
                self.lightD_M.updateRow(i+1, l+1, values[0], \
                                        values[1], \
                                        values[2], \
                                        values[3], \
                                        values[4], \
                                        values[5], \
                                        values[6])

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
        self.skinTensParams_M.setData(self.skinTensParams_M.index(0, ProcessorModel.SkinTensionParamsModel.CoeffCol), values[1] )
        
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
            self.brakes_M.updateRow(1, l+1, \
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
        # 15. Extrados colors
        logging.debug(self.__className+'.readFile: Extrados colors')
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int(self.remTabSpace( stream.readLine() ) )
        self.extradColsConf_M.setNumConfigs(numConfigs)
        
        for configCounter in range(0, numConfigs):
            values =  self.splitLine( stream.readLine() )
            
            self.extradColsConf_M.updateRow(configCounter+1, values[0])
            
            numConfigLines = int(values[1])
            self.extradColsDet_M.setNumRowsForConfig(configCounter+1, numConfigLines)
                   
            for l in range(0, numConfigLines):
                values =  self.splitLine( stream.readLine() )
                self.extradColsDet_M.updateRow(configCounter+1, l+1, values[1] )
            
        ##############################
        # 16. Intrados colors
        logging.debug(self.__className+'.readFile: Intrados colors')
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int(self.remTabSpace( stream.readLine() ) )
        self.intradColsConf_M.setNumConfigs(numConfigs)
        
        for configCounter in range(0, numConfigs):
            values =  self.splitLine( stream.readLine() )
            
            self.intradColsConf_M.updateRow(configCounter+1, values[0])
            
            numConfigLines = int(values[1])
            self.intradColsDet_M.setNumRowsForConfig(configCounter+1, numConfigLines)
                   
            for l in range(0, numConfigLines):
                values =  self.splitLine( stream.readLine() )
                self.intradColsDet_M.updateRow(configCounter+1, l+1, values[1] )
        
        
        ##############################
        # 17. Aditional rib points
        logging.debug(self.__className+'.readFile: Additional rib points')
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int(self.remTabSpace( stream.readLine() ) )
        self.addRibPts_M.setNumRowsForConfig(1, 0)
        self.addRibPts_M.setNumRowsForConfig(1, numConfigs)
        
        for l in range(0, numConfigs):
            values =  self.splitLine( stream.readLine() )
            
            self.addRibPts_M.updateRow(1, l+1, values[0], values[1])

        ##############################
        # 18. Elastic lines corrections
        logging.debug(self.__className+'.readFile: Elastic Lines correction')
        for i in range(3):
            line = stream.readLine()
        
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.LoadCol), self.remTabSpace( stream.readLine() ) )
        
        values =  self.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.TwoLineDistACol), values[0] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.TwoLineDistBCol), values[1] )
        
        values =  self.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.ThreeLineDistACol), values[0] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.ThreeLineDistBCol), values[1] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.ThreeLineDistCCol), values[2] )

        values =  self.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FourLineDistACol), values[0] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FourLineDistBCol), values[1] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FourLineDistCCol), values[2] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FourLineDistDCol), values[3] )
        
        values =  self.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FiveLineDistACol), values[0] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FiveLineDistBCol), values[1] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FiveLineDistCCol), values[2] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FiveLineDistDCol), values[3] )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, self.elLinesCorr_M.FiveLineDistECol), values[4] )

        for l in range (0,5):
            values =  self.splitLine( stream.readLine() )
            self.elLinesDef_M.updateRow(1, l+1, values[1], values[2], values[3])
            
        ##############################
        # 19. DXF layer names
        logging.debug(self.__className+'.readFile: DXF layer names')
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int( self.remTabSpace( stream.readLine() ) )
        self.dxfLayNames_M.setNumRowsForConfig(1,0)
        self.dxfLayNames_M.setNumRowsForConfig(1, numConfigs)
        
        for l in range(0, numConfigs):
            values =  self.splitLine( stream.readLine() )
            
            self.dxfLayNames_M.updateRow(1, l+1, values[0], values[1])
            
                ##############################
        # 20. Marks types
        logging.debug(self.__className+'.readFile: Marks types')
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int( self.remTabSpace( stream.readLine() ) )
        self.marksT_M.setNumRowsForConfig(1,0)
        self.marksT_M.setNumRowsForConfig(1, numConfigs)
        
        for l in range(0, numConfigs):
            values =  self.splitLine( stream.readLine() )
            
            self.marksT_M.updateRow(1, l+1, values[0], \
                                    values[1], values[2], values[3], \
                                    values[4], values[5], values[6])
            
        ##############################
        # 21. JONCS DEFINITION (NYLON RODS)
        logging.debug(self.__className+'.readFile: Joncs definition')
        for i in range(3):
            line = stream.readLine()
        
        # delete all what is there
        self.joncsDef_M.setNumConfigs(0)
            
        scheme = int( self.remTabSpace( stream.readLine() ) )
            
        if scheme == 1:
            # in scheme 1 config num is always 1
            configNum = 1
            
            numGroups =  int( self.remTabSpace( stream.readLine() ) )
            self.joncsDef_M.setNumRowsForConfig(configNum, numGroups)
            
            for g in range (0, numGroups):
                valuesA = self.splitLine( stream.readLine() )
                valuesB = self.splitLine( stream.readLine() )
                valuesC = self.splitLine( stream.readLine() )
                valuesD = self.splitLine( stream.readLine() )
                self.joncsDef_M.updateTypeOneRow(configNum, g+1, \
                                                 valuesA[1], valuesA[2], \
                                                 valuesB[0], valuesB[1], valuesB[2], valuesB[3], \
                                                 valuesC[0], valuesC[1], valuesC[2], valuesC[3], \
                                                 valuesD[0], valuesD[1], valuesD[2], valuesD[3] )
        
        elif scheme == 2:
            numBlocs =  int( self.remTabSpace( stream.readLine() ) )
            
            for b in range (0,numBlocs):
                values = self.splitLine( stream.readLine() )
                
                blocType = int(values[1])
                if blocType == 1:
                    numGroups =  int( self.remTabSpace( stream.readLine() ) )
                    self.joncsDef_M.setNumRowsForConfig(b+1, numGroups)
                    
                    for g in range (0, numGroups):
                        valuesA = self.splitLine( stream.readLine() )
                        valuesB = self.splitLine( stream.readLine() )
                        valuesC = self.splitLine( stream.readLine() )
                        valuesD = self.splitLine( stream.readLine() )
                        self.joncsDef_M.updateTypeOneRow(b+1, g+1, \
                                                         valuesA[1], valuesA[2], \
                                                         valuesB[0], valuesB[1], valuesB[2], valuesB[3], \
                                                         valuesC[0], valuesC[1], valuesC[2], valuesC[3], \
                                                         valuesD[0], valuesD[1], valuesD[2], valuesD[3] )

                else:
                    numGroups =  int( self.remTabSpace( stream.readLine() ) )
                    self.joncsDef_M.setNumRowsForConfig(b+1, numGroups)
                    
                    for g in range (0, numGroups):
                        valuesA = self.splitLine( stream.readLine() )
                        valuesB = self.splitLine( stream.readLine() )
                        valuesC = self.splitLine( stream.readLine() )
                        self.joncsDef_M.updateTypeTwoRow(b+1, g+1, \
                                                         valuesA[1], valuesA[2], \
                                                         valuesB[0], valuesB[1], valuesB[2], valuesB[3], valuesB[4], \
                                                         valuesC[0], valuesC[1], valuesC[2], valuesC[3])
        # Little bad hack. Some of the GUI depends on data within the rows set above. 
        # To get teh GUI updated properly we fake here a model update to force an update in the GUI.  
        self.joncsDef_M.numRowsForConfigChanged.emit(0, 0)

        ##############################
        # 22. NOSE MYLARS DEFINITION
        logging.debug(self.__className+'.readFile: Nose mylars')
        for i in range(3):
            line = stream.readLine()
            
        data = int(self.remTabSpace( stream.readLine() ) )
        self.noseMylars_M.setNumConfigs(0)
        
        if data != 0:
            # we have data to read
            
            numConfigs = int(self.remTabSpace( stream.readLine() ) )
            self.noseMylars_M.setNumRowsForConfig(1, numConfigs)
        
            for c in range(0, numConfigs):
                valuesA = self.splitLine( stream.readLine() )
                valuesB = self.splitLine( stream.readLine() )
                
                self.noseMylars_M.updateRow(1, c+1, \
                                            valuesA[1], valuesA[2], \
                                            valuesB[0], valuesB[1], valuesB[2], valuesB[3], valuesB[4], valuesB[5])  
       
        ##############################
        # 23. TAB REINFORCEMENTS
        logging.debug(self.__className+'.readFile: Jump over Tab reinforcements')
                
        counter = 0
        while counter < 4:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1
        
        ##############################
        # 24. GENERAL 2D DXF OPTIONS
        # be carefull: previous code has already read both **** lines of header        
        logging.debug(self.__className+'.readFile: General 2D DXF options')
            
        data = int( self.remTabSpace( stream.readLine() ) )
        
        self.twoDDxf_M.setIsUsed(False)
        
        if data != 0:
            self.twoDDxf_M.setIsUsed(True)
            self.twoDDxf_M.setNumRowsForConfig(1, 6)
            # we have data to read
            for l in range(0, 6 ):
                values =  self.splitLine( stream.readLine() )
                self.twoDDxf_M.updateRow(1, l+1, values[0], values[1], values[2])    
            
        ##############################
        # 25. GENERAL 3D DXF OPTIONS
        logging.debug(self.__className+'.readFile: General 3D DXF options')
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.remTabSpace( stream.readLine() ) )
        
        self.threeDDxf_M.setIsUsed(False)
        
        if data != 0:
            self.threeDDxf_M.setIsUsed(True)
            self.threeDDxf_M.setNumRowsForConfig(1, 9)
            # we have data to read
            for l in range(0, 6 ):
                values =  self.splitLine( stream.readLine() )
                self.threeDDxf_M.updateRow(1, l+1, values[0], values[1], values[2])
                
            for l in range(0, 3 ):
                values =  self.splitLine( stream.readLine() )
                self.threeDDxf_M.updateRow(1, l+1+6, values[0], values[2], values[3], values[1])
        
        ##############################
        # 26. GLUE VENTS
        logging.debug(self.__className+'.readFile: Glue vents')
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.remTabSpace( stream.readLine() ) )
        
        self.glueVent_M.setIsUsed(False)
        
        if data != '0':
            self.glueVent_M.setIsUsed(True)
            # we have data to read
            for l in range( 0, self.wing_M.halfNumRibs ):
                values =  self.splitLine( stream.readLine() )
                self.glueVent_M.updateRow(1, l+1, values[1])
        
        ##############################
        # 26. SPECIAL WING TIP
        logging.debug(self.__className+'.readFile: Special wing tip')
        for i in range(3):
            line = stream.readLine()
        
        data = int( self.remTabSpace( stream.readLine() ) )   
        
        self.specWingTyp_M.setIsUsed(False)
        self.specWingTyp_M.setNumRowsForConfig(1, 1)
        
        if data != 0:
            self.specWingTyp_M.setIsUsed(True)
            
            valuesA =  self.splitLine( stream.readLine() )
            valuesB =  self.splitLine( stream.readLine() )
            
            self.specWingTyp_M.updateRow(1, 1, valuesA[1], valuesB[1])
            
        ##############################
        # 28. PARAMETERS FOR CALAGE VARIATION
        logging.debug(self.__className+'.readFile: Calage variation')
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.remTabSpace( stream.readLine() ) )   
        
        self.calageVar_M.setIsUsed(False)
        self.calageVar_M.setNumRowsForConfig(1, 1)
        
        if data != 0:
            self.calageVar_M.setIsUsed(True)
            
            valuesA =  self.splitLine( stream.readLine() )
            valuesB =  self.splitLine( stream.readLine() )
            valuesC =  self.splitLine( stream.readLine() )
            
            self.calageVar_M.updateRow(1, 1, \
                                       valuesA[0], \
                                       valuesB[0], valuesB[1], valuesB[2], valuesB[3], valuesB[4], valuesB[5], \
                                       valuesC[0], valuesC[1], valuesC[2], valuesC[3])
        
        ##############################
        # 29. 3D SHAPING
        logging.debug(self.__className+'.readFile: 3D Shaping')
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.remTabSpace( stream.readLine() ) )
        
        self.threeDShConf_M.setNumConfigs(0)
        self.threeDShUpDet_M.setNumConfigs(0)
        self.threeDShLoDet_M.setNumConfigs(0)
        
        if data != 0:
            # overread type as it is always 1
            line = stream.readLine()
            
            values =  self.splitLine( stream.readLine() )
            numGroups = int (values[1])
            self.threeDShConf_M.setNumConfigs(numGroups)
            
            for g in range(0, numGroups):
                # ribs and so
                values = self.splitLine( stream.readLine() )
                
                self.threeDShConf_M.updateRow(g+1, 1, values[2], values[3])
                
                # upper config
                values = self.splitLine( stream.readLine() )
                numUpCuts = int (values[1] )
                if numUpCuts == 1:
                    self.threeDShUpDet_M.setNumRowsForConfig(g+1, numUpCuts)
                    
                    values = self.splitLine( stream.readLine() )
                    self.threeDShUpDet_M.updateRow(g+1, 1, values[1], values[2], values[3])
                    
                elif numUpCuts == 2:
                    self.threeDShUpDet_M.setNumRowsForConfig(g+1, numUpCuts)
                    
                    values = self.splitLine( stream.readLine() )
                    self.threeDShUpDet_M.updateRow(g+1, 1, values[1], values[2], values[3])
                    
                    values = self.splitLine( stream.readLine() )
                    self.threeDShUpDet_M.updateRow(g+1, 2, values[1], values[2], values[3])
                    
                # lower config
                values = self.splitLine( stream.readLine() )
                numLoCuts = int (values[1] )
                if numLoCuts == 1:
                    self.threeDShLoDet_M.setNumRowsForConfig(g+1, numUpCuts)
                    
                    values = self.splitLine( stream.readLine() )
                    self.threeDShLoDet_M.updateRow(g+1, 1, values[1], values[2], values[3])
            
            line = stream.readLine()
            
            self.threeDShPr_M.setNumRowsForConfig(1, 0)
            self.threeDShPr_M.setNumRowsForConfig(1, 5)
            
            for l in range(0,5):
                values = self.splitLine( stream.readLine() )
                self.threeDShPr_M.updateRow(1, l+1, values[0], values[1], values[2], values[3], values[4])
                
        ##############################
        # 30. AIRFOIL THICKNESS
        logging.debug(self.__className+'.readFile: Airfoil thickness')
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.remTabSpace( stream.readLine() ) )
        
        self.airfThick_M.setIsUsed(False)
        
        if data != 0:
            self.airfThick_M.setIsUsed(True)
            # we have data to read
            for l in range( 0, self.wing_M.halfNumRibs ):
                values =  self.splitLine( stream.readLine() )
                self.airfThick_M.updateRow(1, l+1, values[1])
        
        
        ##############################
        # 31. NEW SKIN TENSION
        logging.debug(self.__className+'.readFile: New skin tension')
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.remTabSpace( stream.readLine() ) )
        
        self.newSkinTensConf_M.setNumConfigs(0)
        self.newSkinTensDet_M.setNumConfigs(0)
        
        if data != 0:
            numGroups = int( self.remTabSpace( stream.readLine() ) )
            self.newSkinTensConf_M.setNumConfigs(numGroups)
            
            for g in range (0, numGroups):
                # comment line
                line = stream.readLine()
                
                values = self.splitLine( stream.readLine() )
                self.newSkinTensConf_M.updateRow(g+1, values[1], values[2], values[4])
                
                numLines = int(values[3])
                self.newSkinTensDet_M.setNumRowsForConfig(g+1, numLines)
                for l in range (0, numLines):
                    values = self.splitLine( stream.readLine() )
                    self.newSkinTensDet_M.updateRow(g+1, l+1, values[1], values[2], values[3], values[4])
            
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
        
        if forProc == False:
            # Regular file write into a file specified by the user
            outFile = QFile(self.getFileName())
        else:
            # Special file write into the directory where the PreProcessor resides
            config = ConfigReader()
            pathName = os.path.join(config.getProcDirectory(), 'leparagliding.txt')
            
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
        stream << '* LABORATORI D\'ENVOL PARAGLIDING DESIGN\n'
        stream << '* Input data file version 3.15\n'
        stream << separator
        today = date.today()
        stream << '* Version %s\n' %today.strftime("%Y-%m-%d")
        stream << separator
        
        values = self.wing_M.getRow()
        stream << '*             1. GEOMETRY\n'
        stream << separator
        stream << '* Brand name\n'
        stream << '\"%s\"\n' %values(ProcessorModel.WingModel.BrandNameCol)
        stream << '* Wing name\n'
        stream << '\"%s\"\n' %values(ProcessorModel.WingModel.WingNameCol)
        stream << '* Drawing scale\n'
        stream << '%s\n' %values(ProcessorModel.WingModel.DrawScaleCol)
        stream << '* Wing scale\n'
        stream << '%s\n' %values(ProcessorModel.WingModel.WingScaleCol)
        stream << '* Number of cells\n'
        stream << '\t%s\n' %values(ProcessorModel.WingModel.NumCellsCol)
        stream << '* Number of ribs\n'
        stream << '\t%s\n' %values(ProcessorModel.WingModel.NumRibsCol)
        stream << '* Alpha max and parameter\n'
        stream << '\t%s' %values(ProcessorModel.WingModel.AlphaMaxTipCol)
        stream << '\t%s' %values(ProcessorModel.WingModel.AlphaModeCol)
        if values(ProcessorModel.WingModel.AlphaModeCol) == '2':
            stream << '\t%s\n' %values(ProcessorModel.WingModel.AlphaMaxCentCol)
        else:
            stream << '\n'
        
        stream << '* Paraglider type and parameter\n'
        stream << '\t\"%s\"' %values(ProcessorModel.WingModel.ParaTypeCol)
        stream << '\t%s\n' %values(ProcessorModel.WingModel.ParaParamCol)
        stream << '* Rib geometric parameters\n'
        stream << '* Rib    x-rib    y-LE    y-TE    xp    z    beta    RP    Washin\n'
        for l in range (0, self.wing_M.halfNumRibs):
            values = self.rib_M.getRow(l+1)
            stream << '%s' %(l+1)
            
            for p in range (0, 8):
                stream << '\t%s' %values(p)
                if p ==7:
                    stream << '\n'
        
        stream << separator            
        stream << '*             2. AIRFOILS\n'
        stream << separator
        stream << '* Airfoil name, intake in, intake out, open , disp. rrw\n'
        for l in range (0, self.wing_M.halfNumRibs):
            values = self.airf_M.getRow(l+1)
            stream << '%s' %(l+1)
            
            for p in range (0, 7):
                stream << '\t%s' %values(p)
                if p ==6:
                    stream << '\n'
                    
        stream << separator            
        stream << '*            3. ANCHOR POINTS\n'
        stream << separator
        stream << '* Airf    Anch    A    B    C    D    E    F\n'
        for l in range (0, self.wing_M.halfNumRibs):
            values = self.anchPoints_M.getRow(l+1)
            stream << '%s' %(l+1)
            
            for p in range (0, 7):
                stream << '\t%s' %values(p)
                if p ==6:
                    stream << '\n'
     
        stream << separator            
        stream << '*          4. AIRFOIL HOLES\n'
        stream << separator
        numConfigs = int( self.lightC_M.numConfigs() )
        stream << '%s\n' %(numConfigs)
        
        for g in range (0, numConfigs):
            values = self.lightC_M.getRow(g+1)
            stream << '%s\n' %values(0)
            stream << '%s\n' %values(1)

            numLines = self.lightD_M.numRowsForConfig(g+1)
            stream << '%s\n' %(numLines)
            for l in range (0, numLines):
                values = self.lightD_M.getRow(g+1, l+1)
                for p in range (0, 7):
                    if p>0:
                        stream << '\t' 
                    stream << '%s' %values(p)
                    if p ==6:
                        stream << '\t0.\t0.\n'
        
        stream << separator            
        stream << '*           5. SKIN TENSION\n'
        stream << separator
        stream << 'Extrados\n'
        
        for l in range (0,6):
            values = self.skinTens_M.getRow(l+1)
            
            for p in range (0, 4):
                    if p>0:
                        stream << '\t' 
                    stream << '%s' %values(p)
                    if p ==3:
                        stream << '\n'
            
        values = self.skinTensParams_M.getRow()
        stream << '%s\n' %values(0)
        stream << '%s' %values(1)
        stream << '\t%s\n' %values(2)

        stream << separator            
        stream << '*           6. SEWING ALLOWANCES\n'
        stream << separator

        values = self.sewAll_M.getRow(1)
        for p in range (0, 3):
                if p>0:
                    stream << '\t' 
                stream << '%s' %values(p)
                if p ==2:
                    stream << '\tupper panels (mm)\n'
        
        values = self.sewAll_M.getRow(2)
        for p in range (0, 3):
                if p>0:
                    stream << '\t' 
                stream << '%s' %values(p)
                if p ==2:
                    stream << '\tlower panels (mm)\n'
                    
        values = self.sewAll_M.getRow(3)
        stream << '%s' %values(0)
        stream << '\tribs (mm)\n'
        
        values = self.sewAll_M.getRow(4)
        stream << '%s' %values(0)
        stream << '\tvribs (mm)\n'
        
        stream << separator            
        stream << '*           7. MARKS\n'
        stream << separator
        
        values = self.marks_M.getRow()
        stream << '%s' %values(0)
        stream << '\t%s' %values(1)
        stream << '\t%s\n' %values(2)       
                
        stream << separator            
        stream << '*           8. Global angle of attack estimation\n'
        stream << separator
        values = self.globAoA_M.getRow()
        stream << '* Finesse GR\n'
        stream << '\t%s\n' %values(0)
        stream << '* Center of pressure % of chord\n'
        stream << '\t%s\n' %values(1)
        stream << '* Calage %\n'
        stream << '\t%s\n' %values(2)
        stream << '* Risers lenght cm\n'
        stream << '\t%s\n' %values(3)
        stream << '* Line lenght cm\n'
        stream << '\t%s\n' %values(4)
        stream << '* Karabiners cm\n'
        stream << '\t%s\n' %values(5)
            
        stream << separator            
        stream << '*          9. SUSPENSION LINES DESCRIPTION\n'
        stream << separator
        values = self.wing_M.getRow()
        stream << '%s\n' %values(ProcessorModel.WingModel.LinesConcTypeCol)
        
        numConfigs = self.lines_M.numConfigs()
        stream << '%s\n' %numConfigs
        
        for g in range (0, numConfigs):
            numLines = self.lines_M.numRowsForConfig(g+1)
            stream << '%s\n' %numLines
            
            for l in range (0, numLines):
                values = self.lines_M.getRow(g+1, l+1)
                
                for p in range (0, 11):
                    if p>0:
                        stream << '\t' 
                    stream << '%s' %values(p)
                    if p ==10:
                        stream << '\n'

        stream << separator            
        stream << '*       10. BRAKES\n'
        stream << separator
        
        values = self.wing_M.getRow()
        stream << '%s\n' %values(ProcessorModel.WingModel.BrakeLengthCol)
        
        numLines = self.brakes_M.numRowsForConfig(1)
        stream << '%s\n' %numLines
        for l in range (0, numLines):
            values = self.brakes_M.getRow(1, l+1)
            
            for p in range (0, 11):
                if p>0:
                    stream << '\t' 
                stream << '%s' %values(p)
                if p ==10:
                    stream << '\n'
        
        stream << '* Brake distribution\n'           
        values = self.brakeL_M.getRow()
        
        for p in range (0, 5):
            if p>0:
                stream << '\t' 
            stream << '%s' %values(p)
            if p ==4:
                stream << '\n'
        for p in range (5, 10):
            if p>5:
                stream << '\t' 
            stream << '%s' %values(p)
            if p ==9:
                stream << '\n'
                
        stream << separator            
        stream << '*       11. Ramification lengths\n'
        stream << separator
        
        values = self.ramif_M.getRow(1, 1)
        stream << '%s' %values(0)
        stream << '\t%s\n' %values(1)
        
        values = self.ramif_M.getRow(1, 2)
        stream << '%s' %values(0)
        stream << '\t%s' %values(1)
        stream << '\t%s\n' %values(2)
        
        values = self.ramif_M.getRow(1, 3)
        stream << '%s' %values(0)
        stream << '\t%s\n' %values(1)
        
        values = self.ramif_M.getRow(1, 2)
        stream << '%s' %values(0)
        stream << '\t%s' %values(1)
        stream << '\t%s\n' %values(2)
        
        stream << separator            
        stream << '*    12. H V and VH ribs\n'
        stream << separator
        numLines = self.hVvHRibs_M.numRowsForConfig(1)
        stream << '%s\n' %numLines
        values = self.wing_M.getRow()
        stream << '%s' %values(ProcessorModel.WingModel.xSpacingCol)
        stream << '\t%s\n' %values(ProcessorModel.WingModel.ySpacingCol)
        
        for l in range (0, numLines):
            values = self.hVvHRibs_M.getRow(1, l+1)
            
            for p in range (0, 10):
                if p>0:
                    stream << '\t' 
                stream << '%s' %values(p)
            
            if values(1) == 6 or values(1) == 16:
                stream << '\t%s' %values(10)
                stream << '\t%s\n' %values(11)
            else:
                stream << '\n'
                
        stream << separator            
        stream << '*    15. Extrados colors\n'
        stream << separator
        numGroups = self.extradColsConf_M.numConfigs()
        stream << '%s\n' %numGroups
        
        for g in range (0, numGroups):
            numLines = self.extradColsDet_M.numRowsForConfig(g+1)
            
            values = self.extradColsConf_M.getRow(g+1)
            stream << '%s' %values(0)
            stream << '\t%s\n' %numLines
            
            for l in range (0, numLines):
                values = self.extradColsDet_M.getRow(g+1, l+1)
                stream << '%s' %(l+1)
                stream << '\t%s\t0.\n' %values(0)

        stream << separator            
        stream << '*    16. Intrados colors\n'
        stream << separator   
        numGroups = self.intradColsConf_M.numConfigs()
        stream << '%s\n' %numGroups
        
        for g in range (0, numGroups):
            numLines = self.intradColsDet_M.numRowsForConfig(g+1)
            
            values = self.intradColsConf_M.getRow(g+1)
            stream << '%s' %values(0)
            stream << '\t%s\n' %numLines
            
            for l in range (0, numLines):
                values = self.intradColsDet_M.getRow(g+1, l+1)
                stream << '%s' %(l+1)
                stream << '\t%s\t0.\n' %values(0)  
                
        stream << separator            
        stream << '*       17. Aditional rib points\n'
        stream << separator  
        numLines = self.addRibPts_M.numRowsForConfig(1)
        stream << '%s\n' %numLines
        
        for l in range (0, numLines):
            values = self.addRibPts_M.getRow(1, l+1)
            stream << '%s' %values(0)
            stream << '\t%s\n' %values(1)

        stream << separator            
        stream << '*       18. Elastic lines corrections\n'
        stream << separator
        values = self.elLinesCorr_M.getRow()
        stream << '%s\n' %values(0)
        
        stream << '%s' %values(1)
        stream << '\t%s\n' %values(2)
        
        stream << '%s' %values(3)
        stream << '\t%s' %values(4)
        stream << '\t%s\n' %values(5)
        
        stream << '%s' %values(6)
        stream << '\t%s' %values(7)
        stream << '\t%s' %values(8)
        stream << '\t%s\n' %values(9)
        
        stream << '%s' %values(10)
        stream << '\t%s' %values(11)
        stream << '\t%s' %values(12)
        stream << '\t%s' %values(13)
        stream << '\t%s\n' %values(14)
        
        numLines = self.elLinesDef_M.numRowsForConfig(1)
        for l in range (0, numLines):
            values = self.elLinesDef_M.getRow(1, l+1)
            
            for p in range (0, 4):
                if p>0:
                    stream << '\t' 
                stream << '%s' %values(p)
                if p== 3:
                    stream << '\n'
                    
        stream << separator            
        stream << '*       19. DXF layer names\n'
        stream << separator
        numLines = self.dxfLayNames_M.numRowsForConfig(1)
        stream << '%s\n' %numLines
        
        for l in range (0, numLines):
            values = self.dxfLayNames_M.getRow(1, l+1)
            
            for p in range (0, 2):
                if p>0:
                    stream << '\t' 
                stream << '%s' %values(p)
                if p== 1:
                    stream << '\n'
        
        
        stream << separator            
        stream << '*       20. Marks types\n'
        stream << separator
        numLines = self.marksT_M.numRowsForConfig(1)
        stream << '%s\n' %numLines
        
        for l in range (0, numLines):
            values = self.marksT_M.getRow(1, l+1)
            
            for p in range (0, 7):
                if p>0:
                    stream << '\t' 
                stream << '%s' %values(p)
                if p== 6:
                    stream << '\n'    

        stream << separator            
        stream << '*       21. JONCS DEFINITION (NYLON RODS)\n'
        stream << separator
        numGroups = self.joncsDef_M.numConfigs()
        if numGroups == 0:
            stream << '0\n'
        else:
            stream << '2\n' # we always use scheme 2!
            stream << '%s\n' %numGroups
            
            for g in range (0, numGroups):
                numLines = self.joncsDef_M.numRowsForConfig(g+1)
                values = self.joncsDef_M.getRow(g+1, 1)
                scheme = values(ProcessorModel.JoncsDefModel.TypeCol)
                
                stream << '%s' %(g+1)
                stream << '\t%s\n' %scheme
                stream << '%s\n' %numLines

                for  l in range (0, numLines):
                    values = self.joncsDef_M.getRow(g+1, l+1)

                    stream << '%s' %(l+1)
                    stream << '\t%s' %values(ProcessorModel.JoncsDefModel.FirstRibCol)
                    stream << '\t%s\n' %values(ProcessorModel.JoncsDefModel.LastRibCol)
                    
                    # Line 1
                    stream << '%s' %values(ProcessorModel.JoncsDefModel.pBACol)
                    stream << '\t%s' %values(ProcessorModel.JoncsDefModel.pBBCol)
                    stream << '\t%s' %values(ProcessorModel.JoncsDefModel.pBCCol)
                    if scheme == 1:
                        stream << '\t%s\n' %values(ProcessorModel.JoncsDefModel.pBDCol)
                    else:
                        stream << '\t%s' %values(ProcessorModel.JoncsDefModel.pBDCol)
                        stream << '\t%s\n' %values(ProcessorModel.JoncsDefModel.pBECol)
                        
                    # Line 2
                    stream << '%s' %values(ProcessorModel.JoncsDefModel.pCACol)
                    stream << '\t%s' %values(ProcessorModel.JoncsDefModel.pCBCol)
                    stream << '\t%s' %values(ProcessorModel.JoncsDefModel.pCCCol)   
                    stream << '\t%s\n' %values(ProcessorModel.JoncsDefModel.pCDCol)
                    
                    if scheme == 1:
                        # Line 3
                        stream << '%s' %values(ProcessorModel.JoncsDefModel.pDACol)
                        stream << '\t%s' %values(ProcessorModel.JoncsDefModel.pDBCol)
                        stream << '\t%s' %values(ProcessorModel.JoncsDefModel.pDCCol)   
                        stream << '\t%s\n' %values(ProcessorModel.JoncsDefModel.pDDCol)
                        
        stream << separator            
        stream << '*       22. NOSE MYLARS DEFINITION\n'
        stream << separator
        numGroups = self.noseMylars_M.numConfigs()
        if numGroups == 0:
            stream << '0\n'
        else:
            stream << '1\n'
            stream << '%s\n' %numGroups
            
            for g in range (0, numGroups):
                numLines = self.noseMylars_M.numRowsForConfig(g+1)

                for  l in range (0, numLines):
                    values = self.noseMylars_M.getRow(g+1, l+1)
                            
                    stream << '%s' %(l+1)
                    stream << '\t%s' %values(ProcessorModel.NoseMylarsModel.FirstRibCol)
                    stream << '\t%s\n' %values(ProcessorModel.NoseMylarsModel.LastRibCol)
                    
                    for p in range (0,6):
                        if p>0:
                            stream << '\t'
                        
                        stream << '%s' %values(ProcessorModel.NoseMylarsModel.xOneCol+p)
                        
                        if p==5:
                            stream << '\n'
                    
        stream << separator            
        stream << '*       23. TAB REINFORCEMENTS\n'
        stream << separator
        stream << '0\n' # not yet operational
        
        stream << separator            
        stream << '*       24. GENERAL 2D DXF OPTIONS\n'
        stream << separator
        if self.twoDDxf_M.isUsed() == False:
            stream << '0\n'
        else:
            stream << '1\n'
            numLines = self.twoDDxf_M.numRowsForConfig(1)
            
            for l in range (0, numLines):
                values = self.twoDDxf_M.getRow(1, l+1)
                
                for p in range (0, 3):
                    if p>0:
                        stream << '\t' 
                    stream << '%s' %values(p)
                    if p== 2:
                        stream << '\n'  
        
        stream << separator            
        stream << '*       25. GENERAL 3D DXF OPTIONS\n'
        stream << separator
        if self.threeDDxf_M.isUsed() == False:
            stream << '0\n'
        else:
            stream << '1\n'
            for l in range (0, 6):
                values = self.threeDDxf_M.getRow(1, l+1)
                
                stream << '%s' %values(0)
                stream << '\t%s' %values(2)
                stream << '\t%s\n' %values(3)
            
            for l in range (6, 9):
                values = self.threeDDxf_M.getRow(1, l+1)
                for p in range (0, 4):
                    if p>0:
                        stream << '\t' 
                    stream << '%s' %values(p)
                    if p== 3:
                        stream << '\n'
                        
        stream << separator            
        stream << '*       26. GLUE VENTS\n'
        stream << separator
        if self.glueVent_M.isUsed() == False:
            stream << '0\n'
        else:
            stream << '1\n'
            numLines = self.glueVent_M.numRowsForConfig(1)
            
            for l in range (0, numLines):
                values = self.glueVent_M.getRow(1, l+1)
                
                for p in range (0, 2):
                    if p>0:
                        stream << '\t' 
                    stream << '%s' %values(p)
                    if p== 1:
                        stream << '\n'
                        
        stream << separator            
        stream << '*       27. SPECIAL WING TIP\n'
        stream << separator
        if self.specWingTyp_M.isUsed() == False:
            stream << '0\n'
        else:
            stream << '1\n'
            
            values = self.specWingTyp_M.getRow(1, 1)
            stream << 'AngleLE\t%s\n' %values(ProcessorModel.SpecWingTipModel.AngleLECol)
            stream << 'AngleTE\t%s\n' %values(ProcessorModel.SpecWingTipModel.AngleTECol)
            
        stream << separator            
        stream << '*       28. PARAMETERS FOR CALAGE VARIATION\n'
        stream << separator
        if self.calageVar_M.isUsed() == False:
            stream << '0\n'
        else:
            stream << '1\n'
            
            values = self.calageVar_M.getRow(1, 1)
            stream << '%s\n' %values(ProcessorModel.CalageVarModel.NumRisersCol)
            
            stream << '%s' %values(ProcessorModel.CalageVarModel.PosACol)
            stream << '\t%s' %values(ProcessorModel.CalageVarModel.PosBCol)
            stream << '\t%s' %values(ProcessorModel.CalageVarModel.PosCCol)
            stream << '\t%s' %values(ProcessorModel.CalageVarModel.PosDCol)
            stream << '\t%s' %values(ProcessorModel.CalageVarModel.PosECol)
            stream << '\t%s\n' %values(ProcessorModel.CalageVarModel.PosFCol)
            
            stream << '%s' %values(ProcessorModel.CalageVarModel.MaxNegAngCol)
            stream << '\t%s' %values(ProcessorModel.CalageVarModel.NumNegStepsCol)
            stream << '\t%s' %values(ProcessorModel.CalageVarModel.MaxPosAngCol)
            stream << '\t%s\n' %values(ProcessorModel.CalageVarModel.NumPosStepsCol)
            
        stream << separator            
        stream << '*       29. 3D SHAPING\n'
        stream << separator
        numGroups = self.threeDShConf_M.numConfigs()
        if numGroups == 0:
            stream << '0\n'
        else:
            stream << '1\n'

            stream << '1\n'
            stream << 'groups\t%s\n' %numGroups
            
            for g in range (0, numGroups):
                values = self.threeDShConf_M.getRow(g+1, 1)
                stream << 'group\t%s' %(g+1)
                stream << '\t%s' %values(ProcessorModel.ThreeDShConfModel.FirstRibCol)
                stream << '\t%s\n' %values(ProcessorModel.ThreeDShConfModel.LastRibCol)
                
                numLines = self.threeDShUpDet_M.numRowsForConfig(g+1)
                stream << 'upper\t%s\t1\n' %numLines
                
                for l in range (0, numLines):
                    values = self.threeDShUpDet_M.getRow(g+1, l+1)
                    stream << '%s' %(l+1)
                    
                    for p in range (0, 3):
                        stream << '\t%s' %values(p)
                        if p== 2:
                            stream << '\n'
                            
                numLines = self.threeDShLoDet_M.numRowsForConfig(g+1)
                stream << 'lower\t%s\t1\n' %numLines
                
                for l in range (0, numLines):
                    values = self.threeDShLoDet_M.getRow(g+1, l+1)
                    stream << '%s' %(l+1)
                    
                    for p in range (0, 3):
                        stream << '\t%s' %values(p)
                        if p== 2:
                            stream << '\n'

            stream << '* Print parameters\n'
            numLines = self.threeDShPr_M.numRowsForConfig(1)
            for l in range (0, numLines):
                values = self.threeDShPr_M.getRow(1, l+1)
                
                for p in range (0, 5):
                    if p>0:
                        stream << '\t'
                    stream << '%s' %values(p)
                    if p== 4:
                        stream << '\n'
        
        stream << separator            
        stream << '*       30. AIRFOIL THICKNESS MODIFICATION\n'
        stream << separator
        if self.airfThick_M.isUsed() == False:
            stream << '0\n'
        else:
            stream << '1\n'
            
            numLines = self.airfThick_M.numRowsForConfig(1)
            for l in range (0, numLines):
                values = self.airfThick_M.getRow(1, l+1)
                
                stream << '%s' %(l+1)
                stream << '\t%s\n' %values(0)
                
        stream << separator            
        stream << '*       31. NEW SKIN TENSION MODULE\n'
        stream << separator
        numGroups = self.newSkinTensConf_M.numConfigs()
        if numGroups == 0:
            stream << '0\n'
        else:
            stream << '1\n'
            stream << '%s\n' %numGroups
            
            for g in range (0, numGroups):
                stream << '* Skin tension group\n'
                values = self.newSkinTensConf_M.getRow(g+1, 1)
                numLines = self.newSkinTensDet_M.numRowsForConfig(g+1)
                
                stream << '%s' %(g+1)
                stream << '\t%s' %values(ProcessorModel.NewSkinTensConfModel.InitialRibCol)
                stream << '\t%s' %values(ProcessorModel.NewSkinTensConfModel.FinalRibCol)
                stream << '\t%s' %numLines
                stream << '\t1\n'
                
                for l in range (0, numLines):
                    values = self.newSkinTensDet_M.getRow(g+1, l+1)
                    
                    stream << '%s' %(l+1)
                    for p in range (0, 4):
                        stream << '\t%s' %values(p)
                        if p== 3:
                            stream << '\n'
        
        stream.flush()
        outFile.close()
        
        if forProc == False:
            # Then we need to set the right file version
            self.setFileVersion('3.10')
        
            # Make flags in order
            #self.dataStatusUpdate.emit(self.__className,'Open')

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



        
    class AddRibPointsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the parameters for the additional rib points. 
        '''
        __className = 'AddRibPointsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column used for ordering the individual lines of a config'''
        XCoordCol = 1
        ''':attr: Number of the col holding the X-Coordinate'''
        YCoordCol = 2
        ''':attr: Number of the col holding the Y-Coordinate'''
        ConfigNumCol = 3
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists AddRibPoints;")
            query.exec("create table if not exists AddRibPoints ("
                    "OrderNum INTEGER,"
                    "XCoord REAL,"
                    "YCoord REAL,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("AddRibPoints")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("X-Coordinate [% Chord]"))
            self.setHeaderData(2, Qt.Horizontal, _("Y-Coordinate [% Chord]"))
        
        def updateRow(self, configNum, orderNum, xCoord, yCoord):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE AddRibPoints SET "
                          "XCoord= :xCoord, "
                          "YCoord= :yCoord "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":xCoord", xCoord )
            query.bindValue(":yCoord", yCoord )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "XCoord, "
                            "YCoord "
                            "FROM AddRibPoints WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value


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
        
        
        def createTable(self):
            '''
            :method: Creates initially the empty anchor points table
            ''' 
            logging.debug(self.__className+'.createTable')   
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
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Airfoils")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(0, Qt.Horizontal, _("Rib Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Name"))
            self.setHeaderData(2, Qt.Horizontal, _("Intake Start"))
            self.setHeaderData(3, Qt.Horizontal, _("Intake End"))
            self.setHeaderData(4, Qt.Horizontal, _("Open-close"))
            self.setHeaderData(5, Qt.Horizontal, _("Displac"))
            self.setHeaderData(6, Qt.Horizontal, _("Rel weight"))
            self.setHeaderData(7, Qt.Horizontal, _("rrw"))
            
        def getRow(self, ribNum):
            '''
            :method: reads values back from the internal database for a specific rib number
            :param ribNum: Rib number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "AirfName, "
                            "IntakeStart, "
                            "IntakeEnd, "
                            "OpenClose, "
                            "Displac, "
                            "RelWeight, "
                            "rrw "
                            "FROM Airfoils WHERE (RibNum = :rib)")
            query.bindValue(":rib", ribNum )
            query.exec()
            query.next()
            return query.value

    class AirfoilThicknessModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'AirfoilThicknessModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''
       
        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        CoeffCol = 1
        ''':attr: Number of the col holding thickness parameter'''
        ConfigNumCol = 2
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("AirfoilThickness")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(0, Qt.Horizontal, _("Airfoil num"))
            self.setHeaderData(1, Qt.Horizontal, _("Coeff"))
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists AirfoilThickness;")
            query.exec("create table if not exists AirfoilThickness ("
                    "OrderNum INTEGER, "
                    "Coeff REAL, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, coeff):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE AirfoilThickness SET "
                          "Coeff= :coeff "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":coeff", coeff )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className+'.setIsUsed')
            self.__isUsed = isUsed
            self.usageUpd.emit()
        
        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className+'.isUsed')
            return self.__isUsed
        
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "Coeff "
                            "FROM AirfoilThickness WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

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
            
            self.setHeaderData(0, Qt.Horizontal, _("Rib Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Num Anchors"))
            self.setHeaderData(2, Qt.Horizontal, _("Pos A"))
            self.setHeaderData(3, Qt.Horizontal, _("Pos B"))
            self.setHeaderData(4, Qt.Horizontal, _("Pos C"))
            self.setHeaderData(5, Qt.Horizontal, _("Pos D"))
            self.setHeaderData(6, Qt.Horizontal, _("Pos E"))
            self.setHeaderData(7, Qt.Horizontal, _("Pos F"))
            
        def getRow(self, ribNum):
            '''
            :method: reads values back from the internal database for a specific rib number
            :param ribNum: Rib number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "NumAnchors, "
                            "PosA, "
                            "PosB, "
                            "PosC, "
                            "PosD, "
                            "PosE, "
                            "PosF "
                            "FROM AnchorPoints WHERE (RibNum = :rib)")
            query.bindValue(":rib", ribNum )
            query.exec()
            query.next()
            return query.value

    class BrakesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the lines parameters. 
        '''
        __className = 'BrakesModel'
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
        
        def updateRow(self, configNum, orderNum, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
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
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "NumBranches, "
                            "BranchLvlOne, "
                            "OrderLvlOne, "
                            "LevelOfRamTwo, "
                            "OrderLvlTwo, "
                            "LevelOfRamThree, "
                            "OrderLvlThree, "
                            "BranchLvlFour, "
                            "OrderLvlFour, "
                            "AnchorLine, "
                            "AnchorRibNum "
                            "FROM Brakes WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

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
            
        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "s1, "
                            "s2, "
                            "s3, "
                            "s4, "
                            "s5, "
                            "d1, "
                            "d2, "
                            "d3, "
                            "d4, "
                            "d5 "
                            "FROM BrakeLenght")
            query.exec()
            query.next()
            
            return query.value
        
    class CalageVarModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'CalageVarModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''
       
        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        NumRisersCol = 1
        ''':attr: Number of the col holding the fixed line name '''
        PosACol = 2
        ''':attr: Number of the col holding the position for riser A'''
        PosBCol = 3
        ''':attr: Number of the col holding the position for riser B'''
        PosCCol = 4
        ''':attr: Number of the col holding the position for riser C'''
        PosDCol = 5
        ''':attr: Number of the col holding the position for riser D'''
        PosECol = 6
        ''':attr: Number of the col holding the position for riser E'''
        PosFCol = 7
        ''':attr: Number of the col holding the position for riser F'''
        MaxNegAngCol = 8 
        ''':attr: Number of the col holding the max negative angle'''
        NumNegStepsCol = 9 
        ''':attr: Number of the col holding the number of steps for the positive angle simulation'''
        MaxPosAngCol = 10
        ''':attr: Number of the col holding the max positive angle'''
        NumPosStepsCol = 11 
        ''':attr: Number of the col holding the number of steps for the negative angle simulation'''
        ConfigNumCol = 12
        ''':attr: num of column for config number (always 1)'''
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("CalageVar")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setNumRowsForConfig(1,1)
                    
            self.setHeaderData(1, Qt.Horizontal, _("Num Risers"))
            self.setHeaderData(2, Qt.Horizontal, _("Pos R. A [%]"))
            self.setHeaderData(3, Qt.Horizontal, _("Pos R. B [%]"))
            self.setHeaderData(4, Qt.Horizontal, _("Pos R. C [%]"))
            self.setHeaderData(5, Qt.Horizontal, _("Pos R. D [%]"))
            self.setHeaderData(6, Qt.Horizontal, _("Pos R. E [%]"))
            self.setHeaderData(7, Qt.Horizontal, _("Pos R. F [%]"))
            self.setHeaderData(8, Qt.Horizontal, _("Max neg ang [deg]"))
            self.setHeaderData(9, Qt.Horizontal, _("Num pos steps"))
            self.setHeaderData(10, Qt.Horizontal, _("Max pos ang [deg]"))
            self.setHeaderData(11, Qt.Horizontal, _("Num neg steps"))
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists CalageVar;")
            query.exec("create table if not exists CalageVar ("
                    "OrderNum INTEGER, "
                    "NumRisers INTEGER, "
                    "PosA REAL, "
                    "PosB REAL, "
                    "PosC REAL, "
                    "PosD REAL, "
                    "PosE REAL, "
                    "PosF REAL, "
                    "MaxNegAng REAL, "
                    "NumNegSteps INTEGER, "
                    "MaxPosAng REAL, "
                    "NumPosSteps INTEGER, "
                    "ConfigNum INTEGER, "
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, numRisers, posA, posB, posC, posD, posE, posF, maxNegAng, numNegSteps, maxPosAng, numPosSteps):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE CalageVar SET "
                          "NumRisers= :numRisers, "
                          "PosA= :posA, "
                          "PosB= :posB, "
                          "PosC= :posC, "
                          "PosD= :posD, "
                          "PosE= :posE, "
                          "PosF= :posF, "
                          "MaxNegAng= :maxNegAng, "
                          "NumNegSteps= :numNegSteps, "
                          "MaxPosAng= :maxPosAng, "
                          "NumPosSteps= :numPosSteps "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":numRisers", numRisers )
            query.bindValue(":posA", posA )
            query.bindValue(":posB", posB )
            query.bindValue(":posC", posC )
            query.bindValue(":posD", posD )
            query.bindValue(":posE", posE )
            query.bindValue(":posF", posF )
            query.bindValue(":maxNegAng", maxNegAng )
            query.bindValue(":numNegSteps", numNegSteps )
            query.bindValue(":maxPosAng", maxPosAng )
            query.bindValue(":numPosSteps", numPosSteps )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
        
        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className+'.setIsUsed')
            self.__isUsed = isUsed
            self.usageUpd.emit()
        
        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className+'.isUsed')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "NumRisers, "
                            "PosA, "
                            "PosB, "
                            "PosC, "
                            "PosD, "
                            "PosE, "
                            "PosF, "
                            "MaxNegAng, "
                            "NumNegSteps, "
                            "MaxPosAng, "
                            "NumPosSteps "
                            "FROM CalageVar WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value


    class DxfLayerNamesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'DxfLayerNamesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        LayerCol = 1
        ''':attr: Number of the col holding the lepg name of a layer'''
        DescriptionCol = 2
        ''':attr: Number of the col holding the user defined name of a layer'''
        ConfigNumCol = 3
        ''':attr: num of column for config number (always 1)'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists DxfLayerNames;")
            query.exec("create table if not exists DxfLayerNames ("
                    "OrderNum INTEGER,"
                    "Layer text,"
                    "Description text,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("DxfLayerNames")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(1, Qt.Horizontal, _("Layer name"))
            self.setHeaderData(2, Qt.Horizontal, _("Description"))
            
        def updateRow(self, configNum, orderNum, layer, desc):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE DxfLayerNames SET "
                          "Layer= :layer, "
                          "Description= :desc "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":layer", layer )
            query.bindValue(":desc", desc )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "Layer, "
                            "Description "
                            "FROM DxfLayerNames WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class ElasticLinesCorrModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the parameters for the elastic lines correction. 
        '''
        __className = 'ElasticLinesCorrModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        LoadCol = 0 
        ''':attr: Num of column for flight load'''
        TwoLineDistACol = 1
        ''':attr: Num of column for 1st two line load dist'''
        TwoLineDistBCol = 2
        ''':attr: Num of column for 2nd two line load dist'''
        ThreeLineDistACol = 3
        ''':attr: Num of column for 1st tree line load dist'''
        ThreeLineDistBCol = 4
        ''':attr: Num of column for 2nd tree line load dist'''
        ThreeLineDistCCol = 5
        ''':attr: Num of column for 3rd tree line load dist'''
        FourLineDistACol = 6
        ''':attr: Num of column for 1st four line load distr'''
        FourLineDistBCol = 7
        ''':attr: Num of column for 2nd four line load distr'''
        FourLineDistCCol = 8
        ''':attr: Num of column for 3rd four line load distr'''
        FourLineDistDCol = 9
        ''':attr: Num of column for 4th four line load distr'''
        FiveLineDistACol = 10
        ''':attr: Num of column for 1st five line load distr'''
        FiveLineDistBCol = 11
        ''':attr: Num of column for 2nd five line load distr'''
        FiveLineDistCCol = 12
        ''':attr: Num of column for 3rd five line load distr'''
        FiveLineDistDCol = 13
        ''':attr: Num of column for 4th five line load distr'''
        FiveLineDistECol = 14
        ''':attr: Num of column for 5th five line load distr'''
        
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists ElaslticLinesCorr;")
            query.exec("create table if not exists ElaslticLinesCorr ("
                    "Load REAL,"
                    "TwoLineDistA REAL, "
                    "TwoLineDistB REAL, "
                    "ThreeLineDistA REAL, "
                    "ThreeLineDistB REAL, "
                    "ThreeLineDistC REAL, "
                    "FourLineDistA REAL, "
                    "FourLineDistB REAL, "
                    "FourLineDistC REAL, "
                    "FourLineDistD REAL, "
                    "FiveLineDistA REAL, "
                    "FiveLineDistB REAL, "
                    "FiveLineDistC REAL, "
                    "FiveLineDistD REAL, "
                    "FiveLineDistE REAL, "
                    "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into ElaslticLinesCorr (ID) Values( '1' );")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ElaslticLinesCorr")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "Load, "
                            "TwoLineDistA, "
                            "TwoLineDistB, "
                            "ThreeLineDistA, "
                            "ThreeLineDistB, "
                            "ThreeLineDistC, "
                            "FourLineDistA, "
                            "FourLineDistB, "
                            "FourLineDistC, "
                            "FourLineDistD, "
                            "FiveLineDistA, "
                            "FiveLineDistB, "
                            "FiveLineDistC, "
                            "FiveLineDistD, "
                            "FiveLineDistE "
                            "FROM ElaslticLinesCorr")
            query.exec()
            query.next()
            return query.value

    class ElasticLinesDefModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Elastic lines deformation parameters. (2nd part of elastic lines correction)
        '''
        __className = 'ElasticLinesDefModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: used here for the number of lines'''
        DefLowCol = 1
        ''':attr: Number of the col holding the deformation in the lower level'''
        DefMidCol = 2
        ''':attr: Number of the col holding the deformation in the medium level'''
        DefHighCol = 3
        ''':attr: Number of the col holding the deformation in the higher level'''
        ConfigNumCol = 4
        ''':attr: num of column for config number (always 1)'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists ElaslticLinesDef;")
            query.exec("create table if not exists ElaslticLinesDef ("
                    "OrderNum INTEGER,"
                    "DefLow REAL,"
                    "DefMid REAL,"
                    "DefHigh REAL,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ElaslticLinesDef")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(0, Qt.Horizontal, _("Num lines per rib"))
            self.setHeaderData(1, Qt.Horizontal, _("Def in lower level"))
            self.setHeaderData(2, Qt.Horizontal, _("Def in mid level"))
            self.setHeaderData(3, Qt.Horizontal, _("Def in higher level"))
            
            self.setNumRowsForConfig(1,5)
            
        def updateRow(self, configNum, orderNum, defLow, defMid, defHigh):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ElaslticLinesDef SET "
                          "DefLow= :defLow, "
                          "DefMid= :defMid, "
                          "DefHigh= :defHigh "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":defLow", defLow )
            query.bindValue(":defMid", defMid )
            query.bindValue(":defHigh", defHigh )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "DefLow, "
                            "DefMid, "
                            "DefHigh "
                            "FROM ElaslticLinesDef WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class ExtradColsConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the Extrados colors configuration 
        '''
        __className = 'ExtradColsConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''
        
        def createTable(self):
                '''
                :method: Creates initially the empty table.
                ''' 
                logging.debug(self.__className+'.createTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists ExtradColsConf;")
                query.exec("create table if not exists ExtradColsConf ("
                        "OrderNum INTEGER,"
                        "FirstRib INTEGER,"
                        "ConfigNum INTEGER,"
                        "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ExtradColsConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
        
        def updateRow(self, configNum, firstRib):
            logging.debug(self.__className+'.updateRow')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ExtradColsConf SET FirstRib= :firstRib WHERE (ConfigNum = :config);")
            query.bindValue(":firstRib", firstRib )
            query.bindValue(":config", configNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "FirstRib "
                            "FROM ExtradColsConf WHERE (ConfigNum = :config)")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            return query.value

            
    class ExtradColsDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all detail data related to the Extrados colors 
        '''
        __className = 'ExtradColsDetModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        DistTeCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''
        
        def createTable(self):
                '''
                :method: Creates initially the empty table.
                ''' 
                logging.debug(self.__className+'.createTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists ExtradColsDet;")
                query.exec("create table if not exists ExtradColsDet ("
                        "OrderNum INTEGER,"
                        "DistTe INTEGER,"
                        "ConfigNum INTEGER,"
                        "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ExtradColsDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Dist TE [% chord]"))
        
        def updateRow(self, configNum, orderNum, distTe):
            logging.debug(self.__className+'.updateRow')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ExtradColsDet SET DistTe= :distTe WHERE (ConfigNum = :config  AND OrderNum = :order);")
            query.bindValue(":distTe", distTe )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "DistTe "
                            "FROM ExtradColsDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value
            
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
            
        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "Finesse, "
                            "CentOfPress, "
                            "Calage, "
                            "Risers, "
                            "Lines, "
                            "Karabiners "
                            "FROM GlobalAoA")
            query.exec()
            query.next()
            return query.value

    class GlueVentModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'GlueVentModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''
       
        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        VentParamCol = 1
        ''':attr: Number of the col holding the vent parameter'''
        ConfigNumCol = 2
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("GlueVent")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(0, Qt.Horizontal, _("Airfoil num"))
            self.setHeaderData(1, Qt.Horizontal, _("Vent param"))
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists GlueVent;")
            query.exec("create table if not exists GlueVent ("
                    "OrderNum INTEGER, "
                    "VentParam REAL, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, ventParam):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE GlueVent SET "
                          "VentParam= :ventParam "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":ventParam", ventParam )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className+'.setIsUsed')
            self.__isUsed = isUsed
            self.usageUpd.emit()
        
        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className+'.isUsed')
            return self.__isUsed
        
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "VentParam "
                            "FROM GlueVent WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value
    
    class HvVhRibsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the lines parameters. 
        '''
        __className = 'HvVhRibsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
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

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "RibNum, "
                            "Type, "
                            "IniRib, "
                            "ParamA, "
                            "ParamB, "
                            "ParamC, "
                            "ParamD, "
                            "ParamE, "
                            "ParamF, "
                            "ParamG, "
                            "ParamH, "
                            "ParamI "
                            "FROM HvVhRibs WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class IntradColsConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the Intrados colors configuration 
        '''
        __className = 'IntradColsConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''
        
        def createTable(self):
                '''
                :method: Creates initially the empty table.
                ''' 
                logging.debug(self.__className+'.createTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists IntradColsConf;")
                query.exec("create table if not exists IntradColsConf ("
                        "OrderNum INTEGER,"
                        "FirstRib INTEGER,"
                        "ConfigNum INTEGER,"
                        "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("IntradColsConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
        
        def updateRow(self, configNum, firstRib):
            logging.debug(self.__className+'.updateRow')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE IntradColsConf SET FirstRib= :firstRib WHERE (ConfigNum = :config);")
            query.bindValue(":firstRib", firstRib )
            query.bindValue(":config", configNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "FirstRib "
                            "FROM IntradColsConf WHERE (ConfigNum = :config)")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            return query.value

            
    class IntradColsDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all detail data related to the Intrados colors 
        '''
        __className = 'IntradColsDetModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        DistTeCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''
        
        def createTable(self):
                '''
                :method: Creates initially the empty table.
                ''' 
                logging.debug(self.__className+'.createTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists IntradColsDet;")
                query.exec("create table if not exists IntradColsDet ("
                        "OrderNum INTEGER,"
                        "DistTe INTEGER,"
                        "ConfigNum INTEGER,"
                        "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("IntradColsDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Dist TE [% chord]"))
        
        def updateRow(self, configNum, orderNum, distTe):
            logging.debug(self.__className+'.updateRow')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE IntradColsDet SET DistTe= :distTe WHERE (ConfigNum = :config  AND OrderNum = :order);")
            query.bindValue(":distTe", distTe )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "DistTe "
                            "FROM IntradColsDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value


    class JoncsDefModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Joncs definition data
        '''
        __className = 'JoncsDefModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: Number of the col holding the first rib'''
        LastRibCol = 2
        ''':attr: Number of the col holding the last rib'''
        pBACol = 3 
        ''':attr: Number of the col holding the 1st param of 2nd row'''
        pBBCol = 4
        ''':attr: Number of the col holding the 2nd param of 2nd row'''
        pBCCol = 5
        ''':attr: Number of the col holding the 3rd param of 2nd row'''
        pBDCol = 6 
        ''':attr: Number of the col holding the 4th param of 2nd row'''
        pBECol = 7
        ''':attr: Number of the col holding the 5th param of 2nd row'''
        pCACol = 8 
        ''':attr: Number of the col holding the 1st param of 3rd row'''
        pCBCol = 9
        ''':attr: Number of the col holding the 2nd param of 3rd row'''
        pCCCol = 10
        ''':attr: Number of the col holding the 3rd param of 3rd row'''
        pCDCol = 11
        ''':attr: Number of the col holding the 4th param of 3rd row'''
        pDACol = 12
        ''':attr: Number of the col holding the 1st param of 4th row'''
        pDBCol = 13
        ''':attr: Number of the col holding the 2nd param of 4th row'''
        pDCCol = 14
        ''':attr: Number of the col holding the 3rd param of 4th row'''
        pDDCol = 15
        ''':attr: Number of the col holding the 4th param of 4th row'''
        TypeCol = 16 
        ''':attr: Number of the col holding the type num'''
        ConfigNumCol = 17
        ''':attr: num of column for config number (always 1)'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists JoncsDef;")
            query.exec("create table if not exists JoncsDef ("
                    "OrderNum INTEGER, "
                    "FirstRib INTEGER, "
                    "LastRib INTEGER, "
                    "pBA REAL, "
                    "pBB REAL, "
                    "pBC REAL, "
                    "PBD REAL, "
                    "pBE REAL, "
                    "pCA REAL, "
                    "pCB REAL, "
                    "pCC REAL, "
                    "PCD REAL, "
                    "pDA REAL, "
                    "pDB REAL, "
                    "pDC REAL, "
                    "PDD REAL, "
                    "Type INTEGER, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("JoncsDef")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))                    
            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
            self.setHeaderData(3, Qt.Horizontal, _("Row 2 A"))
            self.setHeaderData(4, Qt.Horizontal, _("Row 2 B"))
            self.setHeaderData(5, Qt.Horizontal, _("Row 2 C"))
            self.setHeaderData(6, Qt.Horizontal, _("Row 2 D"))
            self.setHeaderData(7, Qt.Horizontal, _("Row 2 E"))
            self.setHeaderData(8, Qt.Horizontal, _("Row 3 A"))
            self.setHeaderData(9, Qt.Horizontal, _("Row 3 B"))
            self.setHeaderData(10, Qt.Horizontal, _("Row 3 C"))
            self.setHeaderData(11, Qt.Horizontal, _("Row 3 D"))
            self.setHeaderData(12, Qt.Horizontal, _("Row 4 A"))
            self.setHeaderData(13, Qt.Horizontal, _("Row 4 B"))
            self.setHeaderData(14, Qt.Horizontal, _("Row 4 C"))
            self.setHeaderData(15, Qt.Horizontal, _("Row 4 D"))
            
        def updateTypeOneRow(self, configNum, orderNum, firstRib, lastRib, pBA, pBB, pBC, pBD, pCA, pCB, pCC, pCD, pDA, pDB, pDC, pDD):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateTypeOneRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE JoncsDef SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib, "
                          "pBA= :pBA, "
                          "pBB= :pBB, "
                          "pBC= :pBC, "
                          "pBD= :pBD, "
                          "pCA= :pCA, "
                          "pCB= :pCB, "
                          "pCC= :pCC, "
                          "pCD= :pCD, "
                          "pDA= :pDA, "
                          "pDB= :pDB, "
                          "pDC= :pDC, "
                          "pDD= :pDD, "
                          "Type= :t "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib )
            query.bindValue(":lastRib", lastRib )
            query.bindValue(":pBA", pBA )
            query.bindValue(":pBB", pBB )
            query.bindValue(":pBC", pBC )
            query.bindValue(":pBD", pBD )
            query.bindValue(":pCA", pCA )
            query.bindValue(":pCB", pCB )
            query.bindValue(":pCC", pCC )
            query.bindValue(":pCD", pCD )
            query.bindValue(":pDA", pDA )
            query.bindValue(":pDB", pDB )
            query.bindValue(":pDC", pDC )
            query.bindValue(":pDD", pDD )
            query.bindValue(":t", 1 )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def updateTypeTwoRow(self, configNum, orderNum, firstRib, lastRib, pBA, pBB, pBC, pBD, pBE ,pCA, pCB, pCC, pCD):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateTypeTwoRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE JoncsDef SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib, "
                          "pBA= :pBA, "
                          "pBB= :pBB, "
                          "pBC= :pBC, "
                          "pBD= :pBD, "
                          "pBE= :pBE, "
                          "pCA= :pCA, "
                          "pCB= :pCB, "
                          "pCC= :pCC, "
                          "pCD= :pCD, "
                          "Type= 2 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib )
            query.bindValue(":lastRib", lastRib )
            query.bindValue(":pBA", pBA )
            query.bindValue(":pBB", pBB )
            query.bindValue(":pBC", pBC )
            query.bindValue(":pBD", pBD )
            query.bindValue(":pBE", pBE )
            query.bindValue(":pCA", pCA )
            query.bindValue(":pCB", pCB )
            query.bindValue(":pCC", pCC )
            query.bindValue(":pCD", pCD )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def setType(self, configNum, typeNum):
            '''
            :method: Sets for all rows of a specific config the type num 
            :param typeNum: 1: type== 1; 2: type== 2
            '''
            logging.debug(self.__className+'.setType')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE JoncsDef SET "
                          "type= :typeNum "
                          "WHERE (ConfigNum = :config);")
            query.bindValue(":typeNum", typeNum )
            query.bindValue(":config", configNum )
            query.exec()
        
        def getType(self, configNum):
            '''
            :method: Detects for a defined config if the type is set. 
            :return: 0: type is empty; 1: type== 1; 2: type== 2
            '''
            logging.debug(self.__className+'.getType')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select Type FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum ASC;")
            query.bindValue(":config", configNum )
            query.exec()
            typeNum = 0
            if query.next():
                typeNum = query.value(0)
                if typeNum == "":
                    typeNum = 0
            
            return typeNum
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "FirstRib, "
                            "LastRib, "
                            "pBA, "
                            "pBB, "
                            "pBC, "
                            "PBD, "
                            "pBE, "
                            "pCA, "
                            "pCB, "
                            "pCC, "
                            "PCD, "
                            "pDA, "
                            "pDB, "
                            "pDC, "
                            "PDD, "
                            "Type "
                            "FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value
            
            
    class LightConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the global lightening config parameters 
        '''
       
        __className = 'LightConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        __numConfigs = 0
        
        OrderNumCol = 0 
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        InitialRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        FinalRibCol = 2 
        ''':attr: number of the column holding the final rib'''
        ConfigNumCol = 3
        ''':attr: number of the column holding the config number'''
        
        def createTable(self):
                '''
                :method: Creates initially the empty LightConf table.
                ''' 
                logging.debug(self.__className+'.createTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists LightConf;")
                query.exec("create table if not exists LightConf ("
                        "OrderNum INTEGER,"
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
            self.createTable()
            self.setTable("LightConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(1, Qt.Horizontal, _("Initial Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Final Rib"))
        
        def updateRow(self, config, initialRib, finalRib):
            logging.debug(self.__className+'.setConfigRow')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE LightConf SET InitialRib= :initial , FinalRib= :final WHERE (ConfigNum = :config);")
            query.bindValue(":initial", initialRib )
            query.bindValue(":final", finalRib )
            query.bindValue(":config", config )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config number
            :param configNum: Configuration number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select "
                            "InitialRib, "
                            "FinalRib "
                            "FROM LightConf WHERE (ConfigNum = :config)")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            return query.value


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

        def createTable(self):
                '''
                :method: Creates initially the empty lightening details table.
                ''' 
                logging.debug(self.__className+'.createTable')   
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
            self.createTable()
            self.setTable("LightDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Light Typ"))
            self.setHeaderData(2, Qt.Horizontal, _("Dist LE"))
            self.setHeaderData(3, Qt.Horizontal, _("Dist chord"))
            self.setHeaderData(4, Qt.Horizontal, _("Hor axis"))
            self.setHeaderData(5, Qt.Horizontal, _("Vert axis"))
            self.setHeaderData(6, Qt.Horizontal, _("Rot angle"))
            self.setHeaderData(7, Qt.Horizontal, _("Opt "))

        def updateRow(self, configNum, orderNum, LightTyp, DistLE, DisChord, HorAxis, VertAxis, RotAngle, Opt1):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
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
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "LightTyp, "
                            "DistLE, "
                            "DisChord, "
                            "HorAxis, "
                            "VertAxis, "
                            "RotAngle, "
                            "Opt1 "
                            "FROM LightDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value
       
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
                
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "NumBranches, "
                            "BranchLvlOne, "
                            "OrderLvlOne, "
                            "LevelOfRamTwo, "
                            "OrderLvlTwo, "
                            "LevelOfRamThree, "
                            "OrderLvlThree, "
                            "BranchLvlFour, "
                            "OrderLvlFour, "
                            "AnchorLine, "
                            "AnchorRibNum "
                            "FROM Lines WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

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
            
        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "MarksSp, "
                            "PointRad, "
                            "PointDispl "
                            "FROM Marks")
            query.exec()
            query.next()
            return query.value

    class MarksTypesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'MarksTypesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        TypeCol = 1
        ''':attr: Number of the col holding the type description of the mark'''
        FormOneCol = 2
        ''':attr: Number of the col holding the first mark form'''
        FormOnePOneCol = 3 
        ''':attr: Number of the col holding the first parameter for the 1st mark form'''
        FormOnePTwoCol = 4
        ''':attr: Number of the col holding the 2nd parameter for the 1st mark form'''
        FormTwoCol = 5
        ''':attr: Number of the col holding the 2nd mark form'''
        FormTwoPOneCol = 6 
        ''':attr: Number of the col holding the first parameter for the 2nd mark form'''
        FormTwoPTwoCol = 7
        ''':attr: Number of the col holding the 2nd parameter for the 2nd mark form'''
        ConfigNumCol = 8
        ''':attr: num of column for config number (always 1)'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists MarksTypes;")
            query.exec("create table if not exists MarksTypes ("
                    "OrderNum INTEGER,"
                    "Type text,"
                    "FormOne INTEGER,"
                    "FormOnePOne REAL,"
                    "FormOnePTwo REAL,"
                    "FormTwo INTEGER,"
                    "FormTwoPOne REAL,"
                    "FormTwoPTwo REAL,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("MarksTypes")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
                    
            self.setHeaderData(1, Qt.Horizontal, _("Marks type"))
            self.setHeaderData(2, Qt.Horizontal, _("Form 1"))
            self.setHeaderData(3, Qt.Horizontal, _("Form 1 1st param"))
            self.setHeaderData(4, Qt.Horizontal, _("Form 1 2nd param"))
            self.setHeaderData(5, Qt.Horizontal, _("Form 2"))
            self.setHeaderData(6, Qt.Horizontal, _("Form 2 1st param"))
            self.setHeaderData(7, Qt.Horizontal, _("Form 2 2nd param"))
            
        def updateRow(self, configNum, orderNum, pType, formOne, formOnePOne, formOnePTwo, formTwo, formTwoPOne, formTwoPTwo):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE MarksTypes SET "
                          "Type= :pType, "
                          "FormOne= :formOne, "
                          "FormOnePOne= :formOnePOne, "
                          "FormOnePTwo= :formOnePTwo, "
                          "FormTwo= :formTwo, "
                          "FormTwoPOne= :formTwoPOne, "
                          "FormTwoPTwo= :formTwoPTwo "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":pType", pType )
            query.bindValue(":formOne", formOne )
            query.bindValue(":formOnePOne", formOnePOne )
            query.bindValue(":formOnePTwo", formOnePTwo )
            query.bindValue(":formTwo", formTwo )
            query.bindValue(":formTwoPOne", formTwoPOne )
            query.bindValue(":formTwoPTwo", formTwoPTwo )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "Type, "
                            "FormOne, "
                            "FormOnePOne, "
                            "FormOnePTwo, "
                            "FormTwo, "
                            "FormTwoPOne, "
                            "FormTwoPTwo "
                            "FROM MarksTypes WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class NewSkinTensConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the group wide parameters for New Skin Tension 
        '''
       
        __className = 'NewSkinTensConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        __numConfigs = 0
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        InitialRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        FinalRibCol = 2 
        ''':attr: number of the column holding the final rib'''
        TypeCol = 3
        ''':attr: number of the column holding type information'''
        ConfigNumCol = 4
        ''':attr: number of the column holding the config number'''
        
        def createTable(self):
                '''
                :method: Creates initially the empty table.
                ''' 
                logging.debug(self.__className+'.createTable')   
                query = QSqlQuery()
                    
                query.exec("DROP TABLE if exists NewSkinTensConf;")
                query.exec("create table if not exists NewSkinTensConf ("
                        "OrderNum INTEGER,"
                        "InitialRib INTEGER,"
                        "FinalRib INTEGER,"
                        "Type INTEGER,"
                        "ConfigNum INTEGER,"
                        "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("NewSkinTensConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
            self.setHeaderData(3, Qt.Horizontal, _("Type"))
        
        def updateRow(self, config, initialRib, finalRib, calcT):
            logging.debug(self.__className+'.updateRow')
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE NewSkinTensConf SET InitialRib= :initial , FinalRib= :final, Type= :calcT WHERE (ConfigNum = :config);")
            query.bindValue(":initial", initialRib )
            query.bindValue(":final", finalRib )
            query.bindValue(":calcT", calcT )
            query.bindValue(":config", config )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "InitialRib, "
                            "FinalRib, "
                            "Type "
                            "FROM NewSkinTensConf WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class NewSkinTensDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all detail data related to New skin tension. 
        '''
        __className = 'NewSkinTensionDetModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        TopDistLECol = 1
        ''':attr: Distance in% of chord on the leading edge of extrados'''
        TopWideCol = 2
        ''':attr: Extrados over-wide corresponding in % of chord'''
        BottDistTECol = 3
        ''':attr: Distance in% of chord on trailing edge'''
        BottWideCol = 4
        ''':attr: Intrados over-wide corresponding in% of chord'''
        ConfigNumCol = 5
        ''':attr: number of the column holding the config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty Skin tension table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists NewSkinTensDet;")
            query.exec("create table if not exists NewSkinTensDet ("
                    "OrderNum INTEGER, "
                    "TopDistLE REAL, "
                    "TopWide REAL, "
                    "BotDistTE REAL, "
                    "BotWide REAL, "
                    "ConfigNum INTEGER, "
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("NewSkinTensDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setHeaderData(0, Qt.Horizontal, _("Order num"))            
            self.setHeaderData(1, Qt.Horizontal, _("Top dist LE"))
            self.setHeaderData(2, Qt.Horizontal, _("Top widening"))
            self.setHeaderData(3, Qt.Horizontal, _("Bott dist TE"))
            self.setHeaderData(4, Qt.Horizontal, _("Bott widening"))
        
        def updateRow(self, configNum, orderNum, topDistLE, topWide, botDistTE, botWide):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: add transaction
            query = QSqlQuery()
            query.prepare("UPDATE NewSkinTensDet SET "
                          "TopDistLE= :topDis, "
                          "TopWide= :topWide, "
                          "BotDistTE= :botDis, "
                          "BotWide= :botWide  "
                          "WHERE (ConfigNum = :config AND OrderNum= :order);")
            query.bindValue(":topDis", topDistLE )
            query.bindValue(":topWide", topWide )
            query.bindValue(":botDis", botDistTE )
            query.bindValue(":botWide", botWide )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "TopDistLE, "
                            "TopWide, "
                            "BotDistTE, "
                            "BotWide "
                            "FROM NewSkinTensDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class NoseMylarsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'NoseMylarsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: Number of the col holding the first rib'''
        LastRibCol = 2
        ''':attr: Number of the col holding the last rib'''
        xOneCol = 3 
        ''':attr: Number of the col holding the 1st param of 2nd row'''
        uOneCol = 4
        ''':attr: Number of the col holding the 2nd param of 2nd row'''
        uTwoCol = 5
        ''':attr: Number of the col holding the 3rd param of 2nd row'''
        xTwoCol = 6 
        ''':attr: Number of the col holding the 4th param of 2nd row'''
        vOneCol = 7
        ''':attr: Number of the col holding the 5th param of 2nd row'''
        vTwoCol = 8 
        ''':attr: Number of the col holding the 1st param of 3rd row'''
        ConfigNumCol = 9
        ''':attr: num of column for config number (always 1)'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists NoseMylars;")
            query.exec("create table if not exists NoseMylars ("
                    "OrderNum INTEGER, "
                    "FirstRib INTEGER, "
                    "LastRib INTEGER, "
                    "xOne REAL, "
                    "uOne REAL, "
                    "uTwo REAL, "
                    "xTwo REAL, "
                    "vOne REAL, "
                    "vTwo REAL, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("NoseMylars")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))                    
            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
            self.setHeaderData(3, Qt.Horizontal, _("X1 [%chord"))
            self.setHeaderData(4, Qt.Horizontal, _("U1 [%chord"))
            self.setHeaderData(5, Qt.Horizontal, _("U2 [%chord"))
            self.setHeaderData(6, Qt.Horizontal, _("X2 [%chord"))
            self.setHeaderData(7, Qt.Horizontal, _("V1 [%chord"))
            self.setHeaderData(8, Qt.Horizontal, _("V2 [%chord"))
            
        def updateRow(self, configNum, orderNum, firstRib, lastRib, xOne, uOne, uTwo, xTwo, vOne, vTwo):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE NoseMylars SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib, "
                          "xOne= :xOne, "
                          "uOne= :uOne, "
                          "uTwo= :uTwo, "
                          "xTwo= :xTwo, "
                          "vOne= :vOne, "
                          "vTwo= :vTwo "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib )
            query.bindValue(":lastRib", lastRib )
            query.bindValue(":xOne", xOne )
            query.bindValue(":uOne", uOne )
            query.bindValue(":uTwo", uTwo )
            query.bindValue(":xTwo", xTwo )
            query.bindValue(":vOne", vOne )
            query.bindValue(":vTwo", vTwo )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "FirstRib, "
                            "LastRib, "
                            "xOne, "
                            "uOne, "
                            "uTwo, "
                            "xTwo, "
                            "vOne, "
                            "vTwo "
                            "FROM NoseMylars WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

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
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "Rows, "
                            "ThirdToSail,"
                            "FourthToSail "
                            "FROM Ramification WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            query.next()
            return query.value
           
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
            
            self.setHeaderData(0, Qt.Horizontal, _("Rib Num"))
            
        def updateRow(self, ribNum, xrib, yLE, yTE, xp, z, beta, RP, Washin):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE Rib SET "
                          "xrib = :xrib, "
                          "yLE = :yLE, "
                          "yTE = :yTE, "
                          "xp = :xp, "
                          "z = :z, "
                          "beta = :beta, "
                          "RP = :RP, "
                          "Washin = :Washin "
                          "WHERE (RibNum = :ribNum);")
            query.bindValue(":xrib", xrib )
            query.bindValue(":yLE", yLE )
            query.bindValue(":yTE", yTE )
            query.bindValue(":xp", xp )
            query.bindValue(":z", z )
            query.bindValue(":beta", beta )
            query.bindValue(":RP", RP )
            query.bindValue(":Washin", Washin )
            query.bindValue(":ribNum", ribNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def getRow(self, ribNum):
            '''
            :method: reads values back from the internal database for a specific rib number
            :param ribNum: Rib number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "xrib, "
                            "yLE, "
                            "yTE, "
                            "xp, "
                            "z, "
                            "beta, "
                            "RP, "
                            "Washin "
                            "FROM Rib WHERE (RibNum = :rib)")
            query.bindValue(":rib", ribNum )
            query.exec()
            query.next()
            return query.value

    
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
            
            self.setHeaderData(0, Qt.Horizontal, _("Top dist LE"))
            self.setHeaderData(1, Qt.Horizontal, _("Top widening"))
            self.setHeaderData(2, Qt.Horizontal, _("Bott dist TE"))
            self.setHeaderData(3, Qt.Horizontal, _("Bott widening"))
        
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
            
        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config number
            :param configNum: Configuration number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select "
                            "TopDistLE, "
                            "TopWide, "
                            "BottDistTE, "
                            "BottWide "
                            "FROM SkinTension WHERE (ID = :config)")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            return query.value

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
            
        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select "
                            "StrainMiniRibs, "
                            "NumPoints, "
                            "Coeff "
                            "FROM SkinTensionParams")
            query.exec()
            query.next()
            return query.value
            
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
            
        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific rib number
            :param ribNum: Rib number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "EdgeSeam, "
                            "LESeem, "
                            "TESeem "
                            "FROM SewingAllowances WHERE (ID = :config)")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            return query.value

    class SpecWingTipModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'SpecWingTipModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''
       
        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        AngleLECol = 1
        ''':attr: Number of the col holding the LE angle'''
        AngleTECol = 2
        ''':attr: Number of the col holding the TE angle'''
        ConfigNumCol = 3
        ''':attr: num of column for config number (always 1)'''
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SpecWingTip")
            
            self.setHeaderData(1, Qt.Horizontal, _("LE Angle [deg]"))
            self.setHeaderData(2, Qt.Horizontal, _("TE Angle [deg]"))
            
            self.setNumRowsForConfig(1,1)
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists SpecWingTip;")
            query.exec("create table if not exists SpecWingTip ("
                    "OrderNum INTEGER,"
                    "AngleLE REAL,"
                    "AngleTE REAL,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, angleLE, angleTE):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE SpecWingTip SET "
                          "AngleLE= :angleLE, "
                          "AngleTE= :angleTE "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":angleLE", angleLE )
            query.bindValue(":angleTE", angleTE )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
        
        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className+'.setIsUsed')
            self.__isUsed = isUsed
            self.usageUpd.emit()
        
        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className+'.isUsed')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "AngleLE, "
                            "AngleTE "
                            "FROM SpecWingTip WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value
        
        
    class ThreeDDxfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'ThreeDDxfModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''
       
        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        LineNameCol = 1
        ''':attr: Number of the col holding the fixed line name '''
        UnifilarCol = 2
        ''':attr: Number of the col holding the unifilar flag'''
        ColorCodeCol = 3
        ''':attr: Number of the col holding the color code'''
        ColorNameCol = 4 
        ''':attr: Number of the col holding the optional color name'''
        ConfigNumCol = 5
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDDxf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setNumRowsForConfig(1,9)
                    
            self.setHeaderData(1, Qt.Horizontal, _("Line Name"))
            self.setHeaderData(2, Qt.Horizontal, _("Unifilar"))
            self.setHeaderData(3, Qt.Horizontal, _("Color code"))
            self.setHeaderData(4, Qt.Horizontal, _("Color name (opt)"))
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists ThreeDDxf;")
            query.exec("create table if not exists ThreeDDxf ("
                    "OrderNum INTEGER,"
                    "LineName TEXT,"
                    "Unifilar INTEGER, "
                    "ColorCode INTEGER,"
                    "ColorName TEXT,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, lineName, colorCode, colorName, unifilar=0):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ThreeDDxf SET "
                          "LineName= :lineName, "
                          "Unifilar= :unifilar, "
                          "ColorCode= :colorCode, "
                          "ColorName= :colorName "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":lineName", lineName )
            query.bindValue(":unifilar", unifilar )
            query.bindValue(":colorCode", colorCode )
            query.bindValue(":colorName", colorName )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className+'.setIsUsed')
            self.__isUsed = isUsed
            self.usageUpd.emit()
        
        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className+'.isUsed')
            return self.__isUsed
        
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "LineName, "
                            "Unifilar, "
                            "ColorCode, "
                            "ColorName "
                            "FROM ThreeDDxf WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value


    class ThreeDShConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the 3d Shaping configuration
        '''
        __className = 'ThreeDShConfModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: Number of the col holding the first rib'''
        LastRibCol = 2
        ''':attr: Number of the col holding the last rib'''
        ConfigNumCol = 3
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists ThreeDShapingConf;")
            query.exec("create table if not exists ThreeDShapingConf ("
                    "OrderNum INTEGER, "
                    "FirstRib INTEGER, "
                    "LastRib INTEGER, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))                    
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
            
        def updateRow(self, configNum, orderNum, firstRib, lastRib):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingConf SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib )
            query.bindValue(":lastRib", lastRib )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "OrderNum, "
                            "FirstRib, "
                            "LastRib "
                            "FROM ThreeDShapingConf WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class ThreeDShUpDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the 3d Shaping data for the upper panels
        '''
        __className = 'ThreeDShUpDetModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        IniPointCol = 1 
        ''':attr: Number of the col holding initial point of the zone of influence'''
        CutPointCol = 2
        ''':attr: Number of the col holding position of the point where the cut is set'''
        DepthCol = 3
        ''':attr: Number of the col holding the shaping depth'''
        ConfigNumCol = 4
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists ThreeDShapingUpDetail;")
            query.exec("create table if not exists ThreeDShapingUpDetail ("
                    "OrderNum INTEGER, "
                    "IniPoint INTEGER, "
                    "CutPoint INTEGER, "
                    "Depth REAL, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingUpDetail")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Ini P [%chord]"))                    
            self.setHeaderData(2, Qt.Horizontal, _("Cut P [%chord]"))
            self.setHeaderData(3, Qt.Horizontal, _("Depth [Coef]"))
            
        def updateRow(self, configNum, orderNum, iniPoint, cutPoint, depth):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingUpDetail SET "
                          "IniPoint= :iniPoint, "
                          "CutPoint= :cutPoint, "
                          "Depth= :depth "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":iniPoint", iniPoint )
            query.bindValue(":cutPoint", cutPoint )
            query.bindValue(":depth", depth )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "IniPoint, "
                            "CutPoint, "
                            "Depth "
                            "FROM ThreeDShapingUpDetail WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value
            
    class ThreeDShLoDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the 3d Shaping data for the lower panels
        '''
        __className = 'ThreeDShLoDetModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        IniPointCol = 1 
        ''':attr: Number of the col holding initial point of the zone of influence'''
        CutPointCol = 2
        ''':attr: Number of the col holding position of the point where the cut is set'''
        DepthCol = 3
        ''':attr: Number of the col holding the shaping depth'''
        ConfigNumCol = 4
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists ThreeDShapingLoDetail;")
            query.exec("create table if not exists ThreeDShapingLoDetail ("
                    "OrderNum INTEGER, "
                    "IniPoint INTEGER, "
                    "CutPoint INTEGER, "
                    "Depth REAL, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingLoDetail")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Ini P [%chord]"))                    
            self.setHeaderData(2, Qt.Horizontal, _("Cut P [%chord]"))
            self.setHeaderData(3, Qt.Horizontal, _("Depth [Coef]"))
            
        def updateRow(self, configNum, orderNum, iniPoint, cutPoint, depth):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingLoDetail SET "
                          "IniPoint= :iniPoint, "
                          "CutPoint= :cutPoint, "
                          "Depth= :depth "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":iniPoint", iniPoint )
            query.bindValue(":cutPoint", cutPoint )
            query.bindValue(":depth", depth )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "IniPoint, "
                            "CutPoint, "
                            "Depth "
                            "FROM ThreeDShapingLoDetail WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class ThreeDShPrintModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Print data for 3d Shaping
        '''
        __className = 'ThreeDShPrintModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        NameCol = 1
        ''':attr: Number of the col holding the layer name'''
        DrawCol = 2
        ''':attr: Number of the col holding the info if the layer shall be drawn'''
        FirstPanelCol = 3 
        ''':attr: Number of the col holding the number of the first panel to print'''
        LastPanelCol = 4
        ''':attr: Number of the col holding the number of the last panel to print'''
        SymmetricCol = 5
        ''':attr: Number of the col holding the symmetric information'''
        ConfigNumCol = 6
        ''':attr: num of column for config number'''
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists ThreeDShapingPrint;")
            query.exec("create table if not exists ThreeDShapingPrint ("
                    "OrderNum INTEGER, "
                    "Name TEXT, "
                    "Draw INTEGER, "
                    "FirstPanel INTEGER, "
                    "LastPanel INTEGER, "
                    "Symmetric INTEGER, "
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")
            
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingPrint")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setNumConfigs(1)
            self.setNumRowsForConfig(1, 5)

#             self.setHeaderData(0, Qt.Horizontal, _("Order num"))                    
#             self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
#             self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
#             self.setHeaderData(3, Qt.Horizontal, _("Row 2 A"))
#             self.setHeaderData(4, Qt.Horizontal, _("Row 2 B"))
#             self.setHeaderData(5, Qt.Horizontal, _("Row 2 C"))
            
        def updateRow(self, configNum, orderNum, name, draw, firstPanel, lastPanel, symmetric):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingPrint SET "
                          "Name= :name, "
                          "Draw= :draw, "
                          "FirstPanel= :firstPanel, "
                          "LastPanel= :lastPanel, "
                          "Symmetric= :symmetric "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":name", name )
            query.bindValue(":draw", draw )
            query.bindValue(":firstPanel", firstPanel )
            query.bindValue(":lastPanel", lastPanel )
            query.bindValue(":symmetric", symmetric )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            
        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "Name, "
                            "Draw, "
                            "FirstPanel, "
                            "LastPanel, "
                            "Symmetric "
                            "FROM ThreeDShapingPrint WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

    class TwoDDxfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'TwoDDxfModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''
       
        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        OrderNumCol = 0 
        ''':attr: num of column for ordering the individual lines of a config'''
        LineNameCol = 1
        ''':attr: Number of the col holding the fixed line name '''
        ColorCodeCol = 2
        ''':attr: Number of the col holding the color code'''
        ColorNameCol = 3 
        ''':attr: Number of the col holding the optional color name'''
        ConfigNumCol = 4
        ''':attr: num of column for config number (always 1)'''
        
        def __init__(self, parent=None): # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("TwoDDxf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            
            self.setNumRowsForConfig(1,6)
                    
            self.setHeaderData(1, Qt.Horizontal, _("Line Name"))
            self.setHeaderData(2, Qt.Horizontal, _("Color code"))
            self.setHeaderData(3, Qt.Horizontal, _("Color name (opt)"))
        
        def createTable(self):
            '''
            :method: Creates initially the empty table
            ''' 
            logging.debug(self.__className+'.createTable')   
            query = QSqlQuery()
                
            query.exec("DROP TABLE if exists TwoDDxf;")
            query.exec("create table if not exists TwoDDxf ("
                    "OrderNum INTEGER,"
                    "LineName TEXT,"
                    "ColorCode INTEGER,"
                    "ColorName TEXT,"
                    "ConfigNum INTEGER,"
                    "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, lineName, colorCode, colorName):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateRow')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE TwoDDxf SET "
                          "LineName= :lineName, "
                          "ColorCode= :colorCode, "
                          "ColorName= :colorName "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":lineName", lineName )
            query.bindValue(":colorCode", colorCode )
            query.bindValue(":colorName", colorName )
            query.bindValue(":config", configNum )
            query.bindValue(":order", orderNum )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
        
        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className+'.setIsUsed')
            self.__isUsed = isUsed
            self.usageUpd.emit()
        
        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className+'.isUsed')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "LineName, "
                            "ColorCode, "
                            "ColorName "
                            "FROM TwoDDxf WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum )
            query.exec()
            query.next()
            # now we are at the first row
            i=1
            while i < orderNum:
                query.next()
                i+=1
            return query.value

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
            self.glueVent_M = ProcessorModel.GlueVentModel()
            self.airfThick_M = ProcessorModel.AirfoilThicknessModel()
            
            # self.dataChanged.connect(self.syncRibNumData)
            self.dataChanged.connect(self.manDataChange)
            
        def manDataChange(self, q):
            '''
            :method: If NumRibs is changed manually we must keep halfNumRibs and Ribs table in sync.
            '''
            logging.debug(self.__className+'.manDataChange')
            
            if q.column() == self.NumRibsCol:
                self.syncRibNumData()
            
             
        def syncRibNumData(self):
            '''
            :method: If NumRibs is changed we must keep halfNumRibs and Ribs table in sync. This method will calculate \
                the current number of half ribs and calls the method to setup the model accordingly.
            '''
            logging.debug(self.__className+'.syncRibNumData')
            
            numRibs = self.index(0, self.NumRibsCol).data()
            
            try:
                numRibs = int(numRibs)
                goOn = True
            except ValueError:
                return
            
            if goOn:
                self.halfNumRibs = math.ceil(float(numRibs) / 2)
                    
                self.rib_M.setupRibRows(self.halfNumRibs)
                self.airf_M.setupRibRows(self.halfNumRibs)
                self.anchPoints_M.setupRibRows(self.halfNumRibs)
                self.glueVent_M.setNumRowsForConfig(1, self.halfNumRibs)
                self.airfThick_M.setNumRowsForConfig(1, self.halfNumRibs)

        def updateNumCells(self, numCells):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateNumCells')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE Wing SET "
                          "NumCells= :numCells; ")
            query.bindValue(":numCells", numCells )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
                    
        def updateNumRibs(self, numRibs):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className+'.updateNumRibs')
            
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("UPDATE Wing SET "
                          "NumRibs= :numRibs; ")
            query.bindValue(":numRibs", numRibs )
            query.exec()
            self.select() # to a select() to assure the model is updated properly
            self.syncRibNumData()
        
        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className+'.getRow')
                    
            # TODO: Add transaction
            query = QSqlQuery()
            query.prepare("Select " 
                            "BrandName, "
                            "WingName, "
                            "DrawScale, "
                            "WingScale, "
                            "NumCells, "
                            "NumRibs, "
                            "AlphaMode, "
                            "AlphaMaxCent, "
                            "AlphaMaxTip, "
                            "ParaType, "
                            "ParaParam, "
                            "LinesConcType, "
                            "Brakelength, "
                            "xSpacing, "
                            "ySpacing FROM Wing")
            query.exec()
            query.next()
            return query.value
