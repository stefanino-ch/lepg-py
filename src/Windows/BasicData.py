'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy,  QVBoxLayout, QHeaderView, QHBoxLayout
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class BasicData(QMdiSubWindow):
    '''
    :class: Window to display and edit the Basic Data  
    '''

    __className = 'ProcBasicData'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.wing_M = ProcessorModel.WingModel()
        self.wing_M.dataChanged.connect(self.checkNumCellsRibs)

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
                window_ly
                     Tables
                    -------------------------
                                | helpBar
                                | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(400, 300)

        self.window_Ly = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Basic Data"))
        
        # Brand name
        brandName_T = TableView()
        brandName_T.setModel( self.wing_M )
        
        for i in range (ProcessorModel.WingModel.WingNameCol, self.wing_M.columnCount() ):
            brandName_T.hideColumn(i)
        brandName_T.verticalHeader().setVisible(False)
        brandName_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        brandName_T.setFixedHeight(2 + brandName_T.horizontalHeader().height() + brandName_T.rowHeight(0))
        
        brandName_T.setHelpBar(self.helpBar)
        brandName_T.setHelpText(ProcessorModel.WingModel.BrandNameCol, _('Proc-BrandNameDesc'))
        
        brandName_T.enableRegExpValidator(ProcessorModel.WingModel.BrandNameCol, ProcessorModel.WingModel.BrandNameCol, "(.|\s)*\S(.|\s)*")
        
        self.window_Ly.addWidget(brandName_T)          
        
        # Wing name
        wingName_T = TableView()
        wingName_T.setModel( self.wing_M )
        
        wingName_T.hideColumn(0)
        for i in range (ProcessorModel.WingModel.DrawScaleCol, self.wing_M.columnCount() ):
            wingName_T.hideColumn(i)
        wingName_T.verticalHeader().setVisible(False)
        wingName_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        wingName_T.setFixedHeight(2 + wingName_T.horizontalHeader().height() + wingName_T.rowHeight(0))
        
        wingName_T.setHelpBar(self.helpBar)
        wingName_T.setHelpText(ProcessorModel.WingModel.WingNameCol, _('Proc-WingNameDesc'))
        
        wingName_T.enableRegExpValidator(ProcessorModel.WingModel.WingNameCol, ProcessorModel.WingModel.WingNameCol, "(.|\s)*\S(.|\s)*")
        
        self.window_Ly.addWidget(wingName_T)        
        
        # Scales
        scales_T = TableView()
        scales_T.setModel( self.wing_M )
        
        for i in range (ProcessorModel.WingModel.BrandNameCol, ProcessorModel.WingModel.WingNameCol+1 ):
            scales_T.hideColumn(i)
        for i in range (ProcessorModel.WingModel.NumCellsCol, self.wing_M.columnCount() ):
            scales_T.hideColumn(i)
        scales_T.verticalHeader().setVisible(False)
        scales_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        scales_T.setFixedHeight(2 + scales_T.horizontalHeader().height() + scales_T.rowHeight(0))
        
        scales_T.setHelpBar(self.helpBar)
        scales_T.setHelpText(ProcessorModel.WingModel.DrawScaleCol, _('Proc-DrawScaleDesc'))
        scales_T.setHelpText(ProcessorModel.WingModel.WingScaleCol, _('Proc-WingScaleDesc'))
        
        scales_T.enableDoubleValidator(ProcessorModel.WingModel.DrawScaleCol, ProcessorModel.WingModel.WingScaleCol, 0, 10, 2)
       
        self.window_Ly.addWidget(scales_T)
        
        # numbers
        self.numbers_T = TableView()
        self.numbers_T.setModel( self.wing_M )
        
        for i in range (ProcessorModel.WingModel.BrandNameCol, ProcessorModel.WingModel.WingScaleCol+1 ):
            self.numbers_T.hideColumn(i)
        for i in range (ProcessorModel.WingModel.AlphaMaxTipCol, self.wing_M.columnCount() ):
            self.numbers_T.hideColumn(i)
        self.numbers_T.verticalHeader().setVisible(False)
        self.numbers_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.numbers_T.setFixedHeight(2 + self.numbers_T.horizontalHeader().height() + self.numbers_T.rowHeight(0))
        
        self.numbers_T.setHelpBar(self.helpBar)
        self.numbers_T.setHelpText(ProcessorModel.WingModel.NumCellsCol, _('Proc-NumCellsDesc'))
        self.numbers_T.setHelpText(ProcessorModel.WingModel.NumRibsCol, _('Proc-NumRibsDesc'))
        
        self.numbers_T.enableIntValidator(ProcessorModel.WingModel.NumCellsCol, ProcessorModel.WingModel.NumRibsCol, 1, 999)
       
        self.window_Ly.addWidget(self.numbers_T)

        # alpha max and param
        self.alpha_T = TableView()
        self.alpha_T.setModel( self.wing_M )
        
        for i in range (ProcessorModel.WingModel.BrandNameCol, ProcessorModel.WingModel.NumRibsCol+1 ):
            self.alpha_T.hideColumn(i)
        for i in range (ProcessorModel.WingModel.ParaTypeCol, self.wing_M.columnCount() ):
            self.alpha_T.hideColumn(i)
        self.alpha_T.verticalHeader().setVisible(False)
        self.alpha_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.alpha_T.setFixedHeight(2 + self.alpha_T.horizontalHeader().height() + self.alpha_T.rowHeight(0))
        
        self.alpha_T.setHelpBar(self.helpBar)
        self.alpha_T.setHelpText(ProcessorModel.WingModel.AlphaModeCol, _('Proc-AlphaModeDesc'))
        self.alpha_T.setHelpText(ProcessorModel.WingModel.AlphaMaxCentCol, _('Proc-AlphaMaxCentDesc'))
        self.alpha_T.setHelpText(ProcessorModel.WingModel.AlphaMaxTipCol, _('Proc-AlphaMaxTipDesc'))
        
        self.alpha_T.enableDoubleValidator(ProcessorModel.WingModel.AlphaMaxTipCol, ProcessorModel.WingModel.AlphaMaxTipCol, -10, -10, 1)
        self.alpha_T.enableIntValidator(ProcessorModel.WingModel.AlphaModeCol, ProcessorModel.WingModel.ParaParamCol, 0, 2)
        self.alpha_T.enableDoubleValidator(ProcessorModel.WingModel.AlphaMaxCentCol, ProcessorModel.WingModel.AlphaMaxCentCol, -10, -10, 1)
        
        self.window_Ly.addWidget(self.alpha_T)
        
        # para type and param
        self.type_T = TableView()
        self.type_T.setModel( self.wing_M )
        
        for i in range (ProcessorModel.WingModel.BrandNameCol, ProcessorModel.WingModel.AlphaMaxCentCol+1 ):
            self.type_T.hideColumn(i)
        for i in range (ProcessorModel.WingModel.LinesConcTypeCol, self.wing_M.columnCount() ):
            self.type_T.hideColumn(i)
        self.type_T.verticalHeader().setVisible(False)
        self.type_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.type_T.setFixedHeight(2 + self.type_T.horizontalHeader().height() + self.type_T.rowHeight(0))
        
        self.type_T.setHelpBar(self.helpBar)
        self.type_T.setHelpText(ProcessorModel.WingModel.ParaTypeCol, _('Proc-ParaTypeDesc'))
        self.type_T.setHelpText(ProcessorModel.WingModel.ParaParamCol, _('Proc-ParaParamDesc'))
        
        self.type_T.enableRegExpValidator(ProcessorModel.WingModel.ParaTypeCol, ProcessorModel.WingModel.ParaTypeCol, "(.|\s)*\S(.|\s)*")
        self.type_T.enableIntValidator(ProcessorModel.WingModel.ParaParamCol, ProcessorModel.WingModel.ParaParamCol, 0, 1)
       
        self.window_Ly.addWidget(self.type_T)
                   
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/basicData.html')
        
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()        
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.window_Ly.addLayout(bottomLayout)
        
        self.win.setLayout(self.window_Ly)
        
    def checkNumCellsRibs(self, q):
        '''
        :method: The difference between NumCells and NumRibs must be 1, if this is not the case we have a nonsense setup
        ''' 
        logging.debug(self.__className + '.checkNumCellsRibs')
        
        if q.column() == self.wing_M.NumRibsCol or q.column() == self.wing_M.NumCellsCol:
            try:
                numCells = int(self.wing_M.index(0, self.wing_M.NumCellsCol).data())
                numRibs = int(self.wing_M.index(0, self.wing_M.NumRibsCol).data())
            except:
                return
            
            cells = isinstance(numCells, int)
            ribs = isinstance(numRibs, int)
                        
            if cells and ribs:
                diff = abs(numCells-numRibs)
                if diff == 1:
                    self.numbers_T.setStyleSheet(self.styleSheet())
                else:
                    self.numbers_T.setStyleSheet("border: 1px solid red")
               
    
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className + '.btnPress')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    