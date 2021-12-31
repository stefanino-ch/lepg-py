'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QGroupBox
from PyQt5.QtWidgets import QLabel

from gui.elements.WindowBtnBar import WindowBtnBar

from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.PreProcModel import PreProcModel
from DataStores.ProcModel import ProcModel

class DataStatusOverview(QMdiSubWindow):
    '''
    :class: Window displaying: Filenames, if files are saved, if data withing windows has been applied
    '''
    
    __className = 'DataStatusOverview'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        ''' 
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.dws = DataWindowStatus()
        self.ppm = PreProcModel()
        self.pm = ProcModel()
        
        self.buildWindow()
        self.dws.statusUpdated.connect(self.updateStatus)
        self.ppm.dataStatusUpdate.connect(self.dataChanged)
        self.pm.dataStatusUpdate.connect(self.dataChanged)
    
    def closeEvent(self, event):  # @UnusedVariable
        '''
        :method: Called upon window close
        '''
        logging.debug(self.__className+'.closeEvent')
    
    def buildWindow(self):
        '''
        :method: Builds the window. 
        
        Structure::
        
            window
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
                    btn_bar
        '''
        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
                
        self.windowGrid = QGridLayout()
        self.__winGridRow = 0

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Data Status Overview"))

        self.preProcF = QGroupBox()    
        self.preProcF.setTitle(_("Pre Processor"))
        self.preProcF.setFixedWidth(350)
        self.windowGrid.addWidget(self.preProcF, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        ##
        self.preProcG = QGridLayout()
        self.__preProcGridR = 0
        self.preProcF.setLayout(self.preProcG)
         
        ##
        self.preProcFilenameL = QLabel(_('Filename'))
        self.preProcFilenameD = QLabel(self.shortenPath(self.ppm.get_file_name()))
        self.preProcFilenameD.adjustSize()

        self.preProcG.addWidget(self.preProcFilenameL, self.__preProcGridR , 0)
        self.preProcG.addWidget(self.preProcFilenameD, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        ##
        self.preProcFileversL = QLabel(_('File version'))
        self.preProcFileversD = QLabel(self.ppm.get_file_version())

        self.preProcG.addWidget(self.preProcFileversL, self.__preProcGridR, 0)
        self.preProcG.addWidget(self.preProcFileversD, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        
        #############################
        self.procF = QGroupBox()    
        self.procF.setTitle(_("Processor"))
        self.procF.setFixedWidth(350)
        self.windowGrid.addWidget(self.procF, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        ##
        self.procG = QGridLayout()
        self.__procGridR = 0
        self.procF.setLayout(self.procG)
         
        ##
        self.procFilenameL = QLabel(_('Filename'))
        self.procFilenameD = QLabel(self.shortenPath(self.pm.get_file_name()))
        self.procFilenameD.adjustSize()

        self.procG.addWidget(self.procFilenameL, self.__procGridR , 0)
        self.procG.addWidget(self.procFilenameD, self.__procGridR, 1)
        self.__procGridR += 1
        ##
        self.procFileversL = QLabel(_('File version'))
        self.procFileversD = QLabel(self.pm.get_file_version())

        self.procG.addWidget(self.procFileversL, self.__procGridR, 0)
        self.procG.addWidget(self.procFileversD, self.__procGridR, 1)
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
        '''
        :mathod: does shorten the path strings in a way that the filename at the end and only part of the path is shown. 
        :parameter path: the full path to be shortened
        :returns: the short form of the path
        '''
        self.__stringLength = 50
        if len(path) > self.__stringLength:
            return '...'+path[-(self.__stringLength-3):]
        else:
            return path
        
    def updateStatus(self, q):
        '''
        :method: Updates the status information displayed in the window
        '''
        if q == 'PreProcDataEdit':
            self.preProcDataStatusS.setText(self.dws.getWindowDataStatusChar('PreProcDataEdit'))
        
        elif q== 'PreProcFile':
            self.preProcFileStatD.setText(self.dws.getFileStatusChar('PreProcFile'))
            
    def dataChanged(self, n, q):
        '''
        :method: Updates the status information displayed in the window
        '''
        if n == 'PreProcModel':
            if q == 'FileNamePath':
                self.preProcFilenameD.setText(self.shortenPath(self.ppm.get_file_name()))
        
            elif q == 'FileVersion':
                self.preProcFileversD.setText(self.ppm.get_file_version())
        
        elif n == 'ProcModel':
            if q == 'FileNamePath':
                self.procFilenameD.setText(self.shortenPath(self.pm.get_file_name()))
                
            elif q == 'FileVersion':
                self.procFileversD.setText(self.pm.get_file_version())
            
    def btnPress(self, q):
        '''
        :method: Handels the button events from the window
        '''
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__className+'.btn_press unrecognized button press '+q)
        