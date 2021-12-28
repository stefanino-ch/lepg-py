'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QHeaderView
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class SkinTension(QMdiSubWindow):
    '''
    :class: Window to display and edit Skin tension data  
    '''

    __className = 'SkinTension'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.skinTens_M = ProcessorModel.SkinTensionModel()
        self.skinTensParams_M = ProcessorModel.SkinTensionParamsModel()
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
                     paramsTable
                    ---------------------------
                                helpBar | btn_bar
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Skin tension"))
        
        table = TableView()
        table.setModel( self.skinTens_M )
        table.hideColumn(self.skinTens_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setHelpBar(self.helpBar)
        
        table.setHelpText(ProcessorModel.SkinTensionModel.TopDistLECol, _('SkinTension-TopDistLEDesc'))
        table.setHelpText(ProcessorModel.SkinTensionModel.TopWideCol, _('SkinTension-TopOverWideDesc'))
        table.setHelpText(ProcessorModel.SkinTensionModel.BottDistTECol, _('SkinTension-BottDistTEDesc'))
        table.setHelpText(ProcessorModel.SkinTensionModel.BottWideCol, _('SkinTension-BottOverWideDesc'))

        table.enableDoubleValidator(ProcessorModel.SkinTensionModel.TopDistLECol, ProcessorModel.SkinTensionModel.BottWideCol, 0, 100, 3)
        table.setFixedHeight(2 + table.horizontalHeader().height() + 6*table.rowHeight(0))
        self.windowLayout.addWidget(table)

        paramsTable = TableView()
        paramsTable.setModel( self.skinTensParams_M )
        paramsTable.hideColumn(self.skinTensParams_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        paramsTable.verticalHeader().setVisible(False)
        paramsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        paramsTable.setHelpBar(self.helpBar)
        
        paramsTable.setHelpText(ProcessorModel.SkinTensionParamsModel.StrainMiniRibsCol, _('SkinTension-StrainMiniRibsDesc'))
        paramsTable.setHelpText(ProcessorModel.SkinTensionParamsModel.NumPointsCol, _('SkinTension-NumPointsDesc'))
        paramsTable.setHelpText(ProcessorModel.SkinTensionParamsModel.CoeffCol, _('SkinTension-CoeffDesc'))

        paramsTable.enableDoubleValidator(ProcessorModel.SkinTensionParamsModel.StrainMiniRibsCol, ProcessorModel.SkinTensionParamsModel.StrainMiniRibsCol, 0, 100, 3)
        paramsTable.enableIntValidator(ProcessorModel.SkinTensionParamsModel.NumPointsCol, ProcessorModel.SkinTensionParamsModel.NumPointsCol, 0, 1000)
        paramsTable.enableDoubleValidator(ProcessorModel.SkinTensionParamsModel.CoeffCol, ProcessorModel.SkinTensionParamsModel.CoeffCol, 0, 1, 1)
        
        paramsLayout = QHBoxLayout()
        paramsLayout.addWidget(paramsTable)
        paramsLayout.addStretch()
        paramsTable.setFixedWidth( 2 + 3*paramsTable.columnWidth(0) + 2*paramsTable.columnWidth(1) + 2*paramsTable.columnWidth(2) )
        paramsTable.setFixedHeight(2 + paramsTable.horizontalHeader().height() + paramsTable.rowHeight(0))
        self.windowLayout.addLayout(paramsLayout)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/skinTension.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()        
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)
    
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
    