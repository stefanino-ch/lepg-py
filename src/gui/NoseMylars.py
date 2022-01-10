'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, \
    QHBoxLayout, QVBoxLayout, QPushButton, QDataWidgetMapper
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.ProcModel import ProcModel

class NoseMylars(QMdiSubWindow):
    '''
    :class: Window to display and edit Brake line details  
    '''

    __className = 'NoseMylars'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.noseMylars_M = ProcModel.NoseMylarsModel()
        self.noseMylars_M.numRowsForConfigChanged.connect( self.modelSizeChanged )
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
                    Table
                    -------------------------
                        OrderBtn  help_bar  | btn_bar
                            
        Naming:
            Conf is always one as there is only one configuration possible
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(700, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Nose mylars"))
        
        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.noseMylars_M)
        
        numLines_L = QLabel(_('Number of configs'))
        numLines_L.setAlignment(Qt.AlignRight)
        numLines_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
        self.numLines_S = QSpinBox()
        self.numLines_S.setRange(0,999)
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
        self.proxyModel.setSourceModel(self.noseMylars_M)
        
        table_T = TableView()
        table_T.setModel( self.proxyModel )
        table_T.verticalHeader().setVisible(False)
        table_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_T.hideColumn( self.noseMylars_M.columnCount()-1 )
        table_T.hideColumn( self.noseMylars_M.columnCount()-2 )
        self.windowLayout.addWidget(table_T)
         
        table_T.enableIntValidator(ProcModel.NoseMylarsModel.OrderNumCol, ProcModel.NoseMylarsModel.LastRibCol, 1, 999)
        table_T.enableDoubleValidator(ProcModel.NoseMylarsModel.xOneCol, ProcModel.NoseMylarsModel.vTwoCol, 1, 100, 1)
          
        table_T.setHelpBar(self.helpBar)
        table_T.setHelpText(ProcModel.NoseMylarsModel.OrderNumCol, _('OrderNumDesc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.FirstRibCol, _('NoseMylars-FirstRibDesc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.LastRibCol, _('NoseMylars-LastRibDesc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.xOneCol, _('NoseMylars-x1Desc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.uOneCol, _('NoseMylars-u1Desc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.uTwoCol, _('NoseMylars-u2Desc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.xTwoCol, _('NoseMylars-x2Desc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.vOneCol, _('NoseMylars-v1Desc'))
        table_T.setHelpText(ProcModel.NoseMylarsModel.vTwoCol, _('NoseMylars-v2Desc'))
        
        sortBtn = QPushButton(_('Sort by order_num'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)
        
        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue(self.noseMylars_M.num_rows_for_config(1))
        self.numLines_S.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/noseMylars.html')
        
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
        self.numLines_S.setValue(self.noseMylars_M.num_rows_for_config(1))
        self.numLines_S.blockSignals(False)
        
                   
    def numLinesChange(self): 
        '''
        :method: Called upon manual changes of the lines spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.num_lines_change')
        self.noseMylars_M.set_num_rows_for_config(1, self.numLines_S.value())

    def sortBtnPress(self):
        '''
        :method: Executed if the sort button is pressed. Does a one time sort based on the numbers in the OrderNum column.
        '''
        logging.debug(self.__className+'.sort_btn_press')

        self.proxyModel.sort(ProcModel.NoseMylarsModel.OrderNumCol, Qt.AscendingOrder)
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
    