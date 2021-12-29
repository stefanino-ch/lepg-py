'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class GlueVent(QMdiSubWindow):
    '''
    :class: Window to display and edit Glue vent data
    '''

    __className = 'GlueVent'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.glueVent_M = ProcessorModel.GlueVentModel()
        self.glueVent_M.usageUpd.connect( self.usageUpdate )
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
        self.win.setMinimumSize(500, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Glue vent"))
        
        usage_L = QLabel(_('Type'))
        self.usage_CB = QComboBox()
        self.usage_CB.addItem(_("Defaults"))
        self.usage_CB.addItem(_("User defined"))
        self.usage_CB.currentIndexChanged.connect(self.usageCbChange)
        usage_Lo = QHBoxLayout()
        usage_Lo.addWidget(usage_L)
        usage_Lo.addWidget(self.usage_CB)
        usage_Lo.addStretch()
        
        self.windowLayout.addLayout(usage_Lo)
        
        one_T = TableView()
        one_T.setModel( self.glueVent_M )
        one_T.verticalHeader().setVisible(False)
        one_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        one_T.hideColumn( self.glueVent_M.columnCount()-1 )
        one_T.hideColumn( self.glueVent_M.columnCount()-2 )
        self.windowLayout.addWidget(one_T)
        
        one_T.enableIntValidator(ProcessorModel.GlueVentModel.OrderNumCol, ProcessorModel.GlueVentModel.OrderNumCol, 0, 999)
        one_T.enableDoubleValidator(ProcessorModel.GlueVentModel.VentParamCol, ProcessorModel.GlueVentModel.VentParamCol, -3, 1, 0)
          
        one_T.setHelpBar(self.helpBar)
        one_T.setHelpText(ProcessorModel.GlueVentModel.OrderNumCol, _('GlueVent-AirfoilNumDesc'))
        one_T.setHelpText(ProcessorModel.GlueVentModel.VentParamCol, _('GlueVent-VentParamDesc'))

        self.usageUpdate()
        
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/glueVent.html')
        
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
        
        if self.glueVent_M.isUsed():
            self.usage_CB.setCurrentIndex(1)
        else:
            self.usage_CB.setCurrentIndex(0)
            
    def usageCbChange(self):
        '''
        :method: Updates the model as soon the usage CB has been changed
        '''
        logging.debug(self.__className+'.usageCbChange')
        if self.usage_CB.currentIndex() == 0:
            self.glueVent_M.setIsUsed(False)
        else:
            self.glueVent_M.setIsUsed(True)
            
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
    