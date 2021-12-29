'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QHBoxLayout, \
    QVBoxLayout, QComboBox, QLabel
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class ThreeDDxfModel(QMdiSubWindow):
    '''
    :class: Window to display and edit Brake line details  
    '''

    __className = 'ThreeDDxfModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.threeDDxf_M = ProcessorModel.ThreeDDxfModel()
        self.threeDDxf_M.usageUpd.connect( self.usageUpdate )
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
        
        self.setWindowIcon(QIcon('gui\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(500, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("3D DXF Options"))

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
        one_T.setModel( self.threeDDxf_M )
        one_T.verticalHeader().setVisible(False)
        one_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        one_T.hideColumn( self.threeDDxf_M.columnCount()-1 )
        one_T.hideColumn( self.threeDDxf_M.columnCount()-2 )
        one_T.hideColumn( 2 )
        one_T.hideColumn( 0 )
        for l in range (6, 9):
            one_T.hideRow(l)
        one_T.setFixedHeight(2 + one_T.horizontalHeader().height() + 6*one_T.rowHeight(0))
        self.windowLayout.addWidget(one_T)
         
        one_T.enableRegExpValidator(ProcessorModel.ThreeDDxfModel.LineNameCol, ProcessorModel.ThreeDDxfModel.LineNameCol, "^[a-zA-Z0-9_.-]*$")
        one_T.enableIntValidator(ProcessorModel.ThreeDDxfModel.ColorCodeCol, ProcessorModel.ThreeDDxfModel.ColorCodeCol, 0, 255)
        one_T.enableRegExpValidator(ProcessorModel.ThreeDDxfModel.LineNameCol, ProcessorModel.ThreeDDxfModel.LineNameCol, "^[a-zA-Z0-9_.-]*$")
          
        one_T.setHelpBar(self.helpBar)
        one_T.setHelpText(ProcessorModel.ThreeDDxfModel.LineNameCol, _('ThreeDDxf-LineNameDesc'))
        one_T.setHelpText(ProcessorModel.ThreeDDxfModel.ColorCodeCol, _('ThreeDDxf-ColorCodeDesc'))
        one_T.setHelpText(ProcessorModel.ThreeDDxfModel.ColorNameCol, _('ThreeDDxf-ColorNameDesc'))
        
        two_T = TableView()
        two_T.setModel( self.threeDDxf_M )
        two_T.verticalHeader().setVisible(False)
        two_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        two_T.hideColumn( self.threeDDxf_M.columnCount()-1 )
        two_T.hideColumn( self.threeDDxf_M.columnCount()-2 )
        two_T.hideColumn( 0 )
        for l in range (0, 6):
            two_T.hideRow(l)
        two_T.setFixedHeight(2 + two_T.horizontalHeader().height() + 3*two_T.rowHeight(6))
        self.windowLayout.addWidget(two_T)
         
        two_T.enableRegExpValidator(ProcessorModel.ThreeDDxfModel.LineNameCol, ProcessorModel.ThreeDDxfModel.LineNameCol, "^[a-zA-Z0-9_.-]*$")
        two_T.enableIntValidator(ProcessorModel.ThreeDDxfModel.UnifilarCol, ProcessorModel.ThreeDDxfModel.UnifilarCol, 0, 1)
        two_T.enableIntValidator(ProcessorModel.ThreeDDxfModel.ColorCodeCol, ProcessorModel.ThreeDDxfModel.ColorCodeCol, 0, 255)
        two_T.enableRegExpValidator(ProcessorModel.ThreeDDxfModel.LineNameCol, ProcessorModel.ThreeDDxfModel.LineNameCol, "^[a-zA-Z0-9_.-]*$")
          
        two_T.setHelpBar(self.helpBar)
        two_T.setHelpText(ProcessorModel.ThreeDDxfModel.LineNameCol, _('ThreeDDxf-LineNameDesc'))
        two_T.setHelpText(ProcessorModel.ThreeDDxfModel.UnifilarCol, _('ThreeDDxf-UnifilarDesc'))
        two_T.setHelpText(ProcessorModel.ThreeDDxfModel.ColorCodeCol, _('ThreeDDxf-ColorCodeDesc'))
        two_T.setHelpText(ProcessorModel.ThreeDDxfModel.ColorNameCol, _('ThreeDDxf-ColorNameDesc'))       

        self.usageUpdate()
         
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/threeDDxf.html')
        
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
        
        if self.threeDDxf_M.isUsed():
            self.usage_CB.setCurrentIndex(1)
        else:
            self.usage_CB.setCurrentIndex(0)
            
    def usageCbChange(self):
        '''
        :method: Updates the model as soon the usage CB has been changed
        '''
        logging.debug(self.__className+'.usageCbChange')
        if self.usage_CB.currentIndex() == 0:
            self.threeDDxf_M.setIsUsed(False)
        else:
            self.threeDDxf_M.setIsUsed(True)
            
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
    