'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, \
    QGridLayout, QLabel, QWidget
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class SeewingAllowances(QMdiSubWindow):
    '''
    :class: Window to display and edit Seewing allowances data  
    '''

    __className = 'SeewingAllowances'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.sewAll_M = ProcessorModel.SewingAllowancesModel()
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
                         uppeP_T
                         lowerP_T
                         ribs_t
                         vRibsT
                ---------------------------
                            helpBar | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(450, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Sewing allowances"))
        
        editGrid_L = QGridLayout()
        
        
        ##### upper panel
        upperP_L = QLabel(_('Upper panel'))
        upperP_L.setAlignment(Qt.AlignRight)
        
        upperP_T = TableView()
        upperP_T.setModel( self.sewAll_M )
        upperP_T.hideRow(1)
        upperP_T.hideRow(2)
        upperP_T.hideRow(3)
        
        upperP_T.hideColumn(self.sewAll_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        upperP_T.verticalHeader().setVisible(False)
        upperP_T.setHelpBar(self.helpBar)
        
        upperP_T.setHelpText(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, _('SewingAllowances-EdgeSeamDesc'))
        upperP_T.setHelpText(ProcessorModel.SewingAllowancesModel.LeSeemCol, _('SewingAllowances-LeSeamDesc'))
        upperP_T.setHelpText(ProcessorModel.SewingAllowancesModel.TeSeemCol, _('SewingAllowances-TeSeamDesc'))

        upperP_T.enableIntValidator(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, ProcessorModel.SewingAllowancesModel.TeSeemCol, 1, 100)
        upperP_T.setFixedHeight(2 + upperP_T.horizontalHeader().height() + upperP_T.rowHeight(0))
        upperP_T.setFixedWidth(2 +upperP_T.columnWidth(0)+upperP_T.columnWidth(1)+upperP_T.columnWidth(2) )

        editGrid_L.addWidget(upperP_L,0,0)
        editGrid_L.addWidget(upperP_T,0,1)
        editGrid_L.addWidget(QWidget(),0,3)
        
        ##### lower panel
        lowerP_L = QLabel(_('Lower panel'))
        lowerP_L.setAlignment(Qt.AlignRight)
        
        lowerP_T = TableView()
        lowerP_T.setModel( self.sewAll_M )
        lowerP_T.hideRow(0)
        lowerP_T.hideRow(2)
        lowerP_T.hideRow(3)
        
        lowerP_T.hideColumn(self.sewAll_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        lowerP_T.verticalHeader().setVisible(False)
        lowerP_T.setHelpBar(self.helpBar)
        
        lowerP_T.setHelpText(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, _('SewingAllowances-EdgeSeamDesc'))
        lowerP_T.setHelpText(ProcessorModel.SewingAllowancesModel.LeSeemCol, _('SewingAllowances-LeSeamDesc'))
        lowerP_T.setHelpText(ProcessorModel.SewingAllowancesModel.TeSeemCol, _('SewingAllowances-TeSeamDesc'))

        lowerP_T.enableIntValidator(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, ProcessorModel.SewingAllowancesModel.TeSeemCol, 1, 100)
        lowerP_T.setFixedHeight(2 + upperP_T.horizontalHeader().height() + upperP_T.rowHeight(0))
        lowerP_T.setFixedWidth(2 +upperP_T.columnWidth(0)+upperP_T.columnWidth(1)+upperP_T.columnWidth(2) )

        editGrid_L.addWidget(lowerP_L,1,0)
        editGrid_L.addWidget(lowerP_T,1,1)
        editGrid_L.addWidget(QWidget(),1,3)
        
        ##### ribs panel
        ribs_L = QLabel(_('Ribs'))
        ribs_L.setAlignment(Qt.AlignRight)
        
        ribs_T = TableView()
        ribs_T.setModel( self.sewAll_M )
        ribs_T.hideRow(0)
        ribs_T.hideRow(1)
        ribs_T.hideRow(3)
        ribs_T.hideColumn(1)
        ribs_T.hideColumn(2)
        
        ribs_T.hideColumn(self.sewAll_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        ribs_T.verticalHeader().setVisible(False)
        ribs_T.setHelpBar(self.helpBar)
        
        ribs_T.setHelpText(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, _('SewingAllowances-RibsSeemDesc'))

        ribs_T.enableIntValidator(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, ProcessorModel.SewingAllowancesModel.EdgeSeamCol, 1, 100)
        ribs_T.setFixedHeight(2 + upperP_T.horizontalHeader().height() + upperP_T.rowHeight(0))
        ribs_T.setFixedWidth(2 +upperP_T.columnWidth(0) )

        editGrid_L.addWidget(ribs_L,2,0)
        editGrid_L.addWidget(ribs_T,2,1)
        editGrid_L.addWidget(QWidget(),2,3)
        
        ##### ribs panel
        vRibs_L = QLabel(_('V-Ribs'))
        vRibs_L.setAlignment(Qt.AlignRight)
        
        vRibs_T = TableView()
        vRibs_T.setModel( self.sewAll_M )
        vRibs_T.hideRow(0)
        vRibs_T.hideRow(1)
        vRibs_T.hideRow(2)
        vRibs_T.hideColumn(1)
        vRibs_T.hideColumn(2)
        
        vRibs_T.hideColumn(self.sewAll_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        vRibs_T.verticalHeader().setVisible(False)
        vRibs_T.setHelpBar(self.helpBar)
        
        vRibs_T.setHelpText(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, _('SewingAllowances-V-RibsSeemDesc'))

        vRibs_T.enableIntValidator(ProcessorModel.SewingAllowancesModel.EdgeSeamCol, ProcessorModel.SewingAllowancesModel.EdgeSeamCol, 1, 100)
        vRibs_T.setFixedHeight(2 + upperP_T.horizontalHeader().height() + upperP_T.rowHeight(0))
        vRibs_T.setFixedWidth(2 +upperP_T.columnWidth(0) )

        editGrid_L.addWidget(vRibs_L,3,0)
        editGrid_L.addWidget(vRibs_T,3,1)
        editGrid_L.addWidget(QWidget(),3,3)

        self.windowLayout.addLayout(editGrid_L)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/seewingAllowances.html')

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
    