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
from binhex import LINELEN

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
    __SchemesParams = [ [0 for x in range(8)] for y in range(1)]
    
    # GENERAL 2D DXF OPTIONS
    
    # GENERAL 3D DXF OPTIONS
    
    # GLUE VENTS
    
    # SPECIAL WING TIP
    
    # PARAMETERS FOR CALAGE VARIATION
    
    # 3D SHAPING
    
    # AIRFOIL THICKNESS MODIFICATION
    
    # NEW SKIN TENSION MODULE
    
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
        Asks for a new filename. 
        Starts afterwards the writing process.  
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
        Reads the data file and saves the data in the internal varibles.
        Filename and Path must be set first!
        '''
        logging.debug(self.__className+'.readFile')
        inFile = QFile(self.getSingleVal('FileNamePath'))
        inFile.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(inFile)

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

        # AIRFOILS
        for i in range(4):
            line = stream.readLine()
        
        for i in range( 0, self.getSingleVal('HalfNumRibs') ):
            values =  self.splitLine( stream.readLine() )
            self.setAirfoilParams(i, values[1], values[2], values[3], values[4], values[5], values[6], values[7])
        
        # ANCHOR POINTS
        for i in range(4):
            line = stream.readLine()
        
        for i in range( 0, self.getSingleVal('HalfNumRibs') ):
            values =  self.splitLine( stream.readLine() )
            self.setAnchorPointParams(i, values[1], values[2], values[3], values[4], values[5], values[6], values[7])    
        
        # AIRFOIL HOLES
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

        # SKIN TENSION
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
        
        # SEWING ALLOWANCES
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
    
        # MARKS
        for i in range(3):
            line = stream.readLine()
            
        values = self.splitLine( stream.readLine() )
        self.setSingleVal('MarksP1', values[0] )
        self.setSingleVal('MarksP2', values[1] )
        self.setSingleVal('MarksP3', values[2] )
        
        # Global angle of attack estimation
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
        
        # SUSPENSION LINES DESCRIPTION
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
        # BRAKES
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
                self.setBrakePathParams(configCounter, paramCounter, values[paramCounter])
                
        # Ramification lengths
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
        
        # H V and VH ribs (Mini Ribs)
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
        
        # Extrados colors
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
        
        # Intrados colors
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
        
        # Aditional rib points
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumAddRibPoints', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            self.setAddRibPointsParams(configCounter, 0, values[0] )
            self.setAddRibPointsParams(configCounter, 1, values[1] )
        
        # Elastic lines corrections
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
        
        # DXF layer names
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumDxfLayers', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range(0, 2):
                self.setDxfLayerParams(configCounter, paramCounter, values[paramCounter])
        
        # Marks types
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NumMarkTypes', numConfigs )
        
        for configCounter in range(0, int(numConfigs)):
            values =  self.splitLine( stream.readLine() )
            
            for paramCounter in range(0, 7):
                self.setMarkTypeParams(configCounter, paramCounter, values[paramCounter])
        
        # JONCS DEFINITION (NYLON RODS)
        for i in range(3):
            line = stream.readLine()
            
        joncsType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('JoncsType', joncsType )
        
        if joncsType != '0':
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
        
        # NOSE MYLARS DEFINITION
        for i in range(3):
            line = stream.readLine()
            
        noseMylarsType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('NoseMylarsType', noseMylarsType )
        
        if joncsType != '0':
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
                                                    
        # TAB REINFORCEMENTS
        for i in range(3):
            line = stream.readLine()
            
        tabReinfType = self.remTabSpace( stream.readLine() )
        self.setSingleVal('TabReinfType', tabReinfType )
        
        if tabReinfType != '0':
            # we have data to read
            
            numConfigs = self.remTabSpace( stream.readLine() )
            self.setSingleVal('NumTabReinfConfigs', numConfigs )
            
            for configCounter in range(0, int(numConfigs)):
                
                for lineCounter in range(0, 2 ):
                    values =  self.splitLine( stream.readLine() )
                    
                    for paramCounter in range (0, 3):
                        self.setTabReinfParams(configCounter, lineCounter, paramCounter, values[paramCounter])
                    
                    if lineCounter > 0:
                        self.setTabReinfParams(configCounter, lineCounter, 3, values[3])
        
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
                
        # GENERAL 2D DXF OPTIONS
        # be carefull: previous code has already read first line of header
        for i in range(2):
            line = stream.readLine()
            
        
        # GENERAL 3D DXF OPTIONS
        
        # GLUE VENTS
        
        # SPECIAL WING TIP
        
        # PARAMETERS FOR CALAGE VARIATION
        
        # 3D SHAPING
        
        # AIRFOIL THICKNESS MODIFICATION
        
        # NEW SKIN TENSION MODULE
        
        # Clean up 
        inFile.close()
        self.dataStatusUpdate.emit(self.__className,'Open')
        

    

        
       
    
    
  
    def writeFile(self, forProc=False):
        '''
        Writes all the values into a data file. 
        Filename must have been set already before, unless the file shall be written for the PreProcessor.
                
        @param forProc: Set this to True if the file must be saved in the directory where the PreProcessor resides
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
        stream << 'c01= ' << self.getSingleVal('LE_c0') << '\n'
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
        # TODO: add emit signal
            
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
        # TODO: add emit signal
            
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
        # TODO: add emit signal
    
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
        # TODO: add emit signal
    
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
        # TODO: add emit signal
    
    def setSkinTensionParams(self, lineNum, paramNum, value):
        '''
        Saves Skin Tension params into the data store.
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSkinTensionParams |'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value))
        
        self.__SkinTensionParams[lineNum][paramNum] = value
        # TODO: add emit signal
        
    def setSewingAllPanelsParams(self, lineNum, paramNum, value):
        '''
        Saves Sewing allowances for panels params into the data store.
        @param lineNum: Number of the configuration line. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSewingAllPanelsParams |'+ str(lineNum)+'|'+ str(paramNum)+'|'+ str(value))
        
        self.__SewingAllPanelsParams[lineNum][paramNum] = value
        # TODO: add emit signal 
        
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
        # TODO: add emit signal
    
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
        # TODO: add emit signal  
    
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
        # TODO: add emit signal
        
    def setBrakeDistrParams(self, confNum, paramNum, value):
        '''
        Saves Brake distribution params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setBrakeDistrParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
            
        self.__BrakeDistrParams[confNum][paramNum] = value
        # TODO: add emit signal    
        
    def setRamLengthParams(self, confNum, paramNum, value):
        '''
        Saves Ramification Length params into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setRamLengthParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
            
        self.__RamLengthParams[confNum][paramNum] = value
        # TODO: add emit signal 
    
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
        # TODO: add emit signal
    
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
        # TODO: add emit signal
        
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
        # TODO: add emit signal
        
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
        # TODO: add emit signal
        
    def setIntradColorsParams(self, confNum, lineNum, paramNum, value):
        '''
        Saves overall Extrados description params into the data store.
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
        # TODO: add emit signal
    
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
        # TODO: add emit signal
    
    def setLoadDistrParams(self, confNum, paramNum, value):
        '''
        Saves Load Distribution data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setLoadDistrParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        self.__LoadDistrParams[confNum][paramNum] = value
        # TODO: add emit signal
        
    def setLoadDeformParams(self, confNum, paramNum, value):
        '''
        Saves Load Deformation data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setLoadDeformParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        self.__LoadDeformParams[confNum][paramNum] = value
        # TODO: add emit signal
    
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
        # TODO: add emit signal
    
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
        # TODO: add emit signal
    
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
        # TODO: add emit signal
        
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
        # TODO: add emit signal
        
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
            self.__TabReinfParams.append([['','','','']])
        
        if lineNum >= len(self.__TabReinfParams[confNum]):
            self.__TabReinfParams[confNum].append(['','','',''])
            
        self.__TabReinfParams[confNum][lineNum][paramNum] = value
        # TODO: add emit signal
        
    def setSchemesParams(self, confNum, paramNum, value):
        '''
        Saves Schemes data into the data store.
        @param confNum: Number of the configuration set. Indexing starts with 0!
        @param paramNum: Number of the parameter to set. Indexing starts with 0!
        @param value: The individual data to save
        '''
        logging.debug(self.__className+'.setSchemesParams |'+ str(confNum)+'|'+ str(paramNum)+'|'+ str(value)+'|')
        
        if confNum >= len(self.__SchemesParams):
            self.__SchemesParams.append(['','','','','','','',''])
            
        self.__SchemesParams[confNum][paramNum] = value
        # TODO: add emit signal
    
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
