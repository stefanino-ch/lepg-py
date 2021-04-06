'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QGroupBox
from PyQt5.QtWidgets import QLabel

from Windows.WindowBtnBar import WindowBtnBar

from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.PreProcessorModel import PreProcessorModel
from DataStores.ProcessorModel import ProcessorModel

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
        self.ppm = PreProcessorModel()
        self.pm = ProcessorModel()
        
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
        self.preProcFilenameD = QLabel(self.shortenPath(self.ppm.getFileName()))
        self.preProcFilenameD.adjustSize()

        self.preProcG.addWidget(self.preProcFilenameL, self.__preProcGridR , 0)
        self.preProcG.addWidget(self.preProcFilenameD, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        ##
        self.preProcFileversL = QLabel(_('File version'))
        self.preProcFileversD = QLabel(self.ppm.getFileVersion())

        self.preProcG.addWidget(self.preProcFileversL, self.__preProcGridR, 0)
        self.preProcG.addWidget(self.preProcFileversD, self.__preProcGridR, 1)
        self.__preProcGridR += 1
        
        # ##
        # self.preProcFileStatL = QLabel(_('File status'))
        # self.preProcFileStatD = QLabel( self.dws.getFileStatusChar('PreProcFile'))
        # self.preProcG.addWidget(self.preProcFileStatL, self.__preProcGridR, 0)
        # self.preProcG.addWidget(self.preProcFileStatD, self.__preProcGridR, 1)
        # self.__preProcGridR += 1
        #
        # ##        
        # self.preProcDataStatusL = QLabel(_('Data Status'))
        # self.preProcDataStatusS = QLabel( self.dws.getWindowDataStatusChar('PreProcDataEdit'))
        #
        # self.preProcG.addWidget(self.preProcDataStatusL, self.__preProcGridR , 0)
        # self.preProcG.addWidget(self.preProcDataStatusS, self.__preProcGridR, 1)
        # self.__preProcGridR += 1
        
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
        self.procFilenameD = QLabel(self.shortenPath(self.pm.getFileName()))
        self.procFilenameD.adjustSize()

        self.procG.addWidget(self.procFilenameL, self.__procGridR , 0)
        self.procG.addWidget(self.procFilenameD, self.__procGridR, 1)
        self.__procGridR += 1
        ##
        self.procFileversL = QLabel(_('File version'))
        self.procFileversD = QLabel(self.pm.getFileVersion())

        self.procG.addWidget(self.procFileversL, self.__procGridR, 0)
        self.procG.addWidget(self.procFileversD, self.__procGridR, 1)
        self.__procGridR += 1
        
        ##
        # self.procFileStatL = QLabel(_('File status'))
        # self.procFileStatD = QLabel( self.dws.getFileStatusChar('ProcFile'))
        # self.procG.addWidget(self.procFileStatL, self.__procGridR, 0)
        # self.procG.addWidget(self.procFileStatD, self.__procGridR, 1)
        # self.__procGridR += 1
        #
        # ##        
        # self.procDataStatusL = QLabel(_('Data Status'))
        # self.procDataStatusS = QLabel( self.dws.getWindowDataStatusChar('ProcDataEdit'))
        #
        # self.procG.addWidget(self.procDataStatusL, self.__procGridR , 0)
        # self.procG.addWidget(self.procDataStatusS, self.__procGridR, 1)
        # self.__procGridR += 1
        
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
          
        # elif q == 'ProcDataEdit':
            # self.procDataStatusS.setText(self.dws.getWindowDataStatusChar('ProcDataEdit'))
            #
        # elif q== 'ProcFile':
            # self.procFileStatD.setText(self.dws.getFileStatusChar('ProcFile'))
            
            
    def dataChanged(self, n, q):
        '''
        :method: Updates the status information displayed in the window
        '''
        if n == 'PreProcessorModel':
            if q == 'FileNamePath':
                self.preProcFilenameD.setText(self.shortenPath(self.ppm.getFileName()))
        
            elif q == 'FileVersion':
                self.preProcFileversD.setText(self.ppm.getFileVersion())
        
        elif n == 'ProcessorModel':
            if q == 'FileNamePath':
                self.procFilenameD.setText(self.shortenPath(self.pm.getFileName()))
                
            elif q == 'FileVersion':
                self.procFileversD.setText(self.pm.getFileVersion())
            
    def btnPress(self, q):
        '''
        :method: Handels the button events from the window
        '''
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__className+'.btnPress unrecognized button press '+q)
        