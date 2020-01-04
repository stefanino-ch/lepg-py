'''
Main Class of lepg

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''

import gettext
import sys
import logging.config

from ConfigReader.ConfigReader import ConfigReader
from DataStores.PreProcessorStore import PreProcessorStore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit, QAction, QMessageBox, QFileDialog
from Windows.DataStatusOverview import DataStatusOverview
from Windows.PreProcDataEdit import PreProcDataEdit
from DataWindowStatus.DataWindowStatus import DataWindowStatus


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        # Setup the logger
        logging.config.fileConfig('logger.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger('root')
        # DEBUG
        # INFO
        # WARNING
        # ERROR
        # CRITICAL
        logging.debug('Session start')
        
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
        
        self.dataStatus = DataWindowStatus()
        
        super(MainWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("lepg")
        self.mainMenu = self.menuBar()
        
        # Build the individual menus
        self.buildFileMenu()
        self.buildPreProcMenu()
        self.buildViewMenu()
        self.buildSetupMenu()
        
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
        logging.debug('Session exit')
        sys.exit()  
        
    def fileDataStatus(self):
        fileDataStatusW = DataStatusOverview()
        self.mdi.addSubWindow(fileDataStatusW)
        fileDataStatusW.show()
    
    def buildPreProcMenu(self):  
        # Define the actions
        preProcNewFileAct = QAction(_('New PreProc File'), self)
        preProcNewFileAct.setStatusTip(_('Create a new empty file'))
        preProcNewFileAct.setEnabled(False)
        
        preProcOpenFileAct = QAction(_('Open PreProc File'), self)
        preProcOpenFileAct.setStatusTip(_('Open a file'))
        preProcOpenFileAct.triggered.connect(self.preProcOpenFile)
        
        preProcSaveAct = QAction(_('Save PreProc File'), self)
        preProcSaveAct.setStatusTip(_('Save the current file'))
        preProcSaveAct.setEnabled(False)
        
        preProcSaveAsAct = QAction(_('Save PreProc File As ..'), self)
        preProcSaveAsAct.setStatusTip(_('Save the current file'))
        preProcSaveAsAct.setEnabled(False)
        
        preProcEditAct = QAction(_('Edit PreProc Data'), self)
        preProcEditAct.setStatusTip(_('Open the edit window for the PreProc data'))
        preProcEditAct.triggered.connect(self.preProcEdit)
        
        preProcCalcAct = QAction(_('Calculate'), self)
        preProcCalcAct.setStatusTip(_('Run the Pre Processor'))
        preProcCalcAct.setEnabled(False)
        
        # Build the menu
        geomMenu = self.mainMenu.addMenu(_('Pre Processor'))
        geomMenu.addAction(preProcNewFileAct)
        geomMenu.addAction(preProcOpenFileAct)
        geomMenu.addAction(preProcSaveAct)
        geomMenu.addAction(preProcSaveAsAct)
        geomMenu.addSeparator()
        geomMenu.addAction(preProcEditAct)
        geomMenu.addAction(preProcCalcAct)
        
    def preProcOpenFile(self):
        # ask first for the filename
        fileName, _filter =QFileDialog.getOpenFileName(
                        None,
                        _('Open Geometry file'),
                        "",
                        "Geometry Files (*.txt);;All Files (*)")
        
        self.pps = PreProcessorStore()

        # TODO: file open must also set flags in Data Status
        if self.pps.isValid(fileName):
            self.pps.setFileName(fileName, True)
        
    def preProcEdit(self):
        
        if self.dataStatus.windowExists('PreProcDataEdit') == False:
            self.__preProcEditW = PreProcDataEdit()
            self.dataStatus.registerWindow('PreProcDataEdit')
            self.mdi.addSubWindow(self.__preProcEditW)

        self.__preProcEditW.show() 



#         self.preProcEditW = PreProcDataEdit()
#         self.mdi.addSubWindow(self.preProcEditW)
#         self.preProcEditW.show()  

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
        
        # add actions
        setupMenu = self.mainMenu.addMenu(_('Setup'))
        setupLangMenu = setupMenu.addMenu(_('Language'))
        setupLangMenu.addAction(setupLangEnAct)
        setupLangMenu.addAction(setupLangDeAct)
    
    def setupLangDe(self):
        '''
        TODO: proper description
        '''
        config = ConfigReader()
        config.setLanguage("de")
        self.displayRestartMsg()
        
    def setupLangEn(self):
        '''
        TODO: proper description
        '''
        config = ConfigReader()
        config.setLanguage("en")
        self.displayRestartMsg()  
        
    def displayRestartMsg(self):
        '''
        TODO: proper description
        TODO: proper translation
        TODO: proper sizing
        '''
        msg = QMessageBox()
        
        msg.setWindowTitle("Language switch")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please restart")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()  
        
        
    def fileMenuActions(self, q):
        if q.text() == _('New'):
            MainWindow.count = MainWindow.count+1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("subwindow"+str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()
    
        
def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()