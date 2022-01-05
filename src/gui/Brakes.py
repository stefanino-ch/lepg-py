'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, \
    QHBoxLayout, QVBoxLayout, QPushButton, QDataWidgetMapper
from gui.elements.LineEdit import LineEdit
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.ProcModel import ProcModel

class Brakes(QMdiSubWindow):
    '''
    :class: Window to display and edit Brake line details  
    '''

    __className = 'Brakes'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.wing_M = ProcModel.WingModel()
        
        self.brakes_M = ProcModel.BrakesModel()
        self.brakes_M.numRowsForConfigChanged.connect( self.modelSizeChanged )
        
        self.brakeL_M = ProcModel.BrakeLengthModel()
        
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
                        numLinesSpin
                        LinesTable
                    -------------------------
                        OrderBtn  help_bar  | btn_bar
                            
        Naming:
        
            conf is always one as there is only one brake line configuration allowed
            details equals brake line paths
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1100, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Edit Brake lines"))
        
        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.wing_M)
        
        length_L = QLabel(_('Brake lenght [cm]'))
        length_L.setAlignment(Qt.AlignRight)
        length_E = LineEdit()
        length_E.setFixedWidth(40)
        self.wrapper.addMapping(length_E, ProcModel.WingModel.BrakeLengthCol)
        length_E.enableIntValidator(0, 20000)
        length_E.setHelpText(_('Brakes-LineLengthDesc'))
        length_E.setHelpBar(self.helpBar)
        
        lengthLayout = QHBoxLayout()
        lengthLayout.addWidget(length_L)
        lengthLayout.addWidget(length_E)
        lengthLayout.addStretch()
        self.windowLayout.addLayout(lengthLayout)
        
        self.wrapper.toFirst()
        
        ###############
        numLines_L = QLabel(_('Number of Brake paths'))
        numLines_L.setAlignment(Qt.AlignRight)
        numLines_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
        self.numLines_S = QSpinBox()
        self.numLines_S.setRange(1,999)
        self.numLines_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numLines_S.valueChanged.connect(self.numLinesChange)
        numLinesEdit = self.numLines_S.lineEdit()
        numLinesEdit.setReadOnly(True)
        
        numLinesLayout = QHBoxLayout()
        numLinesLayout.addWidget(numLines_L)
        numLinesLayout.addWidget(self.numLines_S)
        numLinesLayout.addStretch()
        self.windowLayout.addLayout(numLinesLayout)
        ###############
        
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.brakes_M)
        
        brakes_T = TableView()
        brakes_T.setModel( self.proxyModel )
        brakes_T.verticalHeader().setVisible(False)
        brakes_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        brakes_T.hideColumn( self.brakes_M.columnCount()-1 )
        brakes_T.hideColumn( self.brakes_M.columnCount()-2 )
        self.windowLayout.addWidget(brakes_T)
        
        brakes_T.enableIntValidator(ProcModel.BrakesModel.OrderNumCol, ProcModel.BrakesModel.OrderNumCol, 1, 999)
        brakes_T.enableIntValidator(ProcModel.BrakesModel.NumBranchesCol, ProcModel.BrakesModel.NumBranchesCol, 1, 4)
        brakes_T.enableIntValidator(ProcModel.BrakesModel.BranchLvlOneCol, ProcModel.BrakesModel.OrderLvlFourCol, 1, 99)
        brakes_T.enableIntValidator(ProcModel.BrakesModel.AnchorLineCol, ProcModel.BrakesModel.AnchorLineCol, 1, 6)
        # TODO: updata max num ribs
        brakes_T.enableDoubleValidator(ProcModel.BrakesModel.AnchorRibNumCol, ProcModel.BrakesModel.AnchorRibNumCol, 1, 999, 1)
         
        brakes_T.setHelpBar(self.helpBar)
        brakes_T.setHelpText(ProcModel.BrakesModel.OrderNumCol, _('OrderNumDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.NumBranchesCol, _('Brakes-NumBranchesDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.BranchLvlOneCol, _('Brakes-BranchLvlOneDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.OrderLvlOneCol, _('Brakes-OrderLvlOneDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.LevelOfRamTwoCol, _('Brakes-LevelOfRamTwoDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.OrderLvlTwoCol, _('Brakes-OrderLvlTwoDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.LevelOfRamThreeCol, _('Brakes-LevelOfRamThreeDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.OrderLvlThreeCol, _('Brakes-OrderLvlThreeDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.BranchLvlFourCol, _('Brakes-BranchLvlFourDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.OrderLvlFourCol, _('Brakes-OrderLvlFourDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.AnchorLineCol, _('Brakes-AnchorLineDesc'))
        brakes_T.setHelpText(ProcModel.BrakesModel.AnchorRibNumCol, _('Brakes-AnchorRibNumDesc'))
        
        centerDist_T = TableView()
        centerDist_T.setModel( self.brakeL_M )
        centerDist_T.verticalHeader().setVisible(False)
        centerDist_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for c in range (5, self.brakeL_M.columnCount()):
            centerDist_T.hideColumn( c )
        centerDist_T.setFixedHeight(2 + centerDist_T.horizontalHeader().height() + centerDist_T.rowHeight(0))
        centerDistLayout = QHBoxLayout()
        centerDistLayout.addWidget(centerDist_T)
        centerDistLayout.addStretch()
        self.windowLayout.addLayout(centerDistLayout)
        
        centerDist_T.enableIntValidator(ProcModel.BrakeLengthModel.s1Col, ProcModel.BrakeLengthModel.s5Col, 0, 100)
        
        centerDist_T.setHelpBar(self.helpBar)
        centerDist_T.setHelpText(ProcModel.BrakeLengthModel.s1Col, _('Brakes-s1Desc'))
        centerDist_T.setHelpText(ProcModel.BrakeLengthModel.s2Col, _('Brakes-s2Desc'))
        centerDist_T.setHelpText(ProcModel.BrakeLengthModel.s3Col, _('Brakes-s3Desc'))
        centerDist_T.setHelpText(ProcModel.BrakeLengthModel.s4Col, _('Brakes-s4Desc'))
        centerDist_T.setHelpText(ProcModel.BrakeLengthModel.s5Col, _('Brakes-s5Desc'))
        
        lengthInc_T = TableView()
        lengthInc_T.setModel( self.brakeL_M )
        lengthInc_T.verticalHeader().setVisible(False)
        lengthInc_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for c in range (0,5):
            lengthInc_T.hideColumn( c )
        lengthInc_T.hideColumn( self.brakeL_M.columnCount()-1 )
        lengthInc_T.setFixedHeight(2 + lengthInc_T.horizontalHeader().height() + lengthInc_T.rowHeight(0))
        lengthIncLayout = QHBoxLayout()
        lengthIncLayout.addWidget(lengthInc_T)
        lengthIncLayout.addStretch()
        self.windowLayout.addLayout(lengthIncLayout)
        
        lengthInc_T.enableIntValidator(ProcModel.BrakeLengthModel.d1Col, ProcModel.BrakeLengthModel.d5Col, 0, 100)
        
        lengthInc_T.setHelpBar(self.helpBar)
        lengthInc_T.setHelpText(ProcModel.BrakeLengthModel.d1Col, _('Brakes-d1Desc'))
        lengthInc_T.setHelpText(ProcModel.BrakeLengthModel.d2Col, _('Brakes-d2Desc'))
        lengthInc_T.setHelpText(ProcModel.BrakeLengthModel.d3Col, _('Brakes-d3Desc'))
        lengthInc_T.setHelpText(ProcModel.BrakeLengthModel.d4Col, _('Brakes-d4Desc'))
        lengthInc_T.setHelpText(ProcModel.BrakeLengthModel.d5Col, _('Brakes-d5Desc'))
         
        sortBtn = QPushButton(_('Sort by order_num'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)
        
        if self.brakes_M.numConfigs() > 0:
            self.modelSizeChanged()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/brakes.html')
        
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(sortBtn)
        bottomLayout.addStretch() 
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)
            
    def modelSizeChanged(self):
        '''
        :method: Called after the model has been changed it's size. Herein we assure the GUI follows the model.
        '''
        logging.debug(self.__className+'.modelSizeChanged')
            
        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue( self.brakes_M.numRowsForConfig(1) )
        self.numLines_S.blockSignals(False)
        
                   
    def numLinesChange(self): 
        '''
        :method: Called upon manual changes of the lines spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.num_lines_change')
        self.brakes_M.setNumRowsForConfig(1, self.numLines_S.value() )

    def sortBtnPress(self):
        '''
        :method: Executed if the sort button is pressed. Does a one time sort based on the numbers in the OrderNum column.
        '''
        logging.debug(self.__className+'.sort_btn_press')

        self.proxyModel.sort(ProcModel.BrakesModel.OrderNumCol, Qt.AscendingOrder)
        self.proxyModel.setDynamicSortFilter(False)
    
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
    