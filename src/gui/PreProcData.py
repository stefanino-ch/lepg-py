"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget,\
                            QSizePolicy, QHeaderView,\
                            QLabel, QComboBox
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.PreProcModel import PreProcModel


class PreProcData(QMdiSubWindow):
    """
    :class: Window to display and edit Skin tension data
    """

    __className = 'PreProcData'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        self.win = None
        self.window_ly = None
        self.help_bar = None
        self.vault_t_cb = None
        self.vault_table = None
        self.btnBar = None
        logging.debug(self.__className+'.__init__')
        super().__init__()

        self.gen_M = PreProcModel.GenModel()
        self.leadingE_M = PreProcModel.LeadingEdgeModel()
        self.trailingE_M = PreProcModel.TrailingEdgeModel()

        self.vault_M = PreProcModel.VaultModel()
        self.vault_M.didSelect.connect(self.vault_model_change)

        self.build_window()

    def closeEvent(self, event):  # @UnusedVariable
        """
        :method: Called at the time the user closes the window.
        """
        logging.debug(self.__className+'.closeEvent')

    def build_window(self):
        """
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
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 400)

        self.window_ly = QVBoxLayout()

        self.help_bar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Pre-Processor data"))

        gen_l = QLabel(_("Generals"))
        gen_table = TableView()
        gen_table.setModel(self.gen_M)
        gen_table.hideColumn(0)
        gen_table.hideColumn(self.gen_M.columnCount()-2)
        # hide the ID column which is always at the end of the model
        gen_table.hideColumn(self.gen_M.columnCount()-1)
        gen_table.verticalHeader().setVisible(False)
        gen_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        gen_table.setFixedHeight(2
                                 + gen_table.horizontalHeader().height()
                                 + gen_table.rowHeight(0))
        gen_table.setHelpBar(self.help_bar)

        gen_table.setHelpText(PreProcModel.GenModel.WingNameCol,
                              _('PreProc-WingNameDesc'))

        gen_table.enableRegExpValidator(PreProcModel.GenModel.WingNameCol,
                                        PreProcModel.GenModel.WingNameCol,
                                        "^[a-zA-Z0-9_.-]*$")

        gen_ly = QHBoxLayout()
        gen_ly.addWidget(gen_table)
        gen_ly.addStretch()
        self.window_ly.addWidget(gen_l)
        self.window_ly.addLayout(gen_ly)

        # Leading Edge
        # TODO: remove type as the only allowed value is 1
        le_l = QLabel(_("Leading edge"))
        le_table = TableView()
        le_table.setModel(self.leadingE_M)
        le_table.hideColumn(0)

        # Type is always 1
        # Therefore we hide the Column in the GUI
        le_table.hideColumn(1)
        le_table.hideColumn(self.leadingE_M.columnCount()-2)
        # hide the ID column which is always at the end of the model
        le_table.hideColumn(self.leadingE_M.columnCount()-1)
        le_table.verticalHeader().setVisible(False)
        le_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        le_table.setFixedHeight(2
                                + le_table.horizontalHeader().height()
                                + le_table.rowHeight(0))

        le_table.setHelpBar(self.help_bar)
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.TypeCol,
                             _('PreProc-LE-Type-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.aOneCol,
                             _('PreProc-LE-a1-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.bOneCol,
                             _('PreProc-LE-b1-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.xOneCol,
                             _('PreProc-LE-x1-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.xTwoCol,
                             _('PreProc-LE-x2-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.xmCol,
                             _('PreProc-LE-xm-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.cZeroOneCol,
                             _('PreProc-LE-c01-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.exOneCol,
                             _('PreProc-LE-ex1-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.cZeroTwoCol,
                             _('PreProc-LE-c02-Desc'))
        le_table.setHelpText(PreProcModel.LeadingEdgeModel.exTwoCol,
                             _('PreProc-LE-ex2-Desc'))

        self.window_ly.addWidget(le_l)
        self.window_ly.addWidget(le_table)

        # Trailing Edge
        # TODO: remove type as the only allowed value is 1
        te_l = QLabel(_("Trailing edge"))
        te_table = TableView()
        te_table.setModel(self.trailingE_M)
        te_table.hideColumn(0)

        # Type is always 1
        # Therefore we hide the Column in the GUI
        te_table.hideColumn(1)
        te_table.hideColumn(self.trailingE_M.columnCount()-2)
        # hide the ID column which is always at the end of the model
        te_table.hideColumn(self.trailingE_M.columnCount()-1)
        te_table.verticalHeader().setVisible(False)
        te_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        te_table.setFixedHeight(2
                                + te_table.horizontalHeader().height()
                                + te_table.rowHeight(0))

        te_table.setHelpBar(self.help_bar)
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.TypeCol,
                             _('PreProc-TE-Type-Desc'))
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.aOneCol,
                             _('PreProc-TE-a1-Desc'))
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.bOneCol,
                             _('PreProc-TE-b1-Desc'))
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.xOneCol,
                             _('PreProc-TE-x1-Desc'))
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.xmCol,
                             _('PreProc-TE-xm-Desc'))
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.cZeroCol,
                             _('PreProc-TE-c0-Desc'))
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.yZeroCol,
                             _('PreProc-TE-y0-Desc'))
        te_table.setHelpText(PreProcModel.TrailingEdgeModel.expCol,
                             _('PreProc-TE-exp-Desc'))

        self.window_ly.addWidget(te_l)
        self.window_ly.addWidget(te_table)

        # Vault
        vault_l = QLabel(_("Vault"))
        vault_t_l = QLabel(_("Type"))
        vault_t_l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                            QSizePolicy.Fixed))
        self.vault_t_cb = QComboBox()
        self.vault_t_cb.addItem(_("Sin-Cos"))
        self.vault_t_cb.addItem(_("Radius-Angle"))
        self.vault_t_cb.currentIndexChanged.connect(self.vault_cb_change)

        self.vault_table = TableView()
        self.vault_table.setModel(self.vault_M)
        self.vault_table.hideColumn(0)
        self.vault_table.hideColumn(1)
        self.vault_table.hideColumn(self.vault_M.columnCount() - 2)
        # hide the ID column which is always at the end of the model
        self.vault_table.hideColumn(self.vault_M.columnCount() - 1)
        self.vault_table.verticalHeader().setVisible(False)
        self.vault_table.horizontalHeader()\
            .setSectionResizeMode(QHeaderView.Stretch)
        self.vault_table.setFixedHeight(2
                                        + self.vault_table.horizontalHeader()
                                        .height()
                                        + self.vault_table.rowHeight(0))

        self.vault_table.setHelpBar(self.help_bar)
        self.vault_table.setHelpText(PreProcModel.VaultModel.aOneCol,
                                     _('PreProc-Vault-a1-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.bOneCol,
                                     _('PreProc-Vault-b1-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.xOneCol,
                                     _('PreProc-Vault-x1-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.cOneCol,
                                     _('PreProc-Vault-c1-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.rOneRACol,
                                     _('PreProc-Vault-r1-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.rTwoRACol,
                                     _('PreProc-Vault-r2-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.rThrRACol,
                                     _('PreProc-Vault-r3-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.rFouRACol,
                                     _('PreProc-Vault-r4-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.aOneRACol,
                                     _('PreProc-Vault-ra1-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.aTwoRACol,
                                     _('PreProc-Vault-ra2-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.aThrRACol,
                                     _('PreProc-Vault-ra3-Desc'))
        self.vault_table.setHelpText(PreProcModel.VaultModel.aFouRACol,
                                     _('PreProc-Vault-ra4-Desc'))

        self.vault_table.enableDoubleValidator(
                            PreProcModel.VaultModel.aOneCol,
                            PreProcModel.VaultModel.aFouRACol,
                            0,
                            10000,
                            4)

        self.window_ly.addWidget(vault_l)
        vault_t_ly = QHBoxLayout()
        vault_t_ly.addWidget(vault_t_l)
        vault_t_ly.addWidget(self.vault_t_cb)
        vault_t_ly.addStretch()
        self.window_ly.addLayout(vault_t_ly)
        self.window_ly.addWidget(self.vault_table)

        self.vault_model_change()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('preproc/name_le_te_vault.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_bar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def vault_cb_change(self):
        """
        :method: Called if the Vault combobox is changed
        """
        logging.debug(self.__className+'.vault_cb_change')

        # first check if CB is set correctly
        if self.vault_t_cb.currentIndex() == 0:
            self.vault_M.update_type(1, 1, 1)
            self.set_type_one_columns()
        else:
            self.vault_M.update_type(1, 1, 2)
            self.set_type_two_columns()

    def vault_model_change(self):
        """
        :method:
        """
        logging.debug(self.__className+'.vaultModelUpdate')

        vault_t = self.vault_M.get_type(1, 1)

        if vault_t == 1:
            self.vault_t_cb.blockSignals(True)
            self.vault_t_cb.setCurrentIndex(0)
            self.vault_t_cb.blockSignals(False)
            self.set_type_one_columns()
        else:
            self.vault_t_cb.blockSignals(True)
            self.vault_t_cb.setCurrentIndex(1)
            self.vault_t_cb.blockSignals(False)
            self.set_type_two_columns()

    def set_type_one_columns(self):
        """
        :method: Change the Vault table to display all columns needed for
                 type 1.
        """
        logging.debug(self.__className+'.set_type_one_columns')

        for i in range(PreProcModel.VaultModel.aOneCol,
                       PreProcModel.VaultModel.cOneCol + 1):
            self.vault_table.showColumn(i)

        for i in range(PreProcModel.VaultModel.rOneRACol,
                       PreProcModel.VaultModel.aFouRACol + 1):
            self.vault_table.hideColumn(i)

    def set_type_two_columns(self):
        """
        :method: Change the Vault table to display all columns needed for
                 type 2.
        """
        logging.debug(self.__className+'.set_type_two_columns')

        for i in range(PreProcModel.VaultModel.aOneCol,
                       PreProcModel.VaultModel.cOneCol + 1):
            self.vault_table.hideColumn(i)

        for i in range(PreProcModel.VaultModel.rOneRACol,
                       PreProcModel.VaultModel.aFouRACol + 1):
            self.vault_table.showColumn(i)

    def btn_press(self, q):
        """
        :method: Handling of all pressed buttons.
        """
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
