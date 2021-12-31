'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QSpinBox
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from DataStores.PreProcModel import PreProcModel

class PreProcCellsDistribution(QMdiSubWindow):
    '''
    :class: Window to display and edit the cells distribution data for the pre-processor  
    '''

    __className = 'PreProcCellsDistribution'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.cellsDistr_M = PreProcModel.CellsDistrModel()
        self.cellsDistr_M.didSelect.connect( self.modelChange )
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
        
            window
                window_ly
                    usage_CB
                    numLines_S
                    Table
                    -------------------------
                        help_bar  | btn_bar
                            
        Naming:
            Conf is always one as there is only one configuration possible
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(450, 200)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Pre-Processor cells distribution"))
        
        usage_L = QLabel(_('Type'))
        usage_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.usage_CB = QComboBox()
        self.usage_CB.addItem(_("1: uniform "))
        self.usage_CB.addItem(_("2: linear"))
        self.usage_CB.addItem(_("3: prop to chord"))
        self.usage_CB.addItem(_("4: explicit"))
        self.usage_CB.currentIndexChanged.connect(self.usageCbChange)
        usage_Ly = QHBoxLayout()
        usage_Ly.addWidget(usage_L)
        usage_Ly.addWidget(self.usage_CB)
        usage_Ly.addStretch()
        
        self.windowLayout.addLayout(usage_Ly)
        
        self.numLines_L = QLabel(_('Num cells'))
        self.numLines_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numLines_S = QSpinBox()
        self.numLines_S.setRange(1,999)
        self.numLines_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numLines_S.valueChanged.connect(self.numLinesChange)
        numLinesEdit = self.numLines_S.lineEdit()
        numLinesEdit.setReadOnly(True)
        numLines_Ly = QHBoxLayout()
        numLines_Ly.addWidget(self.numLines_L)
        numLines_Ly.addWidget(self.numLines_S)
        numLines_Ly.addStretch()
        
        self.windowLayout.addLayout(numLines_Ly)
        
        self.one_T = TableView()
        self.one_T.setModel( self.cellsDistr_M )
        self.one_T.verticalHeader().setVisible(False)
        self.one_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.one_T.hideColumn( self.cellsDistr_M.columnCount()-1 )
        self.one_T.hideColumn( self.cellsDistr_M.columnCount()-2 )

        self.windowLayout.addWidget(self.one_T)
        
        self.one_T.enableIntValidator(PreProcModel.CellsDistrModel.OrderNumCol, PreProcModel.CellsDistrModel.OrderNumCol, 1, 999)
        self.one_T.enableDoubleValidator(PreProcModel.CellsDistrModel.CoefCol, PreProcModel.CellsDistrModel.CoefCol, 0, 1, 1)
        self.one_T.enableDoubleValidator(PreProcModel.CellsDistrModel.WidthCol, PreProcModel.CellsDistrModel.WidthCol, 1, 500, 1)
        self.one_T.enableIntValidator(PreProcModel.CellsDistrModel.NumCellsCol, PreProcModel.CellsDistrModel.NumCellsCol, 1, 999)
          
        self.one_T.setHelpBar(self.helpBar)
        self.one_T.setHelpText(PreProcModel.CellsDistrModel.OrderNumCol, _('PreProc-CellNumDesc'))
        self.one_T.setHelpText(PreProcModel.CellsDistrModel.CoefCol, _('PreProc-DistrCoefDesc'))
        self.one_T.setHelpText(PreProcModel.CellsDistrModel.WidthCol, _('PreProc-WidthDesc'))
        self.one_T.setHelpText(PreProcModel.CellsDistrModel.NumCellsCol, _('PreProc-NumCellsDesc'))

        self.modelChange()
        
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('preproc/cellDistribution.html')
        
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch() 
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)

    def modelChange(self):
        '''
        :method: Updates the GUI as soon the model changes
        '''
        logging.debug(self.__className+'.usageUpdate')
        
        typeN = self.cellsDistr_M.get_type(1, 1)
        
        if typeN == 1:
            self.usage_CB.blockSignals(True)
            self.usage_CB.setCurrentIndex(0)
            self.usage_CB.blockSignals(False)
            
            self.setTypeOneColumns()
            
        elif typeN == 2:
            self.usage_CB.blockSignals(True)
            self.usage_CB.setCurrentIndex(1)
            self.usage_CB.blockSignals(False)
            
            self.setTypeTwoThrColumns()
            
        elif typeN == 3:
            self.usage_CB.blockSignals(True)
            self.usage_CB.setCurrentIndex(2)
            self.usage_CB.blockSignals(False)
            
            self.setTypeTwoThrColumns()
        
        elif typeN == 4: 
            self.usage_CB.blockSignals(True)
            self.usage_CB.setCurrentIndex(3)
            self.usage_CB.blockSignals(False)
            
            self.setTypeFouColumns()
            
    def usageCbChange(self):
        '''
        :method: Updates the model as soon the usage CB has been changed
        '''
        logging.debug(self.__className+'.usageCbChange')
        if self.usage_CB.currentIndex() == 0:
            self.cellsDistr_M.setNumRowsForConfig(1, 1)
            self.cellsDistr_M.update_type(1, 1, 1)
            
        elif self.usage_CB.currentIndex()==1: 
            self.cellsDistr_M.setNumRowsForConfig(1, 1)
            self.cellsDistr_M.update_type(1, 1, 2)
        
        elif self.usage_CB.currentIndex()==2:
            self.cellsDistr_M.setNumRowsForConfig(1, 1)
            self.cellsDistr_M.update_type(1, 1, 3)
            
        elif self.usage_CB.currentIndex()==3: 
            self.cellsDistr_M.update_type(1, 1, 4)
            
    def numLinesChange(self):
        '''
        :method: Updates the model as soon the usage CB has been changed
        '''
        logging.debug(self.__className+'.numLinesChange')
        self.cellsDistr_M.setNumRowsForConfig(1, self.numLines_S.value() )
            
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className+'.btn_press')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btn_press unrecognized button press '+q)
            
    def setTypeOneColumns(self):
        '''
        :method: shows/ hides the spinbox and the table colums to for type 1 data
        '''
        logging.debug(self.__className+'.setTypeOneColumns')
        
        self.numLines_L.setVisible(False)
        self.numLines_S.setVisible(False)
        
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.OrderNumCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.DistrTypeCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.CoefCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.WidthCol)
        self.one_T.showColumn(PreProcModel.CellsDistrModel.NumCellsCol)

    def setTypeTwoThrColumns(self):
        '''
        :method: shows/ hides the spinbox and the table colums to for type 2 and 3 data 
        '''
        logging.debug(self.__className+'.setTypeTwoThrColumns')
        
        self.numLines_L.setVisible(False)
        self.numLines_S.setVisible(False)
        
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.OrderNumCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.DistrTypeCol)
        self.one_T.showColumn(PreProcModel.CellsDistrModel.CoefCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.WidthCol)
        self.one_T.showColumn(PreProcModel.CellsDistrModel.NumCellsCol)
        
    def setTypeFouColumns(self):
        '''
        :method: shows/ hides the spinbox and the table colums to for type 4 data 
        '''
        logging.debug(self.__className+'.setTypeFouColumns')
        
        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue( self.cellsDistr_M.numRowsForConfig(1) )
        self.numLines_S.blockSignals(False)
        
        self.numLines_L.setVisible(True)
        self.numLines_S.setVisible(True)
        
        self.one_T.showColumn(PreProcModel.CellsDistrModel.OrderNumCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.DistrTypeCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.CoefCol)
        self.one_T.showColumn(PreProcModel.CellsDistrModel.WidthCol)
        self.one_T.hideColumn(PreProcModel.CellsDistrModel.NumCellsCol)
    