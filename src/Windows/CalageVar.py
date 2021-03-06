'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class CalageVar(QMdiSubWindow):
    '''
    :class: Window to display and edit Brake line details  
    '''

    __className = 'CalageVar'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.calageVar_M = ProcessorModel.CalageVarModel()
        self.calageVar_M.usageUpd.connect( self.usageUpdate )
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
                    Table
                    Table
                    Table
                    -------------------------
                        helpBar  | btnBar
                            
        Naming:
            Conf is always one as there is only one configuration possible
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(600, 200)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Calage variation "))
        
        usage_L = QLabel(_('Type'))
        self.usage_CB = QComboBox()
        self.usage_CB.addItem(_("None"))
        self.usage_CB.addItem(_("Type 1"))
        self.usage_CB.currentIndexChanged.connect(self.usageCbChange)
        usage_Lo = QHBoxLayout()
        usage_Lo.addWidget(usage_L)
        usage_Lo.addWidget(self.usage_CB)
        usage_Lo.addStretch()
        
        self.windowLayout.addLayout(usage_Lo)
        
        one_T = TableView()
        one_T.setModel( self.calageVar_M )
        one_T.verticalHeader().setVisible(False)
        one_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        one_T.hideColumn( 0 )
        for i in range (ProcessorModel.CalageVarModel.PosACol, ProcessorModel.CalageVarModel.NumPosStepsCol+1):
            one_T.hideColumn( i )
        one_T.hideColumn( self.calageVar_M.columnCount()-2 )
        one_T.hideColumn( self.calageVar_M.columnCount()-1 )

        one_T.setFixedHeight(2 + one_T.horizontalHeader().height() + one_T.rowHeight(0))
        oneT_Lo = QHBoxLayout()
        oneT_Lo.addWidget(one_T)
        oneT_Lo.addStretch()
        oneT_Lo.addStretch()
        self.windowLayout.addLayout(oneT_Lo)
        
        one_T.enableIntValidator(ProcessorModel.CalageVarModel.NumRisersCol, ProcessorModel.CalageVarModel.NumRisersCol, 2, 6)

        one_T.setHelpBar(self.helpBar)
        one_T.setHelpText(ProcessorModel.CalageVarModel.NumRisersCol, _('CalageVar-NumRisersDesc'))

        two_T = TableView()
        two_T.setModel( self.calageVar_M )
        two_T.verticalHeader().setVisible(False)
        two_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range (0, ProcessorModel.CalageVarModel.NumRisersCol+1):
            two_T.hideColumn( i )
        for i in range (ProcessorModel.CalageVarModel.MaxNegAngCol, ProcessorModel.CalageVarModel.NumPosStepsCol+1):
            two_T.hideColumn( i )
        two_T.hideColumn( self.calageVar_M.columnCount()-2 )
        two_T.hideColumn( self.calageVar_M.columnCount()-1 )

        two_T.setFixedHeight(2 + two_T.horizontalHeader().height() + two_T.rowHeight(0))
        twoT_Lo = QHBoxLayout()
        twoT_Lo.addWidget(two_T)
        self.windowLayout.addLayout(twoT_Lo)
        
        two_T.enableDoubleValidator(ProcessorModel.CalageVarModel.PosACol, ProcessorModel.CalageVarModel.PosFCol, 0, 100, 2)

        two_T.setHelpBar(self.helpBar)
        two_T.setHelpText(ProcessorModel.CalageVarModel.PosACol, _('CalageVar-PosADesc'))
        two_T.setHelpText(ProcessorModel.CalageVarModel.PosBCol, _('CalageVar-PosBDesc'))
        two_T.setHelpText(ProcessorModel.CalageVarModel.PosCCol, _('CalageVar-PosCDesc'))
        two_T.setHelpText(ProcessorModel.CalageVarModel.PosDCol, _('CalageVar-PosDDesc'))
        two_T.setHelpText(ProcessorModel.CalageVarModel.PosECol, _('CalageVar-PosEDesc'))
        two_T.setHelpText(ProcessorModel.CalageVarModel.PosFCol, _('CalageVar-PosFDesc'))

        three_T = TableView()
        three_T.setModel( self.calageVar_M )
        three_T.verticalHeader().setVisible(False)
        three_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range (0, ProcessorModel.CalageVarModel.PosFCol+1):
            three_T.hideColumn( i )
        three_T.hideColumn( self.calageVar_M.columnCount()-2 )
        three_T.hideColumn( self.calageVar_M.columnCount()-1 )

        three_T.setFixedHeight(2 + three_T.horizontalHeader().height() + three_T.rowHeight(0))
        threeT_Lo = QHBoxLayout()
        threeT_Lo.addWidget(three_T)
        self.windowLayout.addLayout(threeT_Lo)

        three_T.enableDoubleValidator(ProcessorModel.CalageVarModel.MaxNegAngCol, ProcessorModel.CalageVarModel.MaxNegAngCol, -45, 0, 2)
        three_T.enableIntValidator(ProcessorModel.CalageVarModel.NumNegStepsCol, ProcessorModel.CalageVarModel.NumNegStepsCol, 1, 100)
        three_T.enableDoubleValidator(ProcessorModel.CalageVarModel.MaxPosAngCol, ProcessorModel.CalageVarModel.MaxPosAngCol, 0, 45, 2)
        three_T.enableIntValidator(ProcessorModel.CalageVarModel.NumPosStepsCol, ProcessorModel.CalageVarModel.NumPosStepsCol, 1, 100)

        three_T.setHelpBar(self.helpBar)
        three_T.setHelpText(ProcessorModel.CalageVarModel.MaxNegAngCol, _('CalageVar-MaxNegAngDesc'))
        three_T.setHelpText(ProcessorModel.CalageVarModel.NumNegStepsCol, _('CalageVar-NumNegStepsDesc'))
        three_T.setHelpText(ProcessorModel.CalageVarModel.MaxPosAngCol, _('CalageVar-MaxPosAngDesc'))
        three_T.setHelpText(ProcessorModel.CalageVarModel.NumPosStepsCol, _('CalageVar-NumPosStepsDesc'))

        self.usageUpdate()
        
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/calageVar.html')
        
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch() 
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)

    def usageUpdate(self):
        '''
        :method: Updates the GUI as soon in the model the usage flag has been changed
        '''
        logging.debug(self.__className+'.usageUpdate')
        
        if self.calageVar_M.isUsed():
            self.usage_CB.setCurrentIndex(1)
        else:
            self.usage_CB.setCurrentIndex(0)
            
    def usageCbChange(self):
        '''
        :method: Updates the model as soon the usage CB has been changed
        '''
        logging.debug(self.__className+'.usageCbChange')
        if self.usage_CB.currentIndex() == 0:
            self.calageVar_M.setIsUsed(False)
        else:
            self.calageVar_M.setIsUsed(True)
            
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
    