'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, QGridLayout, QLabel, QWidget, QHeaderView
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class Ramification(QMdiSubWindow):
    '''
    :class: Window to display and edit Seewing allowances data  
    '''

    __className = 'Ramification'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.ramif_M = ProcessorModel.RamificationModel()
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
                    editGrid_L
                        threeLineRows_T
                        FourLineRows_T
                        ThreeBrakeRows_T
                        fourBrakeRows_T
                ---------------------------
                            helpBar | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(450, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Ramification"))
        
        editGrid_L = QGridLayout()
        
        ##### 3 line rows
        threeLineRows_L = QLabel(_('3 Line rows'))
        threeLineRows_L.setAlignment(Qt.AlignRight)
        
        threeLineRows_T = TableView()
        threeLineRows_T.setModel( self.ramif_M )
        threeLineRows_T.hideRow(1)
        threeLineRows_T.hideRow(2)
        threeLineRows_T.hideRow(3)
        
        threeLineRows_T.hideColumn( 0 ) # hide the OrderNum column
        threeLineRows_T.hideColumn( 1 ) # hide the Rows column
        threeLineRows_T.hideColumn(self.ramif_M.columnCount() -1 ) # hide the ID column
        threeLineRows_T.hideColumn(self.ramif_M.columnCount() -2 ) # hide the Config column
        threeLineRows_T.hideColumn(self.ramif_M.columnCount() -3 ) # hide the Config column
        
        threeLineRows_T.verticalHeader().setVisible(False)
        threeLineRows_T.setHelpBar(self.helpBar)
        
        #threeLineRows_T.setHelpText(ProcessorModel.RamificationModel.RowsCol, _('Ramification-RowsDesc'))
        threeLineRows_T.setHelpText(ProcessorModel.RamificationModel.ThirdToSailCol, _('Ramification-3L-ThirdLineToSailDesc'))

        #threeLineRows_T.enableIntValidator(ProcessorModel.RamificationModel.RowsCol, ProcessorModel.RamificationModel.RowsCol, 3, 4)
        threeLineRows_T.enableIntValidator(ProcessorModel.RamificationModel.ThirdToSailCol, ProcessorModel.RamificationModel.ThirdToSailCol, 1, 2000)
        
        threeLineRows_T.setFixedHeight(2 + threeLineRows_T.horizontalHeader().height() + threeLineRows_T.rowHeight(0))
        threeLineRows_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        editGrid_L.addWidget(threeLineRows_L,0,0)
        editGrid_L.addWidget(threeLineRows_T,0,1)
        editGrid_L.addWidget(QWidget(),0,2)
        editGrid_L.addWidget(QWidget(),0,3)
        
        ##### 4 line rows
        fourLineRows_L = QLabel(_('4 Line rows'))
        fourLineRows_L.setAlignment(Qt.AlignRight)
        
        fourLineRows_T = TableView()
        fourLineRows_T.setModel( self.ramif_M )
        fourLineRows_T.hideRow(0)
        fourLineRows_T.hideRow(2)
        fourLineRows_T.hideRow(3)
        
        fourLineRows_T.hideColumn( 0 ) # hide the OrderNum column
        fourLineRows_T.hideColumn( 1 ) # hide the Rows column
        fourLineRows_T.hideColumn(self.ramif_M.columnCount() -1 ) # hide the ID column
        fourLineRows_T.hideColumn(self.ramif_M.columnCount() -2 ) # hide the Config column
        
        fourLineRows_T.verticalHeader().setVisible(False)
        fourLineRows_T.setHelpBar(self.helpBar)
        
        # fourLineRows_T.setHelpText(ProcessorModel.RamificationModel.RowsCol, _('Ramification-RowsDesc'))
        fourLineRows_T.setHelpText(ProcessorModel.RamificationModel.ThirdToSailCol, _('Ramification-4L-ThirdLineToSailDesc'))
        fourLineRows_T.setHelpText(ProcessorModel.RamificationModel.FourthToSailCol, _('Ramification-4L-FourthLineToSailDesc'))

        # fourLineRows_T.enableIntValidator(ProcessorModel.RamificationModel.RowsCol, ProcessorModel.RamificationModel.RowsCol, 3, 4)
        fourLineRows_T.enableIntValidator(ProcessorModel.RamificationModel.ThirdToSailCol, ProcessorModel.RamificationModel.ThirdToSailCol, 1, 2000)
        fourLineRows_T.enableIntValidator(ProcessorModel.RamificationModel.FourthToSailCol, ProcessorModel.RamificationModel.FourthToSailCol, 1, 2000)
        
        fourLineRows_T.setFixedHeight(2 + fourLineRows_T.horizontalHeader().height() + fourLineRows_T.rowHeight(1))
        fourLineRows_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        editGrid_L.addWidget(fourLineRows_L,1,0)
        editGrid_L.addWidget(fourLineRows_T,1,1,1,2)
        editGrid_L.addWidget(QWidget(),1,3)
        
        ##### 3 brake rows
        threeBrakeRows_L = QLabel(_('3 Brake rows'))
        threeBrakeRows_L.setAlignment(Qt.AlignRight)
        
        threeBrakeRows_T = TableView()
        threeBrakeRows_T.setModel( self.ramif_M )
        threeBrakeRows_T.hideRow(0)
        threeBrakeRows_T.hideRow(1)
        threeBrakeRows_T.hideRow(3)
        
        threeBrakeRows_T.hideColumn( 0 ) # hide the OrderNum column
        threeBrakeRows_T.hideColumn( 1 ) # hide the Rows column
        threeBrakeRows_T.hideColumn(self.ramif_M.columnCount() -1 ) # hide the ID column
        threeBrakeRows_T.hideColumn(self.ramif_M.columnCount() -2 ) # hide the Config column
        threeBrakeRows_T.hideColumn(self.ramif_M.columnCount() -3 ) # hide the Config column
        threeBrakeRows_T.verticalHeader().setVisible(False)
        threeBrakeRows_T.setHelpBar(self.helpBar)
        
        # threeBrakeRows_T.setHelpText(ProcessorModel.RamificationModel.RowsCol, _('Ramification-RowsDesc'))
        threeBrakeRows_T.setHelpText(ProcessorModel.RamificationModel.ThirdToSailCol, _('Ramification-3L-ThirdBrakeToSailDesc'))

        # threeBrakeRows_T.enableIntValidator(ProcessorModel.RamificationModel.RowsCol, ProcessorModel.RamificationModel.RowsCol, 3, 4)
        threeBrakeRows_T.enableIntValidator(ProcessorModel.RamificationModel.ThirdToSailCol, ProcessorModel.RamificationModel.ThirdToSailCol, 1, 2000)
        
        threeBrakeRows_T.setFixedHeight(2 + threeBrakeRows_T.horizontalHeader().height() + threeBrakeRows_T.rowHeight(2))
        threeBrakeRows_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        editGrid_L.addWidget(threeBrakeRows_L,2,0)
        editGrid_L.addWidget(threeBrakeRows_T,2,1)
        editGrid_L.addWidget(QWidget(),2,2)
        editGrid_L.addWidget(QWidget(),2,3)
        
        ##### 4 brake rows
        fourBrakeRows_L = QLabel(_('4 Brake rows'))
        fourBrakeRows_L.setAlignment(Qt.AlignRight)
        
        fourBrakeRows_T = TableView()
        fourBrakeRows_T.setModel( self.ramif_M )
        fourBrakeRows_T.hideRow(0)
        fourBrakeRows_T.hideRow(1)
        fourBrakeRows_T.hideRow(2)
        
        fourBrakeRows_T.hideColumn( 0 ) # hide the OrderNum column
        fourBrakeRows_T.hideColumn( 1 ) # hide the Rows column
        fourBrakeRows_T.hideColumn(self.ramif_M.columnCount() -1 ) # hide the ID column
        fourBrakeRows_T.hideColumn(self.ramif_M.columnCount() -2 ) # hide the Config column
        fourBrakeRows_T.verticalHeader().setVisible(False)
        fourBrakeRows_T.setHelpBar(self.helpBar)
        
        # fourBrakeRows_T.setHelpText(ProcessorModel.RamificationModel.RowsCol, _('Ramification-RowsDesc'))
        fourBrakeRows_T.setHelpText(ProcessorModel.RamificationModel.ThirdToSailCol, _('Ramification-4L-ThirdBrakeToSailDesc'))
        fourBrakeRows_T.setHelpText(ProcessorModel.RamificationModel.FourthToSailCol, _('Ramification-4L-FourthBrakeToSailDesc'))

        # fourBrakeRows_T.enableIntValidator(ProcessorModel.RamificationModel.RowsCol, ProcessorModel.RamificationModel.RowsCol, 3, 4)
        fourBrakeRows_T.enableIntValidator(ProcessorModel.RamificationModel.ThirdToSailCol, ProcessorModel.RamificationModel.ThirdToSailCol, 1, 2000)
        fourBrakeRows_T.enableIntValidator(ProcessorModel.RamificationModel.FourthToSailCol, ProcessorModel.RamificationModel.FourthToSailCol, 1, 2000)
        
        fourBrakeRows_T.setFixedHeight(2 + fourBrakeRows_T.horizontalHeader().height() + fourBrakeRows_T.rowHeight(3))
        fourBrakeRows_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        editGrid_L.addWidget(fourBrakeRows_L,3,0)
        editGrid_L.addWidget(fourBrakeRows_T,3,1,1,2)
        editGrid_L.addWidget(QWidget(),3,3)

        self.windowLayout.addLayout(editGrid_L)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/ramification.html')

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
        logging.debug(self.__className+'.btnPress')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    