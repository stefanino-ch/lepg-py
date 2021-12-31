'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget,\
                            QSizePolicy, QHeaderView,\
                            QLabel, QComboBox
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from DataStores.PreProcModel import PreProcModel


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

        self.gen_M = PreProcModel.GenModel()
        self.leadingE_M = PreProcModel.LeadingEdgeModel()
        self.trailingE_M = PreProcModel.TrailingEdgeModel()

        self.vault_M = PreProcModel.VaultModel()
        self.vault_M.didSelect.connect(self.vaultModelChange)

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
                     Gen Table
                     LE Table
                     TE Table
                     Vault Table
                    ---------------------------
                                help_bar | btn_bar
        '''
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
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
        genTable.setModel(self.gen_M)
        genTable.hideColumn(0)
        genTable.hideColumn(self.gen_M.columnCount()-2)
        # hide the ID column which is always at the end of the model
        genTable.hideColumn(self.gen_M.columnCount()-1)
        genTable.verticalHeader().setVisible(False)
        genTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        genTable.setFixedHeight(2
                                + genTable.horizontalHeader().height()
                                + genTable.rowHeight(0))
        genTable.setHelpBar(self.helpBar)

        genTable.setHelpText(PreProcModel.GenModel.WingNameCol,
                             _('PreProc-WingNameDesc'))

        genTable.enableRegExpValidator(PreProcModel.GenModel.WingNameCol,
                                       PreProcModel.GenModel.WingNameCol,
                                       "^[a-zA-Z0-9_.-]*$")

        gen_Ly = QHBoxLayout()
        gen_Ly.addWidget(genTable)
        gen_Ly.addStretch()
        self.windowLayout.addWidget(gen_L)
        self.windowLayout.addLayout(gen_Ly)

        # Leading Edge
        # TODO: remove type as the only allowed value is 1
        le_L = QLabel(_("Leading edge"))
        leTable = TableView()
        leTable.setModel(self.leadingE_M)
        leTable.hideColumn(0)

        # Type is always 1
        # Therefore we hide the Column in the GUI
        leTable.hideColumn(1)
        leTable.hideColumn(self.leadingE_M.columnCount()-2)
        # hide the ID column which is always at the end of the model
        leTable.hideColumn(self.leadingE_M.columnCount()-1)
        leTable.verticalHeader().setVisible(False)
        leTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        leTable.setFixedHeight(2
                               + leTable.horizontalHeader().height()
                               + leTable.rowHeight(0))

        leTable.setHelpBar(self.helpBar)
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.TypeCol,
                            _('PreProc-LE-Type-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.aOneCol,
                            _('PreProc-LE-a1-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.bOneCol,
                            _('PreProc-LE-b1-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.xOneCol,
                            _('PreProc-LE-x1-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.xTwoCol,
                            _('PreProc-LE-x2-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.xmCol,
                            _('PreProc-LE-xm-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.cZeroOneCol,
                            _('PreProc-LE-c01-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.exOneCol,
                            _('PreProc-LE-ex1-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.cZeroTwoCol,
                            _('PreProc-LE-c02-Desc'))
        leTable.setHelpText(PreProcModel.LeadingEdgeModel.exTwoCol,
                            _('PreProc-LE-ex2-Desc'))

        self.windowLayout.addWidget(le_L)
        self.windowLayout.addWidget(leTable)

        # Trailing Edge
        # TODO: remove type as the only allowed value is 1
        te_L = QLabel(_("Trailing edge"))
        teTable = TableView()
        teTable.setModel(self.trailingE_M)
        teTable.hideColumn(0)

        # Type is always 1
        # Therefore we hide the Column in the GUI
        teTable.hideColumn(1)
        teTable.hideColumn(self.trailingE_M.columnCount()-2)
        # hide the ID column which is always at the end of the model
        teTable.hideColumn(self.trailingE_M.columnCount()-1)
        teTable.verticalHeader().setVisible(False)
        teTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        teTable.setFixedHeight(2
                               + teTable.horizontalHeader().height()
                               + teTable.rowHeight(0))

        teTable.setHelpBar(self.helpBar)
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.TypeCol,
                            _('PreProc-TE-Type-Desc'))
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.aOneCol,
                            _('PreProc-TE-a1-Desc'))
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.bOneCol,
                            _('PreProc-TE-b1-Desc'))
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.xOneCol,
                            _('PreProc-TE-x1-Desc'))
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.xmCol,
                            _('PreProc-TE-xm-Desc'))
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.cZeroCol,
                            _('PreProc-TE-c0-Desc'))
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.yZeroCol,
                            _('PreProc-TE-y0-Desc'))
        teTable.setHelpText(PreProcModel.TrailingEdgeModel.expCol,
                            _('PreProc-TE-exp-Desc'))

        self.windowLayout.addWidget(te_L)
        self.windowLayout.addWidget(teTable)

        # Vault
        vault_L = QLabel(_("Vault"))
        vaultT_L = QLabel(_("Type"))
        vaultT_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                           QSizePolicy.Fixed))
        self.vaultT_CB = QComboBox()
        self.vaultT_CB.addItem(_("Sin-Cos"))
        self.vaultT_CB.addItem(_("Radius-Angle"))
        self.vaultT_CB.currentIndexChanged.connect(self.vaultCbChange)

        self.vaultTable = TableView()
        self.vaultTable.setModel(self.vault_M)
        self.vaultTable.hideColumn(0)
        self.vaultTable.hideColumn(1)
        self.vaultTable.hideColumn(self.vault_M.columnCount()-2)
        # hide the ID column which is always at the end of the model
        self.vaultTable.hideColumn(self.vault_M.columnCount()-1)
        self.vaultTable.verticalHeader().setVisible(False)
        self.vaultTable.horizontalHeader()\
            .setSectionResizeMode(QHeaderView.Stretch)
        self.vaultTable.setFixedHeight(2
                                       + self.vaultTable.horizontalHeader()
                                       .height()
                                       + self.vaultTable.rowHeight(0))

        self.vaultTable.setHelpBar(self.helpBar)
        self.vaultTable.setHelpText(PreProcModel.VaultModel.aOneCol,
                                    _('PreProc-Vault-a1-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.bOneCol,
                                    _('PreProc-Vault-b1-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.xOneCol,
                                    _('PreProc-Vault-x1-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.cOneCol,
                                    _('PreProc-Vault-c1-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.rOneRACol,
                                    _('PreProc-Vault-r1-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.rTwoRACol,
                                    _('PreProc-Vault-r2-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.rThrRACol,
                                    _('PreProc-Vault-r3-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.rFouRACol,
                                    _('PreProc-Vault-r4-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.aOneRACol,
                                    _('PreProc-Vault-ra1-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.aTwoRACol,
                                    _('PreProc-Vault-ra2-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.aThrRACol,
                                    _('PreProc-Vault-ra3-Desc'))
        self.vaultTable.setHelpText(PreProcModel.VaultModel.aFouRACol,
                                    _('PreProc-Vault-ra4-Desc'))

        self.vaultTable.enableDoubleValidator(
                            PreProcModel.VaultModel.aOneCol,
                            PreProcModel.VaultModel.aFouRACol,
                            0,
                            10000,
                            4)

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
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
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
        :method: Called if the Vault combobox is changed
        '''
        logging.debug(self.__className+'.vaultCbChange')

        # first check if CB is set correctly
        if self.vaultT_CB.currentIndex() == 0:
            self.vault_M.update_type(1, 1, 1)
            self.setTypeOneColumns()
        else:
            self.vault_M.update_type(1, 1, 2)
            self.setTypeTwoColumns()

    def vaultModelChange(self):
        '''
        :method:
        '''
        logging.debug(self.__className+'.vaultModelUpdate')

        vaultT = self.vault_M.get_type(1, 1)

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
        :method: Change the Vault table to display all columns needed for
                 type 1.
        '''
        logging.debug(self.__className+'.setTypeOneColumns')

        for i in range(PreProcModel.VaultModel.aOneCol,
                       PreProcModel.VaultModel.cOneCol + 1):
            self.vaultTable.showColumn(i)

        for i in range(PreProcModel.VaultModel.rOneRACol,
                       PreProcModel.VaultModel.aFouRACol + 1):
            self.vaultTable.hideColumn(i)

    def setTypeTwoColumns(self):
        '''
        :method: Change the Vault table to display all columns needed for
                 type 2.
        '''
        logging.debug(self.__className+'.setTypeTwoColumns')

        for i in range(PreProcModel.VaultModel.aOneCol,
                       PreProcModel.VaultModel.cOneCol + 1):
            self.vaultTable.hideColumn(i)

        for i in range(PreProcModel.VaultModel.rOneRACol,
                       PreProcModel.VaultModel.aFouRACol + 1):
            self.vaultTable.showColumn(i)

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
            logging.error(self.__className
                          + '.btn_press unrecognized button press '+q)
