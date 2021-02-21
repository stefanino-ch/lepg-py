'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.ProcessorModel import ProcessorModel

class ProcRibHoles(QMdiSubWindow):
    '''
    :class: Window to display and edit airfoils holes data  
    '''

    __className = 'ProcRibHoles'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.lightC_M = ProcessorModel.LightConfModel()
        self.lightC_M.numConfigsChanged.connect( self.modelNumConfigsChanged )
        
        self.lightD_M = ProcessorModel.LightDetModel()
        self.lightD_M.numDetailsChanged.connect(self.updateTabs)
        
        self.confProxyModel = []

        self.detProxyModel = []
        self.numDet_S = []

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
            
        Structure:: 
        
            win
                windowLayout
                    numConfSpin
                    
                    Tabs
                    configTable
                    numDetSpin
                    detailTable
                    -------------------------
                            helpBar  | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Edit rib holes (Rib lightening)"))
        
        numConf_L = QLabel(_('Number of configurations'))
        numConf_L.setAlignment(Qt.AlignRight)
        numConf_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numConf_S = QSpinBox()
        self.numConf_S.setRange(0,999)
        self.numConf_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numConf_S.setValue( self.lightC_M.numConfigs() )
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
        if self.lightC_M.numConfigs() > 0:
            self.modelNumConfigsChanged( self.lightC_M.numConfigs() ) 
        
        sortBtn = QPushButton(_('Sort by orderNum'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/ribHoles.html')
        
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
        logging.debug(self.__className+'.modelNumConfigsChanged')
        self.lightC_M.setNumConfigs( self.numConf_S.value() )
    
    def modelNumConfigsChanged(self, numConfigs):
        '''
        :method: Called upon canges of the configs model. Does assure all GUI elements will follow the changes. 
        '''
        logging.debug(self.__className+'.modelNumConfigsChanged')

        if self.numConf_S.value() != numConfigs:
            self.numConf_S.setValue( numConfigs )
            
        diff = abs(numConfigs - self.tabs.count() )
        if diff != 0:
            # we have to update the tabs
            i=0
            if numConfigs > self.tabs.count():
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
        logging.debug(self.__className+'.detSpinChange')
        self.lightD_M.setNumDetailRows(self.tabs.currentIndex()+1, self.numDet_S[self.tabs.currentIndex()].value() )
    
    def addTab(self):
        '''
        :method: Creates a new tab inculding all its widgets. 
        '''
        logging.debug(self.__className+'.addTab')
        
        currNumTabs = self.tabs.count()
        
        tabWidget = QWidget()
        tabLayout = QVBoxLayout()
        
        # Configuration 
        confTable = TableView()
        self.confProxyModel.append(QSortFilterProxyModel())
        self.confProxyModel[currNumTabs].setSourceModel(self.lightC_M)
        self.confProxyModel[currNumTabs].setFilterKeyColumn(ProcessorModel.LightConfModel.ConfigNumCol)
        self.confProxyModel[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )
        confTable.setModel( self.confProxyModel[currNumTabs] )
        confTable.verticalHeader().setVisible(False)
        confTable.hideColumn(self.lightC_M.columnCount() -1 )
        confTable.hideColumn(self.lightC_M.columnCount() -2 )
        
        confTable.enableIntValidator(ProcessorModel.LightConfModel.InitialRibCol, ProcessorModel.LightConfModel.FinalRibCol, 1, 999)
        
        confTable.setHelpBar(self.helpBar)
        confTable.setHelpText(ProcessorModel.LightConfModel.InitialRibCol, _('Proc-InitialRibDesc'))
        confTable.setHelpText(ProcessorModel.LightConfModel.FinalRibCol, _('Proc-FinalRibDesc'))
        
        confLayout = QHBoxLayout()
        confLayout.addWidget(confTable)
        confLayout.addStretch()
        confTable.setFixedWidth( 2 + confTable.columnWidth(0) + confTable.columnWidth(1) )
        confTable.setFixedHeight(2 + confTable.horizontalHeader().height() + confTable.rowHeight(0))
        tabLayout.addLayout(confLayout)
        
        # Data lines
        numDet_L = QLabel(_('Number of Lines'))
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
        self.detProxyModel[currNumTabs].setSourceModel(self.lightD_M)
        self.detProxyModel[currNumTabs].setFilterKeyColumn(ProcessorModel.LightDetModel.ConfigNumCol)
        self.detProxyModel[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )
        detTable.setModel( self.detProxyModel[currNumTabs] )
        detTable.verticalHeader().setVisible(False)
        detTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        detTable.hideColumn(self.lightD_M.columnCount() -1 )
        detTable.hideColumn(self.lightD_M.columnCount() -2 )
        tabLayout.addWidget(detTable)
         
        detTable.enableIntValidator(ProcessorModel.LightDetModel.OrderNumCol, ProcessorModel.LightDetModel.OrderNumCol, 1, 999)
        detTable.enableIntValidator(ProcessorModel.LightDetModel.LightTypCol, ProcessorModel.LightDetModel.LightTypCol, 1, 3)
        detTable.enableDoubleValidator(ProcessorModel.LightDetModel.DistLECol, ProcessorModel.LightDetModel.VertAxisCol, 0, 100, 2)
        detTable.enableDoubleValidator(ProcessorModel.LightDetModel.RotAngleCol, ProcessorModel.LightDetModel.RotAngleCol, 0, 360, 2)
        detTable.enableDoubleValidator(ProcessorModel.LightDetModel.Opt1Col, ProcessorModel.LightDetModel.Opt1Col, 0, 100, 2)
        
        detTable.setHelpBar(self.helpBar)
        detTable.setHelpText(ProcessorModel.LightDetModel.OrderNumCol, _('Proc-OrderNumDesc'))
        detTable.setHelpText(ProcessorModel.LightDetModel.LightTypCol, _('Proc-LigthTypeDesc'))
        detTable.setHelpText(ProcessorModel.LightDetModel.DistLECol, _('Proc-DistLEDesc'))
        detTable.setHelpText(ProcessorModel.LightDetModel.DisChordCol, _('Proc-DisChordDesc'))
        detTable.setHelpText(ProcessorModel.LightDetModel.HorAxisCol, _('Proc-HorAxisDesc'))
        detTable.setHelpText(ProcessorModel.LightDetModel.VertAxisCol, _('Proc-VertAxisDesc'))
        detTable.setHelpText(ProcessorModel.LightDetModel.RotAngleCol, _('Proc-RotAngleDesc'))
        detTable.setHelpText(ProcessorModel.LightDetModel.Opt1Col, _('Proc-Opt1Desc'))
        
        # then setup spin
        if self.detProxyModel[currNumTabs].rowCount() ==0:
            # a new tab was created from the gui
            self.lightD_M.setNumDetailRows(currNumTabs+1, 1 )
        # a new tab was added based on file load. The model has been updated already before. 
        self.numDet_S[currNumTabs].setValue(self.detProxyModel[currNumTabs].rowCount())
        tabWidget.setLayout(tabLayout)
        

        i =  self.tabs.addTab(tabWidget, str(currNumTabs+1) )
        self.tabs.setCurrentIndex(i)
    
    def removeTab(self):
        '''
        :method: Removes the last tab from the GUI. Does take care at the same time of the class internal elements and the data model. 
        ''' 
        logging.debug(self.__className+'.removeTab')
        numTabs = self.tabs.count()
        self.tabs.removeTab(numTabs-1)
        # cleanup arrays
        self.confProxyModel.pop(numTabs-1)
        self.detProxyModel.pop(numTabs-1)
        self.numDet_S.pop(numTabs-1)
        self.lightD_M.setNumDetailRows(numTabs, 0 )
    
    def updateTabs(self):
        '''
        :method: called upon canges of the details model. Does assure all GUI elements will follow the changes. 
        '''
        logging.debug(self.__className+'.updateTabs')
        
        i=0
        while i< self.tabs.count():
            if self.numDet_S[i].value != self.lightD_M.numDetailRows(i+1):
                self.numDet_S[i].setValue( self.lightD_M.numDetailRows(i+1) )
            i+=1
            
    def sortBtnPress(self):
        '''
        :method: Executed if the sort button is pressed. Does a one time sort based on the numbers in the OrderNum column.
        '''
        logging.debug(self.__className+'.btnPress')
        
        if self.tabs.count() >0:
            currTab = self.tabs.currentIndex()
            self.detProxyModel[currTab].sort(ProcessorModel.LightDetModel.OrderNumCol, Qt.AscendingOrder)
            self.detProxyModel[currTab].setDynamicSortFilter(False)
    
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
    