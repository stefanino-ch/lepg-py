'''
Does take care about the data handling for the Processor. 

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
import math
import os
import logging
import re

from PyQt5.QtCore import QObject, QFile, QTextStream, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from Singleton.Singleton import Singleton
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from ConfigReader.ConfigReader import ConfigReader

class ProcessorStore(QObject, metaclass=Singleton):
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
    __className = 'ProcessorStore'
    
    # Variables used across the class
    # Single values
    __simpleData ={
        'FileNamePath' :  '' ,
        'FileVersion' : '',
        'BrandName' : '',
        'WingName' : '',  
        'DrawScale' : '',
        'WingScale' : '', 
        'NumCells' : '',
        'NumRibs' : '',
        'HalfNumRibs': '', 
        'AlphaMaxP1' : '',
        'AlphaMaxP2' : '',
        'AlphaMaxP3' : '', 
        'ParaTypeP1' : '',
        'ParaTypeP2' : '',
        'NumAirfoilHoleConfigs' : '',
        'StrainMiniRibs' : '',
        'NumSkinTensionPoints' : '',
        'SkinTensionCoeff' : '',
        'SewingAllRibs' : '',
        'SewingAllVRibs' : '',
        'MarksP1' : '',
        'MarksP2' : '',
        'MarksP3' : '',
        'FinesseGR' : '',
        'CentOfPress' : '',
        'Calage' : '',
        'RaisersLenght' : '',
        'LineLength' : '',
        'Karabiners' : '',
        'LineDescConc' : '',
        'NumLineDesConfigs' : '',
        'BrakeLength' : '',
        'NumBrakePath' : '',
        'NumMiniRibs' : '',
        'MiniRibXSpacing' : '',
        'MiniRibYSpacing' : '',
        'NumRibsExtradColors': '',
        'NumRibsIntradColors': '',
        'NumAddRibPoints': '',
        'InFlightLoad': '',
        'NumDxfLayers': '',
        'NumMarkTypes': '',
        'JoncsType': '',
        'NumJoncsConfigs': '',
        'NoseMylarsType': '',
        'NumNoseMylarsConfigs': '',
        'TabReinfType': '',
        'NumTabReinfConfigs': '',
        'twoDDxfType': '',
        'threeDDxfType': '',
        'glueVentType': '',
        'specWingTypType': '',
        'specWingTypAngLE': '',
        'specWingTypAngTE': '',
        'calageVarType': '',
        'numCalageVarRisers': '',
        'threeDShapingType': '',
        'threeDShapingTheory': '',
        'NumThreeDShapingGroups': '',
        'airfoilThiknessModifType': '',
        'skinTensionType': '',
        'numSkinTensionGroups': '',
    }
    
    # Rib geometric parameters
    __RibGeomParams = [ [0 for x in range(8)] for y in range(1)]
    # Airfolis
    __AirfoilParams = [ [0 for x in range(7)] for y in range(1)]
    # ANCHOR POINTS
    __AnchorPointParams = [ [0 for x in range(7)] for y in range(1)]
    # AIRFOIL HOLES
    __AirfHoleConf = [ [0 for x in range(3)] for y in range(1)]
    __AirfHoleParams = [ [ [0 for x in range(9)] for y in range(1)] for z in range(1)]
    # Skin Tension
    __SkinTensionParams = [ [0 for x in range(4)] for y in range(6)]
    # SEWING ALLOWANCES
    __SewingAllPanelsParams = [ [0 for x in range(3)] for y in range(2)]
    # SUSPENSION LINES DESCRIPTION
    __LineDescConf = [0 for x in range(1)]
    __LineDescParams = [ [ [0 for x in range(11)] for y in range(1)] for z in range(1)]
    # BRAKES
    __BrakePathParams = [ [0 for x in range(11)] for y in range(1)]
    __BrakeDistrParams = [ [0 for x in range(5)] for y in range(2)]
    # Ramification lengths
    __RamLengthParams = [ [0 for x in range(3)] for y in range(4)]
    # H V and VH ribs (Mini Ribs)
    __MiniRibParams = [ [0 for x in range(12)] for y in range(1)]
    # Extrados colors
    __ExtradColorsConf = [ [0 for x in range(2)] for y in range(1)]
    __ExtradColorsParams = [ [ [0 for x in range(3)] for y in range(1)] for z in range(1)]
    # Intrados colors
    __IntradColorsConf = [ [0 for x in range(2)] for y in range(1)]
    __IntradColorsParams = [ [ [0 for x in range(3)] for y in range(1)] for z in range(1)]
    # Aditional rib points
    __AddRibPointsParams = [ [0 for x in range(2)] for y in range(1)]
    # Elastic lines corrections
    __LoadDistrParams = [ [0 for x in range(5)] for y in range(4)]
    __LoadDeformParams = [ [0 for x in range(3)] for y in range(5)]
    # DXF layer names
    __DxfLayerParams = [ [0 for x in range(2)] for y in range(1)]
    # Marks types
    __MarkTypeParams = [ [0 for x in range(7)] for y in range(1)]
    # JONCS DEFINITION (NYLON RODS)
    __JoncsConfigsParams = [ [ [0 for x in range(4)] for y in range(1)] for z in range(1)]
    # NOSE MYLARS DEFINITION
    __NoseMylarsParams = [ [ [0 for x in range(6)] for y in range(1)] for z in range(1)]
    # TAB REINFORCEMENTS
    __TabReinfParams = [ [ [0 for x in range(4)] for y in range(1)] for z in range(1)]
    __SchemesParams = [ [0 for x in range(1)] for y in range(1)]
    # GENERAL 2D DXF OPTIONS
    __2DDxfParams = [ [0 for x in range(3)] for y in range(6)]
    # GENERAL 3D DXF OPTIONS
    __3DDxfParams = [ [0 for x in range(4)] for y in range(9)]
    # GLUE VENTS
    __GlueVentParams = [0 for x in range(1)]
    # SPECIAL WING TIP
    # n/a
    # PARAMETERS FOR CALAGE VARIATION
    __calageVarCordParams = [0 for x in range(1)]
    __calageVarAngleParams = [0 for x in range(1)]
    # 3D SHAPING
    __threeDShapingGroupConf = [ [0 for x in range(3)] for y in range(1)]
    __threeDShapingUpGroupParams = [ [ [0 for x in range(3)] for y in range(1)] for z in range(1)]
    __threeDShapingLoGroupParams = [ [ [0 for x in range(3)] for y in range(1)] for z in range(1)]
    __threeDShapingPrintParams = [ [0 for x in range(5)] for y in range(5)]
    # 30. AIRFOIL THICKNESS MODIFICATION
    __airfThiknessModifParams = [0 for x in range(1)]
    # 31. NEW SKIN TENSION MODULE
    __skinTensionGroupConf = [ [0 for x in range(4)] for y in range(1)]
    __skinTensionGroupParams = [ [ [0 for x in range(4)] for y in range(1)] for z in range(1)]
    
    __separator = '**************************************************************\n'
    
    def __init__(self):
        logging.debug(self.__className+'.__init__')
        super().__init__()
        self.dws = DataWindowStatus()
        self.dws.registerSignal(self.dataStatusUpdate)
    
    def isValid( self, fileName ):
        '''
        Checks if a file can be opened and contains a valid title and known version number.
        '''
        logging.debug(self.__className +'.isValid')
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
            if line.find('3.10') >= 0:
                self.setSingleVal('FileVersion', '3.10')
                versionOK = True

            if line.find('Input data file') >= 0:
                titleOK = True
            lineCounter += 1

        inFile.close()
        
        if not ( (versionOK and titleOK) ):
            logging.error('Result of Proc Version check %s', versionOK)
            logging.error('Result of Proc Title check %s', titleOK)
            
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('File read error'))
            msgBox.setText(_('File seems not to be a valid Proc File! \nVersion detected: ')+ str(versionOK)+ _('\nTitle detected: ')+ str(titleOK))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            
            self.setSingleVal('FileNamePath', '')
            self.setSingleVal('FileVersion', '')
        return versionOK and titleOK
    
    def openFile(self):
        '''
        Checks for unapplied/ unsaved data, and appropriate handling. 
        Does the File Open dialog. 
        '''
        # Make sure there is no unsaved/ unapplied data
        if not (self.dws.getWindowDataStatus('ProcDataEdit') and self.dws.getFileStatus('ProcFile')):
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
                        _('Open Proc file'),
                        "",
                        "Processor Files (*.txt);;All Files (*)")

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the dialog  
            # an empty tuple is retured
            if self.isValid(fileName[0]):
                self.setFileName(fileName[0])
                self.readFile()
            
    def saveFile(self):
        '''
        Checks if there is already a valid file name, if not it asks for it. 
        Starts afterwards the writing process.  
        '''
        logging.debug(self.__className+'.saveFile')
        
        filename = self.getFileName()
        if filename != '':
            # We do have already a valid filename
            self.writeFile()
        else:
            # Ask first for the filename
            fileName = QFileDialog.getSaveFileName(
                        None,
                        _('Save Processor file'),
                        "",
                        "Processor Files (*.txt);;All Files (*)")
            
            if fileName != ('', ''):
                # User has really selected a file, if it would have aborted the dialog  
                # an empty tuple is retured
                self.setFileName(fileName[0])
                self.writeFile()
            
    def saveFileAs(self):
        '''
        Asks for a new filename. 
        Starts afterwards the writing process.  
        '''
        logging.debug(self.__className+'.saveFileAs')
        
        # Ask first for the filename
        fileName = QFileDialog.getSaveFileName(
                    None,
                    _('Save Processor file as'),
                    "",
                    "Processor Files (*.txt);;All Files (*)")
        
        if fileName != ('', ''):
                # User has really selected a file, if it would have aborted the dialog  
                # an empty tuple is retured
                self.setFileName(fileName[0])
                self.writeFile()
    
    def readFile(self):
        '''
        Reads the data file and saves the data in the internal varibles.
        Filename and Path must be set first!
        '''
        logging.debug(self.__className+'.readFile')
        inFile = QFile(self.getSingleVal('FileNamePath'))
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
        self.setSingleVal('BrandName', self.remTabSpaceQuot(line) )
        
        # Wing name
        line = stream.readLine()
        line = stream.readLine()
        self.setSingleVal('WingName', self.remTabSpaceQuot(line) )
        
        # Draw scale
        line = stream.readLine()
        line = stream.readLine()
        value = self.remTabSpace( line )
        self.setSingleVal('DrawScale', value )
        
        # Wing scale
        line = stream.readLine()
        self.setSingleVal('WingScale', self.remTabSpace( stream.readLine() ) )
        
        # Number of cells
        line = stream.readLine()
        self.setSingleVal('NumCells', self.remTabSpace( stream.readLine() ) )
        
        # Number of Ribs
        line = stream.readLine()
        self.setSingleVal('NumRibs', self.remTabSpace( stream.readLine() ) )
        
        # Alpha max and parameter
        line = stream.readLine()
        values =  self.splitLine( stream.readLine() )
        self.setSingleVal('AlphaMaxP1', values[0])
        self.setSingleVal('AlphaMaxP2', values[1])
        
        if len(values) > 2: 
            self.setSingleVal('AlphaMaxP3', values[2])
        else:
            self.setSingleVal('AlphaMaxP3', '')
        
        # Paraglider type and parameter
        line = stream.readLine()
        values =  self.splitLine( stream.readLine() )
        self.setSingleVal('ParaTypeP1', self.remTabSpaceQuot( values[0]) )
        self.setSingleVal('ParaTypeP2', values[1])
        
        # Rib geometric parameters
        # Rib    x-rib    y-LE    y-TE    xp    z    beta    RP    Washin
        line = stream.readLine()
        line = stream.readLine()

        for i in range( 0, self.getSingleVal('HalfNumRibs') ):
            values =  self.splitLine( stream.readLine() )
            self.setRibGeomParams(i, values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])

        ##############################
        # 2. AIRFOILS
        for i in range(4):
            line = stream.readLine()
        
        for i in range( 0, self.getSingleVal('HalfNumRibs') ):
            values =  self.splitLine( stream.readLine() )
            self.setAirfoilParams(i, values[1], values[2], values[3], values[4], values[5], values[6], values[7])
        
        ##############################
        # 3. ANCHOR POINTS
        for i in range(4):
            line = stream.readLine()
        
        for i in range( 0, self.getSingleVal('HalfNumRibs') ):
            values =  self.splitLine( stream.readLine() )
            self.setAnchorPointParams(i, values[1], values[2], values[3], values[4], values[5], values[6], values[7])    
        
        ##############################
        # 4. AIRFOIL HOLES
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumAirfHoleConf', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            self.setAirfHoleConf(configCounter, 0, self.remTabSpace( stream.readLine() ) )
            self.setAirfHoleConf(configCounter, 1, self.remTabSpace( stream.readLine() ) )
            numConfigLines = self.remTabSpace( stream.readLine() )
            self.setAirfHoleConf(configCounter, 2, numConfigLines )
        
            for lineCounter in range(0, int(numConfigLines) ):
                values =  self.splitLine( stream.readLine() )
                
                for paramCounter in range (0, 9):
                    self.setAirfHoleParams(configCounter, lineCounter, paramCounter, values[paramCounter])

        ##############################
        # 5. SKIN TENSION
        for i in range(4):
            line = stream.readLine()
        
        for lineCounter in range(0, 6 ):
                values =  self.splitLine( stream.readLine() )
                
                for paramCounter in range (0, 4):
                    self.setSkinTensionParams(lineCounter, paramCounter, values[paramCounter])
        
        self.setSingleVal('StrainMiniRibs', self.remTabSpace( stream.readLine() ) )
                          
        values = self.splitLine( stream.readLine() )
        self.setSingleVal('NumSkinTensionPoints', values[0] )
        self.setSingleVal('SkinTensionCoeff', values[1] )
        
        ##############################
        # 6. SEWING ALLOWANCES
        for i in range(3):
            line = stream.readLine()
            
        for lineCounter in range(0, 2 ):
                values =  self.splitLine( stream.readLine() )
                
                for paramCounter in range (0, 3):
                    self.setSewingAllPanelsParams(lineCounter, paramCounter, values[paramCounter])
        
        values = self.splitLine( stream.readLine() )
        self.setSingleVal('SewingAllRibs', values[0] )
        values = self.splitLine( stream.readLine() )
        self.setSingleVal('SewingAllVRibs', values[0] )
    
        ##############################
        # 7. MARKS
        for i in range(3):
            line = stream.readLine()
            
        values = self.splitLine( stream.readLine() )
        self.setSingleVal('MarksP1', values[0] )
        self.setSingleVal('MarksP2', values[1] )
        self.setSingleVal('MarksP3', values[2] )
        
        ##############################
        # 8. Global angle of attack estimation
        for i in range(3):
            line = stream.readLine()
        
        line = stream.readLine()
        self.setSingleVal('FinesseGR', self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.setSingleVal('CentOfPress', self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.setSingleVal('Calage', self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.setSingleVal('RaisersLenght', self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.setSingleVal('LineLength', self.remTabSpace( stream.readLine() ) )
        line = stream.readLine()
        self.setSingleVal('Karabiners', self.remTabSpace( stream.readLine() ) )
        
        ##############################
        # 9. SUSPENSION LINES DESCRIPTION
        for i in range(3):
            line = stream.readLine()
        
        self.setSingleVal('LineDescConc', self.remTabSpace( stream.readLine() ) )
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumLineDesConfigs', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            numConfigLines = self.remTabSpace( stream.readLine() )
            self.setLineDescConf(configCounter, numConfigLines )

        
            for lineCounter in range(0, int(numConfigLines) ):
                values =  self.splitLine( stream.readLine() )
                
                for paramCounter in range (0, 11):
                    self.setLineDescParams(configCounter, lineCounter, paramCounter, values[paramCounter])
        ##############################
        # 10. BRAKES
        for i in range(3):
            line = stream.readLine()
        
        self.setSingleVal('BrakeLength', self.remTabSpace( stream.readLine() ) )
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumBrakePath', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range (0, 11):
                self.setBrakePathParams(configCounter, paramCounter, values[paramCounter])   
        
        line = stream.readLine()
        
        for configCounter in range(0, 2):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range (0, 5):
                self.setBrakeDistrParams(configCounter, paramCounter, values[paramCounter])
                
        ##############################
        # 11. Ramification lengths
        for i in range(3):
            line = stream.readLine()
        
        values =  self.splitLine( stream.readLine() )
        for paramCounter in range (0, 2):
                self.setRamLengthParams(0, paramCounter, values[paramCounter])
        values =  self.splitLine( stream.readLine() )
        for paramCounter in range (0, 3):
                self.setRamLengthParams(1, paramCounter, values[paramCounter])
        values =  self.splitLine( stream.readLine() )
        for paramCounter in range (0, 2):
                self.setRamLengthParams(2, paramCounter, values[paramCounter])
        values =  self.splitLine( stream.readLine() )
        for paramCounter in range (0, 3):
                self.setRamLengthParams(3, paramCounter, values[paramCounter])
        
        ##############################
        # 12. H V and VH ribs (Mini Ribs)
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumMiniRibs', numConfigs )
        
        values =  self.splitLine( stream.readLine() )
        self.setSingleVal('MiniRibXSpacing', values[0] )
        self.setSingleVal('MiniRibYSpacing', values[1] )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range (0, 9):
                self.setMiniRibParams(configCounter, paramCounter, values[paramCounter+1])
                
            if values[1] == '6':
                # we have a type 6 rib-> two additional params to read
                self.setMiniRibParams(configCounter, 9, values[10])
                self.setMiniRibParams(configCounter, 10, values[11])
        
        ##############################
        # 15. Extrados colors
        for i in range(3):
            line = stream.readLine()
                
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumRibsExtradColors', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            numConfigLines = values[1]
            self.setExtradColorsConf(configCounter, 0, values[0] )
            self.setExtradColorsConf(configCounter, 1, values[1] )
                   
            for lineCounter in range(0, int(numConfigLines) ):
                values =  self.splitLine( stream.readLine() )
                
                for paramCounter in range (0, 3):
                    self.setExtradColorsParams(configCounter, lineCounter, paramCounter, values[paramCounter])
        
        ##############################
        # 16. Intrados colors
        for i in range(3):
            line = stream.readLine()
                
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumRibsIntradColors', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            numConfigLines = values[1]
            self.setIntradColorsConf(configCounter, 0, values[0] )
            self.setIntradColorsConf(configCounter, 1, values[1] )
                   
            for lineCounter in range(0, int(numConfigLines) ):
                values =  self.splitLine( stream.readLine() )
                
                for paramCounter in range (0, 3):
                    self.setIntradColorsParams(configCounter, lineCounter, paramCounter, values[paramCounter])
        
        ##############################
        # 17. Aditional rib points
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumAddRibPoints', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            self.setAddRibPointsParams(configCounter, 0, values[0] )
            self.setAddRibPointsParams(configCounter, 1, values[1] )
        
        ##############################
        # 18. Elastic lines corrections
        for i in range(3):
            line = stream.readLine()
        
        self.setSingleVal('InFlightLoad', self.remTabSpace( stream.readLine() ) )
        
        for configCounter in range(0, 4):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range(0, configCounter+2):
                self.setLoadDistrParams(configCounter, paramCounter, values[paramCounter])
        
        for configCounter in range(0, 5):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range(0, 3):
                self.setLoadDeformParams(configCounter, paramCounter, values[paramCounter+1])       
        
        ##############################
        # 19. DXF layer names
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumDxfLayers', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range(0, 2):
                self.setDxfLayerParams(configCounter, paramCounter, values[paramCounter])
        
        ##############################
        # 20. Marks types
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumMarkTypes', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range(0, 7):
                self.setMarkTypeParams(configCounter, paramCounter, values[paramCounter])
        
        ##############################
        # 21. JONCS DEFINITION (NYLON RODS)
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('JoncsType', dataType )
        
        if dataType != '0':
            # we have data to read
            
            numConfigs = self.remTabSpace( stream.readLine() )
            self.setSingleVal('NumJoncsConfigs', numConfigs )
        
            for configCounter in range(0, int(numConfigs)):
                
                for lineCounter in range(0, 4 ):
                    values =  self.splitLine( stream.readLine() )
                    
                    for paramCounter in range (0, 3):
                        self.setJoncsConfigsParams(configCounter, lineCounter, paramCounter, values[paramCounter])
                    
                    if lineCounter > 0:
                        self.setJoncsConfigsParams(configCounter, lineCounter, 3, values[3])
        
        ##############################
        # 22. NOSE MYLARS DEFINITION
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NoseMylarsType', dataType )
        
        if dataType != '0':
            # we have data to read
            
            numConfigs = self.remTabSpace( stream.readLine() )
            self.setSingleVal('NumNoseMylarsConfigs', numConfigs )
        
            for configCounter in range(0, int(numConfigs)):
                
                for lineCounter in range(0, 2 ):
                    values =  self.splitLine( stream.readLine() )
                    
                    for paramCounter in range (0, 3):
                        self.setNoseMylarsParams(configCounter, lineCounter, paramCounter, values[paramCounter])
                    
                    if lineCounter > 0:
                        for paramCounter in range (3, 6):
                            self.setNoseMylarsParams(configCounter, lineCounter, paramCounter, values[paramCounter])
                                                    
        ##############################
        # 23. TAB REINFORCEMENTS
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('TabReinfType', dataType )
        
        if dataType != '0':
            # we have data to read
            
            numConfigs = self.remTabSpace( stream.readLine() )
            self.setSingleVal('NumTabReinfConfigs', numConfigs )
            
            for configCounter in range(0, int(numConfigs)):
                for lineCounter in range(0, 2 ):
                    values =  self.splitLine( stream.readLine() )
                    if lineCounter == 0:
                        for paramCounter in range (0, 3):
                            self.setTabReinfParams(configCounter, lineCounter, paramCounter, values[paramCounter])
                    else:
                        for paramCounter in range (0, 5):
                            self.setTabReinfParams(configCounter, lineCounter, paramCounter, values[paramCounter])
        
        # overread "schemes"
        stream.readLine()
        
        schemeCounter = 0
        
        # check for valid data line
        line = stream.readLine()
        while line.find('*') < 0:
            # line contains no asteriks: read it
            
            values = self.splitLine(line)
            
            for paramCounter in range (0, len(values)):
                self.setSchemesParams(schemeCounter, paramCounter, values[paramCounter])
                
            schemeCounter +=1
            line = stream.readLine()
                
        ##############################
        # 24. GENERAL 2D DXF OPTIONS
        # be carefull: previous code has already read first line of header
        for i in range(2):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('twoDDxfType', dataType )
        
        if dataType != '0':
            # we have data to read
            
            for lineCounter in range(0, 6 ):
                    values =  self.splitLine( stream.readLine() )
                    
                    for paramCounter in range (0, 3):
                        self.setTwoDDxfParams(lineCounter, paramCounter, values[paramCounter])
            
        ##############################
        # 25. GENERAL 3D DXF OPTIONS
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('threeDDxfType', dataType )
        
        if dataType != '0':
            # we have data to read
            
            for lineCounter in range(0, 6 ):
                    values =  self.splitLine( stream.readLine() )
                    
                    for paramCounter in range (0, 3):
                        self.setThreeDDxfParams(lineCounter, paramCounter, values[paramCounter])
                        
            for lineCounter in range(0, 3 ):
                    values =  self.splitLine( stream.readLine() )
                    
                    for paramCounter in range (0, 4):
                        self.setThreeDDxfParams(lineCounter+6, paramCounter, values[paramCounter])
        
        ##############################
        # 26. GLUE VENTS
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('glueVentType', dataType )
        
        if dataType != '0':
            # we have data to read
            for lineCounter in range( 0, self.getSingleVal('HalfNumRibs') ):
                values =  self.splitLine( stream.readLine() )
                
                self.setGlueVentParams(lineCounter, values[1])
            
            
        ##############################
        # 27. SPECIAL WING TIP
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('specWingTypType', dataType )
        
        if dataType != '0':
            # we have data to read
            values =  self.splitLine( stream.readLine() )
            self.setSingleVal('specWingTypAngLE', values[1] )
            values =  self.splitLine( stream.readLine() )
            self.setSingleVal('specWingTypAngTE', values[1] )
        
        ##############################
        # 28. PARAMETERS FOR CALAGE VARIATION
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('calageVarType', dataType )
        
        if dataType != '0':
            # we have data to read
            self.setSingleVal('numCalageVarRisers', self.remTabSpace( stream.readLine() ) )
            
            values =  self.splitLine( stream.readLine() )
            for paramCounter in range( 0, 6 ):
                self.setCalageVarCordParams(paramCounter, values[paramCounter])
            
            values =  self.splitLine( stream.readLine() )
            for paramCounter in range( 0, 4 ):
                self.setCalageVarAngleParams(paramCounter, values[paramCounter])
            
        ##############################
        # 29. 3D SHAPING
        # 1                               threeDShapingType
        # 1                               threeDShapingTheory
        # groups    2                     NumThreeDShapingGroups
        
        # group     1    1    12          __threeDShapingGroupConf
        # upper     2    1                __threeDShapingUpGroupParams
        # 1    25    33    1.0            __threeDShapingUpGroupParams
        # 2    33    44    1.0            __threeDShapingUpGroupParams
        # lower    0    1                 __threeDShapingLoGroupParams
        
        # group    2       13      14     __threeDShapingGroupConf
        # upper    1    1                 __threeDShapingUpGroupParams
        # 1    30    40    1.0            __threeDShapingUpGroupParams
        # lower    0    1                 __threeDShapingLoGroupParams
        
        # * Print parameters
        # Inter3D 1    1    10    1      __threeDShapingPrintParams
        # Ovali3D 1    1    14    0      __threeDShapingPrintParams
        # tesse3D 0    1    14    0      __threeDShapingPrintParams
        # exteDXF 0    1    14    0      __threeDShapingPrintParams
        # exteSTL 0    1    14    0      __threeDShapingPrintParams
        
        for i in range(3):
            line = stream.readLine()
            
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('threeDShapingType', dataType )
        
        if dataType != '0':
            # we have data to read
            self.setSingleVal('threeDShapingTheory', self.remTabSpace( stream.readLine() ) )
            
            values = self.splitLine( stream.readLine() )
            numGroups = values[1]
            self.setSingleVal('NumThreeDShapingGroups', values[1] )
            
            for groupCounter in range (0, int(numGroups) ):
                values = self.splitLine( stream.readLine() )
                for paramCounter in range( 0, 3 ):
                    self.setThreeDShapingGroupConf(groupCounter, paramCounter, values[paramCounter+1])
                
                values = self.splitLine( stream.readLine() )
                numUpGroups = int(values[1])
                for paramCounter in range( 0, 3 ):
                    self.setThreeDShapingUpGroupParams(groupCounter, 0, paramCounter, values[paramCounter])
                
                for upGroupCounter in range(0, numUpGroups): 
                    values = self.splitLine( stream.readLine() )
                    for paramCounter in range( 0, 3 ):
                        self.setThreeDShapingUpGroupParams(groupCounter, upGroupCounter+1, paramCounter, values[paramCounter+1])
                
                values = self.splitLine( stream.readLine() )
                numLoGroups = int(values[1])
                for paramCounter in range( 0, 3 ):
                    self.setThreeDShapingLoGroupParams(groupCounter, 0, paramCounter, values[paramCounter])
                
                for loGroupCounter in range (0, numLoGroups):
                    values = self.splitLine( stream.readLine() )
                    for paramCounter in range( 0, 3 ):
                        self.setThreeDShapingLoGroupParams(groupCounter, loGroupCounter+1, values[paramCounter+1])
        
        # overread print params title
        line = stream.readLine()
        
        for lineCounter in range(5):
            values = self.splitLine( stream.readLine() )
            
            for paramCounter in range(5):
                self.setThreeDShapingPrintParams(lineCounter, paramCounter, values[paramCounter] )
        
        ##############################
        # 30. AIRFOIL THICKNESS MODIFICATION
        
        for i in range(3):
            line = stream.readLine()
        
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('airfoilThiknessModifType', dataType )
        
        if dataType != '0':
            for i in range( 0, self.getSingleVal('HalfNumRibs') ):
                values =  self.splitLine( stream.readLine() )
                self.setAirfThiknessModifParams( i, values[1] )
        
        
        ##############################
        # 31. NEW SKIN TENSION MODULE
        for i in range(3):
            line = stream.readLine()
        
        dataType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('skinTensionType', dataType )
        
        if dataType != '0':
            numGroups = self.remTabSpace( stream.readLine() )
            self.setSingleVal('numSkinTensionGroups', numGroups )
            
            for groupCounter in range (0, int(numGroups) ):
                # read title line
                line = stream.readLine()
                
                # Group configuration
                values = self.splitLine( stream.readLine() )
                numConfigLines = values[3]
                for paramCounter in range( 0, 4 ):
                    self.setSkinTensionGroupConf(groupCounter, paramCounter, values[paramCounter+1] )
                
                # Group params
                for configLineCounter in range (0, int(numConfigLines) ):
                    values = self.splitLine( stream.readLine() )
                    for paramCounter in range( 0, 4 ):
                        self.setSkinTensionGroupParams(groupCounter, configLineCounter, paramCounter, values[paramCounter+1] )
                
        
        # Clean up 
        inFile.close()
        self.dataStatusUpdate.emit(self.__className,'Open')
        
    def writeFile(self, forProc=False):
        '''
        Writes all the values into a data file. 
        Filename must have been set already before, unless the file shall be written for the Processor.
                
        @param forProc: Set this to True if the file must be saved in the directory where the Processor resides
        '''
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

        stream << self.__separator
        stream << '* LABORATORI D\'ENVOL PARAGLIDING DESIGN\n'
        stream << '* Input data file version 3.10\n'
        stream << self.__separator
        stream << '* Version 2020-05-02\n'
        
        ##############################
        # 1. Geometry
        self.writeHeader(stream, '1. GEOMETRY')
        
        stream << '* Brand name\n'
        stream << '\"' << self.getSingleVal('BrandName') << '\"\n'
        
        stream << '* Wing name\n'
        stream << '\"' << self.getSingleVal('WingName') << '\"\n'
        
        stream << '* Drawing scale\n'
        stream << self.getSingleVal('DrawScale') << '\n'
        
        stream << '* Wing scale\n'
        stream << self.getSingleVal('WingScale') << '\n'
        
        stream << '* Number of cells\n'
        stream << '\t'<< self.getSingleVal('NumCells') << '\n'
        
        stream << '* Number of ribs\n'
        stream << '\t'<< self.getSingleVal('NumRibs') << '\n'
        
        stream << '* Alpha max and parameter\n'
        stream << '\t' << self.getSingleVal('AlphaMaxP1')  
        stream << '\t' << self.getSingleVal('AlphaMaxP2')
        stream << '\t' << self.getSingleVal('AlphaMaxP3')<< '\n'
        
        stream << '* Paraglider type and parameter\n'
        stream << '\t'<< '\"' << self.getSingleVal('ParaTypeP1') << '\"'
        stream << '\t'<< self.getSingleVal('ParaTypeP2')<< '\n'
        
        stream << '* Rib geometric parameters\n'
        stream << '* Rib\tx-rib\ty-LE\ty-TE\txp\tz\tbeta\tRP\tWashin\n'
        
        for ribCounter in range( 0, self.getSingleVal('HalfNumRibs') ):
            stream << ribCounter+1 
            
            for paramCounter in range (8):
                stream << '\t' << self.getRibGeomParams(ribCounter, paramCounter)
                
            stream << '\n'
        
        ##############################
        # 2. AIRFOILS
        self.writeHeader(stream, '2. AIRFOILS')
        
        stream << '* Airfoil name, intake in, intake out, open , disp. rrw \n'
        
        for ribCounter in range( 0, self.getSingleVal('HalfNumRibs') ):
            stream << ribCounter+1 
            
            for paramCounter in range (7):
                stream << '\t' << self.getAirfoilParams(ribCounter, paramCounter)
                
            stream << '\n'
        
        ##############################
        # 3. ANCHOR POINTS
        self.writeHeader(stream, '3. ANCHOR POINTS')
        
        stream << '* Airf\tAnch\tA\tB\tC\tD\tE\tF\n'
        
        for ribCounter in range( 0, self.getSingleVal('HalfNumRibs') ):
            stream << ribCounter+1 
            
            for paramCounter in range (7):
                stream << '\t' << self.getAnchorPointParams(ribCounter, paramCounter)
                
            stream << '\n'
        
        ##############################
        # 4. AIRFOIL HOLES
        self.writeHeader(stream, '4. AIRFOIL HOLES')
        
        numConfigs = self.getSingleVal('NumAirfHoleConf')
        stream << numConfigs << '\n'
        
        for configCounter in range( 0, int(numConfigs) ):
            stream << self.getAirfHoleConf(configCounter, 0) << '\n'
            stream << self.getAirfHoleConf(configCounter, 1) << '\n'
            numConfigLines = self.getAirfHoleConf(configCounter, 2)
            stream << numConfigLines << '\n'
            
            for lineCounter in range(0, int(numConfigLines) ):
                for paramCounter in range (0, 9):
                    stream << self.getAirfHoleParams(configCounter, lineCounter, paramCounter) << '\t'
                stream << '\n'
        
        
        ##############################
        # 5. SKIN TENSION
        self.writeHeader(stream, '5. SKIN TENSION')
        stream << 'Extrados' << '\n'
        
        for lineCounter in range(0, 6 ):
            for paramCounter in range (0, 4):
                stream << self.getSkinTensionParams(lineCounter, paramCounter) << '\t'
            stream << '\n'
        
        stream << self.getSingleVal('StrainMiniRibs') << '\n'
        stream << self.getSingleVal('NumSkinTensionPoints') << '\t'
        stream << self.getSingleVal('SkinTensionCoeff') << '\n'

        ##############################
        # 6. SEWING ALLOWANCES
        self.writeHeader(stream, '6. SEWING ALLOWANCES')
       
        for lineCounter in range(0, 2 ):
            for paramCounter in range (0, 3):
                stream << self.getSewingAllPanelsParams(lineCounter, paramCounter) << '\t'
            
            if lineCounter == 0:
                stream << 'upper panels (mm)\n'
            else:
                stream << 'lower panels (mm)\n'
         
        stream << self.getSingleVal('SewingAllRibs')  << '\t' << 'ribs (mm)' << '\n'     
        stream << self.getSingleVal('SewingAllVRibs')  << '\t' << 'vribs (mm)' << '\n'
       
        ##############################
        # 7. MARKS
        self.writeHeader(stream, '7. MARKS')
        
        stream << self.getSingleVal('MarksP1') << '\t'
        stream << self.getSingleVal('MarksP3') << '\t'
        stream << self.getSingleVal('MarksP2') << '\n'
        
        ##############################
        # 8. Global angle of attack estimation
        self.writeHeader(stream, '8. Global angle of attack estimation')
        
        stream << '* Finesse GR\n'
        stream << '\t' << self.getSingleVal('FinesseGR') << '\n'
        
        stream << '* Center of pressure % of chord\n'
        stream << '\t' << self.getSingleVal('CentOfPress') << '\n'
        
        stream << '* Calage %\n'
        stream << '\t' << self.getSingleVal('Calage') << '\n'
        
        stream << '* Risers lenght cm\n'
        stream << '\t' << self.getSingleVal('RaisersLenght') << '\n'
        
        stream << '* Line lenght cm\n'
        stream << '\t' << self.getSingleVal('LineLength') << '\n'
        
        stream << '* Karabiners cm\n'
        stream << '\t' << self.getSingleVal('Karabiners') << '\n'
        
        ##############################
        # 9. SUSPENSION LINES DESCRIPTION
        self.writeHeader(stream, '9. SUSPENSION LINES DESCRIPTION')
        
        stream << self.getSingleVal('LineDescConc') << '\n'
        stream << self.getSingleVal('NumLineDesConfigs') << '\n'
        
        numConfigs = self.getSingleVal('NumLineDesConfigs')
        for configCounter in range(0, int(numConfigs)):
            stream << self.getLineDescConf(configCounter) << '\n'
            
            numConfigLines = self.getLineDescConf(configCounter)
            for lineCounter in range(0, int(numConfigLines) ):
                for paramCounter in range (0, 11):
                    stream << self.getLineDescParams(configCounter, lineCounter, paramCounter) << '\t'
                
                stream << '\n'
        
        ##############################
        # 10. BRAKES
        self.writeHeader(stream, '10. BRAKES')
        
        stream << self.getSingleVal('BrakeLength') << '\n'
        stream << self.getSingleVal('NumBrakePath') << '\n'
        
        numConfigs = self.getSingleVal('NumBrakePath')
        for configCounter in range(0, int(numConfigs)):
            for paramCounter in range (0, 11):
                stream << self.getBrakePathParams(configCounter, paramCounter) << '\t'
            stream << '\n'
            
        stream << '* Brake distribution\n'
        
        for configCounter in range(0, 2):
            for paramCounter in range (0, 5):
                stream << self.getBrakeDistrParams(configCounter, paramCounter) << '\t'
            stream << '\n'
        
        ##############################
        # 11. Ramification lengths
        self.writeHeader(stream, '11. Ramification lengths')
        
        for lineCounter in range (4):
            for paramCounter in range (0, 2):
                    stream << self.getRamLengthParams(lineCounter, paramCounter) << '\t'
            if (lineCounter == 1) or (lineCounter==3):
                stream << self.getRamLengthParams(lineCounter, 2 )
            stream << '\n'
        
        ##############################
        # 12. H V and VH ribs (Mini Ribs)
        self.writeHeader(stream, '12. H V and VH ribs')
        
        stream << self.getSingleVal('NumMiniRibs') << '\n'
        stream << self.getSingleVal('MiniRibXSpacing') << '\t' << self.getSingleVal('MiniRibYSpacing') << '\n'
        
        numConfigs = self.getSingleVal('NumMiniRibs')
        for configCounter in range(0, int(numConfigs)):
            for paramCounter in range (0, 9):
                stream << self.getMiniRibParams(configCounter, paramCounter) << '\t'
            
            if self.getMiniRibParams(configCounter, 0) == '6':
                # we have a type 6 rib-> two additional params to write
                stream << self.getMiniRibParams(configCounter, 9) << '\t'
                stream << self.getMiniRibParams(configCounter, 10)
            stream << '\n'
        
        ##############################
        # 15. Extrados colors
        self.writeHeader(stream, '15. Extrados colors')
        
        stream << self.getSingleVal('NumRibsExtradColors') << '\n'

        numConfigs = self.getSingleVal('NumRibsExtradColors')
        for configCounter in range(0, int(numConfigs)):
            stream << self.getExtradColorsConf(configCounter, 0) << '\t'
            stream << self.getExtradColorsConf(configCounter, 1) << '\n'
             
            numConfigLines = self.getExtradColorsConf(configCounter, 1)       
            for lineCounter in range(0, int(numConfigLines) ):
                for paramCounter in range (0, 3):
                    stream << self.getExtradColorsParams(configCounter, lineCounter, paramCounter) << '\t'
                stream << '\n'
                
        ##############################
        # 16. Intrados colors
        self.writeHeader(stream, '16. Intrados colors')
        
        stream << self.getSingleVal('NumRibsIntradColors') << '\n'

        numConfigs = self.getSingleVal('NumRibsIntradColors')
        for configCounter in range(0, int(numConfigs)):
            stream << self.getIntradColorsConf(configCounter, 0) << '\t'
            stream << self.getIntradColorsConf(configCounter, 1) << '\n'
             
            numConfigLines = self.getIntradColorsConf(configCounter, 1)       
            for lineCounter in range(0, int(numConfigLines) ):
                for paramCounter in range (0, 3):
                    stream << self.getIntradColorsParams(configCounter, lineCounter, paramCounter) << '\t'
                stream << '\n'
        
        ##############################
        # 17. Aditional rib points
        self.writeHeader(stream, '17. Aditional rib points')
        
        stream << self.getSingleVal('NumAddRibPoints') << '\n'
        
        numConfigs = self.getSingleVal('NumAddRibPoints')
        for configCounter in range(0, int(numConfigs)):
            stream << self.getAddRibPointsParams(configCounter, 0) << '\t'
            stream << self.getAddRibPointsParams(configCounter, 1) << '\n'
        
        ##############################
        # 18. Elastic lines corrections
        self.writeHeader(stream, '18. Elastic lines corrections')
        
        stream << self.getSingleVal('InFlightLoad') << '\n'
        
        for configCounter in range(0, 4):
            for paramCounter in range(0, configCounter+2):
                stream << self.getLoadDistrParams(configCounter, paramCounter) << '\t'
            stream << '\n'
        
        for configCounter in range(0, 5):
            stream << configCounter << '\t'
            
            for paramCounter in range(0, 3):
                stream << self.getLoadDeformParams(configCounter, paramCounter) << '\t'
            stream << '\n'
        
        ##############################
        # 19. DXF layer names
        self.writeHeader(stream, '19. DXF layer names')
        
        stream << self.getSingleVal('NumDxfLayers') << '\n'
        
        numConfigs = self.getSingleVal('NumDxfLayers')
        for configCounter in range(0, int(numConfigs)):
            for paramCounter in range(0, 2):
                stream << self.getDxfLayerParams(configCounter, paramCounter) << '\t'
            stream << '\n'
        
        ##############################
        # 20. Marks types
        self.writeHeader(stream, '20. Marks types')
        
        stream << self.getSingleVal('NumMarkTypes') << '\n'
        
        numConfigs = self.getSingleVal('NumMarkTypes')
        for configCounter in range(0, int(numConfigs)):
            for paramCounter in range(0, 7):
                stream << self.getMarkTypeParams(configCounter, paramCounter)  << '\t'
            stream << '\n'
            
        ##############################
        # 21. JONCS DEFINITION (NYLON RODS)
        self.writeHeader(stream, '21. JONCS DEFINITION (NYLON RODS)')
        
        stream << self.getSingleVal('JoncsType') << '\n'
        
        dataType = self.getSingleVal('JoncsType')
        if dataType != '0':
            # we have data to write
            stream << self.getSingleVal('NumJoncsConfigs') << '\n'
            
            numConfigs = self.getSingleVal('NumJoncsConfigs')
            for configCounter in range(0, int(numConfigs)):
                for lineCounter in range(0, 4 ):
                    for paramCounter in range (0, 3):
                        stream << self.getJoncsConfigsParams(configCounter, lineCounter, paramCounter) << '\t'
                    if lineCounter > 0:
                        stream << self.getJoncsConfigsParams(configCounter, lineCounter, 3) << '\t'
                    stream << '\n'
                    
        ##############################
        # 22. NOSE MYLARS DEFINITION
        self.writeHeader(stream, '22. NOSE MYLARS DEFINITION')
        
        stream << self.getSingleVal('NoseMylarsType') << '\n'
        dataType = self.getSingleVal('NoseMylarsType')
        if dataType != '0':
            # we have data to write
             
            stream << self.getSingleVal('NumNoseMylarsConfigs') << '\n'
            numConfigs = self.getSingleVal('NumNoseMylarsConfigs')
            for configCounter in range(0, int(numConfigs)):
                for lineCounter in range(0, 2 ):
                    if lineCounter == 0:
                        for paramCounter in range (0, 3):
                            stream << self.getNoseMylarsParams(configCounter, lineCounter, paramCounter) << '\t'
                        stream << '\n'
                     
                    if lineCounter > 0:
                        for paramCounter in range (0, 6):
                            stream <<  self.getNoseMylarsParams(configCounter, lineCounter, paramCounter) << '\t'
                        stream << '\n'
        
        ##############################
        # 23. TAB REINFORCEMENTS
        self.writeHeader(stream, '23. TAB REINFORCEMENTS')
        
        stream << self.getSingleVal('TabReinfType') << '\n'
        dataType = self.getSingleVal('TabReinfType')
        if dataType != '0':
            # we have data to write
            
            stream << self.getSingleVal('NumTabReinfConfigs') << '\n'
            numConfigs = self.getSingleVal('NumTabReinfConfigs')
            for configCounter in range(0, int(numConfigs)):
                for lineCounter in range(0, 2 ):
                    
                    if lineCounter == 0:
                        for paramCounter in range (0, 3):
                            stream << self.getTabReinfParams(configCounter, lineCounter, paramCounter) << '\t'
                        stream << '\n'
                 
                    if lineCounter > 0:
                        for paramCounter in range (0, 5):
                            stream << self.getTabReinfParams(configCounter, lineCounter, paramCounter) << '\t'
                        stream << '\n'
                        
        # "schemes"
        stream << 'schemes' << '\n'
        
        numLines = self.getNumSchemesLines()
        for lineCounter in range(0, numLines):
            
            numParams = self.getNumSchemesParams(lineCounter)
            for paramCounter in range(0, int(numParams) ):
                stream << self.getSchemesParams(lineCounter, paramCounter) << '\t'
            stream << '\n'
    
        
        ##############################
        # 24. GENERAL 2D DXF OPTIONS
        self.writeHeader(stream, '24. GENERAL 2D DXF OPTIONS')
        
        stream << self.getSingleVal('twoDDxfType') << '\n'
        dataType = self.getSingleVal('twoDDxfType')
        if dataType != '0':
            # we have data to write
            
            for lineCounter in range(0, 6 ):
                for paramCounter in range (0, 3):
                    stream << self.getTwoDDxfParams(lineCounter, paramCounter) << '\t'
                stream << '\n'
        
        ##############################
        # 25. GENERAL 3D DXF OPTIONS
        self.writeHeader(stream, '25. GENERAL 3D DXF OPTIONS')
        
        stream << self.getSingleVal('threeDDxfType') << '\n'
        dataType = self.getSingleVal('threeDDxfType')
        if dataType != '0':
            # we have data to write
            
            for lineCounter in range(0, 6 ):
                for paramCounter in range (0, 3):
                    stream << self.getThreeDDxfParams(lineCounter, paramCounter) << '\t'
                stream << '\n'
                
            for lineCounter in range(0, 3 ):
                for paramCounter in range (0, 4):
                    stream << self.getThreeDDxfParams(lineCounter+6, paramCounter) << '\t'
                stream << '\n'
                
        ##############################
        # 26. GLUE VENTS
        self.writeHeader(stream, '26. GLUE VENTS')
        
        stream << self.getSingleVal('glueVentType') << '\n'
        dataType = self.getSingleVal('glueVentType')
        if dataType != '0':
            # we have data to write
            
            for lineCounter in range( 0, self.getSingleVal('HalfNumRibs') ):
                stream << lineCounter+1 << '\t' << self.getGlueVentParams(lineCounter) << '\n'
        
        ##############################
        # 27. SPECIAL WING TIP
        self.writeHeader(stream, '27. SPECIAL WING TIP')
        
        stream << self.getSingleVal('specWingTypType') << '\n'
        dataType = self.getSingleVal('specWingTypType')
        if dataType != '0':
            # we have data to write
            stream << 'AngleLE\t' << self.getSingleVal('specWingTypAngLE') << '\n'
            stream << 'AngleLE\t' << self.getSingleVal('specWingTypAngTE') << '\n'
        
        ##############################
        # 28. PARAMETERS FOR CALAGE VARIATION
        self.writeHeader(stream, '28. PARAMETERS FOR CALAGE VARIATION')
        
        stream << self.getSingleVal('calageVarType') << '\n'
        dataType = self.getSingleVal('calageVarType')
        if dataType != '0':
            # we have data to write
            
            stream << self.getSingleVal('numCalageVarRisers') << '\n'
            
            for paramCounter in range( 0, 6 ):
                stream << self.getCalageVarCordParams(paramCounter) << '\t'
            stream << '\n'
            
            for paramCounter in range( 0, 4 ):
                stream << self.getCalageVarAngleParams(paramCounter) << '\t'
            stream << '\n'   
        
        ##############################
        # 29. 3D SHAPING
        self.writeHeader(stream, '29. 3D SHAPING')
        
        stream << self.getSingleVal('threeDShapingType') << '\n'
        dataType = self.getSingleVal('threeDShapingType')
        if dataType != '0':
            # we have data to write
            
            stream << self.getSingleVal('threeDShapingTheory') << '\n'
            stream << 'groups\t' << self.getSingleVal('NumThreeDShapingGroups') << '\n'
            
            numGroups = self.getSingleVal('NumThreeDShapingGroups')
            for groupCounter in range (0, int(numGroups) ):

                stream << 'group\t'
                for paramCounter in range( 0, 3 ):
                    stream << self.getThreeDShapingGroupConf(groupCounter, paramCounter) << '\t'
                stream << '\n'

                for paramCounter in range( 0, 3 ):
                    self.getThreeDShapingUpGroupParams(groupCounter, 0, paramCounter)
                
                numUpGroups = self.getNumThreeDShapingUpGroups(groupCounter)
                for upGroupCounter in range(0, numUpGroups+1): 
                    if upGroupCounter>0:
                        stream <<  upGroupCounter << '\t'
                    for paramCounter in range( 0, 3 ):
                        stream << self.getThreeDShapingUpGroupParams(groupCounter, upGroupCounter, paramCounter) << '\t'
                    stream << '\n'
                
                for paramCounter in range( 0, 3 ):
                    self.getThreeDShapingLoGroupParams(groupCounter, 0, paramCounter)
                
                numLoGroups = self.getNumThreeDShapingLoGroups(groupCounter)
                for loGroupCounter in range(0, numLoGroups+1): 
                    if loGroupCounter>0:
                        stream <<  loGroupCounter << '\t'
                    for paramCounter in range( 0, 3 ):
                        stream << self.getThreeDShapingLoGroupParams(groupCounter, loGroupCounter, paramCounter) << '\t'
                    stream << '\n'
            
            stream << '* Print parameters\n'
            
            for lineCounter in range(5):
                for paramCounter in range(5):
                    stream << self.getThreeDShapingPrintParams(lineCounter, paramCounter) << '\t'
                stream << '\n'
        
        ##############################
        # 30. AIRFOIL THICKNESS MODIFICATION
        self.writeHeader(stream, '30. AIRFOIL THICKNESS MODIFICATION')
        
        stream << self.getSingleVal('airfoilThiknessModifType') << '\n'
        dataType = self.getSingleVal('airfoilThiknessModifType')
        if dataType != '0':
            # we have data to write
            
            for lineCounter in range( 0, self.getSingleVal('HalfNumRibs') ):
                stream << lineCounter+1 << '\t' << self.getAirfThiknessModifParams(lineCounter) << '\n'
        
        ##############################
        # 31. NEW SKIN TENSION MODULE
        self.writeHeader(stream, '31. NEW SKIN TENSION MODULE')
        
        stream << self.getSingleVal('skinTensionType') << '\n'
        dataType = self.getSingleVal('skinTensionType')
        if dataType != '0':
            # we have data to write
            
            stream << self.getSingleVal('numSkinTensionGroups') << '\n'
            numGroups = self.getSingleVal('numSkinTensionGroups')
            for groupCounter in range (0, int(numGroups) ):
                stream << '* Skin tension group number ' << groupCounter+1 << '\n'
                # Group configuration
                stream << groupCounter+1 << '\t'
                for paramCounter in range( 0, 4 ):
                    stream <<  self.getSkinTensionGroupConf(groupCounter, paramCounter) << '\t'
                stream << '\n'
                
                # Group params
                numConfigLines = self.getSkinTensionGroupConf(groupCounter, 2)
                for configLineCounter in range (0, int(numConfigLines) ):
                    stream << configLineCounter+1 << '\t'
                    for paramCounter in range( 0, 4 ):
                        stream << self.getSkinTensionGroupParams(groupCounter, configLineCounter, paramCounter) << '\t'
                    stream << '\n'
        
        
        stream.flush()
        outFile.close()
        
        if forProc == False:
            # Then we need to set the right file version
            self.setSingleVal('FileVersion', '3.1')
        
            # Make flags in order
            self.dataStatusUpdate.emit(self.__className,'Open')
            
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
        logging.debug(self.__className+'.setSingleVal |' + parameter +'|'+ value+'|')
        
        self.__simpleData[parameter] = value
        self.dataStatusUpdate.emit(self.__className, parameter)
        
        # Special case for Ribs
        # If num Ribs is changed, set also HalfNumRibs
        if parameter == 'NumRibs':
            value = math.ceil(float(value) / 2)
            self.__simpleData['HalfNumRibs'] = value 
            logging.debug(self.__className+'.setSingleVal |' + 'HalfNumRibs' +'|'+ str(value)+'|')
            self.dataStatusUpdate.emit(self.__className, 'HalfNumRibs')
        
    def getSingleVal(self, parameter):
        return self.__simpleData.get(parameter)
    
    def setRibGeomParams(self, ribNum, p1, p2, p3, p4, p5, p6, p7, p8):
        '''
        Saves Rib Geometry parameters into the data store.
        @param ribNum: Number of the rib. Indexing starts with 0!
        @param p1..8: The individual data to save
        '''
        logging.debug(self.__className+'.setRibGeomParams |'+ str(ribNum)+'|'+ p1+'|'+ p2+'|'+ p3+'|'+ p4+'|'+ p5+'|'+ p6+'|'+ p7+'|'+ p8+'|')
        
        if ribNum >= len(self.__RibGeomParams):
            # in case of building up the array we might need to add elements
            self.__RibGeomParams.append([p1,p2,p3,p4,p5,p6,p7,p8])
        else:
            # element already exists, update the data
            self.__RibGeomParams[ribNum]= [p1, p2, p3, p4, p5, p6, p7, p8]
        
        self.dataStatusUpdate.emit(self.__className, 'RibGeomParams')
    
    def getRibGeomParams(self, ribNum, paramNum):
        '''
        Reads Rib Geometry parameters from the data store.
        @param ribNum: Number of the rib. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getRibGeomParams |'+ str(ribNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__RibGeomParams) >= ribNum:
            if len (self.__RibGeomParams[ribNum]) >= paramNum:
                return  self.__RibGeomParams[ribNum][paramNum]
        else: 
            return ''
            
    def setAirfoilParams(self, ribNum, p1, p2, p3, p4, p5, p6, p7):
        '''
        Saves Airfoil parameters into the data store.
        @param ribNum: Number of the rib. Indexing starts with 0!
        @param p1..7: The individual data to save
        '''
        logging.debug(self.__className+'.setAirfoilParams |'+ str(ribNum)+'|'+ p1+'|'+ p2+'|'+ p3+'|'+ p4+'|'+ p5+'|'+ p6+'|'+ p7+'|')
        
        if ribNum >= len(self.__AirfoilParams):
            # in case of building up the array we might need to add elements
            self.__AirfoilParams.append([p1,p2,p3,p4,p5,p6,p7])
        else:
            # element already exists, update the data
            self.__AirfoilParams[ribNum]= [p1, p2, p3, p4, p5, p6, p7]
        
        self.dataStatusUpdate.emit(self.__className, 'AirfoilParams')
        
    def getAirfoilParams(self, ribNum, paramNum):
        '''
        Reads Airfoil parameters from the data store.
        @param ribNum: Number of the rib. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getAirfoilParams |'+ str(ribNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__AirfoilParams) >= ribNum:
            if len (self.__AirfoilParams[ribNum]) >= paramNum:
                return  self.__AirfoilParams[ribNum][paramNum]
        else: 
            return ''
            
    def setAnchorPointParams(self, ribNum, p1, p2, p3, p4, p5, p6, p7):
        '''
        Saves Anchor Point parameters into the data store.
        @param ribNum: Number of the rib. Indexing starts with 0!
        @param p1..7: The individual data to save
        '''
        logging.debug(self.__className+'.setAnchorPointParams |'+ str(ribNum)+'|'+ p1+'|'+ p2+'|'+ p3+'|'+ p4+'|'+ p5+'|'+ p6+'|'+ p7+'|')
        
        if ribNum >= len(self.__AnchorPointParams):
            # in case of building up the array we might need to add elements
            self.__AnchorPointParams.append([p1,p2,p3,p4,p5,p6,p7])
        else:
            # element already exists, update the data
            self.__AnchorPointParams[ribNum]= [p1, p2, p3, p4, p5, p6, p7]
        
        self.dataStatusUpdate.emit(self.__className, 'AnchorPointParams')

    def getAnchorPointParams(self, ribNum, paramNum):
        '''
        Reads Anchor point parameters from the data store.
        @param ribNum: Number of the rib. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getAnchorPointParams |'+ str(ribNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__AnchorPointParams) >= ribNum:
            if len (self.__AnchorPointParams[ribNum]) >= paramNum:
                return  self.__AnchorPointParams[ribNum][paramNum]
        else: 
            return ''
            
    def setAirfHoleConf(self, confNum, paramNum, value): 
        '''
        Saves overall Airfoil Holes config into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setAirfHoleConf |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__AirfHoleConf):
            self.__AirfHoleConf.append(['','',''])
        
        self.__AirfHoleConf[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'AirfHoleConf')
        
    def getAirfHoleConf(self, confNum, paramNum):
        '''
        Reads Airfoil holes config values from the data store.
        @param confNum: Number of the rib. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getAirfHoleConf |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__AirfHoleConf) >= confNum:
            if len (self.__AirfHoleConf[confNum]) >= paramNum:
                return  self.__AirfHoleConf[confNum][paramNum] 
        else: 
            return ''   
    
    def setAirfHoleParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Airfoil Holes params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setAirfHoleParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__AirfHoleParams):
            self.__AirfHoleParams.append([['','','','','','','','','']])
        
        if lineNum >= len(self.__AirfHoleParams[confNum]):
            self.__AirfHoleParams[confNum].append(['','','','','','','','',''])
            
        self.__AirfHoleParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'AirfHoleParams')
        
    def getAirfHoleParams(self, confNum, lineNum, paramNum):
        '''
        Reads Airfoil holes params values from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getAirfHoleParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__AirfHoleParams) >= confNum:
            if len (self.__AirfHoleParams[confNum]) >= lineNum:
                if len (self.__AirfHoleParams[confNum][lineNum]) >= paramNum:
                    return  self.__AirfHoleParams[confNum][lineNum][paramNum]
        else: 
            return ''
            
    def setSkinTensionParams(self, lineNum, paramNum, value):
        '''
        Saves Skin Tension params into the data store.
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSkinTensionParams |'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value))
        
        self.__SkinTensionParams[lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'SkinTensionParams')
        
    def getSkinTensionParams(self, confNum, paramNum):
        '''
        Reads Skin tension values from the data store.
        @param confNum: Number of the rib. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getSkinTensionParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__SkinTensionParams) >= confNum:
            if len (self.__SkinTensionParams[confNum]) >= paramNum:
                return  self.__SkinTensionParams[confNum][paramNum] 
        else: 
            return ''
        
    def setSewingAllPanelsParams(self, lineNum, paramNum, value):
        '''
        Saves Sewing allowances for panels params into the data store.
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSewingAllPanelsParams |'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value))
        
        self.__SewingAllPanelsParams[lineNum][paramNum] = value
                
        self.dataStatusUpdate.emit(self.__className, 'SewingAllPanelsParams') 
        
    def getSewingAllPanelsParams(self, lineNum, paramNum):
        '''
        Reads Sewing allowances for panels params from the data store.
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getSewingAllPanelsParams |'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__SewingAllPanelsParams) >= lineNum:
            if len (self.__SewingAllPanelsParams[lineNum]) >= paramNum:
                return  self.__SewingAllPanelsParams[lineNum][paramNum] 
        else: 
            return ''
        
        
    def setLineDescConf(self, confNum, value): 
        '''
        Saves overall Line Description config into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setLineDescConf |'+ str(confNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__LineDescConf):
            self.__LineDescConf.append('')
        
        self.__LineDescConf[confNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'LineDescConf')
        
    def getLineDescConf(self, confNum):
        '''
        Reads overall Line Description config from the data store.
        @param confNum: Number of the configuration. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getLineDescConf |'+ str(confNum)+'|')
        
        if len(self.__LineDescConf) >= confNum:
            return  self.__LineDescConf[confNum] 
        else: 
            return ''
    
    def setLineDescParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Line description params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setLineDescParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__LineDescParams):
            self.__LineDescParams.append([['','','','','','','','','','','']])
        
        if lineNum >= len(self.__LineDescParams[confNum]):
            self.__LineDescParams[confNum].append(['','','','','','','','','','',''])
            
        self.__LineDescParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'LineDescParams')
        
    def getLineDescParams(self, confNum, lineNum, paramNum):
        '''
        Reads Line description params from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getLineDescParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__LineDescParams) >= confNum:
            if len (self.__LineDescParams[confNum]) >= lineNum:
                if len (self.__LineDescParams[confNum][paramNum]) >= paramNum:
                    return  self.__LineDescParams[confNum][lineNum][paramNum] 
        else: 
            return ''
    
    def setBrakePathParams(self, confNum, paramNum, value):
        '''
        Saves Brake path params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setBrakePathParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__BrakePathParams):
            self.__BrakePathParams.append(['','','','','','','','','','',''])
            
        self.__BrakePathParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'BrakePathParams')
        
    def getBrakePathParams(self, confNum, paramNum,):
        '''
        Reads Brake path params from the data store.
        @param confNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getBrakePathParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__BrakePathParams) >= confNum:
            if len (self.__BrakePathParams[confNum]) >= paramNum:
                return  self.__BrakePathParams[confNum][paramNum] 
        else: 
            return ''
        
    def setBrakeDistrParams(self, confNum, paramNum, value):
        '''
        Saves Brake distribution params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setBrakeDistrParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
            
        self.__BrakeDistrParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'BrakeDistrParams') 
        
    def getBrakeDistrParams(self, confNum, paramNum,):
        '''
        Reads Brake distribution params from the data store.
        @param confNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getBrakeDistrParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__BrakeDistrParams) >= confNum:
            if len (self.__BrakeDistrParams[confNum]) >= paramNum:
                return  self.__BrakeDistrParams[confNum][paramNum] 
        else: 
            return '' 
        
    def setRamLengthParams(self, confNum, paramNum, value):
        '''
        Saves Ramification Length params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setRamLengthParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
            
        self.__RamLengthParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'RamLengthParams') 
        
    def getRamLengthParams(self, confNum, paramNum,):
        '''
        Reads Ramification Length params from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getRamLengthParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__RamLengthParams) >= confNum:
            if len (self.__RamLengthParams[confNum]) >= paramNum:
                return  self.__RamLengthParams[confNum][paramNum] 
        else: 
            return ''    
    
    def setMiniRibParams(self, confNum, paramNum, value):
        '''
        Saves Mini Rib params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setMiniRibParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__MiniRibParams):
            self.__MiniRibParams.append(['','','','','','','','','','',''])
            
        self.__MiniRibParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'MiniRibParams')
        
    def getMiniRibParams(self, confNum, paramNum,):
        '''
        Reads Mini Rib params from the data store.
        @param confNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getMiniRibParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__MiniRibParams) >= confNum:
            if len (self.__MiniRibParams[confNum]) >= paramNum:
                return  self.__MiniRibParams[confNum][paramNum] 
        else: 
            return ''
    
    def setExtradColorsConf(self, confNum, paramNum, value):
        '''
        Saves Configuration data for each Extrados Colors rib into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setExtradColorsConf |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__ExtradColorsConf):
            self.__ExtradColorsConf.append(['',''])
            
        self.__ExtradColorsConf[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'ExtradColorsConf')
        
    def getExtradColorsConf(self, confNum, paramNum,):
        '''
        Reads data for each Extrados Colors rib from the data store.
        @param confNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getExtradColorsConf |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__ExtradColorsConf) >= confNum:
            if len (self.__ExtradColorsConf[confNum]) >= paramNum:
                return  self.__ExtradColorsConf[confNum][paramNum] 
        else: 
            return ''
        
    def setExtradColorsParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Extrados description params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setExtradColorsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__ExtradColorsParams):
            self.__ExtradColorsParams.append([['','','']])
        
        if lineNum >= len(self.__ExtradColorsParams[confNum]):
            self.__ExtradColorsParams[confNum].append(['','',''])
            
        self.__ExtradColorsParams[confNum][lineNum][paramNum] = value

        self.dataStatusUpdate.emit(self.__className, 'ExtradColorsParams')
        
    def getExtradColorsParams(self, confNum, lineNum, paramNum):
        '''
        Reads overall Extrados description params from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getExtradColorsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__ExtradColorsParams) >= confNum:
            if len (self.__ExtradColorsParams[confNum]) >= lineNum:
                if len (self.__ExtradColorsParams[confNum][lineNum]) >= paramNum:
                    return  self.__ExtradColorsParams[confNum][lineNum][paramNum] 
        else: 
            return ''
        
    def setIntradColorsConf(self, confNum, paramNum, value):
        '''
        Saves Configuration data for each Intrados Colors rib into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setIntradColorsConf |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__IntradColorsConf):
            self.__IntradColorsConf.append(['',''])
            
        self.__IntradColorsConf[confNum][paramNum] = value
       
        self.dataStatusUpdate.emit(self.__className, 'IntradColorsConf')
        
    def getIntradColorsConf(self, confNum, paramNum,):
        '''
        Reads data for each Intrados Colors rib from the data store.
        @param confNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getIntradColorsConf |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__IntradColorsConf) >= confNum:
            if len (self.__IntradColorsConf[confNum]) >= paramNum:
                return  self.__IntradColorsConf[confNum][paramNum] 
        else: 
            return ''
        
    def setIntradColorsParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Intrados description params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setIntradColorsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__IntradColorsParams):
            self.__IntradColorsParams.append([['','','']])
        
        if lineNum >= len(self.__IntradColorsParams[confNum]):
            self.__IntradColorsParams[confNum].append(['','',''])
            
        self.__IntradColorsParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'IntradColorsParams')
        
    def getIntradColorsParams(self, confNum, lineNum, paramNum):
        '''
        Reads overall Intrados description params from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getIntradColorsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__IntradColorsParams) >= confNum:
            if len (self.__IntradColorsParams[confNum]) >= lineNum:
                if len (self.__IntradColorsParams[confNum][lineNum]) >= paramNum:
                    return  self.__IntradColorsParams[confNum][lineNum][paramNum] 
        else: 
            return ''
    
    def setAddRibPointsParams(self, confNum, paramNum, value):
        '''
        Saves Additional Rib Point data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setAddRibPointsParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__AddRibPointsParams):
            self.__AddRibPointsParams.append(['',''])
            
        self.__AddRibPointsParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'AddRibPointsParams')
    
    def getAddRibPointsParams(self, confNum, paramNum,):
        '''
        Reads Additional Rib Point data from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getAddRibPointsParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__AddRibPointsParams) >= confNum:
            if len (self.__AddRibPointsParams[confNum]) >= paramNum:
                return  self.__AddRibPointsParams[confNum][paramNum] 
        else: 
            return ''
    
    def setLoadDistrParams(self, confNum, paramNum, value):
        '''
        Saves Load Distribution data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setLoadDistrParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        self.__LoadDistrParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'LoadDistrParams')
        
    def getLoadDistrParams(self, confNum, paramNum,):
        '''
        Reads Load Distribution data from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getLoadDistrParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__LoadDistrParams) >= confNum:
            if len (self.__LoadDistrParams[confNum]) >= paramNum:
                return  self.__LoadDistrParams[confNum][paramNum] 
        else: 
            return ''
        
    def setLoadDeformParams(self, confNum, paramNum, value):
        '''
        Saves Load Deformation data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setLoadDeformParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        self.__LoadDeformParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'LoadDeformParams')
        
    def getLoadDeformParams(self, confNum, paramNum,):
        '''
        Reads Load Deformation data from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getLoadDeformParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__LoadDeformParams) >= confNum:
            if len (self.__LoadDeformParams[confNum]) >= paramNum:
                return  self.__LoadDeformParams[confNum][paramNum] 
        else: 
            return ''
    
    def setDxfLayerParams(self, confNum, paramNum, value):
        '''
        Saves DXF Layer data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setDxfLayerParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__DxfLayerParams):
            self.__DxfLayerParams.append(['',''])
            
        self.__DxfLayerParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'DxfLayerParams')
        
    def getDxfLayerParams(self, confNum, paramNum,):
        '''
        Reads DXF Layer data from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getDxfLayerParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__DxfLayerParams) >= confNum:
            if len (self.__DxfLayerParams[confNum]) >= paramNum:
                return  self.__DxfLayerParams[confNum][paramNum] 
        else: 
            return ''
    
    def setMarkTypeParams(self, confNum, paramNum, value):
        '''
        Saves Mark Type data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setMarkTypeParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__MarkTypeParams):
            self.__MarkTypeParams.append(['','','','','','',''])
            
        self.__MarkTypeParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'MarkTypeParams')
        
    def getMarkTypeParams(self, confNum, paramNum,):
        '''
        Reads Mark Type data from the data store.
        @param confNum: Number of the configuration read. Indexing starts with 0!
        @param paramNum: Number of the parameter to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getMarkTypeParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__MarkTypeParams) >= confNum:
            if len (self.__MarkTypeParams[confNum]) >= paramNum:
                return  self.__MarkTypeParams[confNum][paramNum] 
        else: 
            return ''
    
    def setJoncsConfigsParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Joncs Config params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setJoncsConfigsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__JoncsConfigsParams):
            self.__JoncsConfigsParams.append([['','','','']])
        
        if lineNum >= len(self.__JoncsConfigsParams[confNum]):
            self.__JoncsConfigsParams[confNum].append(['','','',''])
            
        self.__JoncsConfigsParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'JoncsConfigsParams')
    
    def getJoncsConfigsParams(self, confNum, lineNum, paramNum):
        '''
        Reads overall Joncs Config params from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getJoncsConfigsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__JoncsConfigsParams) >= confNum:
            if len (self.__JoncsConfigsParams[confNum]) >= lineNum:
                if len (self.__JoncsConfigsParams[confNum][lineNum]) >= paramNum:
                    return  self.__JoncsConfigsParams[confNum][lineNum][paramNum] 
        else: 
            return ''
        
    def setNoseMylarsParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Nose Mylars params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setNoseMylarsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__NoseMylarsParams):
            self.__NoseMylarsParams.append([['','','','','','']])
        
        if lineNum >= len(self.__NoseMylarsParams[confNum]):
            self.__NoseMylarsParams[confNum].append(['','','','','',''])
            
        self.__NoseMylarsParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'NoseMylarsParams')
    
    def getNoseMylarsParams(self, confNum, lineNum, paramNum):
        '''
        Reads overall Nose Mylars params from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getNoseMylarsParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__NoseMylarsParams) >= confNum:
            if len (self.__NoseMylarsParams[confNum]) >= lineNum:
                if len (self.__NoseMylarsParams[confNum][lineNum]) >= paramNum:
                    return  self.__NoseMylarsParams[confNum][lineNum][paramNum] 
        else: 
            return ''
        
    def setTabReinfParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Tab Reinforcement params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setTabReinfParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__TabReinfParams):
            self.__TabReinfParams.append([['','','','','']])
        
        if lineNum >= len(self.__TabReinfParams[confNum]):
            self.__TabReinfParams[confNum].append(['','','','',''])
            
        self.__TabReinfParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'TabReinfParams')
    
    def getTabReinfParams(self, confNum, lineNum, paramNum):
        '''
        Reads overall Tab Reinforcement params from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getTabReinfParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__TabReinfParams) >= confNum:
            if len (self.__TabReinfParams[confNum]) >= lineNum:
                if len (self.__TabReinfParams[confNum][lineNum]) >= paramNum:
                    return  self.__TabReinfParams[confNum][lineNum][paramNum] 
        else: 
            return ''
        
    def setSchemesParams(self, confNum, paramNum, value):
        '''
        Saves Schemes data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSchemesParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__SchemesParams):
            self.__SchemesParams.append([])
        if paramNum >= len(self.__SchemesParams[confNum]):
            self.__SchemesParams[confNum].append('')
            
        self.__SchemesParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'SchemesParams')
        
    def getNumSchemesLines(self):
        '''
        Returns the number of Tab Reinforcement Scheme lines into the data store.
        @return: number of Scheme lines
        '''
        logging.debug(self.__className+'.getNumSchemesLines |')
        return len(self.__SchemesParams)
        
    def getNumSchemesParams(self, line):
        '''
        Returns the number of parameters registered in a specific Tabinforcement 
        Scheme line into the data store.
        @param line: the line of which the num of parameters is asked. Indexing starts with 0!
        @return: number of Parameters
        '''
        return len(self.__SchemesParams[line])
    
    def getSchemesParams(self, lineNum, paramNum,):
        '''
        Reads Schemes data from the data store.
        @param lineNum: Number of the line to read. Indexing starts with 0!
        @param paramNum: Number of the parameter to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getSchemesParams |'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__SchemesParams) >= lineNum:
            if len (self.__SchemesParams[lineNum]) >= paramNum:
                return  self.__SchemesParams[lineNum][paramNum] 
        else: 
            return ''
    
    def setTwoDDxfParams(self, confNum, paramNum, value):
        '''
        Saves 2D DXF data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setTwoDParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        self.__2DDxfParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'TwoDDxfParams')
        
    def getTwoDDxfParams(self, confNum, paramNum):
        '''
        Reads 2D DXF data from the data store.
        @param confNum: Number of the config to read. Indexing starts with 0!
        @param paramNum: Number of the parameter to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getSchemesParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__2DDxfParams) >= confNum:
            if len (self.__2DDxfParams[confNum]) >= paramNum:
                return  self.__2DDxfParams[confNum][paramNum] 
        else: 
            return ''
    
    def setThreeDDxfParams(self, confNum, paramNum, value):
        '''
        Saves 3D DXF data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setThreeDParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        self.__3DDxfParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'ThreeDDxfParams')
    
    def getThreeDDxfParams(self, confNum, paramNum):
        '''
        Reads 3D DXF data from the data store.
        @param confNum: Number of the config to read. Indexing starts with 0!
        @param paramNum: Number of the parameter to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getSchemesParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__3DDxfParams) >= confNum:
            if len (self.__3DDxfParams[confNum]) >= paramNum:
                return  self.__3DDxfParams[confNum][paramNum] 
        else: 
            return ''
        
    def setGlueVentParams(self, confNum, value):
        '''
        Saves GlueVent data into the data store.
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setGlueVentParams |'+ str(confNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__GlueVentParams):
            self.__GlueVentParams.append('')
            
        self.__GlueVentParams[confNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'GlueVentParams') 
        
    def getGlueVentParams(self, confNum):
        '''
        Reads GlueVent data from the data store.
        @param confNum: Number of the config to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getGlueVentParams |'+ str(confNum)+'|')
        
        if len(self.__GlueVentParams) >= confNum:
            return  self.__GlueVentParams[confNum]
        else: 
            return ''
        
    def setCalageVarCordParams(self, paramNum, value):
        '''
        Saves Calage Variation % of cord params into the data store.
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setCalageVarCordParam |'+ str(paramNum)+'|'+ str(value)+'|')
        
        if paramNum >= len(self.__calageVarCordParams):
            self.__calageVarCordParams.append('')
            
        self.__calageVarCordParams[paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'CalageVarCordParams')
        
    def getCalageVarCordParams(self, paramNum):
        '''
        Reads Calage Variation % of cord params from the data store.
        @param paramNum: Number of the param to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getCalageVarCordParams |'+ str(paramNum)+'|')
        
        if len(self.__calageVarCordParams) >= paramNum:
            return  self.__calageVarCordParams[paramNum]
        else: 
            return ''
        
    def setCalageVarAngleParams(self, paramNum, value):
        '''
        Saves Calage Variation angle variation params into the data store.
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setCalageVarAngleParams |'+ str(paramNum)+'|'+ str(value)+'|')
        
        if paramNum >= len(self.__calageVarAngleParams):
            self.__calageVarAngleParams.append('')
            
        self.__calageVarAngleParams[paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'CalageVarAngleParams')
        
    def getCalageVarAngleParams(self, paramNum):
        '''
        Reads Calage Variation angle variation params from the data store.
        @param paramNum: Number of the param to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getCalageVarCordParams |'+ str(paramNum)+'|')
        
        if len(self.__calageVarAngleParams) >= paramNum:
            return  self.__calageVarAngleParams[paramNum]
        else: 
            return ''
    
    def setThreeDShapingGroupConf(self, confNum, paramNum, value):
        '''
        Saves the individual gropu configurations for the 3D Shaping into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setThreeDShapingGroupConf |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__threeDShapingGroupConf):
            self.__threeDShapingGroupConf.append(['','',''])
            
        self.__threeDShapingGroupConf[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'ThreeDShapingGroupConf')
        
    def getThreeDShapingGroupConf(self, confNum, paramNum):
        '''
        Reads individual gropu configurations for the 3D Shaping from the data store.
        @param confNum: Number of the config to read. Indexing starts with 0!
        @param paramNum: Number of the parameter to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getThreeDShapingGroupConf |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__threeDShapingGroupConf) >= confNum:
            if len (self.__threeDShapingGroupConf[confNum]) >= paramNum:
                return  self.__threeDShapingGroupConf[confNum][paramNum] 
        else: 
            return ''
    
    def setThreeDShapingUpGroupParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves parameters for 3D Shaping upper groups into the data store.
        @param confNum: Number of the Group. Indexing starts with 0!
        @param lineNum: Number of the line withing the group. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0! Conf line numbers are ignored!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setThreeDShapingUpGroupParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__threeDShapingUpGroupParams):
            self.__threeDShapingUpGroupParams.append([['','','']])
        
        if lineNum >= len(self.__threeDShapingUpGroupParams[confNum]):
            self.__threeDShapingUpGroupParams[confNum].append(['','',''])
            
        self.__threeDShapingUpGroupParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'ThreeDShapingUpGroupParams')
    
    def getNumThreeDShapingUpGroups(self, confNum):
        '''
        Returns the number of 3D shaping up groups for a specific configuration into the data store.
        @param confNum: the configuration number of which num of groups is asked. Indexing starts with 0!
        @return: number of groups
        '''
        logging.debug(self.__className+'.getNumThreeDShapingUpGroups |'+ str(confNum)+'|')
        return len(self.__threeDShapingUpGroupParams[confNum])-1

    def getThreeDShapingUpGroupParams(self, confNum, lineNum, paramNum):
        '''
        Reads parameters for 3D Shaping upper groups from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getThreeDShapingUpGroupParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__threeDShapingUpGroupParams) >= confNum:
            if len (self.__threeDShapingUpGroupParams[confNum]) >= lineNum:
                if len (self.__threeDShapingUpGroupParams[confNum][lineNum]) >= paramNum:
                    return  self.__threeDShapingUpGroupParams[confNum][lineNum][paramNum] 
        else: 
            return ''
        
    def setThreeDShapingLoGroupParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves parameters for 3D Shaping lower groups into the data store.
        @param confNum: Number of the Group. Indexing starts with 0!
        @param lineNum: Number of the line withing the group. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0! Conf line numbers are ignored!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setThreeDShapingLoGroupParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__threeDShapingLoGroupParams):
            self.__threeDShapingLoGroupParams.append([['','','']])
        
        if lineNum >= len(self.__threeDShapingLoGroupParams[confNum]):
            self.__threeDShapingLoGroupParams[confNum].append(['','',''])
            
        self.__threeDShapingLoGroupParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'ThreeDShapingLoGroupParams')
    
    def getNumThreeDShapingLoGroups(self, confNum):
        '''
        Returns the number of 3D shaping lo groups for a specific configuration into the data store.
        @param confNum: the configuration number of which num of groups is asked. Indexing starts with 0!
        @return: number of groups
        '''
        logging.debug(self.__className+'.getNumThreeDShapingLoGroups |'+ str(confNum)+'|')
        return len(self.__threeDShapingLoGroupParams[confNum])-1
    
    def getThreeDShapingLoGroupParams(self, confNum, lineNum, paramNum):
        '''
        Reads parameters for 3D Shaping lower groups from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getThreeDShapingLoGroupParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__threeDShapingLoGroupParams) >= confNum:
            if len (self.__threeDShapingLoGroupParams[confNum]) >= lineNum:
                if len (self.__threeDShapingLoGroupParams[confNum][lineNum]) >= paramNum:
                    return  self.__threeDShapingLoGroupParams[confNum][lineNum][paramNum] 
        else: 
            return ''
    
    def setThreeDShapingPrintParams(self, confNum, paramNum, value):
        '''
        Saves the individual print params for the 3D Shaping into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setThreeDShapingPrintParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
            
        self.__threeDShapingPrintParams[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'ThreeDShapingPrintParams')
    
    def getThreeDShapingPrintParams(self, confNum, paramNum):
        '''
        Reads individual individual print params for the 3D Shaping from the data store.
        @param confNum: Number of the config to read. Indexing starts with 0!
        @param paramNum: Number of the parameter to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getThreeDShapingPrintParams |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__threeDShapingPrintParams) >= confNum:
            if len (self.__threeDShapingPrintParams[confNum]) >= paramNum:
                return  self.__threeDShapingPrintParams[confNum][paramNum] 
        else: 
            return ''
        
    def setAirfThiknessModifParams(self, confNum, value):
        '''
        Saves parameters for Airfoil Thikness Modification into the data store.
        @param confNum: Number of the rib. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setAirfThiknessModifParams |'+ str(confNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__airfThiknessModifParams):
            self.__airfThiknessModifParams.append('')
            
        self.__airfThiknessModifParams[confNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'AirfThiknessModifParams')
        
    def getAirfThiknessModifParams(self, confNum):
        '''
        Reads parameters for Airfoil Thikness Modification from the data store.
        @param confNum: Number of the config to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getAirfThiknessModifParams |'+ str(confNum)+'|')
        
        if len(self.__airfThiknessModifParams) >= confNum:
            return  self.__airfThiknessModifParams[confNum]
        else: 
            return ''
        
    def setSkinTensionGroupConf(self, confNum, paramNum, value):
        '''
        Saves the individual group configurations for the Skin Tension into the data store.
        @param confNum: Number of the configuration. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSkinTensionGroupConf |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__skinTensionGroupConf):
            self.__skinTensionGroupConf.append(['','','',''])
            
        self.__skinTensionGroupConf[confNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'SkinTensionGroupConf')
        
    def getSkinTensionGroupConf(self, confNum, paramNum):
        '''
        Reads individual group configurations for the Skin Tension from the data store.
        @param confNum: Number of the config to read. Indexing starts with 0!
        @param paramNum: Number of the parameter to read. Indexing starts with 0!
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getSkinTensionGroupConf |'+ str(confNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__skinTensionGroupConf) >= confNum:
            if len (self.__skinTensionGroupConf[confNum]) >= paramNum:
                return  self.__skinTensionGroupConf[confNum][paramNum] 
        else: 
            return ''
        
    def setSkinTensionGroupParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves parameters for Skin Tension groups into the data store.
        @param confNum: Number of the Group. Indexing starts with 0!
        @param lineNum: Number of the line withing the group. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0! Conf line numbers are ignored!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSkinTensionGroupParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__skinTensionGroupParams):
            self.__skinTensionGroupParams.append([['','','','']])
        
        if lineNum >= len(self.__skinTensionGroupParams[confNum]):
            self.__skinTensionGroupParams[confNum].append(['','','',''])
            
        self.__skinTensionGroupParams[confNum][lineNum][paramNum] = value
        
        self.dataStatusUpdate.emit(self.__className, 'SkinTensionGroupParams')
        
    def getSkinTensionGroupParams(self, confNum, lineNum, paramNum):
        '''
        Reads parameters for Skin Tension groups from the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param lineNum: Number of the line. Indexing starts with 0!
        @param paramNum: Individual param num
        @return: Parameter value
        '''
        logging.debug(self.__className+'.getSkinTensionGroupParams |'+ str(confNum)+'|'+ str(lineNum)+'|'+ str(paramNum)+'|')
        
        if len(self.__skinTensionGroupParams) >= confNum:
            if len (self.__skinTensionGroupParams[confNum]) >= lineNum:
                if len (self.__skinTensionGroupParams[confNum][lineNum]) >= paramNum:
                    return  self.__skinTensionGroupParams[confNum][lineNum][paramNum] 
        else: 
            return ''
    
    def remTabSpaceQuot(self, line):
        '''
        Removes from a string all leading, trailing spaces tabs and quotations
        @param Line: The string to be cleaned
        @return: cleaned string 
        '''
        line = self.remTabSpace(line)
        line = re.sub(r'^\"+|\"+$', '', line )
        return line
    
    def remTabSpace(self, line):
        '''
        Deletes all leaing and trailing edges from a string
        @param Line: The string to be cleaned
        @return: cleaned string 
        '''
        value = re.sub(r'^\s+|\s+$', '', line ) 
        return value
    
    def splitLine(self, line):
        '''
        Splits lines with multiple values into a list of values
        delimiters could be spaces and tabs
        @param line: The line to be split
        @return: a list of values 
        '''
        line = self.remTabSpace(line) # remove leadind and trailing waste
        values = re.split(r'[\t\s]\s*', line)
        return values
    
    def writeHeader(self, stream, title):
        '''
        Writes the section header in the data file
        @param stream: The stream to write to
        @title: The section title 
        '''
        stream << self.__separator
        stream << '* '+ title+ '\n'
        stream << self.__separator

