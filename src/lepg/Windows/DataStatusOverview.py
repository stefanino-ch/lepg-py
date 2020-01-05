'''
Window displaying 
    Filenames 
    If files are saved
    If data withing windows has been applied

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy
from PyQt5.QtWidgets import QLabel

from Windows.WindowBtnBar import WindowBtnBar

from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.PreProcessorStore import PreProcessorStore

class DataStatusOverview(QMdiSubWindow):
    '''
    Window displaying 
        Filenames 
        If files are saved
        If data withing windows has been applied
    '''
    __WindowName = 'DataStatusOverview'

    def __init__(self):
        logging.debug(self.__WindowName+'.__init__')
        super().__init__()
        
        self.dws = DataWindowStatus()
        self.pps = PreProcessorStore()
        
        self.buildWindow()
        self.dws.statusUpdated.connect(self.updateStatus)
        self.pps.dataChanged.connect(self.dataChanged)
    
    def closeEvent(self, event):  # @UnusedVariable
        logging.debug(self.__WindowName+'.closeEvent')
    
    def buildWindow(self):
        '''
        Builds the window. 
        
        Layout:
            Data
            Buttons
        '''
        self.win = QWidget()
        self.win.setFixedWidth(350)
        self.setWidget(self.win)
        
        self.windowGrid = QGridLayout()
        self.__winGridRow = 0

        #############################
        # Add window specifics here
        self.setWindowTitle("Data Status Overview")
        
        self.dataGrid = QGridLayout()
        self.__dataGridRow = 0         
        ##
        self.preProcFilenameL = QLabel(_('PreProc Filename'))
        self.preProcFilenameD = QLabel(self.shortenPath(self.pps.getFileName()))
        self.preProcFilenameD.adjustSize()

        self.dataGrid.addWidget(self.preProcFilenameL, self.__dataGridRow , 0)
        self.dataGrid.addWidget(self.preProcFilenameD, self.__dataGridRow, 1)
        self.__dataGridRow += 1
        
        ##
        self.preProcFileversL = QLabel(_('PreProc File version'))
        self.preProcFileversD = QLabel(self.pps.getSingleVal('FileVersion'))
        self.preProcFileversD.adjustSize()

        self.dataGrid.addWidget(self.preProcFileversL, self.__dataGridRow , 0)
        self.dataGrid.addWidget(self.preProcFileversD, self.__dataGridRow, 1)
        self.__dataGridRow += 1
        
        ##        
        self.preProcDataStatusL = QLabel(_('PreProc Data Status'))
        self.preProcDataStatusS = QLabel( self.dws.getWindowDataStatusChar('PreProcDataEdit'))
        
        self.dataGrid.addWidget(self.preProcDataStatusL, self.__dataGridRow , 0)
        self.dataGrid.addWidget(self.preProcDataStatusS, self.__dataGridRow, 1)
        self.__dataGridRow += 1
        
        #############################
        # Rest of standard window setups
        
        self.windowGrid.addLayout(self.dataGrid, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        self.btnBar = WindowBtnBar( 0b0100 )
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        
        self.windowGrid.addWidget(self.btnBar, self.__winGridRow ,0, Qt.AlignRight)
        self.__winGridRow += 1
        
        self.win.setLayout(self.windowGrid)
        
    def shortenPath(self, path):
        self.__stringLength = 45
        if len(path) > self.__stringLength:
            return '...'+path[-(self.__stringLength-3):]
        else:
            return path
        
    def updateStatus(self, q):
        print('updataStatus')
        if q == 'PreProcDataEdit':
            self.preProcDataStatusS.setText(self.dws.getWindowDataStatusChar('PreProcDataEdit'))
            
    def dataChanged(self, q):
        print('dataChanged')
        if q == 'FileNamePath':
            self.preProcFilenameD.setText(self.shortenPath(self.pps.getFileName()))
        
        if q == 'FileVersion':
            self.preProcFileversD.setText(self.pps.getSingleVal('FileVersion'))
            
    def btnPress(self, q):
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__WindowName+'.btnPress unrecognized button press '+q)
        