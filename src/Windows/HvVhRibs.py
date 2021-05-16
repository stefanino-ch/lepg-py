'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, \
    QHBoxLayout, QVBoxLayout, QPushButton, QDataWidgetMapper
from Windows.LineEdit import LineEdit
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class HvVhRibs(QMdiSubWindow):
    '''
    :class: Window to display and edit Brake line details  
    '''

    __className = 'HvVhRibs'
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
        
        self.ribs_M = ProcessorModel.HvVhRibsModel()
        self.ribs_M.numRowsForConfigChanged.connect( self.modelSizeChanged )
        
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
                windowLayout
                    xSpacing
                    ySpacing
                    numLinesSpin
                    Table
                    -------------------------
                        OrderBtn  helpBar  | btnBar
                            
        Naming:
            Conf is always one as there is only one configuration possible
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1100, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("HV VH Ribs"))
        
        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.wing_M)
        
        xSp_L = QLabel(_('x Spacing'))
        xSp_L.setAlignment(Qt.AlignRight)
        xSp_E = LineEdit()
        xSp_E.setFixedWidth(40)
        self.wrapper.addMapping(xSp_E, ProcessorModel.WingModel.xSpacingCol)
        xSp_E.enableDoubleValidator(0, 100, 1)
        xSp_E.setHelpText(_('HvVhRibs-xSpacingDesc'))
        xSp_E.setHelpBar(self.helpBar)
        xSpLayout = QHBoxLayout()
        xSpLayout.addWidget(xSp_L)
        xSpLayout.addWidget(xSp_E)
        xSpLayout.addStretch()
        self.windowLayout.addLayout(xSpLayout)

        ySp_L = QLabel(_('y Spacing'))
        ySp_L.setAlignment(Qt.AlignRight)
        ySp_E = LineEdit()
        ySp_E.setFixedWidth(40)
        self.wrapper.addMapping(ySp_E, ProcessorModel.WingModel.ySpacingCol)
        ySp_E.enableDoubleValidator(0, 100, 1)
        ySp_E.setHelpText(_('HvVhRibs-ySpacingDesc'))
        ySp_E.setHelpBar(self.helpBar)        
        ySpLayout = QHBoxLayout()
        ySpLayout.addWidget(ySp_L)
        ySpLayout.addWidget(ySp_E)
        ySpLayout.addStretch()
        self.windowLayout.addLayout(ySpLayout)
        
        self.wrapper.toFirst()
        
        ###############
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
        self.proxyModel.setSourceModel(self.ribs_M)
        
        ribs_T = TableView()
        ribs_T.setModel( self.proxyModel )
        ribs_T.verticalHeader().setVisible(False)
        ribs_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ribs_T.hideColumn( self.ribs_M.columnCount()-1 )
        ribs_T.hideColumn( self.ribs_M.columnCount()-2 )
        self.windowLayout.addWidget(ribs_T)
         
        ribs_T.enableIntValidator(ProcessorModel.HvVhRibsModel.TypeCol, ProcessorModel.HvVhRibsModel.TypeCol, 1, 16)
        ribs_T.enableIntValidator(ProcessorModel.HvVhRibsModel.IniRibCol, ProcessorModel.HvVhRibsModel.IniRibCol, 1, 999)
        ribs_T.enableIntValidator(ProcessorModel.HvVhRibsModel.ParamACol, ProcessorModel.HvVhRibsModel.ParamACol, 1, 6)
        ribs_T.enableIntValidator(ProcessorModel.HvVhRibsModel.ParamBCol, ProcessorModel.HvVhRibsModel.ParamCCol, 1, 100)
        ribs_T.enableDoubleValidator(ProcessorModel.HvVhRibsModel.ParamDCol, ProcessorModel.HvVhRibsModel.ParamICol, 1, 100, 1)
          
        ribs_T.setHelpBar(self.helpBar)
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.OrderNumCol, _('OrderNumDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.TypeCol , _('HvVhRibs-TypeDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.IniRibCol , _('HvVhRibs-IniRibDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamACol , _('HvVhRibs-ParamADesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamBCol , _('HvVhRibs-ParamBDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamCCol , _('HvVhRibs-ParamCDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamDCol , _('HvVhRibs-ParamDDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamECol , _('HvVhRibs-ParamEDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamFCol , _('HvVhRibs-ParamFDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamGCol , _('HvVhRibs-ParamGDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamHCol , _('HvVhRibs-ParamHDesc'))
        ribs_T.setHelpText(ProcessorModel.HvVhRibsModel.ParamICol , _('HvVhRibs-ParamIDesc'))
        
        sortBtn = QPushButton(_('Sort by orderNum'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/hVvHribs.html')
        
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
        self.numLines_S.setValue( self.ribs_M.numRowsForConfig(1) )
        self.numLines_S.blockSignals(False)
        
                   
    def numLinesChange(self): 
        '''
        :method: Called upon manual changes of the lines spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.numLinesChange')
        self.ribs_M.setNumRowsForConfig(1, self.numLines_S.value() )

    def sortBtnPress(self):
        '''
        :method: Executed if the sort button is pressed. Does a one time sort based on the numbers in the OrderNum column.
        '''
        logging.debug(self.__className+'.sortBtnPress')

        self.proxyModel.sort(ProcessorModel.HvVhRibsModel.OrderNumCol, Qt.AscendingOrder)
        self.proxyModel.setDynamicSortFilter(False)
    
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className+'.btnPress')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    