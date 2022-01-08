'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QHeaderView, QPushButton
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.ProcModel import ProcModel

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
        
        self.airf_M = ProcModel.AirfoilsModel()
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
        
            window
                window_ly
                     Table
                    ---------------------------
                     SortBtn | help_bar | btn_bar
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
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
        self.table.setHelpText(ProcModel.AirfoilsModel.RibNumCol, _('Proc-RibNumDesc'))
        self.table.setHelpText(ProcModel.AirfoilsModel.AirfNameCol, _('Proc-AirfoilNameDesc'))
        self.table.setHelpText(ProcModel.AirfoilsModel.IntakeStartCol, _('Proc-IntakeStartDesc'))
        self.table.setHelpText(ProcModel.AirfoilsModel.IntakeEndCol, _('Proc-IntakeEnDesc'))
        self.table.setHelpText(ProcModel.AirfoilsModel.OpenCloseCol, _('Proc-OpenCloseDesc'))
        self.table.setHelpText(ProcModel.AirfoilsModel.DisplacCol, _('Proc-DisplacDesc'))
        self.table.setHelpText(ProcModel.AirfoilsModel.RelWeightCol, _('Proc-RelWeightDesc'))
        self.table.setHelpText(ProcModel.AirfoilsModel.rrwCol, _('Proc-rrwDesc'))
        
        self.table.enableIntValidator(ProcModel.AirfoilsModel.RibNumCol, ProcModel.AirfoilsModel.RibNumCol, 1, 999)
        self.table.enableRegExpValidator(ProcModel.AirfoilsModel.AirfNameCol, ProcModel.AirfoilsModel.AirfNameCol, "(.|\s)*\S(.|\s)*")
        self.table.enableDoubleValidator(ProcModel.AirfoilsModel.IntakeStartCol, ProcModel.AirfoilsModel.IntakeEndCol, 0, 100, 3)
        self.table.enableIntValidator(ProcModel.AirfoilsModel.OpenCloseCol, ProcModel.AirfoilsModel.OpenCloseCol, 0, 1)
        self.table.enableDoubleValidator(ProcModel.AirfoilsModel.DisplacCol, ProcModel.AirfoilsModel.DisplacCol, 0, 3000, 3)
        self.table.enableDoubleValidator(ProcModel.AirfoilsModel.RelWeightCol, ProcModel.AirfoilsModel.rrwCol, 0, 100, 3)
        
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
        logging.debug(self.__className+'.sort_btn_press')
        self.airf_M.sort_table(ProcModel.AirfoilsModel.RibNumCol, Qt.AscendingOrder)
    
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
    