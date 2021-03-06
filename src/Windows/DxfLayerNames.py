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

class DxfLayerNames(QMdiSubWindow):
    '''
    :class: Window to display and edit DXF Layer names  
    '''

    __className = 'DxfLayerNames'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.dxfLayNames_M = ProcessorModel.DxfLayerNamesModel()
        self.dxfLayNames_M.numRowsForConfigChanged.connect( self.modelSizeChanged )
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
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(550, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("DXF layer names"))
        
        numLines_L = QLabel(_('Number of layers'))
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
        
        dxfLayNames_T = TableView()
        dxfLayNames_T.setModel( self.dxfLayNames_M )
        dxfLayNames_T.verticalHeader().setVisible(False)
        dxfLayNames_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dxfLayNames_T.hideColumn( self.dxfLayNames_M.columnCount()-1 )
        dxfLayNames_T.hideColumn( self.dxfLayNames_M.columnCount()-2 )
        dxfLayNames_T.hideColumn( 0 )
        self.windowLayout.addWidget(dxfLayNames_T)
         
        dxfLayNames_T.enableRegExpValidator(ProcessorModel.DxfLayerNamesModel.LayerCol, ProcessorModel.DxfLayerNamesModel.DescriptionCol, "^[a-zA-Z0-9_.-]*$")
          
        dxfLayNames_T.setHelpBar(self.helpBar)
        dxfLayNames_T.setHelpText(ProcessorModel.DxfLayerNamesModel.LayerCol, _('DxfLayNames-LayerDesc'))
        dxfLayNames_T.setHelpText(ProcessorModel.DxfLayerNamesModel.DescriptionCol, _('DxfLayNames-DescriptionDesc'))
        
        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue( self.dxfLayNames_M.numRowsForConfig(1) )
        self.numLines_S.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/dxfLayerNames.html')
        
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
        self.numLines_S.setValue( self.dxfLayNames_M.numRowsForConfig(1) )
        self.numLines_S.blockSignals(False)
        
                   
    def numLinesChange(self): 
        '''
        :method: Called upon manual changes of the lines spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.numLinesChange')
        self.dxfLayNames_M.setNumRowsForConfig(1, self.numLines_S.value() )
    
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
    