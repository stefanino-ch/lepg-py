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

class ProcAirfoils(QMdiSubWindow):
    '''
    :class: Window to display and edit airfoils data  
    '''

    __className = 'ProcAirfoils'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.airf_M = ProcessorModel.AirfoilsModel()
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
                     SortBtn        | helpBar
                                    | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 300)

        self.windowGrid = QGridLayout()
        __winGRowL = 0
        __winGRowR = 0
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Airfoils"))
        
        self.table = TableView()
        self.table.setModel( self.airf_M )
        self.table.hideColumn(self.airf_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHelpBar(self.helpBar)
        self.table.setHelpText(ProcessorModel.AirfoilsModel.RibNumCol, _('Proc-RibNumDesc'))
        self.table.setHelpText(ProcessorModel.AirfoilsModel.AirfNameCol, _('Proc-AirfoilNameDesc'))
        self.table.setHelpText(ProcessorModel.AirfoilsModel.IntakeStartCol, _('Proc-IntakeStartDesc'))
        self.table.setHelpText(ProcessorModel.AirfoilsModel.IntakeEndCol, _('Proc-IntakeEnDesc'))
        self.table.setHelpText(ProcessorModel.AirfoilsModel.OpenCloseCol, _('Proc-OpenCloseDesc'))
        self.table.setHelpText(ProcessorModel.AirfoilsModel.DisplacCol, _('Proc-DisplacDesc'))
        self.table.setHelpText(ProcessorModel.AirfoilsModel.RelWeightCol, _('Proc-RelWeightDesc'))
        self.table.setHelpText(ProcessorModel.AirfoilsModel.rrwCol, _('Proc-rrwDesc'))
        
        self.table.enableIntValidator(ProcessorModel.AirfoilsModel.RibNumCol, ProcessorModel.AirfoilsModel.RibNumCol, 1, 999)
        self.table.enableRegExpValidator(ProcessorModel.AirfoilsModel.AirfNameCol, ProcessorModel.AirfoilsModel.AirfNameCol, "(.|\s)*\S(.|\s)*")
        self.table.enableDoubleValidator(ProcessorModel.AirfoilsModel.IntakeStartCol, ProcessorModel.AirfoilsModel.IntakeEndCol, 0, 100, 2)
        self.table.enableIntValidator(ProcessorModel.AirfoilsModel.OpenCloseCol, ProcessorModel.AirfoilsModel.OpenCloseCol, 0, 1)
        self.table.enableDoubleValidator(ProcessorModel.AirfoilsModel.DisplacCol, ProcessorModel.AirfoilsModel.DisplacCol, 0, 3000, 2)
        self.table.enableDoubleValidator(ProcessorModel.AirfoilsModel.RelWeightCol,ProcessorModel.AirfoilsModel.rrwCol, 0, 100, 2)
        
        self.windowGrid.addWidget(self.table, __winGRowL, 0, 1, 2)
        __winGRowL += 1
        __winGRowR += 1
        
        self.sortBtn = QPushButton(_('Sort by Rib Number'))
        self.sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.sortBtn.clicked.connect(self.sortBtnPress)
        self.windowGrid.addWidget(self.sortBtn,__winGRowL,0,Qt.AlignTop)
        __winGRowL += 1
        

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        # @TODO: setup and enable user help
        #self.btnBar.setHelpPage('preproc/preproc.html')
        
        self.windowGrid.addWidget(self.helpBar, __winGRowR, 1, alignment= Qt.AlignRight)
        __winGRowR += 1
        self.windowGrid.addWidget(self.btnBar, __winGRowR, 1, alignment=  Qt.AlignRight)
        
        self.win.setLayout(self.windowGrid)
    
    def sortBtnPress(self):
        '''
        : method : handles the sort of the table by rib number
        '''
        logging.debug(self.__className+'.sortBtnPress')
        self.airf_M.sortTable(ProcessorModel.AirfoilsModel.RibNumCol, Qt.AscendingOrder)
    
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
    