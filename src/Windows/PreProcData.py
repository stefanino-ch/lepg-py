'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QHeaderView,\
    QLabel, QComboBox
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.PreProcessorModel import PreProcessorModel

class PreProcData(QMdiSubWindow):
    '''
    :class: Window to display and edit Skin tension data  
    '''

    __className = 'PreProcData'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.gen_M = PreProcessorModel.GenModel()
        self.leadingE_M = PreProcessorModel.LeadingEdgeModel()
        self.trailingE_M = PreProcessorModel.TrailingEdgeModel()
        
        self.vault_M = PreProcessorModel.VaultModel()
        self.vault_M.didSelect.connect( self.vaultModelChange )
        
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
                     Gen Table
                     LE Table
                     TE Table
                     Vault Table
                    ---------------------------
                                helpBar | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 400)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Pre-Processor data"))
        
        gen_L = QLabel(_("Generals"))
        genTable = TableView()
        genTable.setModel( self.gen_M )
        genTable.hideColumn(0)
        genTable.hideColumn(self.gen_M.columnCount() -2 )
        genTable.hideColumn(self.gen_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        genTable.verticalHeader().setVisible(False)
        genTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        genTable.setFixedHeight(2 + genTable.horizontalHeader().height() + genTable.rowHeight(0))
        genTable.setHelpBar(self.helpBar)
        
        genTable.setHelpText(PreProcessorModel.GenModel.WingNameCol, _('PreProc-WingNameDesc'))

        genTable.enableRegExpValidator(PreProcessorModel.GenModel.WingNameCol, PreProcessorModel.GenModel.WingNameCol, "^[a-zA-Z0-9_.-]*$")
        
        
        gen_Ly = QHBoxLayout()
        gen_Ly.addWidget(genTable)
        gen_Ly.addStretch()
        self.windowLayout.addWidget(gen_L)
        self.windowLayout.addLayout(gen_Ly)
        
        # Leading Edge
        le_L = QLabel(_("Leading edge"))
        leTable = TableView()
        leTable.setModel( self.leadingE_M )
        leTable.hideColumn(0 )
        leTable.hideColumn(self.leadingE_M.columnCount() -2 )
        leTable.hideColumn(self.leadingE_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        leTable.verticalHeader().setVisible(False)
        leTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        leTable.setFixedHeight(2 + leTable.horizontalHeader().height() + leTable.rowHeight(0))
        
        leTable.setHelpBar(self.helpBar)
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.TypeCol, _('PreProc-LE-Type-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.aOneCol, _('PreProc-LE-a1-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.bOneCol, _('PreProc-LE-b1-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.xOneCol, _('PreProc-LE-x1-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.xTwoCol, _('PreProc-LE-x2-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.xmCol, _('PreProc-LE-xm-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.cZeroOneCol, _('PreProc-LE-c01-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.exOneCol, _('PreProc-LE-ex1-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.cZeroTwoCol, _('PreProc-LE-c02-Desc'))
        leTable.setHelpText(PreProcessorModel.LeadingEdgeModel.exTwoCol, _('PreProc-LE-ex2-Desc'))

        # leTable.enableDoubleValidator(ProcessorModel.SkinTensionModel.TopDistLECol, ProcessorModel.SkinTensionModel.BottWideCol, 0, 100, 3)
        # leTable.setFixedHeight(2 + leTable.horizontalHeader().height() + 6*leTable.rowHeight(0))
        
        self.windowLayout.addWidget(le_L)
        self.windowLayout.addWidget(leTable)

        # Trailing Edge
        te_L = QLabel(_("Trailing edge"))
        teTable = TableView()
        teTable.setModel( self.trailingE_M )
        teTable.hideColumn(0 )
        teTable.hideColumn(self.trailingE_M.columnCount() -2 )
        teTable.hideColumn(self.trailingE_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        teTable.verticalHeader().setVisible(False)
        teTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        teTable.setFixedHeight(2 + teTable.horizontalHeader().height() + teTable.rowHeight(0))
        
        teTable.setHelpBar(self.helpBar)
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.TypeCol, _('PreProc-TE-Type-Desc'))
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.aOneCol, _('PreProc-TE-a1-Desc'))
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.bOneCol, _('PreProc-TE-b1-Desc'))
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.xOneCol, _('PreProc-TE-x1-Desc'))
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.xmCol, _('PreProc-TE-xm-Desc'))
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.cZeroCol, _('PreProc-TE-c0-Desc'))
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.yZeroCol, _('PreProc-TE-y0-Desc'))
        teTable.setHelpText(PreProcessorModel.TrailingEdgeModel.expCol, _('PreProc-TE-exp-Desc'))

        # teTable.enableDoubleValidator(ProcessorModel.SkinTensionModel.TopDistLECol, ProcessorModel.SkinTensionModel.BottWideCol, 0, 100, 3)
        # teTable.setFixedHeight(2 + teTable.horizontalHeader().height() + 6*teTable.rowHeight(0))

        self.windowLayout.addWidget(te_L)
        self.windowLayout.addWidget(teTable)
        
        # Vault
        vault_L = QLabel(_("Vault"))
        vaultT_L = QLabel(_("Type"))
        vaultT_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.vaultT_CB = QComboBox()
        self.vaultT_CB.addItem(_("Sin-Cos"))
        self.vaultT_CB.addItem(_("Radius-Angle"))
        self.vaultT_CB.currentIndexChanged.connect(self.vaultCbChange)
        
        self.vaultTable = TableView()
        self.vaultTable.setModel( self.vault_M )
        self.vaultTable.hideColumn(0)
        self.vaultTable.hideColumn(1)
        self.vaultTable.hideColumn(self.vault_M.columnCount() -2 )
        self.vaultTable.hideColumn(self.vault_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        self.vaultTable.verticalHeader().setVisible(False)
        self.vaultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.vaultTable.setFixedHeight(2 + self.vaultTable.horizontalHeader().height() + self.vaultTable.rowHeight(0))
        
        self.vaultTable.setHelpBar(self.helpBar)
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.aOneCol, _('PreProc-Vault-a1-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.bOneCol, _('PreProc-Vault-b1-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.xOneCol, _('PreProc-Vault-x1-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.cOneCol, _('PreProc-Vault-c1-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.rOneRACol , _('PreProc-Vault-r1-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.rTwoRACol, _('PreProc-Vault-r2-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.rThrRACol, _('PreProc-Vault-r3-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.rFouRACol, _('PreProc-Vault-r4-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.aOneRACol, _('PreProc-Vault-ra1-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.aTwoRACol, _('PreProc-Vault-ra2-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.aThrRACol, _('PreProc-Vault-ra3-Desc'))
        self.vaultTable.setHelpText(PreProcessorModel.VaultModel.aFouRACol, _('PreProc-Vault-ra4-Desc'))
        
        self.vaultTable.enableDoubleValidator(PreProcessorModel.VaultModel.aOneCol, PreProcessorModel.VaultModel.aFouRACol, 0, 10000, 4)
        
        self.windowLayout.addWidget(vault_L)
        vaultT_Ly = QHBoxLayout()
        vaultT_Ly.addWidget(vaultT_L)
        vaultT_Ly.addWidget(self.vaultT_CB)
        vaultT_Ly.addStretch()
        self.windowLayout.addLayout(vaultT_Ly)
        self.windowLayout.addWidget(self.vaultTable) 
        
        self.vaultModelChange()       
        
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('preproc/nameLeTeVault.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()        
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)
        
    def vaultCbChange(self):
        '''
        :method: 
        '''
        logging.debug(self.__className+'.vaultCbChange')
        
        # first check if CB is set correctly
        if self.vaultT_CB.currentIndex() == 0:
            self.vault_M.updateType(1, 1, 1)
            self.setTypeOneColumns()
        else: 
            self.vault_M.updateType(1, 1, 2)
            self.setTypeTwoColumns()
            
    def vaultModelChange(self):
        '''
        :method: 
        '''
        logging.debug(self.__className+'.vaultModelUpdate')
        
        vaultT = self.vault_M.getType(1, 1)
        
        if vaultT == 1:
            self.vaultT_CB.blockSignals(True)
            self.vaultT_CB.setCurrentIndex(0)
            self.vaultT_CB.blockSignals(False)
            self.setTypeOneColumns()
        else: 
            self.vaultT_CB.blockSignals(True)
            self.vaultT_CB.setCurrentIndex(1)
            self.vaultT_CB.blockSignals(False)
            self.setTypeTwoColumns()
    
    def setTypeOneColumns(self):
        '''
        :method: 
        '''
        logging.debug(self.__className+'.setTypeOneColumns')
        
        for i in range (PreProcessorModel.VaultModel.aOneCol, PreProcessorModel.VaultModel.cOneCol+1):
            self.vaultTable.showColumn(i)
            
        for i in range (PreProcessorModel.VaultModel.rOneRACol, PreProcessorModel.VaultModel.aFouRACol+1):
            self.vaultTable.hideColumn(i)
        
    def setTypeTwoColumns(self):
        '''
        :method: 
        '''
        logging.debug(self.__className+'.setTypeTwoColumns')
        
        for i in range (PreProcessorModel.VaultModel.aOneCol, PreProcessorModel.VaultModel.cOneCol+1):
            self.vaultTable.hideColumn(i)
            
        for i in range (PreProcessorModel.VaultModel.rOneRACol, PreProcessorModel.VaultModel.aFouRACol+1):
            self.vaultTable.showColumn(i)
    
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
    