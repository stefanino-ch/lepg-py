'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QHeaderView, QPushButton
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.ProcessorModel import ProcessorModel

class ProcGeometry(QMdiSubWindow):
    '''
    :class: Window to display and edit geometry data  
    '''

    __className = 'ProcGeometry'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.rib_M = ProcessorModel.RibModel()
        self.dws = DataWindowStatus()
        self.buildWindow()
    
    def closeEvent(self, event):  # @UnusedVariable
        '''
        :method: Called at the time the user closes the window.
        '''
        logging.debug(self.__className+'.closeEvent') 
        
    def buildWindow(self):
        '''
        :method: Creates the window including all GUI elements. 
        
        Layout::
        
            Data
            Buttons
            
        Structure:: 
        
            win
                windowGrid 
                     Table
                    -------------------------
                                    | helpBar
                                    | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 300)

        self.windowGrid = QGridLayout()
        __winGRowL = 0
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Geometry"))
        
        self.table = TableView()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHelpBar(self.helpBar)
        self.table.setHelpText(0, _('Proc-RibNumDesc'))
        self.table.setHelpText(2, _('Proc-xribDesc'))
        self.table.setHelpText(3, _('Proc-yLEDesc'))
        self.table.setHelpText(4, _('Proc-yTEDesc'))
        self.table.setHelpText(5, _('Proc-xpDesc'))
        self.table.setHelpText(6, _('Proc-zDesc'))
        self.table.setHelpText(7, _('Proc-betaDesc'))
        self.table.setHelpText(8, _('Proc-RPDesc'))
        self.table.setHelpText(9, _('Proc-WashinDesc'))
        
        self.table.enableIntValidator(ProcessorModel.RibModel.RibNumCol, ProcessorModel.RibModel.RibNumCol, 1, 999)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.xribCol, ProcessorModel.RibModel.xribCol, -500, 3000, 2)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.yLECol, ProcessorModel.RibModel.yTECol, -500, 1000, 2)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.xpCol, ProcessorModel.RibModel.xpCol, -500, 3000, 2)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.zCol, ProcessorModel.RibModel.zCol, -500, 3000, 2)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.betaCol, ProcessorModel.RibModel.betaCol, 75, 105, 2)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.RPCol, ProcessorModel.RibModel.RPCol, 0, 100, 2)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.WashinCol, ProcessorModel.RibModel.WashinCol, -10, 10, 2)
        
        self.windowGrid.addWidget(self.table, __winGRowL, 0)
        __winGRowL += 1
        
        self.sortBtn = QPushButton(_('Sort by Rib Number'))
        self.sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.sortBtn.clicked.connect(self.sortBtnPress)
        self.windowGrid.addWidget(self.sortBtn,__winGRowL,0)
        __winGRowL += 1
        
        self.table.setModel( self.rib_M )

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        # @TODO: setup and enable user help
        #self.btnBar.setHelpPage('preproc/preproc.html')
        
        self.windowGrid.addWidget(self.helpBar, __winGRowL, 0, alignment= Qt.AlignRight)
        __winGRowL += 1
        self.windowGrid.addWidget(self.btnBar, __winGRowL, 0, alignment=  Qt.AlignRight)
        
        self.win.setLayout(self.windowGrid)
    
    def sortBtnPress(self):
        '''
        : method : handles the sort of the table by rib number
        '''
        logging.debug(self.__className+'.sortBtnPress')
        self.rib_M.sortTable(ProcessorModel.RibModel.RibNumCol, Qt.AscendingOrder)
    
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className+'.btnPress')
        if q == 'Apply':
            print('apply')
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    