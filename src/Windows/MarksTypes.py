'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, \
    QHBoxLayout, QVBoxLayout
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class MarksTypes(QMdiSubWindow):
    '''
    :class: Window to display and edit Brake line details  
    '''

    __className = 'MarksTypes'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.marksT_M = ProcessorModel.MarksTypesModel()
        self.marksT_M.numRowsForConfigChanged.connect( self.modelSizeChanged )
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
                    numLinesSpin
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
        self.win.setMinimumSize(900, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Marks types"))
        
        numLines_L = QLabel(_('Number of marks'))
        numLines_L.setAlignment(Qt.AlignRight)
        numLines_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
        self.numLines_S = QSpinBox()
        self.numLines_S.setRange(0,10)
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
        
        marksTypes_T = TableView()
        marksTypes_T.setModel( self.marksT_M )
        marksTypes_T.verticalHeader().setVisible(False)
        marksTypes_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        marksTypes_T.hideColumn( self.marksT_M.columnCount()-1 )
        marksTypes_T.hideColumn( self.marksT_M.columnCount()-2 )
        marksTypes_T.hideColumn( 0 )
        self.windowLayout.addWidget(marksTypes_T)
         
        marksTypes_T.enableRegExpValidator(ProcessorModel.MarksTypesModel.TypeCol, ProcessorModel.MarksTypesModel.TypeCol, "^[a-zA-Z0-9_.-]*$")
        marksTypes_T.enableIntValidator(ProcessorModel.MarksTypesModel.FormOneCol, ProcessorModel.MarksTypesModel.FormOneCol, 1, 3)
        marksTypes_T.enableDoubleValidator(ProcessorModel.MarksTypesModel.FormOnePOneCol, ProcessorModel.MarksTypesModel.FormOnePTwoCol, 0, 100, 2)
        marksTypes_T.enableIntValidator(ProcessorModel.MarksTypesModel.FormTwoCol, ProcessorModel.MarksTypesModel.FormTwoCol, 1, 3)
        marksTypes_T.enableDoubleValidator(ProcessorModel.MarksTypesModel.FormTwoPOneCol, ProcessorModel.MarksTypesModel.FormTwoPTwoCol, 0, 100, 2)
          
        marksTypes_T.setHelpBar(self.helpBar)
        marksTypes_T.setHelpText(ProcessorModel.MarksTypesModel.TypeCol, _('MarksTypes-TypeDesc'))
        marksTypes_T.setHelpText(ProcessorModel.MarksTypesModel.FormOneCol, _('MarksTypes-FormOneDesc'))
        marksTypes_T.setHelpText(ProcessorModel.MarksTypesModel.FormOnePOneCol, _('MarksTypes-FormOnePOneDesc'))
        marksTypes_T.setHelpText(ProcessorModel.MarksTypesModel.FormOnePTwoCol, _('MarksTypes-FormOnePTwoDesc'))
        marksTypes_T.setHelpText(ProcessorModel.MarksTypesModel.FormTwoCol, _('MarksTypes-FormTwoDesc'))
        marksTypes_T.setHelpText(ProcessorModel.MarksTypesModel.FormTwoPOneCol, _('MarksTypes-FormTwoPOneDesc'))
        marksTypes_T.setHelpText(ProcessorModel.MarksTypesModel.FormTwoPTwoCol, _('MarksTypes-FormTwoPTwoDesc'))
        
        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue( self.marksT_M.numRowsForConfig(1) )
        self.numLines_S.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/marksTypes.html')
        
        bottomLayout = QHBoxLayout()
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
        self.numLines_S.setValue( self.marksT_M.numRowsForConfig(1) )
        self.numLines_S.blockSignals(False)
        
                   
    def numLinesChange(self): 
        '''
        :method: Called upon manual changes of the lines spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.numLinesChange')
        self.marksT_M.setNumRowsForConfig(1, self.numLines_S.value() )
    
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
    