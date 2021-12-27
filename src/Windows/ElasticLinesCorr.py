'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QLabel, QDataWidgetMapper,\
    QVBoxLayout, QHBoxLayout, QHeaderView
from Windows.gui_elements.LineEdit import LineEdit
from Windows.gui_elements.WindowHelpBar import WindowHelpBar
from Windows.gui_elements.WindowBtnBar import WindowBtnBar
from Windows.gui_elements.TableView import TableView
from DataStores.ProcessorModel import ProcessorModel

class ElasticLinesCorr(QMdiSubWindow):
    '''
    :class: Window to display and edit the Basic Data  
    '''

    __className = 'ElasticLinesCorr'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.elLinesCorr_M = ProcessorModel.ElasticLinesCorrModel()
        self.elLinesDef_M = ProcessorModel.ElasticLinesDefModel()

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
                windowGrid 
                     Labels    | Edit fields
                     ...       | ...
                    -------------------------
                                | helpBar
                                | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(300, 300)
        
        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        
        self.setWindowTitle(_("Elastic lines correction"))

        self.gridLayout = QGridLayout()
        __gridRow = 0
        
        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.elLinesCorr_M)
        
        load_L = QLabel(_('In flight load [kg]'))
        load_L.setAlignment(Qt.AlignRight)
        self.load_E = LineEdit()
        self.wrapper.addMapping(self.load_E, ProcessorModel.ElasticLinesCorrModel.LoadCol)
        self.load_E.enableDoubleValidator(0, 500, 2)
        self.load_E.setHelpText(_('ElLinesCorr-LoadDesc'))
        self.load_E.setHelpBar(self.helpBar)
        self.gridLayout.addWidget(load_L, __gridRow, 0)
        self.gridLayout.addWidget(self.load_E, __gridRow, 1)
        __gridRow += 1
        
        self.gridLayout.addWidget(QLabel(_('Load distr [%]')), __gridRow, 1)
        self.gridLayout.addWidget(QLabel(_('Load distr [%]')), __gridRow, 2)
        self.gridLayout.addWidget(QLabel(_('Load distr [%]')), __gridRow, 3)
        self.gridLayout.addWidget(QLabel(_('Load distr [%]')), __gridRow, 4)
        self.gridLayout.addWidget(QLabel(_('Load distr [%]')), __gridRow, 5)
        __gridRow += 1
        
        # Two Lines
        twoLineT_L = QLabel(_('Two Lines'))
        twoLineT_L.setAlignment(Qt.AlignRight)
        self.twoLineA_E = LineEdit()
        self.wrapper.addMapping(self.twoLineA_E, ProcessorModel.ElasticLinesCorrModel.TwoLineDistACol)
        self.twoLineA_E.enableDoubleValidator(0, 100, 2)
        self.twoLineA_E.setHelpText(_('ElLinesCorr-TwoLineDistDesc'))
        self.twoLineA_E.setHelpBar(self.helpBar)
        
        self.twoLineB_E = LineEdit()
        self.wrapper.addMapping(self.twoLineB_E, ProcessorModel.ElasticLinesCorrModel.TwoLineDistBCol)
        self.twoLineB_E.enableDoubleValidator(0, 100, 2)
        self.twoLineB_E.setHelpText(_('ElLinesCorr-TwoLineDistDesc'))
        self.twoLineB_E.setHelpBar(self.helpBar)
        
        self.gridLayout.addWidget(twoLineT_L, __gridRow, 0)
        self.gridLayout.addWidget(self.twoLineA_E, __gridRow, 1)
        self.gridLayout.addWidget(self.twoLineB_E, __gridRow, 2)
        __gridRow += 1
        
        # Three Lines
        threeLineT_L = QLabel(_('Three Lines'))
        threeLineT_L.setAlignment(Qt.AlignRight)
        self.threeLineA_E = LineEdit()
        self.wrapper.addMapping(self.threeLineA_E, ProcessorModel.ElasticLinesCorrModel.ThreeLineDistACol)
        self.threeLineA_E.enableDoubleValidator(0, 100, 2)
        self.threeLineA_E.setHelpText(_('ElLinesCorr-ThreeLineDistDesc'))
        self.threeLineA_E.setHelpBar(self.helpBar)
        
        self.threeLineB_E = LineEdit()
        self.wrapper.addMapping(self.threeLineB_E, ProcessorModel.ElasticLinesCorrModel.ThreeLineDistBCol)
        self.threeLineB_E.enableDoubleValidator(0, 100, 2)
        self.threeLineB_E.setHelpText(_('ElLinesCorr-ThreeLineDistDesc'))
        self.threeLineB_E.setHelpBar(self.helpBar)

        self.threeLineC_E = LineEdit()
        self.wrapper.addMapping(self.threeLineC_E, ProcessorModel.ElasticLinesCorrModel.ThreeLineDistCCol)
        self.threeLineC_E.enableDoubleValidator(0, 100, 2)
        self.threeLineC_E.setHelpText(_('ElLinesCorr-ThreeLineDistDesc'))
        self.threeLineC_E.setHelpBar(self.helpBar)
        
        self.gridLayout.addWidget(threeLineT_L, __gridRow, 0)
        self.gridLayout.addWidget(self.threeLineA_E, __gridRow, 1)
        self.gridLayout.addWidget(self.threeLineB_E, __gridRow, 2)
        self.gridLayout.addWidget(self.threeLineC_E, __gridRow, 3)
        __gridRow += 1
        
        # Four Lines
        fourLineT_L = QLabel(_('Four Lines'))
        fourLineT_L.setAlignment(Qt.AlignRight)
        self.fourLineA_E = LineEdit()
        self.wrapper.addMapping(self.fourLineA_E, ProcessorModel.ElasticLinesCorrModel.FourLineDistACol)
        self.fourLineA_E.enableDoubleValidator(0, 100, 2)
        self.fourLineA_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineA_E.setHelpBar(self.helpBar)
        
        self.fourLineB_E = LineEdit()
        self.wrapper.addMapping(self.fourLineB_E, ProcessorModel.ElasticLinesCorrModel.FourLineDistBCol)
        self.fourLineB_E.enableDoubleValidator(0, 100, 2)
        self.fourLineB_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineB_E.setHelpBar(self.helpBar)

        self.fourLineC_E = LineEdit()
        self.wrapper.addMapping(self.fourLineC_E, ProcessorModel.ElasticLinesCorrModel.FourLineDistCCol)
        self.fourLineC_E.enableDoubleValidator(0, 100, 2)
        self.fourLineC_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineC_E.setHelpBar(self.helpBar)
        
        self.fourLineD_E = LineEdit()
        self.wrapper.addMapping(self.fourLineD_E, ProcessorModel.ElasticLinesCorrModel.FourLineDistDCol)
        self.fourLineD_E.enableDoubleValidator(0, 100, 2)
        self.fourLineD_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineD_E.setHelpBar(self.helpBar)
        
        self.gridLayout.addWidget(fourLineT_L, __gridRow, 0)
        self.gridLayout.addWidget(self.fourLineA_E, __gridRow, 1)
        self.gridLayout.addWidget(self.fourLineB_E, __gridRow, 2)
        self.gridLayout.addWidget(self.fourLineC_E, __gridRow, 3)
        self.gridLayout.addWidget(self.fourLineD_E, __gridRow, 4)
        __gridRow += 1
        
        # Five Lines
        fiveLineT_L = QLabel(_('Five Lines'))
        fiveLineT_L.setAlignment(Qt.AlignRight)
        self.fiveLineA_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineA_E, ProcessorModel.ElasticLinesCorrModel.FiveLineDistACol)
        self.fiveLineA_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineA_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineA_E.setHelpBar(self.helpBar)
        
        self.fiveLineB_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineB_E, ProcessorModel.ElasticLinesCorrModel.FiveLineDistBCol)
        self.fiveLineB_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineB_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineB_E.setHelpBar(self.helpBar)

        self.fiveLineC_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineC_E, ProcessorModel.ElasticLinesCorrModel.FiveLineDistCCol)
        self.fiveLineC_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineC_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineC_E.setHelpBar(self.helpBar)
        
        self.fiveLineD_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineD_E, ProcessorModel.ElasticLinesCorrModel.FiveLineDistDCol)
        self.fiveLineD_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineD_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineD_E.setHelpBar(self.helpBar)
        
        self.fiveLineE_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineE_E, ProcessorModel.ElasticLinesCorrModel.FiveLineDistECol)
        self.fiveLineD_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineE_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineE_E.setHelpBar(self.helpBar)        
        
        self.gridLayout.addWidget(fiveLineT_L, __gridRow, 0)
        self.gridLayout.addWidget(self.fiveLineA_E, __gridRow, 1)
        self.gridLayout.addWidget(self.fiveLineB_E, __gridRow, 2)
        self.gridLayout.addWidget(self.fiveLineC_E, __gridRow, 3)
        self.gridLayout.addWidget(self.fiveLineD_E, __gridRow, 4)
        self.gridLayout.addWidget(self.fiveLineE_E, __gridRow, 5)
        __gridRow += 1

        self.windowLayout.addLayout(self.gridLayout) 
        
        def_T = TableView()
        def_T.setModel( self.elLinesDef_M )
        def_T.verticalHeader().setVisible(False)
        def_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        def_T.hideColumn( self.elLinesDef_M.columnCount()-1 )
        def_T.hideColumn( self.elLinesDef_M.columnCount()-2 )
        def_T.setFixedHeight(2 + def_T.horizontalHeader().height() + 5* def_T.rowHeight(0))
        self.windowLayout.addWidget(def_T)
        
        def_T.enableIntValidator(ProcessorModel.ElasticLinesDefModel.OrderNumCol, ProcessorModel.ElasticLinesDefModel.OrderNumCol, 1,5 )
        def_T.enableDoubleValidator(ProcessorModel.ElasticLinesDefModel.DefLowCol, ProcessorModel.ElasticLinesDefModel.DefHighCol, 0, 10, 2)
        
        def_T.setHelpBar(self.helpBar)
        def_T.setHelpText(ProcessorModel.ElasticLinesDefModel.OrderNumCol, _('ElLinesCorr-NumOfLinesDesc'))
        def_T.setHelpText(ProcessorModel.ElasticLinesDefModel.DefLowCol, _('ElLinesCorr-LowColDesc'))
        def_T.setHelpText(ProcessorModel.ElasticLinesDefModel.DefMidCol, _('ElLinesCorr-MidColDesc'))
        def_T.setHelpText(ProcessorModel.ElasticLinesDefModel.DefHighCol , _('ElLinesCorr-HigColDesc'))
  
        self.wrapper.toFirst()
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/elasticLinesCorr.html')
        
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
        logging.debug(self.__className + '.btnPress')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    