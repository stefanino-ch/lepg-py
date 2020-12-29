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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QGroupBox
from PyQt5.QtWidgets import QLabel

from Windows.WindowBtnBar import WindowBtnBar

from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.PreProcessorStore import PreProcessorStore
from DataStores.ProcessorStore import ProcessorStore

class DataStatusOverview(QMdiSubWindow):
    '''
    Window displaying 
        Filenames 
        If files are saved
        If data withing windows has been applied
    '''
    __windowName = 'DataStatusOverview'

    def __init__(self):
        logging.debug(self.__windowName+'.__init__')
        super().__init__()
        
        self.dws = DataWindowStatus()
        self.pps = PreProcessorStore()
        self.ps = ProcessorStore()
        
        self.buildWindow()
        self.dws.statusUpdated.connect(self.updateStatus)
        self.pps.dataStatusUpdate.connect(self.dataChanged)
        self.ps.dataStatusUpdate.connect(self.dataChanged)
    
    def closeEvent(self, event):  # @UnusedVariable
        logging.debug(self.__windowName+'.closeEvent')
    
    def buildWindow(self):
        '''
        Builds the window. 
        
        Structure:
            win
                windowGrid
                    ---------------------------------
                    preProcF
                        preProcG
                            all labels for PreProc
                    ---------------------------------
                    ProcF
                        ProcG
                            all labels for Proc
                    ---------------------------------
                    btnBar
        '''
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
                
        self.windowGrid = QGridLayout()
        self.__winGridRow = 0

        #############################
        # Add window specifics here
        self.setWindowTitle("Data Status Overview")

        self.preProcF = QGroupBox()    
        self.preProcF.setTitle("Pre Processor")
        self.preProcF.setFixedWidth(350)
        self.windowGrid.addWidget(self.preProcF, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        ##
        self.preProcG = QGridLayout()
        self.__preProcGridR = 0
        self.preProcF.setLayout(self.preProcG)
         
        ##
        self.preProcFilenameL = QLabel(_('Filename'))
        self.preProcFilenameD = QLabel(self.shortenPath(self.pps.getFileName()))
        self.preProcFilenameD.adjustSize()

        self.preProcG.addWidget(self.preProcFilenameL, self.__preProcGridR , 0)
        self.preProcG.addWidget(self.preProcFilenameD, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        ##
        self.preProcFileversL = QLabel(_('File version'))
        self.preProcFileversD = QLabel(self.pps.getSingleVal('FileVersion'))

        self.preProcG.addWidget(self.preProcFileversL, self.__preProcGridR, 0)
        self.preProcG.addWidget(self.preProcFileversD, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        
        ##
        self.preProcFileStatL = QLabel(_('File status'))
        self.preProcFileStatD = QLabel( self.dws.getFileStatusChar('PreProcFile'))
        self.preProcG.addWidget(self.preProcFileStatL, self.__preProcGridR, 0)
        self.preProcG.addWidget(self.preProcFileStatD, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        
        ##        
        self.preProcDataStatusL = QLabel(_('Data Status'))
        self.preProcDataStatusS = QLabel( self.dws.getWindowDataStatusChar('PreProcDataEdit'))
        
        self.preProcG.addWidget(self.preProcDataStatusL, self.__preProcGridR , 0)
        self.preProcG.addWidget(self.preProcDataStatusS, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        
        #############################
        self.procF = QGroupBox()    
        self.procF.setTitle("Processor")
        self.procF.setFixedWidth(350)
        self.windowGrid.addWidget(self.procF, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        ##
        self.procG = QGridLayout()
        self.__procGridR = 0
        self.procF.setLayout(self.procG)
         
        ##
        self.procFilenameL = QLabel(_('Filename'))
        self.procFilenameD = QLabel(self.shortenPath(self.ps.getFileName()))
        self.procFilenameD.adjustSize()

        self.procG.addWidget(self.procFilenameL, self.__procGridR , 0)
        self.procG.addWidget(self.procFilenameD, self.__procGridR, 1)
        self.__procGridR += 1
        ##
        self.procFileversL = QLabel(_('File version'))
        self.procFileversD = QLabel(self.ps.getSingleVal('FileVersion'))

        self.procG.addWidget(self.procFileversL, self.__procGridR, 0)
        self.procG.addWidget(self.procFileversD, self.__procGridR, 1)
        self.__procGridR += 1
        
        ##
        self.procFileStatL = QLabel(_('File status'))
        self.procFileStatD = QLabel( self.dws.getFileStatusChar('ProcFile'))
        self.procG.addWidget(self.procFileStatL, self.__procGridR, 0)
        self.procG.addWidget(self.procFileStatD, self.__procGridR, 1)
        self.__procGridR += 1
        
        ##        
        self.procDataStatusL = QLabel(_('Data Status'))
        self.procDataStatusS = QLabel( self.dws.getWindowDataStatusChar('ProcDataEdit'))
        
        self.procG.addWidget(self.procDataStatusL, self.__procGridR , 0)
        self.procG.addWidget(self.procDataStatusS, self.__procGridR, 1)
        self.__procGridR += 1
        
        #############################
        # Rest of standard window setups
        self.btnBar = WindowBtnBar( 0b0100 )
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        
        self.windowGrid.addWidget(self.btnBar, self.__winGridRow ,0, Qt.AlignRight)
        self.__winGridRow += 1
        
        self.win.setLayout(self.windowGrid)
        
    def shortenPath(self, path):
        self.__stringLength = 50
        if len(path) > self.__stringLength:
            return '...'+path[-(self.__stringLength-3):]
        else:
            return path
        
    def updateStatus(self, q):
        if q == 'PreProcDataEdit':
            self.preProcDataStatusS.setText(self.dws.getWindowDataStatusChar('PreProcDataEdit'))
        
        elif q== 'PreProcFile':
            self.preProcFileStatD.setText(self.dws.getFileStatusChar('PreProcFile'))
            
        elif q == 'ProcDataEdit':
            self.procDataStatusS.setText(self.dws.getWindowDataStatusChar('ProcDataEdit'))
        
        elif q== 'ProcFile':
            self.procFileStatD.setText(self.dws.getFileStatusChar('ProcFile'))
            
            
    def dataChanged(self, n, q):
        if n == 'PreProcessorStore':
            if q == 'FileNamePath':
                self.preProcFilenameD.setText(self.shortenPath(self.pps.getFileName()))
        
            elif q == 'FileVersion':
                self.preProcFileversD.setText(self.pps.getSingleVal('FileVersion'))
        
        elif n == 'ProcessorStore':
            if q == 'FileNamePath':
                self.procFilenameD.setText(self.shortenPath(self.ps.getFileName()))
        
            elif q == 'FileVersion':
                self.procFileversD.setText(self.ps.getSingleVal('FileVersion'))
            
    def btnPress(self, q):
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__windowName+'.btnPress unrecognized button press '+q)
        