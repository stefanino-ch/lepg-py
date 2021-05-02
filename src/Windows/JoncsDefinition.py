'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, \
    QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class JoncsDefinition(QMdiSubWindow):
    '''
    :class: Window to display and edit airfoils holes data  
    '''

    __className = 'JoncsDefinition'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.joncsDef_M = ProcessorModel.JoncsDefModel()
        self.joncsDef_M.numRowsForConfigChanged.connect( self.modelSizeChanged )

        self.type_CB = []        
        self.numLines_S = []
        
        self.proxyModel = []
        self.table = []

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
                    config edit (blocs)
                    numConfSpin
                    Tabs
                        typeRadio
                        numLinesSpin
                        LinesTable
                    -------------------------
                        OrderBtn | helpBar  | btnBar
                            
        Naming:
        
            conf equals blocs
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1100, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Joncs definition (Nylon rods)"))
        
        numConf_L = QLabel(_('Number of blocs'))
        numConf_L.setAlignment(Qt.AlignRight)
        numConf_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
        self.numConf_S = QSpinBox()
        self.numConf_S.setRange(0,20)
        self.numConf_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numConf_S.setValue( self.joncsDef_M.numConfigs() )
        
        edit = self.numConf_S.lineEdit()
        edit.setReadOnly(True)
        self.numConf_S.valueChanged.connect(self.confSpinChange)
         
        numConfLayout = QHBoxLayout()
        numConfLayout.addWidget(numConf_L)
        numConfLayout.addWidget(self.numConf_S)
        numConfLayout.addStretch()
        self.windowLayout.addLayout(numConfLayout)
         
        self.tabs = QTabWidget()
        self.windowLayout.addWidget(self.tabs)
         
        # check if there's already data
        if self.joncsDef_M.numConfigs() > 0:
            self.modelSizeChanged() 
         
        sortBtn = QPushButton(_('Sort by orderNum'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/joncsDefinition.html')
        
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
        logging.debug(self.__className+'.confSpinChange')
        currNumConfigs = self.joncsDef_M.numConfigs()
        mustNumConfigs = self.numConf_S.value()
        
        if currNumConfigs > mustNumConfigs:
            # more tabs than we should have -> remove last
            self.joncsDef_M.setNumRowsForConfig(currNumConfigs, 0)
        
        if currNumConfigs < mustNumConfigs:
            # missing configs -> add one
            self.joncsDef_M.setNumRowsForConfig(mustNumConfigs , 1)
            
    def modelSizeChanged(self):
        '''
        :method: Called after the model has been changed it's size. Herein we assure the GUI follows the model.
        '''
        logging.debug(self.__className+'.modelSizeChanged')
        
        currNumConfigs = self.joncsDef_M.numConfigs() 
        
        # config (num plans) spinbox
        if self.numConf_S.value() != currNumConfigs:
            self.numConf_S.blockSignals(True)
            self.numConf_S.setValue(currNumConfigs)
            self.numConf_S.blockSignals(False)
            
        # number of tabs
        diff = abs(currNumConfigs - self.tabs.count() )
        if diff != 0:
            # we have to update the tabs
            i=0
            if currNumConfigs > self.tabs.count():
                #add tabs
                while i < diff:
                    self.addTab()
                    i += 1
            else:
                #remove tabs
                while i < diff:
                    self.removeTab()
                    i += 1

        # update lines (pahts) spin
        i=0
        while i< self.tabs.count():
            if self.numLines_S[i].value != self.joncsDef_M.numRowsForConfig(i+1):
                self.numLines_S[i].blockSignals(True)
                self.numLines_S[i].setValue( self.joncsDef_M.numRowsForConfig(i+1) )
                self.numLines_S[i].blockSignals(False)
                
            typeNum = self.joncsDef_M.getType(i+1)
            if typeNum == 0:
                # new empty row
                self.joncsDef_M.setType(i+1, 1)
                self.setTypeOneColumns()
            elif typeNum == 1:
                # there is vaild type 1 data
                self.type_CB[i].blockSignals(True)
                self.type_CB[i].setCurrentIndex(0)
                self.type_CB[i].blockSignals(False)
                self.setTypeOneColumns()
            elif typeNum == 2:
                # there is vaild type 1 data
                self.type_CB[i].blockSignals(True)
                self.type_CB[i].setCurrentIndex(1)
                self.type_CB[i].blockSignals(False)
                self.setTypeTwoColumns()

            i+=1
    
    def addTab(self):
        '''
        :method: Creates a new tab inculding all its widgets. 
        '''
        logging.debug(self.__className+'.addTab')
        
        currNumTabs = self.tabs.count()
         
        tabWidget = QWidget()
        tabLayout = QVBoxLayout()

        # Data lines
        typeLayout = QHBoxLayout()
        type_L = QLabel(_('Type'))
        self.type_CB.append(QComboBox())
        self.type_CB[currNumTabs].addItem(_("1"))
        self.type_CB[currNumTabs].addItem(_("2"))
        self.type_CB[currNumTabs].currentIndexChanged.connect(self.typeCbChange)
        typeLayout.addWidget(type_L)
        typeLayout.addWidget(self.type_CB[currNumTabs])
        typeLayout.addStretch()
        tabLayout.addLayout(typeLayout)
        
        linesLayout = QHBoxLayout()
        numLines_L = QLabel(_('Number of groups'))
        numLines_L.setAlignment(Qt.AlignRight)
        numLines_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numLines_S.append(QSpinBox())
        self.numLines_S[currNumTabs].setRange(1,100)
        self.numLines_S[currNumTabs].setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numLines_S[currNumTabs].valueChanged.connect(self.numLinesChange)
        pathEdit = self.numLines_S[currNumTabs].lineEdit()
        pathEdit.setReadOnly(True)
        linesLayout.addWidget(numLines_L)
        linesLayout.addWidget(self.numLines_S[currNumTabs])
        linesLayout.addStretch()
        tabLayout.addLayout(linesLayout)

        self.proxyModel.append(QSortFilterProxyModel())
        self.proxyModel[currNumTabs].setSourceModel(self.joncsDef_M)
        self.proxyModel[currNumTabs].setFilterKeyColumn(ProcessorModel.JoncsDefModel.ConfigNumCol)
        self.proxyModel[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )        
        
        self.table.append(TableView())
        self.table[currNumTabs].setModel(self.proxyModel[currNumTabs])
        self.table[currNumTabs].verticalHeader().setVisible(False)
        self.table[currNumTabs].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table[currNumTabs].hideColumn( self.joncsDef_M.columnCount()-1 )
        self.table[currNumTabs].hideColumn( self.joncsDef_M.columnCount()-2 )
        tabLayout.addWidget(self.table[currNumTabs])
        

# TODO: enable validators
#         branchTable.enableIntValidator(ProcessorModel.LinesModel.OrderNumCol, ProcessorModel.LinesModel.OrderNumCol, 1, 999)
#         branchTable.enableIntValidator(ProcessorModel.LinesModel.NumBranchesCol, ProcessorModel.LinesModel.NumBranchesCol, 1, 4)
#         branchTable.enableIntValidator(ProcessorModel.LinesModel.BranchLvlOneCol, ProcessorModel.LinesModel.OrderLvlFourCol, 1, 99)
#         branchTable.enableIntValidator(ProcessorModel.LinesModel.AnchorLineCol, ProcessorModel.LinesModel.AnchorLineCol, 1, 6)
#         branchTable.enableIntValidator(ProcessorModel.LinesModel.AnchorRibNumCol, ProcessorModel.LinesModel.AnchorRibNumCol, 1, 999)
#         
        self.table[currNumTabs].setHelpBar(self.helpBar)
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.OrderNumCol, _('OrderNumDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.FirstRibCol , _('JoncsDef-FirstRibDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.LastRibCol , _('JoncsDef-LastRibDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pBACol , _('JoncsDef-pBADesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pBBCol , _('JoncsDef-pBBDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pBCCol , _('JoncsDef-pBCDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pBDCol , _('JoncsDef-pBDDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pBECol , _('JoncsDef-pBEDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pCACol , _('JoncsDef-pCADesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pCBCol , _('JoncsDef-pCBDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pCCCol , _('JoncsDef-pCCDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pCDCol , _('JoncsDef-pCDDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pDACol , _('JoncsDef-pDADesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pDBCol , _('JoncsDef-pDBDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pDCCol , _('JoncsDef-pDCDesc'))
        self.table[currNumTabs].setHelpText(ProcessorModel.JoncsDefModel.pDDCol , _('JoncsDef-pDDDesc'))
        
        tabWidget.setLayout(tabLayout)
 
        i =  self.tabs.addTab(tabWidget, str(currNumTabs+1) )
        self.tabs.setCurrentIndex(i)
        
        typeNum = self.joncsDef_M.getType(currNumTabs+1)
        if typeNum == 0:
            # new empty row
            self.joncsDef_M.setType(currNumTabs+1, 1)
            self.setTypeOneColumns()
        elif typeNum == 1:
            # there is vaild type 1 data
            self.type_CB[currNumTabs].blockSignals(True)
            self.type_CB[currNumTabs].setCurrentIndex(0)
            self.type_CB[currNumTabs].blockSignals(False)
            self.setTypeOneColumns()
        elif typeNum == 2:
            # there is vaild type 1 data
            self.type_CB[currNumTabs].blockSignals(True)
            self.type_CB[currNumTabs].setCurrentIndex(1)
            self.type_CB[currNumTabs].blockSignals(False)
            self.setTypeTwoColumns()
    
    def removeTab(self):
        '''
        :method: Removes the last tab from the GUI. Does take care at the same time of the class internal elements and the data model. 
        ''' 
        logging.debug(self.__className+'.removeTab')
        numTabs = self.tabs.count()
        
        self.tabs.removeTab(numTabs-1)
        # cleanup arrays
        self.type_CB.pop(numTabs-1)
        self.numLines_S.pop(numTabs-1)
        self.proxyModel.pop(numTabs-1)
        self.table.pop(numTabs-1)
                   
    def numLinesChange(self): 
        '''
        :method: Called upon manual changes of the lines spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.numLinesChange')
        self.joncsDef_M.setNumRowsForConfig(self.tabs.currentIndex()+1, self.numLines_S[self.tabs.currentIndex()].value() )
        
        currTab = self.tabs.currentIndex()
        if self.type_CB[currTab].currentIndex() == 0:
            self.joncsDef_M.setType(currTab+1, 1)
        else:
            self.joncsDef_M.setType(currTab+1, 2)

    def typeCbChange(self):
        '''
        :method: Called upon manual changes of the type combo. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.typeCbChange')
        
        currTab = self.tabs.currentIndex()
        
        if self.type_CB[currTab].currentIndex() == 0:
            # show rows for type 1
            self.setTypeOneColumns()
            self.joncsDef_M.setType(currTab+1, 1) 
            
        else:
            # show rows for type 2
            self.setTypeOneColumns()
            self.joncsDef_M.setType(currTab+1, 2)  
    
    def setTypeOneColumns(self): 
        '''
        :method: Enables disables table columns to be accurate for type one tables
        '''
        currTab = self.tabs.currentIndex()     
        self.table[currTab].hideColumn( ProcessorModel.JoncsDefModel.pBECol )

        self.table[currTab].showColumn( ProcessorModel.JoncsDefModel.pDACol)
        self.table[currTab].showColumn( ProcessorModel.JoncsDefModel.pDBCol)
        self.table[currTab].showColumn( ProcessorModel.JoncsDefModel.pDCCol)
        self.table[currTab].showColumn( ProcessorModel.JoncsDefModel.pDDCol)
        self.table[currTab].hideColumn( ProcessorModel.JoncsDefModel.TypeCol)
        
    def setTypeTwoColumns(self):
        '''
        :method: Enables disables table columns to be accurate for type two tables
        '''
        currTab = self.tabs.currentIndex()
        self.table[currTab].showColumn( ProcessorModel.JoncsDefModel.pBECol)

        self.table[currTab].hideColumn( ProcessorModel.JoncsDefModel.pDACol)
        self.table[currTab].hideColumn( ProcessorModel.JoncsDefModel.pDBCol)
        self.table[currTab].hideColumn( ProcessorModel.JoncsDefModel.pDCCol)
        self.table[currTab].hideColumn( ProcessorModel.JoncsDefModel.pDDCol)
        self.table[currTab].hideColumn( ProcessorModel.JoncsDefModel.TypeCol)  

    def sortBtnPress(self):
        '''
        :method: Executed if the sort button is pressed. Does a one time sort based on the numbers in the OrderNum column.
        '''
        logging.debug(self.__className+'.sortBtnPress')
                
        if self.tabs.count() >0:
            currTab = self.tabs.currentIndex()
            self.proxyModel[currTab].sort(ProcessorModel.JoncsDefModel.OrderNumCol, Qt.AscendingOrder)
            self.proxyModel[currTab].setDynamicSortFilter(False)
    
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
    