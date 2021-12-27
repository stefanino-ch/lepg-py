'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QHBoxLayout, QVBoxLayout,\
    QComboBox, QLabel
from Windows.gui_elements.TableView import TableView
from Windows.gui_elements.WindowHelpBar import WindowHelpBar
from Windows.gui_elements.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class TwoDDxfModel(QMdiSubWindow):
    '''
    :class: Window to display and edit Brake line details  
    '''

    __className = 'TwoDDxfModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''


    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.twoDDxf_M = ProcessorModel.TwoDDxfModel()
        self.twoDDxf_M.usageUpd.connect( self.usageUpdate )
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
                    -------------------------
                        helpBar  | btnBar
                            
        Naming:
            Conf is always one as there is only one configuration possible
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(500, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("2D DXF Options"))
        
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
        one_T.setModel( self.twoDDxf_M )
        one_T.verticalHeader().setVisible(False)
        one_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        one_T.hideColumn( self.twoDDxf_M.columnCount()-1 )
        one_T.hideColumn( self.twoDDxf_M.columnCount()-2 )
        one_T.hideColumn( 0 )
        one_T.setFixedHeight(2 + one_T.horizontalHeader().height() + 6*one_T.rowHeight(0))
        self.windowLayout.addWidget(one_T)
         
        one_T.enableRegExpValidator(ProcessorModel.TwoDDxfModel.LineNameCol, ProcessorModel.TwoDDxfModel.LineNameCol, "^[a-zA-Z0-9_.-]*$")
        one_T.enableIntValidator(ProcessorModel.TwoDDxfModel.ColorCodeCol, ProcessorModel.TwoDDxfModel.ColorCodeCol, 0, 255)
        one_T.enableRegExpValidator(ProcessorModel.TwoDDxfModel.LineNameCol, ProcessorModel.TwoDDxfModel.LineNameCol, "^[a-zA-Z0-9_.-]*$")
          
        one_T.setHelpBar(self.helpBar)
        one_T.setHelpText(ProcessorModel.TwoDDxfModel.LineNameCol, _('TwoDDxf-LineNameDesc'))
        one_T.setHelpText(ProcessorModel.TwoDDxfModel.ColorCodeCol, _('TwoDDxf-ColorCodeDesc'))
        one_T.setHelpText(ProcessorModel.TwoDDxfModel.ColorNameCol, _('TwoDDxf-ColorNameDesc'))
        
        self.usageUpdate()
        
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/twoDDxf.html')
        
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
        
        if self.twoDDxf_M.isUsed():
            self.usage_CB.setCurrentIndex(1)
        else:
            self.usage_CB.setCurrentIndex(0)
    
    def usageCbChange(self):
        '''
        :method: Updates the model as soon the usage CB has been changed
        '''
        logging.debug(self.__className+'.usageCbChange')
        if self.usage_CB.currentIndex() == 0:
            self.twoDDxf_M.setIsUsed(False)
        else:
            self.twoDDxf_M.setIsUsed(True)
    
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
    