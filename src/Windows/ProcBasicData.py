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
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.ProcessorModel import ProcessorModel

class ProcBasicData(QMdiSubWindow):
    '''
    :class: Window to display and edit the Basic Data  
    '''

    __className = 'ProcBasicData'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.wing_M = ProcessorModel.WingModel()
        self.wing_M.setSort(0, Qt.AscendingOrder)
        
        self.dws = DataWindowStatus()

        self.buildWindow()
    
    def closeEvent(self, event):  # @UnusedVariable
        '''
        :method: Called at the time the user closes the window.
        '''
        logging.debug(self.__className+'.closeEvent') 
        
    def buildWindow(self):
        '''
        :method: Creates the window including all GUI elements. 
        
        Layout::
        
            Data
            Buttons
            
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
        __winGRowL = 0
        __winGRowR = 0
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.procWrapper = QDataWidgetMapper()
        self.procWrapper.setModel(self.wing_M)
        
        self.setWindowTitle(_("Basic Data"))
        
        self.brandName_L = QLabel(_('Brand name [txt]'))
        self.brandName_L.setAlignment(Qt.AlignRight)
        self.brandName_E = LineEdit()
        self.procWrapper.addMapping(self.brandName_E, ProcessorModel.WingModel.BrandNameCol)
        self.brandName_E.enableRegExpValidator("(.|\s)*\S(.|\s)*")
        self.brandName_E.setHelpText(_('Proc-BrandNameDesc'))
        self.brandName_E.setHelpBar(self.helpBar)
        self.windowGrid.addWidget(self.brandName_L, __winGRowL, 0)
        self.windowGrid.addWidget(self.brandName_E, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        # Wing name
        self.wingName_L = QLabel(_('Wing name [txt]'))
        self.wingName_L.setAlignment(Qt.AlignRight)
        self.wingName_E = LineEdit()
        self.procWrapper.addMapping(self.wingName_E, ProcessorModel.WingModel.WingNameCol)
        self.wingName_E.enableRegExpValidator("(.|\s)*\S(.|\s)*")
        self.wingName_E.setHelpText(_('Proc-WingNameDesc'))
        self.wingName_E.setHelpBar(self.helpBar)
        self.windowGrid.addWidget(self.wingName_L, __winGRowL, 0)
        self.windowGrid.addWidget(self.wingName_E, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        # Draw scale
        self.drawScale_L = QLabel(_('Draw scale [coef]'))
        self.drawScale_L.setAlignment(Qt.AlignRight)
        self.drawScale_E = LineEdit()
        self.procWrapper.addMapping(self.drawScale_E, ProcessorModel.WingModel.DrawScaleCol)
        self.drawScale_E.enableDoubleValidator(0.00, 99.99, 2)
        self.drawScale_E.setHelpText(_('Proc-DrawScaleDesc'))
        self.drawScale_E.setHelpBar(self.helpBar)
        self.windowGrid.addWidget(self.drawScale_L, __winGRowL, 0)
        self.windowGrid.addWidget(self.drawScale_E, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        # Wing scale
        self.wingScale_L = QLabel(_('Wing scale [coef]'))
        self.wingScale_L.setAlignment(Qt.AlignRight)
        self.wingScale_E = LineEdit()
        self.procWrapper.addMapping(self.wingScale_E, ProcessorModel.WingModel.WingScaleCol)
        self.wingScale_E.enableDoubleValidator(0.00, 99.99, 2)
        self.wingScale_E.setHelpText(_('Proc-WingScaleDesc'))
        self.wingScale_E.setHelpBar(self.helpBar)
        self.windowGrid.addWidget(self.wingScale_L, __winGRowL, 0)
        self.windowGrid.addWidget(self.wingScale_E, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        # Num cells
        self.numCells_L = QLabel(_('Number of cells [num]'))
        self.numCells_L.setAlignment(Qt.AlignRight)
        self.numCells_E = LineEdit()
        self.procWrapper.addMapping(self.numCells_E, ProcessorModel.WingModel.NumCellsCol)
        self.numCells_E.enableIntValidator(1, 999)
        self.numCells_E.setHelpText(_('Proc-NumCellsDesc'))
        self.numCells_E.setHelpBar(self.helpBar)
        self.windowGrid.addWidget(self.numCells_L, __winGRowL, 0)
        self.windowGrid.addWidget(self.numCells_E, __winGRowR, 1)
        self.numCells_E.textChanged.connect(self.checkNumCellsRibs)
        __winGRowL += 1
        __winGRowR += 1
        
        # Num ribs
        self.numRibs_L = QLabel(_('Number of ribs [num]'))
        self.numRibs_L.setAlignment(Qt.AlignRight)
        self.numRibs_E = LineEdit()
        self.procWrapper.addMapping(self.numRibs_E, ProcessorModel.WingModel.NumRibsCol)
        self.numRibs_E.enableIntValidator(1, 999)
        self.numRibs_E.setHelpText(_('Proc-NumRibsDesc'))
        self.numRibs_E.setHelpBar(self.helpBar)
        self.windowGrid.addWidget(self.numRibs_L, __winGRowL, 0)
        self.windowGrid.addWidget(self.numRibs_E, __winGRowR, 1)
        self.numRibs_E.textChanged.connect(self.checkNumCellsRibs)
        __winGRowL += 1
        __winGRowR += 1
            
        self.procWrapper.toFirst()
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        # @TODO: setup and enable user help
        #self.btnBar.setHelpPage('preproc/preproc.html')
        
        self.windowGrid.addWidget(self.helpBar, __winGRowR ,1, Qt.AlignRight)
        __winGRowR += 1
        self.windowGrid.addWidget(self.btnBar, __winGRowR ,1, Qt.AlignRight)
        __winGRowR += 1
        
        self.win.setLayout(self.windowGrid)
        
    def checkNumCellsRibs(self):
        '''
        :method: The difference between NumCells and NumRibs must be 1, if this is not the case we have a nonsense setup
        ''' 
        logging.debug(self.__className + '.checkNumCellsRibs')
        numCells = self.numCells_E.text()
        numRibs = self.numRibs_E.text()
        
        if numCells.isnumeric() and numRibs.isnumeric():
            diff = abs(int(numCells)-int(numRibs))
            if diff == 1:
                self.numCells_L.setStyleSheet("")
                self.numRibs_L.setStyleSheet("")
            else:
                self.numCells_L.setStyleSheet("background-color: red")
                self.numRibs_L.setStyleSheet("background-color: red")
    
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className + '.btnPress')
        if q == 'Apply':
            print('apply')
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    