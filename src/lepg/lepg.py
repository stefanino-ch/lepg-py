'''
Main Class of lepg

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''

import gettext
import sys
import logging.config

from PyQt5.QtGui import QIcon
from ConfigReader.ConfigReader import ConfigReader
from DataStores.PreProcessorStore import PreProcessorStore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit, QAction, QMessageBox, QFileDialog
from Windows.DataStatusOverview import DataStatusOverview
from Windows.PreProcDataEdit import PreProcDataEdit
from Windows.HelpAbout import HelpAbout
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from Processors.ProcRunner import ProcRunner
from Windows.ProcessorOutput import ProcessorOutput


class MainWindow(QMainWindow):
    
    __className = 'MainWindow'

    def __init__(self, parent = None):
        # Setup the logger
        logging.config.fileConfig('logger.conf', disable_existing_loggers=False)
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
        self.buildViewMenu()
        self.buildSetupMenu()
        self.buildHelpMenu()
        
        # Create the status bar
        self.statusBar()
   
    def buildFileMenu(self):
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
        Does all the work to close properly the application. 
        '''
        logging.debug(self.__className + '.fileExit')
        sys.exit()  
        
    def fileDataStatus(self):
        '''
        Opens the File Data Status overview window.
        '''
        if self.dws.windowExists('DataStatusOverview') == False:
            self.fileDataStatusW = DataStatusOverview()
            self.dws.registerWindow('DataStatusOverview')
            self.mdi.addSubWindow(self.fileDataStatusW)
        self.fileDataStatusW.show() 
    
    def buildPreProcMenu(self):  
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
        preProcRunAct.setStatusTip(_('calculate_preProx_des'))
        preProcRunAct.triggered.connect(self.preProcRun)
        
        # Build the menu
        geomMenu = self.mainMenu.addMenu(_('Pre Processor'))
        geomMenu.addAction(preProcOpenFileAct)
        geomMenu.addAction(preProcSaveAct)
        geomMenu.addAction(preProcSaveAsAct)
        geomMenu.addSeparator()
        geomMenu.addAction(preProcEditAct)
        geomMenu.addAction(preProcRunAct)
        
    def preProcOpenFile(self):
        self.pps.openFile()
        
    def preProcSaveFile(self):
        self.pps.saveFile()
        
    def preProcSaveFileAs(self):
        self.pps.saveFileAs()
        
    def preProcEdit(self):
        '''
        Opens the PreProc edit window.
        '''
        if self.dws.windowExists('PreProcDataEdit') == False:
            self.preProcEditW = PreProcDataEdit()
            self.dws.registerWindow('PreProcDataEdit')
            self.mdi.addSubWindow(self.preProcEditW)

        self.preProcEditW.show() 
        
    def preProcRun(self):
        '''
        Does start the Pre-Processor
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
        viewMenu.addAction(viewCascadeAct)
        viewMenu.addAction(viewTileAct)
        
    def viewCascade(self):
        self.mdi.cascadeSubWindows()
        
    def viewTile(self):
        self.mdi.tileSubWindows()   
        
    def buildSetupMenu(self):
        '''
        Define the actions needed for the setup menu and does build up the menu itself.
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
        Does to setup for the german language display
        '''
        config = ConfigReader()
        config.setLanguage("de")
        self.displayRestartMsg()
        
    def setupLangEn(self):
        '''
        Does to setup for the english language display
        '''
        config = ConfigReader()
        config.setLanguage("en")
        self.displayRestartMsg()  
        
    def displayRestartMsg(self):
        '''
        Displays a message to the user to restart the application after switching the language
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
        Asks the user for the location where the Pre-Processor is saved
        '''
        logging.debug(self.__className + '.setupPreProcLocation')
        fileName = QFileDialog.getOpenFileName(
                        None,
                        _('Select Pre_Processor'),
                        "",
                        "Executable (*.exe)")

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the dialog  
            # an empty tuple is retured
            # Write the info to the config reader
            logging.debug(self.__className + '.setupPreProcLocation Path and Name ' + fileName[0])
            
            config = ConfigReader()
            config.setPreProcPathName(fileName[0])
        
    def fileMenuActions(self, q):
        if q.text() == _('New'):
            MainWindow.count = MainWindow.count+1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("subwindow"+str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()

    def buildHelpMenu(self):
        # Define the actions
        helpAboutAct = QAction(_('About'), self)
        helpAboutAct.setStatusTip(_('Short info about the program'))
        helpAboutAct.triggered.connect(self.helpAbout)
        
        # Build the menu
        fileMenu = self.mainMenu.addMenu(_('Help'))
        fileMenu.addAction(helpAboutAct)
        
    def helpAbout(self):
        '''
        Opens the Help About window.
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