'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''

from os import path

import gettext
import logging.config
import sys
import platform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QMessageBox, QFileDialog, QMenu

from __init__ import __version__

from ConfigReader.ConfigReader import ConfigReader
from DataStores.PreProcessorStore import PreProcessorStore

from DataStores.ProcessorStore import ProcessorStore
from DataStores.ProcessorModel import ProcessorModel

from Windows.DataStatusOverview import DataStatusOverview
from Windows.PreProcDataEdit import PreProcDataEdit
from Windows.WingViewer import WingViewer
from Windows.ProcBasicData import ProcBasicData
from Windows.ProcGeometry import ProcGeometry
from Windows.ProcAirfoils import ProcAirfoils
from Windows.RibHoles import RibHoles
from Windows.HelpAbout import HelpAbout
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from Processors.ProcRunner import ProcRunner
from Windows.ProcessorOutput import ProcessorOutput
from Windows.ProcAnchorPoints import ProcAnchorPoints
from Windows.ProcSkinTension import ProcSkinTension
from Windows.SeewingAllowances import SeewingAllowances
from Windows.Marks import Marks
from Windows.GlobalAoA import GlobalAoA
from Windows.Lines import Lines
from Windows.Brakes import Brakes
from Windows.Ramification import Ramification
from Windows.HvVhRibs import HvVhRibs

class MainWindow(QMainWindow):
    '''
    :class: Creates the main window of the application
    '''
    
    __className = 'MainWindow'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    
    __enableWingFunct = True
    '''
    :attr: Set to true to enable all menus related to wing (Processor) functionality. This is used as a temporary aid allowing easier to sync back to the stable branch.
    ''' 

    def __init__(self, parent = None):
        '''
        :method: Constructor
        '''
        # Setup the logger
        # Additional code needed due to pyinstaller. Check doc there. 
        bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
        path_to_dat = path.abspath(path.join(bundle_dir, 'logger.conf'))
        
        logging.config.fileConfig(path_to_dat, disable_existing_loggers=False)
        self.logger = logging.getLogger('root')
        # DEBUG
        # INFO
        # WARNING
        # ERROR
        # CRITICAL
        logging.debug(self.__className + '.__init__')
        
        # Setup languages
        locale_path = 'translations'
        config = ConfigReader()
        
        if config.getLanguage() == "de":
            lang_de = gettext.translation ('lepg', locale_path, languages=['de'] )
            lang_de.install()
        elif config.getLanguage() =="en":
            lang_en = gettext.translation ('lepg', locale_path, languages=['en'] )
            lang_en.install()
        else:
            lang_en = gettext.translation ('lepg', locale_path, languages=['en'] )
            lang_en.install()
        
        self.pps = PreProcessorStore()
        
        # @TODO: ProcessorModel
        self.ps = ProcessorStore()
        self.pm = ProcessorModel()
        
        self.dws = DataWindowStatus()
        
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("lepg %s" %(__version__))
        self.mainMenu = self.menuBar()
        
        # Build the individual menus
        self.buildFileMenu()
        self.buildPreProcMenu()
        self.buildProcMenu()
        self.buildPlanMenu()
        self.buildViewMenu()
        self.buildSetupMenu()
        self.buildHelpMenu()
        
        # Create the status bar
        self.statusBar()
   
    def buildFileMenu(self):
        '''
        :method: Builds the complete file menu
        '''
        # Define the actions
        fileDataStatusAct = QAction(_('Show Data Status'), self)
        fileDataStatusAct.setStatusTip(_('Provides an overview about what data has (not) been saved'))
        fileDataStatusAct.triggered.connect(self.fileDataStatus)
        
        fileExitAct = QAction(_('Exit'), self)
        fileExitAct.setStatusTip(_('Leave the app'))
        fileExitAct.triggered.connect(self.fileExit)

        # Build the menu
        fileMenu = self.mainMenu.addMenu(_('File'))
        fileMenu.addAction(fileDataStatusAct)
        fileMenu.addSeparator()
        fileMenu.addAction(fileExitAct)
    
    def fileExit(self):
        ''' 
        :method: Does all the work to close properly the application. 
        '''
        logging.debug(self.__className + '.fileExit')
        sys.exit()  
        
    def fileDataStatus(self):
        '''
        :method: Opens the File Data Status overview window.
        '''
        if self.dws.windowExists('DataStatusOverview') == False:
            self.fileDataStatusW = DataStatusOverview()
            self.dws.registerWindow('DataStatusOverview')
            self.mdi.addSubWindow(self.fileDataStatusW)
        self.fileDataStatusW.show() 
    
    def buildPreProcMenu(self):
        '''
        :method: Builds the complete Pre-Processor menu
        '''  
        # Define the actions
        preProcOpenFileAct = QAction(_('Open PreProc File'), self)
        preProcOpenFileAct.setStatusTip(_('open_preProc_file_desc'))
        preProcOpenFileAct.triggered.connect(self.preProcOpenFile)
        
        preProcSaveAct = QAction(_('Save PreProc File'), self)
        preProcSaveAct.setStatusTip(_('save_preProc_file_desc'))
        preProcSaveAct.triggered.connect(self.preProcSaveFile)
        
        preProcSaveAsAct = QAction(_('Save PreProc File As ..'), self)
        preProcSaveAsAct.setStatusTip(_('save_preProc_file_as_desc'))
        preProcSaveAsAct.triggered.connect(self.preProcSaveFileAs)
        
        preProcEditAct = QAction(_('Edit PreProc Data'), self)
        preProcEditAct.setStatusTip(_('edit_preProc_data_description'))
        preProcEditAct.triggered.connect(self.preProcEdit)
        
        preProcRunAct = QAction(_('Run Pre-Processor'), self)
        preProcRunAct.setStatusTip(_('run_preProc_des'))
        preProcRunAct.triggered.connect(self.preProcRun)
        
        # Build the menu
        preProcMenu = self.mainMenu.addMenu(_('Pre Processor'))
        preProcMenu.addAction(preProcOpenFileAct)
        preProcMenu.addAction(preProcSaveAct)
        preProcMenu.addSeparator()
        preProcMenu.addAction(preProcSaveAsAct)
        preProcMenu.addSeparator()
        preProcMenu.addAction(preProcEditAct)
        preProcMenu.addAction(preProcRunAct)
        
    def preProcOpenFile(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Open PreProc File*
        ''' 
        self.pps.openFile()
        
    def preProcSaveFile(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Save PreProc File*
        '''
        self.pps.saveFile()
        
    def preProcSaveFileAs(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Save PreProc File As ..*
        '''
        self.pps.saveFileAs()
        
    def preProcEdit(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Edit PreProc Data*
        '''
        if self.dws.windowExists('PreProcDataEdit') == False:
            self.preProcEditW = PreProcDataEdit()
            self.dws.registerWindow('PreProcDataEdit')
            self.mdi.addSubWindow(self.preProcEditW)

        self.preProcEditW.show() 
        
    def preProcRun(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Run Pre-Processor*
        '''
        logging.debug(self.__className + '.preProcRun')
        
        # Save current file into processor directory
        self.pps.writeFile(True)
        
        # Open the window for the user info
        if self.dws.windowExists('ProcessorOutput') == False:
            self.procOutW = ProcessorOutput()
            self.dws.registerWindow('ProcessorOutput')
            self.mdi.addSubWindow(self.procOutW)
        self.procOutW.show()
        
        # Finally run the processor
        preProcRunner = ProcRunner(self.procOutW)
        preProcRunner.runPreProc()

    def buildProcMenu(self):
        '''
        :method: Builds the complete Processor menu
        '''  
        # Define the actions
        procOpenFile_A = QAction(_('Open Processor File'), self)
        procOpenFile_A.setStatusTip(_('open_Proc_file_desc'))
        procOpenFile_A.triggered.connect(self.procOpenFile)
        procOpenFile_A.setEnabled(self.__enableWingFunct)
        
        procSave_A = QAction(_('Save Processor File'), self)
        procSave_A.setStatusTip(_('save_proc_file_desc'))
        procSave_A.triggered.connect(self.procSaveFile)
        procSave_A.setEnabled(self.__enableWingFunct)
        
        procSaveAs_A = QAction(_('Save Processor File As ..'), self)
        procSaveAs_A.setStatusTip(_('save_proc_file_as_desc'))
        procSaveAs_A.triggered.connect(self.procSaveFileAs)
        procSaveAs_A.setEnabled(self.__enableWingFunct)
        
        procBasicData_A = QAction(_('Basic data'), self)
        procBasicData_A.setStatusTip(_('Editing the wing basics'))
        procBasicData_A.triggered.connect(self.procBasicDataEdit)
        procBasicData_A.setEnabled(self.__enableWingFunct)
        
        procGeometry_A = QAction(_('Geometry'), self)
        procGeometry_A.setStatusTip(_('Edit wing geometry'))
        procGeometry_A.triggered.connect(self.procGeometryEdit)
        procGeometry_A.setEnabled(self.__enableWingFunct)
        
        procAirfoils_A = QAction(_('Airfoils'), self)
        procAirfoils_A.setStatusTip(_('Edit airfoils geometry'))
        procAirfoils_A.triggered.connect(self.procAirfoilsEdit)
        procAirfoils_A.setEnabled(self.__enableWingFunct)
        
        procAnchPoints_A = QAction(_('Anchor Points'), self)
        procAnchPoints_A.setStatusTip(_('Edit Anchor points data'))
        procAnchPoints_A.triggered.connect(self.procAnchorPointsEdit)
        procAnchPoints_A.setEnabled(self.__enableWingFunct)
        
        procRibHoles_A = QAction(_('Rib Holes'), self)
        procRibHoles_A.setStatusTip(_('Edit rib holes (Rib lightening) data'))
        procRibHoles_A.triggered.connect(self.procRibHolesEdit)
        procRibHoles_A.setEnabled(self.__enableWingFunct)
        
        procSkinTension_A = QAction(_('Skin Tension'), self)
        procSkinTension_A.setStatusTip(_('Edit Skin tension data'))
        procSkinTension_A.triggered.connect(self.procSkinTensionEdit)
        procSkinTension_A.setEnabled(self.__enableWingFunct)
        
        procGenAoA_A = QAction(_('Estimated general AoA'), self)
        procGenAoA_A.setStatusTip(_('Edit global AoA data'))
        procGenAoA_A.triggered.connect(self.procGlobalAoAEdit)
        procGenAoA_A.setEnabled(self.__enableWingFunct)
        
        procLines_A = QAction(_('Lines'), self)
        procLines_A.setStatusTip(_('Edit Lines data'))
        procLines_A.triggered.connect(self.procLinesEdit)
        procLines_A.setEnabled(self.__enableWingFunct)
        
        procBrakes_A = QAction(_('Brakes'), self)
        procBrakes_A.setStatusTip(_('Edit Brake lines data'))
        procBrakes_A.triggered.connect(self.procBrakesEdit)
        procBrakes_A.setEnabled(self.__enableWingFunct)
        
        procRam_A = QAction(_('Ramifications length'), self)
        procRam_A.setStatusTip(_('Edit Ramification data'))
        procRam_A.triggered.connect(self.procRamEdit)
        procRam_A.setEnabled(self.__enableWingFunct)
        
        procHvvHRibs_A = QAction(_('HV and VH ribs'), self)
        procHvvHRibs_A.setStatusTip(_('Edit HV/ VH ribs data'))
        procHvvHRibs_A.triggered.connect(self.procHvVhEdit)
        procHvvHRibs_A.setEnabled(self.__enableWingFunct)
        
        procEditExtrCols_A = QAction(_('Extrados colors'), self)
        procEditExtrCols_A.setEnabled(False)
        
        procEditIntrCols_A = QAction(_('Intrados colors'), self)
        procEditIntrCols_A.setEnabled(False)
        
        procEditAddRibPts_A = QAction(_('Additional rib points'), self)
        procEditAddRibPts_A.setEnabled(False)
        
        procEditElLinesCorr_A = QAction(_('Elastic lines correction'), self)
        procEditElLinesCorr_A.setEnabled(False)
        
        procEditJoncsDes_A = QAction(_('Joncs definitions'), self)
        procEditJoncsDes_A.setEnabled(False)
        
        procEditNoseMylars_A = QAction(_('Nose mylars'), self)
        procEditNoseMylars_A.setEnabled(False)
        
        procEditTabReinf_A = QAction(_('Tab reinforcements'), self)
        procEditTabReinf_A.setEnabled(False)
        
        procEditGlueVents_A = QAction(_('Glue vents'), self)
        procEditGlueVents_A.setEnabled(False)
        
        procEditSpecWingt_A = QAction(_('Special wingtip'), self)
        procEditSpecWingt_A.setEnabled(False)
        
        procEditSpeedTrimS_A = QAction(_('Speed/ Trimmer study'), self)
        procEditSpeedTrimS_A.setEnabled(False)
        
        procEdit3DShaping_A = QAction(_('3D shaping'), self)
        procEdit3DShaping_A.setEnabled(False)
        
        procEditThiknessMod_A = QAction(_('Thikness modification'), self)
        procEditThiknessMod_A.setEnabled(False)
        
        procEditNewSkinTens_A = QAction(_('New skin tension'), self)
        procEditNewSkinTens_A.setEnabled(False)
        
        procRunAct = QAction(_('Run Processor'), self)
        procRunAct.setStatusTip(_('run_Processor_des'))
        procRunAct.triggered.connect(self.preProcRun)
        procRunAct.setEnabled(False)
        
        # Build the menu
        procMenu = self.mainMenu.addMenu(_('Processor'))
        procMenu.addAction(procOpenFile_A) 
        procMenu.addAction(procSave_A)
        procMenu.addAction(procSaveAs_A)
        procMenu.addSeparator()
        procMenu.addAction(procBasicData_A)
        procMenu.addAction(procGeometry_A)
        procMenu.addAction(procAirfoils_A)
        procMenu.addAction(procAnchPoints_A)
        procMenu.addAction(procRibHoles_A)
        
        skinTensMenu = QMenu(_('Skin Tension'),self)
        skinTensMenu.addAction(procSkinTension_A)
        skinTensMenu.addAction(procEditNewSkinTens_A)
        procMenu.addMenu(skinTensMenu)
        
        procMenu.addAction(procGenAoA_A)
        procMenu.addAction(procLines_A)
        procMenu.addAction(procBrakes_A)
        procMenu.addAction(procRam_A)
        procMenu.addAction(procHvvHRibs_A)
        
        colsMenu = QMenu(_('Colors'),self)
        colsMenu.addAction(procEditExtrCols_A)
        colsMenu.addAction(procEditIntrCols_A)
        procMenu.addMenu(colsMenu)
        
        procMenu.addAction(procEditAddRibPts_A)
        procMenu.addAction(procEditElLinesCorr_A)
        procMenu.addAction(procEditJoncsDes_A)
        procMenu.addAction(procEditNoseMylars_A)
        procMenu.addAction(procEditTabReinf_A)
        procMenu.addAction(procEditGlueVents_A)
        procMenu.addAction(procEditSpecWingt_A)
        procMenu.addAction(procEditSpeedTrimS_A)
        procMenu.addAction(procEdit3DShaping_A)
        procMenu.addAction(procEditThiknessMod_A)
         
        procMenu.addSeparator()
        procMenu.addAction(procRunAct)
        
    def procOpenFile(self):
        '''
        :method: Called if the user selects *Processor* -> *Open Processor File*
        '''
        self.pm.openFile()
        
        
    def procSaveFile(self):
        '''
        :method: Called if the user selects *Processor* -> *Save Processor File*
        '''
        self.ps.saveFile()
        
    def procSaveFileAs(self):
        '''
        :method: Called if the user selects *Processor* -> *Save Processor File As..*
        '''
        self.ps.saveFileAs()
    
    def procBasicDataEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Basic data*
        '''
        if self.dws.windowExists('ProcBasicData') == False:
            self.basicDataW = ProcBasicData()
            self.dws.registerWindow('ProcBasicData')
            self.mdi.addSubWindow(self.basicDataW)
        self.basicDataW.show()

    def procGeometryEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Geometry*
        '''
        if self.dws.windowExists('ProcGeometry') == False:
            self.geometryW = ProcGeometry()
            self.dws.registerWindow('ProcGeometry')
            self.mdi.addSubWindow(self.geometryW)
        self.geometryW.show()

    def procAirfoilsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Airfoils*
        '''
        if self.dws.windowExists('ProcAirfoils') == False:
            self.airfoilsW = ProcAirfoils()
            self.dws.registerWindow('ProcAirfoils')
            self.mdi.addSubWindow(self.airfoilsW)
        self.airfoilsW.show()
        
    def procAnchorPointsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Anchor Points*
        '''
        if self.dws.windowExists('ProcAnchorPoints') == False:
            self.anchPointsW = ProcAnchorPoints()
            self.dws.registerWindow('ProcAirfoils')
            self.mdi.addSubWindow(self.anchPointsW)
        self.anchPointsW.show()

    def procRibHolesEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Airfoils*
        '''
        if self.dws.windowExists('RibHoles') == False:
            self.ribHolesW = RibHoles()
            self.dws.registerWindow('RibHoles')
            self.mdi.addSubWindow(self.ribHolesW)
        self.ribHolesW.show()
    
    def procSkinTensionEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Skin Tension*
        '''
        if self.dws.windowExists('SkinTension') == False:
            self.skinTensionW = ProcSkinTension()
            self.dws.registerWindow('SkinTension')
            self.mdi.addSubWindow(self.skinTensionW)
        self.skinTensionW.show()
        
    def procGlobalAoAEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Global AoA*
        '''
        if self.dws.windowExists('GlobalAoA') == False:
            self.globAoAW = GlobalAoA()
            self.dws.registerWindow('GlobalAoA')
            self.mdi.addSubWindow(self.globAoAW)
        self.globAoAW.show()
        
    def procLinesEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Lines*
        '''
        if self.dws.windowExists('Lines') == False:
            self.lines_W = Lines()
            self.dws.registerWindow('Lines')
            self.mdi.addSubWindow(self.lines_W)
        self.lines_W.show() 
        
    def procBrakesEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Brakes*
        '''
        if self.dws.windowExists('Brakes') == False:
            self.brakes_W = Brakes()
            self.dws.registerWindow('Brakes')
            self.mdi.addSubWindow(self.brakes_W)
        self.brakes_W.show()

    def procRamEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Ramification*
        '''
        if self.dws.windowExists('Ramification') == False:
            self.ramif_W = Ramification()
            self.dws.registerWindow('Ramification')
            self.mdi.addSubWindow(self.ramif_W)
        self.ramif_W.show()

    def procHvVhEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *HV VH Ribs*
        '''
        if self.dws.windowExists('HvVhRibs') == False:
            self.hVvH_W = HvVhRibs()
            self.dws.registerWindow('HvVhRibs')
            self.mdi.addSubWindow(self.hVvH_W)
        self.hVvH_W.show()
        
    def procRun(self):
        '''
        :method: Called if the user selects *Processor* -> *Run Processor*
        '''
        logging.debug(self.__className + '.preProcRun')
        
        # Save current file into processor directory
        self.pps.writeFile(True)
        
        # Open the window for the user info
        if self.dws.windowExists('ProcessorOutput') == False:
            self.procOutW = ProcessorOutput()
            self.dws.registerWindow('ProcessorOutput')
            self.mdi.addSubWindow(self.procOutW)
        self.procOutW.show()
        
        # Finally run the processor
        preProcRunner = ProcRunner(self.procOutW)
        preProcRunner.runPreProc()
    
    def buildPlanMenu(self):
        '''
        :method: Builds the complete Plan menu
        '''  
        # Define the actions
        
        planSeewingAll_A = QAction(_('Seewing Allowance'), self)
        planSeewingAll_A.setStatusTip(_('Edit Seewing allowances'))
        planSeewingAll_A.triggered.connect(self.planSeewingAllEdit)
        planSeewingAll_A.setEnabled(self.__enableWingFunct)
        
        planMarks_A = QAction(_('Marks'), self)
        planMarks_A.setStatusTip(_('Edit the Marks parameters'))
        planMarks_A.triggered.connect(self.planMarksEdit)
        planMarks_A.setEnabled(self.__enableWingFunct)

        
        procEditDxfLayers_A = QAction(_('DXF Layer names'), self)
        procEditDxfLayers_A.setEnabled(False)
        
        procEditMarksT_A = QAction(_('Marks types'), self)
        procEditMarksT_A.setEnabled(False)

        
        procEditGen2D_A = QAction(_('2D DXF options'), self)
        procEditGen2D_A.setEnabled(False)
        
        procEditGen3D_A = QAction(_('3D DXF options'), self)
        procEditGen3D_A.setEnabled(False)
        
        # Build the menu
        planMenu = self.mainMenu.addMenu(_('Plan'))
        planMenu.addAction(planSeewingAll_A)
        planMenu.addAction(planMarks_A)
        planMenu.addAction(procEditDxfLayers_A)
        planMenu.addAction(procEditMarksT_A)
        planMenu.addAction(procEditGen2D_A)
        planMenu.addAction(procEditGen3D_A)
    
    def planSeewingAllEdit(self):
        '''
        :method: Called if the user selects *Plan* -> *Sewing allowances*
        '''
        if self.dws.windowExists('SeewingAllowances') == False:
            self.seewingAllW = SeewingAllowances()
            self.dws.registerWindow('SeewingAllowances')
            self.mdi.addSubWindow(self.seewingAllW)
        self.seewingAllW.show()
    
    def planMarksEdit(self):
        '''
        :method: Called if the user selects *Plan* -> *Marks*
        '''
        if self.dws.windowExists('Marks') == False:
            self.marksW = Marks()
            self.dws.registerWindow('Marks')
            self.mdi.addSubWindow(self.marksW)
        self.marksW.show()   

    def buildViewMenu(self):
        '''
        :method: Builds the View menu
        '''
        viewWingAct = QAction(_('Wing'), self)
        viewWingAct.setStatusTip(_('Shows the outline of the wing'))
        viewWingAct.triggered.connect(self.viewWing)
        viewWingAct.setEnabled(self.__enableWingFunct)
        
        # Define the actions
        viewCascadeAct = QAction(_('Cascade'), self)
        viewCascadeAct.setStatusTip(_('Cascade all windows'))
        viewCascadeAct.triggered.connect(self.viewCascade)
        #
        viewTileAct = QAction(_('Tile'), self)
        viewTileAct.setStatusTip(_('Tile all windows'))
        viewTileAct.triggered.connect(self.viewTile)
        # Build the menu
        viewMenu = self.mainMenu.addMenu(_('View'))
        viewMenu.addAction(viewWingAct)
        viewMenu.addSeparator()
        viewMenu.addAction(viewCascadeAct)
        viewMenu.addAction(viewTileAct)
    
    def viewWing(self): 
        '''
        :method: Called if the user selects *View* -> *Show Pre-Processor outline*
        '''
        if self.dws.windowExists('WingViewer') == False:
            self.wingViewer_W = WingViewer()
            self.dws.registerWindow('WingViewer')
            self.mdi.addSubWindow(self.wingViewer_W)

        self.wingViewer_W.show()
    
    def viewCascade(self):
        '''
        :method: Called if the user selects *View* -> *Cascade*
        '''
        self.mdi.cascadeSubWindows()
        
    def viewTile(self):
        '''
        :method: Called if the user selects *View* -> *Tile*
        '''
        self.mdi.tileSubWindows()   
        
    def buildSetupMenu(self):
        '''
        :method: Builds the Setup menu
        '''
        #Define actions
        setupLangEnAct = QAction("English", self)
        setupLangEnAct.setStatusTip('Switches the display language to englisch')
        setupLangEnAct.triggered.connect(self.setupLangEn)
        
        setupLangDeAct = QAction("Deutsch", self)
        setupLangDeAct.setStatusTip('Wechselt zur deutschen Anzeige')
        setupLangDeAct.triggered.connect(self.setupLangDe)
        
        setupPreProcAct = QAction(_('Setup Pre-Processor'), self)
        setupPreProcAct.setStatusTip(_('setup_preProc_location'))
        setupPreProcAct.triggered.connect(self.setupPreProcLocation)
        
        # add actions
        setupMenu = self.mainMenu.addMenu(_('Setup'))
        setupLangMenu = setupMenu.addMenu(_('Language'))
        setupLangMenu.addAction(setupLangEnAct)
        setupLangMenu.addAction(setupLangDeAct)
        setupMenu.addSeparator()
        setupMenu.addAction(setupPreProcAct)
    
    def setupLangDe(self):
        '''
        :method: Called if the user selects *Setup* *Language* -> *German*
        '''
        config = ConfigReader()
        config.setLanguage("de")
        self.displayRestartMsg()
        
    def setupLangEn(self):
        '''
        :method: Called if the user selects *Setup* *Language* -> *English*
        '''
        config = ConfigReader()
        config.setLanguage("en")
        self.displayRestartMsg()  
        
    def displayRestartMsg(self):
        '''
        :method: Displays a message to the user to restart the application after switching the language
        '''
        msg = QMessageBox()
        
        msg.setWindowTitle(_("Switching language"))
        msg.setIcon(QMessageBox.Information)
        msg.setText(_("Please restart the application."))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setFixedWidth(300)
        msg.exec_()  
        
    def setupPreProcLocation(self): 
        '''
        :method: Asks the user for the location where the Pre-Processor is saved
        '''
        logging.debug(self.__className + '.setupPreProcLocation')

        # Do platform specific if here as the PreProx extensions are different
        if platform.system() == "Windows":
            fileName = QFileDialog.getOpenFileName(
                            None,
                            _('Select Pre_Processor'),
                            "",
                            "Executable (*.exe)")
        elif platform.system() == "Linux":
            fileName = QFileDialog.getOpenFileName(
                            None,
                            _('Select Pre_Processor'),
                            "",
                            "Compiled Fortran (*.o *.out)")
        else:
            logging.error("Sorry, your operating system is not supported yet")
            return

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the dialog  
            # an empty tuple is retured
            # Write the info to the config reader
            logging.debug(self.__className + '.setupPreProcLocation Path and Name ' + fileName[0])
            
            config = ConfigReader()
            config.setPreProcPathName(fileName[0])

    def buildHelpMenu(self):
        '''
        :method: Builds the Help Menu
        '''
        helpAboutAct = QAction(_('About'), self)
        helpAboutAct.setStatusTip(_('Short info about the program'))
        helpAboutAct.triggered.connect(self.helpAbout)
        
        # Build the menu
        fileMenu = self.mainMenu.addMenu(_('Help'))
        fileMenu.addAction(helpAboutAct)
        
    def helpAbout(self):
        '''
        :method: Opens the Help About window.
        '''
        if self.dws.windowExists('HelpAbout') == False:
            self.helpAboutW = HelpAbout()
            self.dws.registerWindow('HelpAbout')
            self.mdi.addSubWindow(self.helpAboutW)
        self.helpAboutW.show()
        
        
def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
