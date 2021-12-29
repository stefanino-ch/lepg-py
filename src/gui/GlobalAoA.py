'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QHeaderView
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class GlobalAoA(QMdiSubWindow):
    '''
    :class: Window to display and edit global AoA data  
    '''

    __className = 'GlobalAoA'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.globAoA_M = ProcessorModel.GlobAoAModel()
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
                    calage_T
                    length_T
                ---------------------------
                            help_bar | btn_bar
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(250, 200)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Global AoA"))

        calage_T = TableView()
        calage_T.setModel( self.globAoA_M )
      
        calage_T.hideColumn(self.globAoA_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        calage_T.verticalHeader().setVisible(False)
        calage_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        calage_T.setHelpBar(self.helpBar)
        calage_T.hideColumn(3)
        calage_T.hideColumn(4)
        calage_T.hideColumn(5)
        
        calage_T.setHelpText(ProcessorModel.GlobAoAModel.FinesseCol, _('GlobalAoA-FinesseDesc'))
        calage_T.setHelpText(ProcessorModel.GlobAoAModel.CentOfPressCol, _('GlobalAoA-CenterOfPressureDesc'))
        calage_T.setHelpText(ProcessorModel.GlobAoAModel.CalageCol, _('GlobalAoA-CalageDesc'))

        calage_T.enableDoubleValidator(ProcessorModel.GlobAoAModel.FinesseCol, ProcessorModel.GlobAoAModel.FinesseCol, 0, 100, 2)
        calage_T.enableIntValidator(ProcessorModel.GlobAoAModel.CentOfPressCol, ProcessorModel.GlobAoAModel.CalageCol, 0, 100)
                
        calage_T.setFixedHeight(2 + calage_T.horizontalHeader().height() + calage_T.rowHeight(0))

        self.windowLayout.addWidget(calage_T)
        
        #####
        lenght_T = TableView()
        lenght_T.setModel( self.globAoA_M )
      
        lenght_T.hideColumn(self.globAoA_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        lenght_T.verticalHeader().setVisible(False)
        lenght_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        lenght_T.setHelpBar(self.helpBar)
        lenght_T.hideColumn(0)
        lenght_T.hideColumn(1)
        lenght_T.hideColumn(2)
        
        lenght_T.setHelpText(ProcessorModel.GlobAoAModel.RisersCol, _('GlobalAoA-RisersDesc'))
        lenght_T.setHelpText(ProcessorModel.GlobAoAModel.LinesCol, _('GlobalAoA-LinesDesc'))
        lenght_T.setHelpText(ProcessorModel.GlobAoAModel.KarabinersCol, _('GlobalAoA-KarabinersDesc'))

        lenght_T.enableIntValidator(ProcessorModel.GlobAoAModel.RisersCol, ProcessorModel.GlobAoAModel.LinesCol, 0, 2000)
        lenght_T.enableIntValidator(ProcessorModel.GlobAoAModel.KarabinersCol, ProcessorModel.GlobAoAModel.KarabinersCol, 0, 100)
                
        lenght_T.setFixedHeight(2 + lenght_T.horizontalHeader().height() + lenght_T.rowHeight(0))

        self.windowLayout.addWidget(lenght_T)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/globalAoA.html')

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
    