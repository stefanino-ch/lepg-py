'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QHeaderView, QPushButton
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class Airfoils(QMdiSubWindow):
    '''
    :class: Window to display and edit airfoils data  
    '''

    __className = 'Airfoils'
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
                windowLayout 
                     Table
                    ---------------------------
                     SortBtn | helpBar | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 300)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Airfoils"))
        
        self.table = TableView()
        self.table.setModel( self.airf_M )
        self.table.hideColumn(self.airf_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        self.table.verticalHeader().setVisible(False)
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
        self.table.enableDoubleValidator(ProcessorModel.AirfoilsModel.IntakeStartCol, ProcessorModel.AirfoilsModel.IntakeEndCol, 0, 100, 3)
        self.table.enableIntValidator(ProcessorModel.AirfoilsModel.OpenCloseCol, ProcessorModel.AirfoilsModel.OpenCloseCol, 0, 1)
        self.table.enableDoubleValidator(ProcessorModel.AirfoilsModel.DisplacCol, ProcessorModel.AirfoilsModel.DisplacCol, 0, 3000, 3)
        self.table.enableDoubleValidator(ProcessorModel.AirfoilsModel.RelWeightCol,ProcessorModel.AirfoilsModel.rrwCol, 0, 100, 3)
        
        self.windowLayout.addWidget(self.table)
        
        self.sortBtn = QPushButton(_('Sort by Rib Number'))
        self.sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.sortBtn.clicked.connect(self.sortBtnPress)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/airfoils.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.sortBtn)
        bottomLayout.addStretch()        
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)
    
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
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    