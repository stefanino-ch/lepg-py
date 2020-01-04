'''
Window to display and edit the PreProc data.

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QMessageBox
from PyQt5.QtWidgets import QLabel

from Windows.LineEdit import LineEdit
from Windows.WindowBtnBar import WindowBtnBar
from Windows.WindowHelpBar import WindowHelpBar

from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.PreProcessorStore import PreProcessorStore

class PreProcDataEdit(QMdiSubWindow):
    '''
    Window to display and edit the PreProc data. 
    
    @signal dataStatusUpdate : sent out as soon the user has edited data or has clicked a button
    '''
    dataStatusUpdate = pyqtSignal(str,str)
    __WindowName = 'PreProcDataEdit'

    def __init__(self):
        '''
        Constructor
        
        Layout
            Data
            Help window
            Buttons
        '''
        logging.debug(self.__WindowName+'.__init__')
        super().__init__()
        self.pps = PreProcessorStore()
        self.dws = DataWindowStatus()
        self.dws.registerSignal(self.dataStatusUpdate)
        self.buildWindow()
        self.pps.dataChanged.connect(self.updateInputs)   

    def closeEvent(self, event):  # @UnusedVariable
        # Check for unapplied data
        if self.dws.getWindowDataStatus(self.__WindowName) == 0:
            # there is unapplied data
            if self.showCancelDialog() == QMessageBox.Ok:
                # user wants to quit, dont save, close
                self.dataStatusUpdate.emit(self.__WindowName,'Cancel')
                self.dws.unregisterSignal(self.dataStatusUpdate)
                self.dws.unregisterWindow(self.__WindowName)
                self.pps.dataChanged.disconnect(self.updateInputs)
                logging.debug(self.__WindowName+'.closeEvent')
                event.accept()
            else:
                # abort cancel 
                event.ignore()
    
    def buildWindow(self):
        self.win = QWidget()
        self.setWidget(self.win)

        self.windowGrid = QGridLayout()
        self.__winGridRow = 0
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle("Pre Processor data edit")
        
        self.dataGrid = QGridLayout()
        self.__dataGridRow = 0
         
        self.wingNameL = QLabel('Wing name')
        self.wingNameE = LineEdit()
        self.wingNameE.setText(self.pps.getSingleVal('WingName'))
        self.wingNameE.textEdited.connect(self.dataStatusChanged)
        self.wingNameE.setHelpText(_('PreProc-WingNameDesc'))
        self.wingNameE.setHelpBar(self.helpBar)
         
        self.dataGrid.addWidget(self.wingNameL, self.__dataGridRow , 0)
        self.dataGrid.addWidget(self.wingNameE, self.__dataGridRow, 1)
        self.__dataGridRow += 1

        self.windowGrid.addLayout(self.dataGrid, self.__winGridRow, 0)
        self.__winGridRow += 1

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar()
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        
        self.windowGrid.addWidget(self.helpBar,self.__winGridRow ,0, Qt.AlignRight)
        self.__winGridRow += 1
        self.windowGrid.addWidget(self.btnBar,self.__winGridRow ,0, Qt.AlignRight)
        self.__winGridRow += 1
        
        self.win.setLayout(self.windowGrid)
        
    def btnPress(self, q):
        if q == 'Apply':
            self.writeDataToStore()
            self.dataStatusUpdate.emit(self.__WindowName,'Apply')
        elif q == 'Ok':
            self.writeDataToStore()
            self.dataStatusUpdate.emit(self.__WindowName,'Ok')
            self.close()
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__WindowName + '.btnPress unrecognized button press '+q)

    def updateInputs(self, q):
        if q == 'WingName':
            self.wingNameE.setText(self.pps.getSingleVal('WingName'))
        
    def writeDataToStore(self):
        self.pps.setSingleVal('WingName', self.wingNameE.text())
            
    def dataStatusChanged(self):
        self.dataStatusUpdate.emit(self.__WindowName,'edit')
        
    def showCancelDialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Changed data")
        msgBox.setText("Data changed in this window has not been applied.\n\nPress OK to close the window, data will be lost.\nPress Cancel to abort. ")
        msgBox.setIcon(QMessageBox.Warning)
        
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msgBox.exec()

        