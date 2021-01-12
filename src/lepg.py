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
from ConfigReader.ConfigReader import ConfigReader
from DataStores.PreProcessorStore import PreProcessorStore
from DataStores.ProcessorStore import ProcessorStore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QMessageBox, QFileDialog
from Windows.DataStatusOverview import DataStatusOverview
from Windows.PreProcDataEdit import PreProcDataEdit
from Windows.WingViewer import WingViewer
from Windows.HelpAbout import HelpAbout
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from Processors.ProcRunner import ProcRunner
from Windows.ProcessorOutput import ProcessorOutput

class MainWindow(QMainWindow):
    '''
    :class: Creates the main window of the application
    '''
    
    __className = 'MainWindow'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    
    __enableWingFunct = False
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
        self.ps = ProcessorStore()
        self.dws = DataWindowStatus()
        
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("lepg")
        self.mainMenu = self.menuBar()
        
        # Build the individual menus
        self.buildFileMenu()
        self.buildPreProcMenu()
        self.buildProcMenu()
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
        procOpenFileAct = QAction(_('Open Processor File'), self)
        procOpenFileAct.setStatusTip(_('open_Proc_file_desc'))
        procOpenFileAct.triggered.connect(self.procOpenFile)
        procOpenFileAct.setEnabled(self.__enableWingFunct)
        
        procSaveAct = QAction(_('Save Processor File'), self)
        procSaveAct.setStatusTip(_('save_proc_file_desc'))
        procSaveAct.triggered.connect(self.procSaveFile)
        procSaveAct.setEnabled(self.__enableWingFunct)
        
        procSaveAsAct = QAction(_('Save Processor File As ..'), self)
        procSaveAsAct.setStatusTip(_('save_proc_file_as_desc'))
        procSaveAsAct.triggered.connect(self.procSaveFileAs)
        procSaveAsAct.setEnabled(self.__enableWingFunct)
        
        procRunAct = QAction(_('Run Processor'), self)
        procRunAct.setStatusTip(_('run_Processor_des'))
        procRunAct.triggered.connect(self.preProcRun)
        procRunAct.setEnabled(False)
        
        # Build the menu
        procMenu = self.mainMenu.addMenu(_('Processor'))
        procMenu.addAction(procOpenFileAct) 
        procMenu.addAction(procSaveAct)
        procMenu.addAction(procSaveAsAct)
        procMenu.addSeparator()
        procMenu.addAction(procRunAct)
        
    def procOpenFile(self):
        '''
        :method: Called if the user selects *Processor* -> *Open Processor File*
        '''
        self.ps.openFile()
        # @TODO: delete current values upon open file open
        
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
