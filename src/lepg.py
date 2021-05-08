'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import os
from os import path
import webbrowser

import gettext
import logging.config
import sys
from packaging import version

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QMessageBox, QMenu

from __init__ import __version__
from VersionCheck.VersionCheck import VersionCheck 

from ConfigReader.ConfigReader import ConfigReader
from DataStores.PreProcessorModel import PreProcessorModel
from DataStores.ProcessorModel import ProcessorModel

from Windows.DataStatusOverview import DataStatusOverview
from Windows.PreProcData import PreProcData
from Windows.WingViewer import WingViewer
from Windows.BasicData import BasicData
from Windows.Geometry import Geometry
from Windows.Airfoils import Airfoils
from Windows.RibHoles import RibHoles
from Windows.HelpAbout import HelpAbout
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from Processors.ProcRunner import ProcRunner
from Windows.ProcessorOutput import ProcessorOutput
from Windows.AnchorPoints import AnchorPoints
from Windows.SkinTension import SkinTension
from Windows.SeewingAllowances import SeewingAllowances
from Windows.Marks import Marks
from Windows.GlobalAoA import GlobalAoA
from Windows.Lines import Lines
from Windows.Brakes import Brakes
from Windows.Ramification import Ramification
from Windows.HvVhRibs import HvVhRibs
from Windows.ExtradColors import ExtradColors
from Windows.IntradColors import IntradColors
from Windows.AddRibPoints import AddRibPoints
from Windows.ElasticLinesCorr import ElasticLinesCorr
from Windows.DxfLayerNames import DxfLayerNames
from Windows.MarksTypes import MarksTypes
from Windows.JoncsDefinition import JoncsDefinition
from Windows.NoseMylars import NoseMylars
from Windows.TwoDDxf import TwoDDxfModel
from Windows.ThreeDDxf import ThreeDDxfModel
from Windows.GlueVent import GlueVent
from Windows.SpecWingTip import SpecWingTip
from Windows.CalageVar import CalageVar
from Windows.ThreeDShaping import ThreeDShaping
from Windows.AirfoilThickness import AirfoilThickness
from Windows.NewSkinTension import NewSkinTension
from Windows.PreProcCellsDistribution import PreProcCellsDistribution
from Windows.SetupProcessors import SetupProcessors
from Windows.SetupUpdateChecking import SetupUpdateChecking


class MainWindow(QMainWindow):
    '''
    :class: Creates the main window of the application
    '''
    
    __className = 'MainWindow'
    '''
    :attr: Does help to indicate the source of the log messages
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
        
        #self.pps = PreProcessorStore()
        self.ppm = PreProcessorModel()
        self.pm = ProcessorModel()
        
        self.dws = DataWindowStatus()
        
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("lepg-py %s" %(__version__))
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
        
        # VersionCheck
        if config.getCheckForUpdates() == 'yes':
            versChk = VersionCheck()
            versChk.setBranch(config.getTrackBranch())
            
            if versChk.remoteVersionFound():
                remoteVersion = versChk.getRemoteVersion()
                logging.debug(self.__className + ' Remote Version:   '+remoteVersion+'\n')
                logging.debug(self.__className + ' Current Version:  '+__version__+'\n')
                
                if version.parse(remoteVersion) > version.parse(__version__):
                    msgBox = QMessageBox()
                    msgBox.setTextFormat(Qt.RichText)
                    msgBox.setWindowTitle(_('Newer version found'))
                    msgBox.setText(_('Current Version: ')+str(__version__)+('<br>')+\
                                      _('Version on remote: ')+str(remoteVersion)+('<br>')+\
                                      _('Maybe you should consider an update from')+('<br>')+\
                                      ('<a href="https://github.com/stefanino-ch/lepg-py/tree/stable/distribution">Github.com</a>')+('<br>')+('<br>')+\
                                      _('More info about the different versions you will find in the <br>online help: Help-> Online Help')+('<br>')+('<br>')+
                                      _('Or in Settings-> Update checking') )
                    #msgBox.setText(_('<a href="https://github.com">link text</a>'))
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()
            else:
                logging.error(self.__className + 'Unable to get the update information.\n')
                logging.error(self.__className + 'Error information: '+versChk.getErrorInfo()+'\n')
        else: 
            logging.debug(self.__className + ' Update check disabled in config file.\n')
        
   
    def buildFileMenu(self):
        '''
        :method: Builds the complete file menu
        '''
        # Define the actions
        fileDataStatusAct = QAction(_('Show Data Status'), self)
        fileDataStatusAct.setStatusTip(_('Provides an overview about what data has (not) been saved'))
        fileDataStatusAct.triggered.connect(self.fileDataStatus)
        
        fileRestartAct = QAction(_('Restart'), self)
        fileRestartAct.setStatusTip(_('Restart the app'))
        fileRestartAct.triggered.connect(self.fileRestart)
        
        
        fileExitAct = QAction(_('Exit'), self)
        fileExitAct.setStatusTip(_('Leave the app'))
        fileExitAct.triggered.connect(self.fileExit)

        # Build the menu
        fileMenu = self.mainMenu.addMenu(_('File'))
        fileMenu.addAction(fileDataStatusAct)
        fileMenu.addSeparator()
        fileMenu.addAction(fileRestartAct)
        fileMenu.addSeparator()
        fileMenu.addAction(fileExitAct)
    
    def fileDataStatus(self):
        '''
        :method: Opens the File Data Status overview window.
        '''
        if self.dws.windowExists('DataStatusOverview') == False:
            self.fileDataStatusW = DataStatusOverview()
            self.dws.registerWindow('DataStatusOverview')
            self.mdi.addSubWindow(self.fileDataStatusW)
        self.fileDataStatusW.show()
        
    def fileRestart(self):
        ''' 
        :method: Restarts the application.
            Thanks to: https://blog.petrzemek.net/2014/03/23/restarting-a-python-script-within-itself/
        '''
        os.execv(sys.executable, ['python'] + sys.argv)
    
    def fileExit(self):
        ''' 
        :method: Does all the work to close properly the application. 
        '''
        logging.debug(self.__className + '.fileExit')
        sys.exit()  
    
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
        
        preProcEditAct = QAction(_('Name, LE, TE, Vault'), self)
        preProcEditAct.setStatusTip(_('edit_preProc_data_description'))
        preProcEditAct.triggered.connect(self.preProcEdit)
        
        preProcCellsDistrAct = QAction(_('Cells distribution'), self)
        preProcCellsDistrAct.setStatusTip(_('edit_preProc_cellsDistr_description'))
        preProcCellsDistrAct.triggered.connect(self.preProcCellsDistrEdit)
        
        preProcRunAct = QAction(_('Run Pre-Processor'), self)
        preProcRunAct.setStatusTip(_('run_preProc_des'))
        preProcRunAct.triggered.connect(self.preProcRun)
        
        # Build the menu
        preProcMenu = self.mainMenu.addMenu(_('Pre Processor'))
        preProcMenu.addAction(preProcOpenFileAct)
        preProcMenu.addAction(preProcSaveAct)
        preProcMenu.addAction(preProcSaveAsAct)
        preProcMenu.addSeparator()
        preProcMenu.addAction(preProcEditAct)
        preProcMenu.addAction(preProcCellsDistrAct)
        preProcMenu.addSeparator()
        preProcMenu.addAction(preProcRunAct)
        
    def preProcOpenFile(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Open PreProc File*
        ''' 
        self.ppm.openFile()
        
    def preProcSaveFile(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Save PreProc File*
        '''
        self.ppm.saveFile()
        
    def preProcSaveFileAs(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Save PreProc File As ..*
        '''
        self.ppm.saveFileAs()
        
    def preProcEdit(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Name, LE, TE, Vault*
        '''
        if self.dws.windowExists('PreProcDataEdit') == False:
            self.preProcEditW = PreProcData()
            self.dws.registerWindow('PreProcDataEdit')
            self.mdi.addSubWindow(self.preProcEditW)
        self.preProcEditW.show() 
        
    def preProcCellsDistrEdit(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Cells distribution*
        '''
        if self.dws.windowExists('PreProcCellsDistribution') == False:
            self.preProcCellsDistrW = PreProcCellsDistribution()
            self.dws.registerWindow('PreProcCellsDistribution')
            self.mdi.addSubWindow(self.preProcCellsDistrW)
        self.preProcCellsDistrW.show()
        
    def preProcRun(self):
        '''
        :method: Called if the user selects *Pre Processor* -> *Run Pre-Processor*
        '''
        logging.debug(self.__className + '.preProcRun')
        
        # Save current file into processor directory
        self.ppm.writeFile(True)
        
        # Open the window for the user info
        if self.dws.windowExists('ProcessorOutput') == False:
            self.procOutW = ProcessorOutput()
            self.dws.registerWindow('ProcessorOutput')
            self.mdi.addSubWindow(self.procOutW)
        self.procOutW.show()
        
        # Finally run the processor
        preProcRunner = ProcRunner(self.procOutW)
        
        if preProcRunner.preProcConfigured() == False:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('Potentially missing configuration!'))
            msgBox.setText(_('For a successful pre-processor run you must configure\nthe pre-processor in Setup->Both Processors.'))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            preProcRunner.runPreProc()

    def buildProcMenu(self):
        '''
        :method: Builds the complete Processor menu
        '''  
        # Define the actions
        preProcImport_A = QAction(_('Import Pre-Proc output file'), self)
        preProcImport_A.setStatusTip(_('import-pre-proc_file_desc'))
        preProcImport_A.triggered.connect(self.preProcImport)
        
        procOpenFile_A = QAction(_('Open Processor File'), self)
        procOpenFile_A.setStatusTip(_('open_Proc_file_desc'))
        procOpenFile_A.triggered.connect(self.procOpenFile)
        
        procSave_A = QAction(_('Save Processor File'), self)
        procSave_A.setStatusTip(_('save_proc_file_desc'))
        procSave_A.triggered.connect(self.procSaveFile)
        
        procSaveAs_A = QAction(_('Save Processor File As ..'), self)
        procSaveAs_A.setStatusTip(_('save_proc_file_as_desc'))
        procSaveAs_A.triggered.connect(self.procSaveFileAs)
        
        procBasicData_A = QAction(_('Basic data'), self)
        procBasicData_A.setStatusTip(_('Editing the wing basics'))
        procBasicData_A.triggered.connect(self.procBasicDataEdit)
        
        procGeometry_A = QAction(_('Geometry'), self)
        procGeometry_A.setStatusTip(_('Edit wing geometry'))
        procGeometry_A.triggered.connect(self.procGeometryEdit)
        
        procAirfoils_A = QAction(_('Airfoils'), self)
        procAirfoils_A.setStatusTip(_('Edit airfoils geometry'))
        procAirfoils_A.triggered.connect(self.procAirfoilsEdit)
        
        procAnchPoints_A = QAction(_('Anchor Points'), self)
        procAnchPoints_A.setStatusTip(_('Edit Anchor points data'))
        procAnchPoints_A.triggered.connect(self.procAnchorPointsEdit)
        
        procRibHoles_A = QAction(_('Rib Holes'), self)
        procRibHoles_A.setStatusTip(_('Edit rib holes (Rib lightening) data'))
        procRibHoles_A.triggered.connect(self.procRibHolesEdit)
        
        procSkinTension_A = QAction(_('Skin Tension'), self)
        procSkinTension_A.setStatusTip(_('Edit Skin tension data'))
        procSkinTension_A.triggered.connect(self.procSkinTensionEdit)
        
        procGenAoA_A = QAction(_('Estimated general AoA'), self)
        procGenAoA_A.setStatusTip(_('Edit global AoA data'))
        procGenAoA_A.triggered.connect(self.procGlobalAoAEdit)
        
        procLines_A = QAction(_('Lines'), self)
        procLines_A.setStatusTip(_('Edit Lines data'))
        procLines_A.triggered.connect(self.procLinesEdit)
        
        procBrakes_A = QAction(_('Brakes'), self)
        procBrakes_A.setStatusTip(_('Edit Brake lines data'))
        procBrakes_A.triggered.connect(self.procBrakesEdit)
        
        procRam_A = QAction(_('Ramifications length'), self)
        procRam_A.setStatusTip(_('Edit Ramification data'))
        procRam_A.triggered.connect(self.procRamEdit)
        
        procHvvHRibs_A = QAction(_('HV and VH ribs'), self)
        procHvvHRibs_A.setStatusTip(_('Edit HV/ VH ribs data'))
        procHvvHRibs_A.triggered.connect(self.procHvVhEdit)
        
        procExtradColors_A = QAction(_('Extrados colors'), self)
        procExtradColors_A.setStatusTip(_('Edit extrados colors data'))
        procExtradColors_A.triggered.connect(self.procExtradColorsEdit)
        
        procIntradColors_A = QAction(_('Intrados colors'), self)
        procIntradColors_A.setStatusTip(_('Edit intrados colors data'))
        procIntradColors_A.triggered.connect(self.procIntradColorsEdit)
        
        procAddRibPts_A = QAction(_('Additional rib points'), self)
        procAddRibPts_A.setStatusTip(_('Edit additional rib points data'))
        procAddRibPts_A.triggered.connect(self.procAddRibPtsEdit)
        
        procElLinesCorr_A = QAction(_('Elastic lines correction'), self)
        procElLinesCorr_A.setStatusTip(_('Edit Elastic lines correction data'))
        procElLinesCorr_A.triggered.connect(self.procElLinesCorrEdit)
        
        procJoncsDef_A = QAction(_('Joncs definitions'), self)
        procJoncsDef_A.setStatusTip(_('Edit Joncs (Nylon rods) definition'))
        procJoncsDef_A.triggered.connect(self.procJoncsDefEdit)
        
        procNoseMylars_A = QAction(_('Nose Mylars'), self)
        procNoseMylars_A.setStatusTip(_('Edit Nose mylars definition'))
        procNoseMylars_A.triggered.connect(self.procNoseMylarsEdit)
        
        procEditTabReinf_A = QAction(_('Tab reinforcements'), self)
        procEditTabReinf_A.setEnabled(False)
        
        procGlueVents_A = QAction(_('Glue vents'), self)
        procGlueVents_A.setStatusTip(_('Edit Glue vent definitions'))
        procGlueVents_A.triggered.connect(self.procGlueVentEdit)
        
        procSpecWingTip_A = QAction(_('Special wingtip'), self)
        procSpecWingTip_A.setStatusTip(_('Edit Special wing tip definitions'))
        procSpecWingTip_A.triggered.connect(self.procSpecWingtTipEdit)
        
        procCalageVar_A = QAction(_('Calage variation'), self)
        procCalageVar_A.setStatusTip(_('Edit parameters for calage variation study'))
        procCalageVar_A.triggered.connect(self.procCalageVarEdit)
        
        procThreeDShaping_A = QAction(_('3D shaping'), self)
        procThreeDShaping_A.setStatusTip(_('Edit parameters 3D shaping'))
        procThreeDShaping_A.triggered.connect(self.procThreeDShapingEdit)
        
        procAirfoilThick_A = QAction(_('Airfoil thickness'), self)
        procAirfoilThick_A.setStatusTip(_('Edit parameters for airfoil thickness'))
        procAirfoilThick_A.triggered.connect(self.procAirfoilThickEdit)
        
        procNewSkinTens_A = QAction(_('New skin tension'), self)
        procNewSkinTens_A.setStatusTip(_('Edit parameters for new skin tension'))
        procNewSkinTens_A.triggered.connect(self.procNewSkinTensionEdit)
        
        procRunAct = QAction(_('Run Processor'), self)
        procRunAct.setStatusTip(_('run_Processor_des'))
        procRunAct.triggered.connect(self.procRun)
        
        # Build the menu
        procMenu = self.mainMenu.addMenu(_('Processor'))
        procMenu.addAction(preProcImport_A)
        procMenu.addSeparator()
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
        skinTensMenu.addAction(procNewSkinTens_A)
        procMenu.addMenu(skinTensMenu)
        
        procMenu.addAction(procGenAoA_A)
        procMenu.addAction(procLines_A)
        procMenu.addAction(procBrakes_A)
        procMenu.addAction(procRam_A)
        procMenu.addAction(procHvvHRibs_A)
        
        colsMenu = QMenu(_('Colors'),self)
        colsMenu.addAction(procExtradColors_A)
        colsMenu.addAction(procIntradColors_A)
        procMenu.addMenu(colsMenu)
        
        procMenu.addAction(procAddRibPts_A)
        procMenu.addAction(procElLinesCorr_A)
        procMenu.addAction(procJoncsDef_A)
        procMenu.addAction(procNoseMylars_A)
        procMenu.addAction(procEditTabReinf_A)
        procMenu.addAction(procGlueVents_A)
        procMenu.addAction(procSpecWingTip_A)
        procMenu.addAction(procCalageVar_A)
        procMenu.addAction(procThreeDShaping_A)
        procMenu.addAction(procAirfoilThick_A)
         
        procMenu.addSeparator()
        procMenu.addAction(procRunAct)
        
    def preProcImport(self):
        '''
        :method: Called if the user selects *Processor* -> *Import Pre-Proc File*
        '''
        self.pm.importPreProcFile()
        
    def procOpenFile(self):
        '''
        :method: Called if the user selects *Processor* -> *Open Processor File*
        '''
        self.pm.openFile()
        
        
    def procSaveFile(self):
        '''
        :method: Called if the user selects *Processor* -> *Save Processor File*
        '''
        self.pm.saveFile()
        
    def procSaveFileAs(self):
        '''
        :method: Called if the user selects *Processor* -> *Save Processor File As..*
        '''
        self.pm.saveFileAs()
    
    def procBasicDataEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Basic data*
        '''
        if self.dws.windowExists('ProcBasicData') == False:
            self.basicDataW = BasicData()
            self.dws.registerWindow('ProcBasicData')
            self.mdi.addSubWindow(self.basicDataW)
        self.basicDataW.show()

    def procGeometryEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Geometry*
        '''
        if self.dws.windowExists('Geometry') == False:
            self.geometryW = Geometry()
            self.dws.registerWindow('Geometry')
            self.mdi.addSubWindow(self.geometryW)
        self.geometryW.show()

    def procAirfoilsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Airfoils*
        '''
        if self.dws.windowExists('Airfoils') == False:
            self.airfoilsW = Airfoils()
            self.dws.registerWindow('Airfoils')
            self.mdi.addSubWindow(self.airfoilsW)
        self.airfoilsW.show()
        
    def procAnchorPointsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Anchor Points*
        '''
        if self.dws.windowExists('AnchorPoints') == False:
            self.anchPointsW = AnchorPoints()
            self.dws.registerWindow('AnchorPoints')
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
            self.skinTensionW = SkinTension()
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

    def procExtradColorsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Extrados colors*
        '''
        if self.dws.windowExists('ExtradosColors') == False:
            self.extradColors_W = ExtradColors()
            self.dws.registerWindow('ExtradosColors')
            self.mdi.addSubWindow(self.extradColors_W)
        self.extradColors_W.show()

    def procIntradColorsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Intrados colors*
        '''
        if self.dws.windowExists('IntradosColors') == False:
            self.intradColors_W = IntradColors()
            self.dws.registerWindow('IntradosColors')
            self.mdi.addSubWindow(self.intradColors_W)
        self.intradColors_W.show()

    def procAddRibPtsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Additional rib points*
        '''
        if self.dws.windowExists('AddRibPoints') == False:
            self.addRibPts_W = AddRibPoints()
            self.dws.registerWindow('AddRibPoints')
            self.mdi.addSubWindow(self.addRibPts_W)
        self.addRibPts_W.show()

    def procElLinesCorrEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Elastic lines correction*
        '''
        if self.dws.windowExists('ElasticLinesCorr') == False:
            self.elLinesCorr_W = ElasticLinesCorr()
            self.dws.registerWindow('ElasticLinesCorr')
            self.mdi.addSubWindow(self.elLinesCorr_W)
        self.elLinesCorr_W.show()

    def procJoncsDefEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Joncs definition*
        '''
        if self.dws.windowExists('JoncsDef') == False:
            self.joncsDef_W = JoncsDefinition()
            self.dws.registerWindow('JoncsDef')
            self.mdi.addSubWindow(self.joncsDef_W)
        self.joncsDef_W.show()

    def procNoseMylarsEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Nose mylars*
        '''
        if self.dws.windowExists('NoseMylars') == False:
            self.noseMylars_W = NoseMylars()
            self.dws.registerWindow('NoseMylars')
            self.mdi.addSubWindow(self.noseMylars_W)
        self.noseMylars_W.show()

    def procGlueVentEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Glue vents*
        '''
        if self.dws.windowExists('GlueVent') == False:
            self.GlueVent_W = GlueVent()
            self.dws.registerWindow('GlueVent')
            self.mdi.addSubWindow(self.GlueVent_W)
        self.GlueVent_W.show()

    def procSpecWingtTipEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Special wing tip*
        '''
        if self.dws.windowExists('SpecWingTip') == False:
            self.SpecWingTip_W = SpecWingTip()
            self.dws.registerWindow('SpecWingTip')
            self.mdi.addSubWindow(self.SpecWingTip_W)
        self.SpecWingTip_W.show()

    def procCalageVarEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Calage variation*
        '''
        if self.dws.windowExists('CalageVar') == False:
            self.calageVar_W = CalageVar()
            self.dws.registerWindow('CalageVar')
            self.mdi.addSubWindow(self.calageVar_W)
        self.calageVar_W.show()

    def procThreeDShapingEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *3D Shapung*
        '''
        if self.dws.windowExists('ThreeDShaping') == False:
            self.threeDSh_W = ThreeDShaping()
            self.dws.registerWindow('ThreeDShaping')
            self.mdi.addSubWindow(self.threeDSh_W)
        self.threeDSh_W.show()

    def procAirfoilThickEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *Airfoil thickness*
        '''
        if self.dws.windowExists('AirfoilThickness') == False:
            self.airfThick_W = AirfoilThickness()
            self.dws.registerWindow('AirfoilThickness')
            self.mdi.addSubWindow(self.airfThick_W)
        self.airfThick_W.show()
        
    def procNewSkinTensionEdit(self):
        '''
        :method: Called if the user selects *Processor* -> *New skin tension*
        '''
        if self.dws.windowExists('NewSkinTension') == False:
            self.newSkinTens_W = NewSkinTension()
            self.dws.registerWindow('NewSkinTension')
            self.mdi.addSubWindow(self.newSkinTens_W)
        self.newSkinTens_W.show()
        
    def procRun(self):
        '''
        :method: Called if the user selects *Processor* -> *Run Processor*
        '''
        logging.debug(self.__className + '.procRun')
        
        # Save current file into processor directory
        self.pm.writeFile(True)

        # Open the window for the user info
        if self.dws.windowExists('ProcessorOutput') == False:
            self.procOutW = ProcessorOutput()
            self.dws.registerWindow('ProcessorOutput')
            self.mdi.addSubWindow(self.procOutW)
        self.procOutW.show()
        
        # Finally run the processor
        procRunner = ProcRunner(self.procOutW)
        
        if procRunner.procConfigured() == False:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(_('Potentially missing configuration!'))
            msgBox.setText(_('For a successful processor run you must configure\nthe processor in Setup->Both Processors.'))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            procRunner.runProc()
    
    def buildPlanMenu(self):
        '''
        :method: Builds the complete Plan menu
        '''  
        # Define the actions
        
        planSeewingAll_A = QAction(_('Seewing Allowance'), self)
        planSeewingAll_A.setStatusTip(_('Edit Seewing allowances'))
        planSeewingAll_A.triggered.connect(self.planSeewingAllEdit)
        
        planMarks_A = QAction(_('Marks'), self)
        planMarks_A.setStatusTip(_('Edit the Marks parameters'))
        planMarks_A.triggered.connect(self.planMarksEdit)
        
        planDxfLayerNames_A = QAction(_('DXF Layer names'), self)
        planDxfLayerNames_A.setStatusTip(_('Edit the names of the individual DXF layers'))
        planDxfLayerNames_A.triggered.connect(self.planDxFLayerNamesEdit)
        
        procMarksT_A = QAction(_('Marks types'), self)
        procMarksT_A.setStatusTip(_('Edit individual paramters for the marks on the plans'))
        procMarksT_A.triggered.connect(self.marksTypesEdit)
        
        procTwoDDxf_A = QAction(_('2D DXF options'), self)
        procTwoDDxf_A.setStatusTip(_('Edit for the 2D dxf plans'))
        procTwoDDxf_A.triggered.connect(self.twoDDxfEdit)
        
        procThreeDDxf_A = QAction(_('3D DXF options'), self)
        procThreeDDxf_A.setStatusTip(_('Edit for the 3D dxf plans'))
        procThreeDDxf_A.triggered.connect(self.threeDDxfEdit)
        
        # Build the menu
        planMenu = self.mainMenu.addMenu(_('Plan'))
        planMenu.addAction(planSeewingAll_A)
        planMenu.addAction(planMarks_A)
        planMenu.addAction(planDxfLayerNames_A)
        planMenu.addAction(procMarksT_A)
        planMenu.addAction(procTwoDDxf_A)
        planMenu.addAction(procThreeDDxf_A)
    
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
        
    def planDxFLayerNamesEdit(self):
        '''
        :method: Called if the user selects *Plan* -> *DXF Layer names*
        '''
        if self.dws.windowExists('DxfLayerNames') == False:
            self.dxfLayNamesW = DxfLayerNames()
            self.dws.registerWindow('DxfLayerNames')
            self.mdi.addSubWindow(self.dxfLayNamesW)
        self.dxfLayNamesW.show() 
    
    def marksTypesEdit(self):
        '''
        :method: Called if the user selects *Plan* -> Marks types*
        '''
        if self.dws.windowExists('MarksTypes') == False:
            self.marksTypesW = MarksTypes()
            self.dws.registerWindow('MarksTypes')
            self.mdi.addSubWindow(self.marksTypesW)
        self.marksTypesW.show() 
        
    def twoDDxfEdit(self):
        '''
        :method: Called if the user selects *Plan* -> 2D DFX *
        '''
        if self.dws.windowExists('TwoDDxf') == False:
            self.twoDDxfW = TwoDDxfModel()
            self.dws.registerWindow('TwoDDxf')
            self.mdi.addSubWindow(self.twoDDxfW)
        self.twoDDxfW.show()
 
    def threeDDxfEdit(self):
        '''
        :method: Called if the user selects *Plan* -> 3D DFX*
        '''
        if self.dws.windowExists('ThreeDDxf') == False:
            self.threeDDxfW = ThreeDDxfModel()
            self.dws.registerWindow('ThreeDDxf')
            self.mdi.addSubWindow(self.threeDDxfW)
        self.threeDDxfW.show()
 

    def buildViewMenu(self):
        '''
        :method: Builds the View menu
        '''
        viewWingAct = QAction(_('Wing'), self)
        viewWingAct.setStatusTip(_('Shows the outline of the wing'))
        viewWingAct.triggered.connect(self.viewWing)
        viewWingAct.setEnabled(False)
        
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
        
        setupProcAct = QAction(_('Both Processors'), self)
        setupProcAct.setStatusTip(_('Setup locations for both processors'))
        setupProcAct.triggered.connect(self.setupProcessors)
        
        setupUpdCheckAct = QAction(_('Update checking'), self)
        setupUpdCheckAct.setStatusTip(_('Setup if and for which version to check for updates'))
        setupUpdCheckAct.triggered.connect(self.setupUpdateChecking)
        
        
        # add actions
        setupMenu = self.mainMenu.addMenu(_('Setup'))
        setupLangMenu = setupMenu.addMenu(_('Language'))
        setupLangMenu.addAction(setupLangEnAct)
        setupLangMenu.addAction(setupLangDeAct)
        setupMenu.addSeparator()
        setupMenu.addAction(setupProcAct)
        setupMenu.addSeparator()
        setupMenu.addAction(setupUpdCheckAct)
    
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

    def setupProcessors(self):
        '''
        :method: Called if the user selects *Setup* -> *Both processors*
        '''
        if self.dws.windowExists('SetupProcessors') == False:
            self.setupProc_W = SetupProcessors()
            self.dws.registerWindow('SetupProcessors')
            self.mdi.addSubWindow(self.setupProc_W)
        self.setupProc_W.show()
        
    def setupUpdateChecking(self):
        '''
        :method: Called if the user selects *Setup* -> *Update checking*
        '''
        if self.dws.windowExists('SetupUpdateChecking') == False:
            self.setupUpdCheck_W = SetupUpdateChecking()
            self.dws.registerWindow('SetupUpdateChecking')
            self.mdi.addSubWindow(self.setupUpdCheck_W)
        self.setupUpdCheck_W.show()

    def buildHelpMenu(self):
        '''
        :method: Builds the Help Menu
        '''
        onlineHelpAct = QAction(_('Online Help'), self)
        onlineHelpAct.setStatusTip(_('Opens the online help in your browser'))
        onlineHelpAct.triggered.connect(self.onlineHelp)
        
        
        helpAboutAct = QAction(_('About'), self)
        helpAboutAct.setStatusTip(_('Short info about the program'))
        helpAboutAct.triggered.connect(self.helpAbout)
        
        # Build the menu
        fileMenu = self.mainMenu.addMenu(_('Help'))
        fileMenu.addAction(onlineHelpAct)
        fileMenu.addAction(helpAboutAct)
        
    def onlineHelp(self):
        '''
        :method: Opens the online help in the browser
        '''
        # webbrowser.open( os.path.join(os.getcwd(), 'userHelp/contents.html' ) )
        
        config = ConfigReader()
        webbrowser.open( os.path.join(os.getcwd(), 'userHelp', config.getLanguage(), 'introduction.html') )
        
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
