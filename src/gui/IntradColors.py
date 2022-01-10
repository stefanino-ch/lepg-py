'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.ProcModel import ProcModel

class IntradColors(QMdiSubWindow):
    '''
    :class: Window to display and edit airfoils holes data  
    '''

    __className = 'IntradColors'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.intradColsConf_M = ProcModel.IntradosColsConfModel()
        self.intradColsConf_M.numRowsForConfigChanged.connect( self.modelNumConfigsChanged )
        
        self.intradColsDet_M = ProcModel.IntradosColsDetModel()
        self.intradColsDet_M.numRowsForConfigChanged.connect(self.updateTabs)
        
        self.confProxyModel = []

        self.detProxyModel = []
        self.numDet_S = []

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
                    numConfSpin
                    
                    Tabs
                        configTable
                        numDetSpin
                        detailTable
                    -------------------------
                            help_bar  | btn_bar
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(400, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Colors lower sail"))
        
        numConf_L = QLabel(_('Number of configs'))
        numConf_L.setAlignment(Qt.AlignRight)
        numConf_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numConf_S = QSpinBox()
        self.numConf_S.setRange(0,999)
        self.numConf_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numConf_S.setValue(self.intradColsConf_M.num_configs())
        confEdit = self.numConf_S.lineEdit()
        confEdit.setReadOnly(True)
        self.numConf_S.valueChanged.connect(self.confSpinChange)
        
        numConfLayout = QHBoxLayout()
        numConfLayout.addWidget(numConf_L)
        numConfLayout.addWidget(self.numConf_S)
        numConfLayout.addStretch()
        self.windowLayout.addLayout(numConfLayout)
        
        self.tabs = QTabWidget()
        self.windowLayout.addWidget(self.tabs)
        
        # check if there's already data
        if self.intradColsConf_M.num_configs() > 0:
            self.modelNumConfigsChanged() 
        
        sortBtn = QPushButton(_('Sort by order_num'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/intradosColors.html')
        
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(sortBtn)
        bottomLayout.addStretch() 
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)
        
    def confSpinChange(self):
        '''
        :method: Called upon manual changes of the config spin. Does assure all elements will follow the user configuration. 
        '''
        logging.debug(self.__className+'.conf_spin_change')
        self.intradColsConf_M.set_num_configs(self.numConf_S.value())
    
    def modelNumConfigsChanged(self):
        '''
        :method: Called upon canges of the configs model. Does assure all GUI elements will follow the changes. 
        '''
        logging.debug(self.__className+'.model_num_configs_changed')
        
        currentNumConfigs = self.intradColsConf_M.num_configs()

        self.numConf_S.blockSignals(True)
        self.numConf_S.setValue( currentNumConfigs )
        self.numConf_S.blockSignals(False)
            
        diff = abs(currentNumConfigs - self.tabs.count() )
        if diff != 0:
            # we have to update the tabs
            i=0
            if currentNumConfigs > self.tabs.count():
                #add tabs
                while i < diff:
                    self.addTab()
                    i += 1
            else:
                #remove tabs
                while i < diff:
                    self.removeTab()
                    i += 1
                    
    def detSpinChange(self): 
        '''
        :method: Called upon manual changes of the detail spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.det_spin_change')
        self.intradColsDet_M.set_num_rows_for_config(self.tabs.currentIndex() + 1, self.numDet_S[self.tabs.currentIndex()].value())
    
    def addTab(self):
        '''
        :method: Creates a new tab inculding all its widgets. 
        '''
        logging.debug(self.__className+'.add_tab')
        
        currNumTabs = self.tabs.count()
        
        tabWidget = QWidget()
        tabLayout = QVBoxLayout()
        
        # Configuration 
        confTable = TableView()
        self.confProxyModel.append(QSortFilterProxyModel())
        self.confProxyModel[currNumTabs].setSourceModel(self.intradColsConf_M)
        self.confProxyModel[currNumTabs].setFilterKeyColumn(ProcModel.IntradosColsConfModel.ConfigNumCol)
        self.confProxyModel[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )
        confTable.setModel( self.confProxyModel[currNumTabs] )
        confTable.verticalHeader().setVisible(False)
        confTable.hideColumn(self.intradColsConf_M.OrderNumCol )
        confTable.hideColumn(self.intradColsConf_M.columnCount() -1 )
        confTable.hideColumn(self.intradColsConf_M.columnCount() -2 )
        
        confTable.enableIntValidator(ProcModel.IntradosColsConfModel.FirstRibCol, ProcModel.IntradosColsConfModel.FirstRibCol, 1, 999)
        
        confTable.setHelpBar(self.helpBar)
        confTable.setHelpText(ProcModel.IntradosColsConfModel.FirstRibCol, _('IntradCols-FirstRibDesc'))
        
        confLayout = QHBoxLayout()
        confLayout.addWidget(confTable)
        confLayout.addStretch()
        confTable.setFixedWidth(2 + confTable.columnWidth(ProcModel.IntradosColsConfModel.FirstRibCol))
        confTable.setFixedHeight(2 + confTable.horizontalHeader().height() + confTable.rowHeight(0))
        tabLayout.addLayout(confLayout)
        
        # Data lines
        numDet_L = QLabel(_('Number of config lines'))
        numDet_L.setAlignment(Qt.AlignRight)
        numDet_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        tabLayout.addWidget(numDet_L)
        self.numDet_S.append(QSpinBox())
        self.numDet_S[currNumTabs].setRange(1,999)
        self.numDet_S[currNumTabs].setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numDet_S[currNumTabs].valueChanged.connect(self.detSpinChange)
        detEdit = self.numDet_S[currNumTabs].lineEdit()
        detEdit.setReadOnly(True)
        
        detNumLayout = QHBoxLayout()
        detNumLayout.addWidget(numDet_L)
        detNumLayout.addWidget(self.numDet_S[currNumTabs])
        detNumLayout.addStretch()
        tabLayout.addLayout(detNumLayout)
        
        # add here the code for the details table
        detTable = TableView()
        self.detProxyModel.append(QSortFilterProxyModel())
        self.detProxyModel[currNumTabs].setSourceModel(self.intradColsDet_M)
        self.detProxyModel[currNumTabs].setFilterKeyColumn(ProcModel.IntradosColsDetModel.ConfigNumCol)
        self.detProxyModel[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )
        detTable.setModel( self.detProxyModel[currNumTabs] )
        detTable.verticalHeader().setVisible(False)
        detTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        detTable.hideColumn(self.intradColsDet_M.columnCount() -1 )
        detTable.hideColumn(self.intradColsDet_M.columnCount() -2 )
        tabLayout.addWidget(detTable)
         
        detTable.enableIntValidator(ProcModel.IntradosColsDetModel.OrderNumCol, ProcModel.IntradosColsDetModel.OrderNumCol, 1, 999)
        detTable.enableDoubleValidator(ProcModel.IntradosColsDetModel.DistTeCol, ProcModel.IntradosColsDetModel.DistTeCol, 0, 100, 0)
         
        detTable.setHelpBar(self.helpBar)
        detTable.setHelpText(ProcModel.LightDetModel.OrderNumCol, _('OrderNumDesc'))
        detTable.setHelpText(ProcModel.LightDetModel.LightTypCol, _('IntradCols-DistTeDesc'))
        
        # then setup spin
        if self.detProxyModel[currNumTabs].rowCount() ==0:
            # a new tab was created from the gui
            self.intradColsDet_M.set_num_rows_for_config(currNumTabs + 1, 1)
        # a new tab was added based on file load. The model has been updated already before. 
        self.numDet_S[currNumTabs].setValue(self.detProxyModel[currNumTabs].rowCount())
        tabWidget.setLayout(tabLayout)

        i =  self.tabs.addTab(tabWidget, str(currNumTabs+1) )
        self.tabs.setCurrentIndex(i)
    
    def removeTab(self):
        '''
        :method: Removes the last tab from the GUI. Does take care at the same time of the class internal elements and the data model. 
        ''' 
        logging.debug(self.__className+'.remove_tab')
        numTabs = self.tabs.count()
        self.tabs.removeTab(numTabs-1)
        # cleanup arrays
        self.confProxyModel.pop(numTabs-1)
        self.detProxyModel.pop(numTabs-1)
        self.numDet_S.pop(numTabs-1)
        self.intradColsDet_M.set_num_rows_for_config(numTabs, 0)
    
    def updateTabs(self):
        '''
        :method: called upon canges of the details model. Does assure all GUI elements will follow the changes. 
        '''
        logging.debug(self.__className+'.update_tabs')
        
        i=0
        while i< self.tabs.count():
            if self.numDet_S[i].value != self.intradColsDet_M.num_rows_for_config(i + 1):
                self.numDet_S[i].setValue(self.intradColsDet_M.num_rows_for_config(i + 1))
            i+=1
            
    def sortBtnPress(self):
        '''
        :method: Executed if the sort button is pressed. Does a one time sort based on the numbers in the OrderNum column.
        '''
        logging.debug(self.__className+'.sort_btn_press')
        
        if self.tabs.count() >0:
            currTab = self.tabs.currentIndex()
            self.detProxyModel[currTab].sort(ProcModel.IntradosColsDetModel.OrderNumCol, Qt.AscendingOrder)
            self.detProxyModel[currTab].setDynamicSortFilter(False)
    
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
    