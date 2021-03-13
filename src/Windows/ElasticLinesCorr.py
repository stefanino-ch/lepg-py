'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QLabel, QDataWidgetMapper
from Windows.LineEdit import LineEdit
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class ElasticLinesCorr(QMdiSubWindow):
    '''
    :class: Window to display and edit the Basic Data  
    '''

    __className = 'ElasticLinesCorr'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.elLinesCorr_M = ProcessorModel.ElasticLinesCorrModel()

        self.buildWindow()
    
    def closeEvent(self, event):  # @UnusedVariable
        '''
        :method: Called at the time the user closes the window.
        '''
        logging.debug(self.__className+'.closeEvent') 
        
    def buildWindow(self):
        '''
        :method: Creates the window including all GUI elements. 
            
        Structure:: 
        
            win
                windowGrid 
                     Labels    | Edit fields
                     ...       | ...
                    -------------------------
                                | helpBar
                                | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(400, 300)

        self.windowGrid = QGridLayout()
        __winGRow = 0
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.elLinesCorr_M)
        
        self.setWindowTitle(_("Elastic lines correction"))
        
        load_L = QLabel(_('in flight load [kg]'))
        load_L.setAlignment(Qt.AlignRight)
        self.load_E = LineEdit()
        self.wrapper.addMapping(self.load_E, ProcessorModel.ElasticLinesCorrModel.LoadCol)
        #self.brandName_E.enableRegExpValidator("(.|\s)*\S(.|\s)*")
        self.load_E.setHelpText(_('ElLinesCorr-LoadDesc'))
        self.load_E.setHelpBar(self.helpBar)
        self.windowGrid.addWidget(load_L, __winGRow, 0)
        self.windowGrid.addWidget(self.load_E, __winGRow, 1)
        __winGRow += 1
        
        self.windowGrid.addWidget(QLabel(_('Load distr [%]')), __winGRow, 1)
        self.windowGrid.addWidget(QLabel(_('Load distr [%]')), __winGRow, 2)
        self.windowGrid.addWidget(QLabel(_('Load distr [%]')), __winGRow, 3)
        self.windowGrid.addWidget(QLabel(_('Load distr [%]')), __winGRow, 4)
        self.windowGrid.addWidget(QLabel(_('Load distr [%]')), __winGRow, 5)
        __winGRow += 1
        
        twoLineT_L = QLabel(_('Two Lines'))
        twoLineT_L.setAlignment(Qt.AlignRight)
        self.twoLineA_E = LineEdit()
        self.wrapper.addMapping(self.twoLineA_E, ProcessorModel.ElasticLinesCorrModel.TwoLineDistACol)
        #self.brandName_E.enableRegExpValidator("(.|\s)*\S(.|\s)*")
        self.twoLineA_E.setHelpText(_('ElLinesCorr-TwoLineDistDesc'))
        self.twoLineA_E.setHelpBar(self.helpBar)
        
        self.twoLineB_E = LineEdit()
        self.wrapper.addMapping(self.twoLineB_E, ProcessorModel.ElasticLinesCorrModel.TwoLineDistBCol)
        #self.brandName_E.enableRegExpValidator("(.|\s)*\S(.|\s)*")
        self.twoLineB_E.setHelpText(_('ElLinesCorr-TwoLineDistDesc'))
        self.twoLineB_E.setHelpBar(self.helpBar)
        
        self.windowGrid.addWidget(twoLineT_L, __winGRow, 0)
        self.windowGrid.addWidget(self.twoLineA_E, __winGRow, 1)
        self.windowGrid.addWidget(self.twoLineB_E, __winGRow, 2)
        __winGRow += 1
        
            
        self.wrapper.toFirst()
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/elasticLinesCorrection.html')
        
        self.windowGrid.addWidget(self.helpBar, __winGRow ,1, Qt.AlignRight)
        __winGRow += 1
        self.windowGrid.addWidget(self.btnBar, __winGRow ,1, Qt.AlignRight)
        __winGRow += 1
        
        self.win.setLayout(self.windowGrid)
    
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className + '.btnPress')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    