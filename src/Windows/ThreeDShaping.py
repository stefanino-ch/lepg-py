'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, QSpinBox, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class ThreeDShaping(QMdiSubWindow):
    '''
    :class: Window to display and edit airfoils holes data  
    '''

    __className = 'ThreeDShaping'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.threeDShConf_M = ProcessorModel.ThreeDShConfModel()
        self.threeDShConf_M.numRowsForConfigChanged.connect( self.modelNumConfigsChanged )
        
        self.threeDShUpDet_M = ProcessorModel.ThreeDShUpDetModel()
        self.threeDShUpDet_M.numRowsForConfigChanged.connect( self.updateTabs)
        
        self.threeDShLoDet_M = ProcessorModel.ThreeDShLoDetModel()
        self.threeDShLoDet_M.numRowsForConfigChanged.connect( self.updateTabs)
        
        self.threeDShPr_M = ProcessorModel.ThreeDShPrintModel()
        
        self.rib_PM = []
        self.upC_PM = []
        self.loC_PM = []

        self.numUpC_S = []
        self.numLoC_S = []

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
                    numConfSpin
                    
                    Tabs
                        ribTable
                        numUpSpin
                        upTable
                        numLoSpin
                        loTable
                        
                    printTable
                    -------------------------
                            helpBar  | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(750, 600)

        self.window_Ly = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("3D shaping"))
        
        numConf_L = QLabel(_('Number of groups'))
        numConf_L.setAlignment(Qt.AlignRight)
        numConf_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numConf_S = QSpinBox()
        self.numConf_S.setRange(0,999)
        self.numConf_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numConf_S.setValue( self.threeDShConf_M.numConfigs() )
        confEdit = self.numConf_S.lineEdit()
        confEdit.setReadOnly(True)
        self.numConf_S.valueChanged.connect(self.confSpinChange)
        
        numConfLayout = QHBoxLayout()
        numConfLayout.addWidget(numConf_L)
        numConfLayout.addWidget(self.numConf_S)
        numConfLayout.addStretch()
        self.window_Ly.addLayout(numConfLayout)
        
        self.tabs = QTabWidget()
        self.window_Ly.addWidget(self.tabs)
        
        # check if there's already data
        if self.threeDShConf_M.numConfigs() > 0:
            self.modelNumConfigsChanged() 

        printTable = TableView()
        printTable.setModel( self.threeDShPr_M )
        printTable.verticalHeader().setVisible(False)
        printTable.hideColumn(self.threeDShPr_M.OrderNumCol )
        printTable.hideColumn(self.threeDShPr_M.columnCount() -2 )
        printTable.hideColumn(self.threeDShPr_M.columnCount() -1 )
        
        # TODO: remove currently not supported rows
        printTable.setHelpBar(self.helpBar)
        printTable.setHelpText(ProcessorModel.ThreeDShPrintModel.NameCol, _('3DShPrint-NameDesc'))
        printTable.setHelpText(ProcessorModel.ThreeDShPrintModel.DrawCol, _('3DShPrint-DrawDesc'))
        printTable.setHelpText(ProcessorModel.ThreeDShPrintModel.FirstPanelCol, _('3DShPrint-FirstPanelDesc'))
        printTable.setHelpText(ProcessorModel.ThreeDShPrintModel.LastPanelCol, _('3DShPrint-LastPanelDesc'))
        printTable.setHelpText(ProcessorModel.ThreeDShPrintModel.SymmetricCol, _('3DShPrint-SymmetricDesc'))
        
        printLayout = QHBoxLayout()
        printLayout.addWidget(printTable)
        printTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        printTable.setFixedHeight(2 + printTable.horizontalHeader().height() + 5*printTable.rowHeight(0))
        self.window_Ly.addLayout(printLayout)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/threeDShaping.html')
        
        bottomLayout = QHBoxLayout()

        bottomLayout.addStretch() 
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.window_Ly.addLayout(bottomLayout)
        
        self.win.setLayout(self.window_Ly)
        
    def confSpinChange(self):
        '''
        :method: Called upon manual changes of the config spin. Does assure all elements will follow the user configuration. 
        '''
        logging.debug(self.__className+'.confSpinChange')
        self.threeDShConf_M.setNumConfigs( self.numConf_S.value() )
    
    def modelNumConfigsChanged(self):
        '''
        :method: Called upon canges of the configs model. Does assure all GUI elements will follow the changes. 
        '''
        logging.debug(self.__className+'.modelNumConfigsChanged')
        
        currentNumConfigs = self.threeDShConf_M.numConfigs()

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
    
    def addTab(self):
        '''
        :method: Creates a new tab inculding all its widgets. 
        '''
        logging.debug(self.__className+'.addTab')
        
        currNumTabs = self.tabs.count()
        
        tabWidget = QWidget()
        tab_Ly = QVBoxLayout()
        
        # Configuration 
        ribTable = TableView()
        self.rib_PM.append(QSortFilterProxyModel())
        self.rib_PM[currNumTabs].setSourceModel(self.threeDShConf_M)
        self.rib_PM[currNumTabs].setFilterKeyColumn(ProcessorModel.ThreeDShConfModel.ConfigNumCol)
        self.rib_PM[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )
        ribTable.setModel( self.rib_PM[currNumTabs] )
        ribTable.verticalHeader().setVisible(False)
        ribTable.hideColumn(self.threeDShConf_M.OrderNumCol )
        ribTable.hideColumn(self.threeDShConf_M.columnCount() -1 )
        ribTable.hideColumn(self.threeDShConf_M.columnCount() -2 )
        
        ribTable.enableIntValidator(ProcessorModel.ThreeDShConfModel.FirstRibCol, ProcessorModel.ThreeDShConfModel.LastRibCol, 1, 999)
        
        ribTable.setHelpBar(self.helpBar)
        ribTable.setHelpText(ProcessorModel.ThreeDShConfModel.FirstRibCol, _('3DSh-FirstRibDesc'))
        ribTable.setHelpText(ProcessorModel.ThreeDShConfModel.LastRibCol, _('3DSh-LastRibDesc'))
        
        rib_Ly = QHBoxLayout()
        rib_Ly.addWidget(ribTable)
        rib_Ly.addStretch()
        ribTable.setFixedWidth( 2 + ribTable.columnWidth(ProcessorModel.ThreeDShConfModel.FirstRibCol) \
                                 + ribTable.columnWidth(ProcessorModel.ThreeDShConfModel.LastRibCol) )
        ribTable.setFixedHeight(2 + ribTable.horizontalHeader().height() + ribTable.rowHeight(0))
        tab_Ly.addLayout(rib_Ly)
        
        ############### upper cuts
        numUpC_L = QLabel(_('Number of upper cuts'))
        numUpC_L.setAlignment(Qt.AlignRight)
        numUpC_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numUpC_S.append(QSpinBox())
        self.numUpC_S[currNumTabs].setRange(0,2)
        self.numUpC_S[currNumTabs].setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numUpC_S[currNumTabs].setValue( self.threeDShUpDet_M.numRowsForConfig(currNumTabs+1) )
        confEdit = self.numUpC_S[currNumTabs].lineEdit()
        confEdit.setReadOnly(True)
        self.numUpC_S[currNumTabs].valueChanged.connect(self.upCChange)
        
        numUpC_Ly = QHBoxLayout()
        numUpC_Ly.addWidget(numUpC_L)
        numUpC_Ly.addWidget(self.numUpC_S[currNumTabs])
        numUpC_Ly.addStretch()
        tab_Ly.addLayout(numUpC_Ly)
        
        upC_T = TableView()
        self.upC_PM.append(QSortFilterProxyModel())
        self.upC_PM[currNumTabs].setSourceModel(self.threeDShUpDet_M)
        self.upC_PM[currNumTabs].setFilterKeyColumn(ProcessorModel.ThreeDShUpDetModel.ConfigNumCol)
        self.upC_PM[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )
        upC_T.setModel( self.upC_PM[currNumTabs] )
        upC_T.verticalHeader().setVisible(False)
        upC_T.hideColumn(self.threeDShUpDet_M.OrderNumCol )
        upC_T.hideColumn(self.threeDShUpDet_M.columnCount() -1 )
        upC_T.hideColumn(self.threeDShUpDet_M.columnCount() -2 )
        
        upC_T.enableIntValidator(ProcessorModel.ThreeDShUpDetModel.IniPointCol, ProcessorModel.ThreeDShUpDetModel.CutPointCol, 0, 100)
        upC_T.enableDoubleValidator(ProcessorModel.ThreeDShUpDetModel.DepthCol, ProcessorModel.ThreeDShUpDetModel.DepthCol, -1, 1, 1)
        
        upC_T.setHelpBar(self.helpBar)
        upC_T.setHelpText(ProcessorModel.ThreeDShUpDetModel.IniPointCol, _('3DSh-IniPointDesc'))
        upC_T.setHelpText(ProcessorModel.ThreeDShUpDetModel.CutPointCol, _('3DSh-CutPointDesc'))
        upC_T.setHelpText(ProcessorModel.ThreeDShUpDetModel.DepthCol, _('3DSh-DepthDesc'))
        
        upC_Ly = QHBoxLayout()
        upC_Ly.addWidget(upC_T)
        upC_Ly.addStretch()
        upC_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        upC_T.setFixedHeight(2 + 3*upC_T.horizontalHeader().height())
        tab_Ly.addLayout(upC_Ly)
        
        ############### lower cuts
        numLoC_L = QLabel(_('Number of lower cuts'))
        numLoC_L.setAlignment(Qt.AlignRight)
        numLoC_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numLoC_S.append(QSpinBox())
        self.numLoC_S[currNumTabs].setRange(0,1)
        self.numLoC_S[currNumTabs].setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.numLoC_S[currNumTabs].setValue( self.threeDShLoDet_M.numRowsForConfig(currNumTabs+1) )
        confEdit = self.numLoC_S[currNumTabs].lineEdit()
        confEdit.setReadOnly(True)
        self.numLoC_S[currNumTabs].valueChanged.connect(self.loCChange)
        
        numLoC_Ly = QHBoxLayout()
        numLoC_Ly.addWidget(numLoC_L)
        numLoC_Ly.addWidget(self.numLoC_S[currNumTabs])
        numLoC_Ly.addStretch()
        tab_Ly.addLayout(numLoC_Ly)
        
        loC_T = TableView()
        self.loC_PM.append(QSortFilterProxyModel())
        self.loC_PM[currNumTabs].setSourceModel(self.threeDShLoDet_M)
        self.loC_PM[currNumTabs].setFilterKeyColumn(ProcessorModel.ThreeDShLoDetModel.ConfigNumCol)
        self.loC_PM[currNumTabs].setFilterRegExp( QRegExp( str(currNumTabs+1) ) )
        loC_T.setModel( self.loC_PM[currNumTabs] )
        loC_T.verticalHeader().setVisible(False)
        loC_T.hideColumn(self.threeDShLoDet_M.OrderNumCol )
        loC_T.hideColumn(self.threeDShLoDet_M.columnCount() -1 )
        loC_T.hideColumn(self.threeDShLoDet_M.columnCount() -2 )
        
        loC_T.enableIntValidator(ProcessorModel.ThreeDShLoDetModel.IniPointCol, ProcessorModel.ThreeDShLoDetModel.CutPointCol, 0, 100)
        loC_T.enableDoubleValidator(ProcessorModel.ThreeDShLoDetModel.DepthCol, ProcessorModel.ThreeDShLoDetModel.DepthCol, -1, 1, 1)
        
        loC_T.setHelpBar(self.helpBar)
        loC_T.setHelpText(ProcessorModel.ThreeDShLoDetModel.IniPointCol, _('3DSh-IniPointDesc'))
        loC_T.setHelpText(ProcessorModel.ThreeDShLoDetModel.CutPointCol, _('3DSh-CutPointDesc'))
        loC_T.setHelpText(ProcessorModel.ThreeDShLoDetModel.DepthCol, _('3DSh-DepthDesc'))
        
        loC_Ly = QHBoxLayout()
        loC_Ly.addWidget(loC_T)
        loC_Ly.addStretch()
        loC_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        loC_T.setFixedHeight(2 + 2*loC_T.horizontalHeader().height())
        tab_Ly.addLayout(loC_Ly)
        
        tabWidget.setLayout(tab_Ly)
 
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
        
        self.rib_PM.pop(numTabs-1)
        self.upC_PM.pop(numTabs-1)
        self.loC_PM.pop(numTabs-1)

        self.numUpC_S.pop(numTabs-1)
        self.numLoC_S.pop(numTabs-1)
        
        # cleanup database
        self.threeDShConf_M.setNumRowsForConfig(numTabs, 0 )
        self.threeDShUpDet_M.setNumRowsForConfig(numTabs, 0 )
        self.threeDShLoDet_M.setNumRowsForConfig(numTabs, 0 )
    
    def updateTabs(self):
        '''
        :method: called upon canges of the details models. Does assure all GUI elements will follow the changes. 
        '''
        logging.debug(self.__className+'.updateTabs')
    
        i=0
        while i< self.tabs.count():
            if self.numUpC_S[i].value != self.threeDShUpDet_M.numRowsForConfig(i+1):
                self.numUpC_S[i].blockSignals(True)
                self.numUpC_S[i].setValue( self.threeDShUpDet_M.numRowsForConfig(i+1) )
                self.numUpC_S[i].blockSignals(False)
            
            if self.numLoC_S[i].value != self.threeDShLoDet_M.numRowsForConfig(i+1):
                self.numLoC_S[i].blockSignals(True)
                self.numLoC_S[i].setValue( self.threeDShLoDet_M.numRowsForConfig(i+1) )
                self.numLoC_S[i].blockSignals(False)
            i+=1

    def upCChange(self): 
        '''
        :method: Called upon manual changes of the number of lower cuts spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.upCChange')
        self.threeDShUpDet_M.setNumRowsForConfig(self.tabs.currentIndex()+1, self.numUpC_S[self.tabs.currentIndex()].value() )

    def loCChange(self): 
        '''
        :method: Called upon manual changes of the number of lower cuts spin. Does assure all elements will follow the user configuration. 
        '''           
        logging.debug(self.__className+'.loCChange')
        self.threeDShLoDet_M.setNumRowsForConfig(self.tabs.currentIndex()+1, self.numLoC_S[self.tabs.currentIndex()].value() )
    
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
    