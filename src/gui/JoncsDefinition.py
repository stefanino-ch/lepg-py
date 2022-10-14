"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, \
                            QHeaderView, QSpinBox, QLabel, \
                            QTabWidget, QHBoxLayout, QVBoxLayout, \
                            QPushButton, QComboBox

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class JoncsDefinition(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit airfoils holes data
    """

    __className = 'JoncsDefinition'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.win = None
        self.windowLayout = None
        self.helpBar = None
        self.tabs = None
        self.btnBar = None
        self.numConf_S = None

        self.pm = ProcModel()

        self.joncsDef_M = ProcModel.JoncsDefModel()
        self.joncsDef_M.numRowsForConfigChanged.connect(self.model_size_changed)

        self.type_CB = []
        self.numLines_s = []

        self.proxyModel = []
        self.table = []

        self.build_window()

    def closeEvent(self, event):  # @UnusedVariable
        """
        :method: Called at the time the user closes the window.
        """
        logging.debug(self.__className + '.closeEvent')

    def build_window(self):
        """
        :method: Creates the window including all GUI elements.

        Structure::

            window
                window_ly
                    config edit (blocs)
                    numConfSpin
                    Tabs
                        typeRadio
                        numLinesSpin
                        LinesTable
                    -------------------------
                        OrderBtn | help_bar  | btn_bar

        Naming:

            conf equals blocs
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1100, 400)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Joncs definition (Nylon rods)"))

        num_conf_l = QLabel(_('Number of blocs'))
        num_conf_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_conf_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                             QSizePolicy.Policy.Fixed))

        self.numConf_S = QSpinBox()
        self.numConf_S.setRange(0, 20)
        self.numConf_S.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                 QSizePolicy.Policy.Fixed))
        self.numConf_S.setValue(self.joncsDef_M.num_configs())

        edit = self.numConf_S.lineEdit()
        edit.setReadOnly(True)
        self.numConf_S.valueChanged.connect(self.conf_spin_change)

        num_conf_layout = QHBoxLayout()
        num_conf_layout.addWidget(num_conf_l)
        num_conf_layout.addWidget(self.numConf_S)
        num_conf_layout.addStretch()
        self.windowLayout.addLayout(num_conf_layout)

        self.tabs = QTabWidget()
        self.windowLayout.addWidget(self.tabs)

        # check if there's already data
        if self.joncsDef_M.num_configs() > 0:
            self.model_size_changed()

        sort_btn = QPushButton(_('Sort by order_num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                           QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/joncsDefinition.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(sort_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottom_layout)

        self.win.setLayout(self.windowLayout)

    def conf_spin_change(self):
        """
        :method: Called upon manual changes of the config spin. Does assure all
                 elements will follow the user configuration.
        """
        logging.debug(self.__className + '.conf_spin_change')
        curr_num_configs = self.joncsDef_M.num_configs()
        must_num_configs = self.numConf_S.value()

        if curr_num_configs > must_num_configs:
            # more tabs than we should have -> remove last
            self.joncsDef_M.set_num_rows_for_config(curr_num_configs, 0)

        if curr_num_configs < must_num_configs:
            # missing configs -> add one
            self.joncsDef_M.set_num_rows_for_config(must_num_configs, 1)

        self.pm.set_file_saved(False)

    def model_size_changed(self):
        """
        :method: Called after the model has been changed it's size. Herein we
                 assure the GUI follows the model.
        """
        logging.debug(self.__className + '.model_size_changed')

        curr_num_configs = self.joncsDef_M.num_configs()

        # config (num plans) spinbox
        if self.numConf_S.value() != curr_num_configs:
            self.numConf_S.blockSignals(True)
            self.numConf_S.setValue(curr_num_configs)
            self.numConf_S.blockSignals(False)

        # number of tabs
        diff = abs(curr_num_configs - self.tabs.count())
        if diff != 0:
            # we have to update the tabs
            i = 0
            if curr_num_configs > self.tabs.count():
                # add tabs
                while i < diff:
                    self.add_tab()
                    i += 1
            else:
                # remove tabs
                while i < diff:
                    self.remove_tab()
                    i += 1

        # update lines (path) spin
        i = 0
        while i < self.tabs.count():
            if self.numLines_s[i].value != self.joncsDef_M.\
                    num_rows_for_config(i + 1):
                self.numLines_s[i].blockSignals(True)
                self.numLines_s[i].setValue(self.joncsDef_M.
                                            num_rows_for_config(i + 1))
                self.numLines_s[i].blockSignals(False)

            type_num = self.joncsDef_M.getType(i + 1)
            if type_num == 0:
                # new empty row
                self.joncsDef_M.setType(i + 1, 1)
                self.set_type_one_columns()
            elif type_num == 1:
                # there is valid type 1 data
                self.type_CB[i].blockSignals(True)
                self.type_CB[i].setCurrentIndex(0)
                self.type_CB[i].blockSignals(False)
                self.set_type_one_columns()
            elif type_num == 2:
                # there is valid type 1 data
                self.type_CB[i].blockSignals(True)
                self.type_CB[i].setCurrentIndex(1)
                self.type_CB[i].blockSignals(False)
                self.set_type_two_columns()

            i += 1

    def add_tab(self):
        """
        :method: Creates a new tab including all its widgets.
        """
        logging.debug(self.__className + '.add_tab')

        curr_num_tabs = self.tabs.count()

        tab_widget = QWidget()
        tab_layout = QVBoxLayout()

        # Data lines
        type_layout = QHBoxLayout()
        type_l = QLabel(_('Type'))
        self.type_CB.append(QComboBox())
        self.type_CB[curr_num_tabs].addItem(_("1"))
        self.type_CB[curr_num_tabs].addItem(_("2"))
        self.type_CB[curr_num_tabs].currentIndexChanged.\
            connect(self.type_cb_change)
        type_layout.addWidget(type_l)
        type_layout.addWidget(self.type_CB[curr_num_tabs])
        type_layout.addStretch()
        tab_layout.addLayout(type_layout)

        lines_layout = QHBoxLayout()
        num_lines_l = QLabel(_('Number of groups'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.numLines_s.append(QSpinBox())
        self.numLines_s[curr_num_tabs].setRange(1, 100)
        self.numLines_s[curr_num_tabs].setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Fixed,
                        QSizePolicy.Policy.Fixed))
        self.numLines_s[curr_num_tabs].\
            valueChanged.connect(self.num_lines_change)
        path_edit = self.numLines_s[curr_num_tabs].lineEdit()
        path_edit.setReadOnly(True)
        lines_layout.addWidget(num_lines_l)
        lines_layout.addWidget(self.numLines_s[curr_num_tabs])
        lines_layout.addStretch()
        tab_layout.addLayout(lines_layout)

        self.proxyModel.append(QSortFilterProxyModel())
        self.proxyModel[curr_num_tabs].setSourceModel(self.joncsDef_M)
        self.proxyModel[curr_num_tabs].\
            setFilterKeyColumn(ProcModel.JoncsDefModel.ConfigNumCol)
        self.proxyModel[curr_num_tabs].\
            setFilterRegExp(QRegExp(str(curr_num_tabs + 1)))

        self.table.append(TableView())
        self.table[curr_num_tabs].setModel(self.proxyModel[curr_num_tabs])
        self.table[curr_num_tabs].verticalHeader().setVisible(False)
        self.table[curr_num_tabs].horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table[curr_num_tabs].hideColumn(self.joncsDef_M.columnCount() - 1)
        self.table[curr_num_tabs].hideColumn(self.joncsDef_M.columnCount() - 2)
        tab_layout.addWidget(self.table[curr_num_tabs])

        # TODO: enable validators
        #         branchTable.en_int_validator(ProcModel.LinesModel.OrderNumCol, ProcModel.LinesModel.OrderNumCol, 1, 999)
        #         branchTable.en_int_validator(ProcModel.LinesModel.NumBranchesCol, ProcModel.LinesModel.NumBranchesCol, 1, 4)
        #         branchTable.en_int_validator(ProcModel.LinesModel.BranchLvlOneCol, ProcModel.LinesModel.OrderLvlFourCol, 1, 99)
        #         branchTable.en_int_validator(ProcModel.LinesModel.AnchorLineCol, ProcModel.LinesModel.AnchorLineCol, 1, 6)
        #         branchTable.en_int_validator(ProcModel.LinesModel.AnchorRibNumCol, ProcModel.LinesModel.AnchorRibNumCol, 1, 999)
        #
        self.table[curr_num_tabs].setHelpBar(self.helpBar)
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.OrderNumCol,
                                              _('OrderNumDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.FirstRibCol,
                                              _('JoncsDef-FirstRibDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.LastRibCol,
                                              _('JoncsDef-LastRibDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pBACol,
                                              _('JoncsDef-pBADesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pBBCol,
                                              _('JoncsDef-pBBDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pBCCol,
                                              _('JoncsDef-pBCDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pBDCol,
                                              _('JoncsDef-pBDDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pBECol,
                                              _('JoncsDef-pBEDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pCACol,
                                              _('JoncsDef-pCADesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pCBCol,
                                              _('JoncsDef-pCBDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pCCCol,
                                              _('JoncsDef-pCCDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pCDCol,
                                              _('JoncsDef-pCDDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pDACol,
                                              _('JoncsDef-pDADesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pDBCol,
                                              _('JoncsDef-pDBDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pDCCol,
                                              _('JoncsDef-pDCDesc'))
        self.table[curr_num_tabs].setHelpText(ProcModel.JoncsDefModel.pDDCol,
                                              _('JoncsDef-pDDDesc'))

        tab_widget.setLayout(tab_layout)

        i = self.tabs.addTab(tab_widget, str(curr_num_tabs + 1))
        self.tabs.setCurrentIndex(i)

        type_num = self.joncsDef_M.getType(curr_num_tabs + 1)
        if type_num == 0:
            # new empty row
            self.joncsDef_M.setType(curr_num_tabs + 1, 1)
            self.set_type_one_columns()
        elif type_num == 1:
            # there is valid type 1 data
            self.type_CB[curr_num_tabs].blockSignals(True)
            self.type_CB[curr_num_tabs].setCurrentIndex(0)
            self.type_CB[curr_num_tabs].blockSignals(False)
            self.set_type_one_columns()
        elif type_num == 2:
            # there is valid type 1 data
            self.type_CB[curr_num_tabs].blockSignals(True)
            self.type_CB[curr_num_tabs].setCurrentIndex(1)
            self.type_CB[curr_num_tabs].blockSignals(False)
            self.set_type_two_columns()

    def remove_tab(self):
        """
        :method: Removes the last tab from the GUI. Does take care at the same
                 time of the class internal elements and the data model.
        """
        logging.debug(self.__className + '.remove_tab')
        num_tabs = self.tabs.count()

        self.tabs.removeTab(num_tabs - 1)
        # cleanup arrays
        self.type_CB.pop(num_tabs - 1)
        self.numLines_s.pop(num_tabs - 1)
        self.proxyModel.pop(num_tabs - 1)
        self.table.pop(num_tabs - 1)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all
                elements will follow the user configuration.
        """
        logging.debug(self.__className + '.num_lines_change')
        self.joncsDef_M.set_num_rows_for_config(
            self.tabs.currentIndex() + 1,
            self.numLines_s[self.tabs.currentIndex()].value())

        curr_tab = self.tabs.currentIndex()
        if self.type_CB[curr_tab].currentIndex() == 0:
            self.joncsDef_M.setType(curr_tab + 1, 1)
        else:
            self.joncsDef_M.setType(curr_tab + 1, 2)

        self.pm.set_file_saved(False)

    def type_cb_change(self):
        """
        :method: Called upon manual changes of the type combo. Does assure all
                 elements will follow the user configuration.
        """
        logging.debug(self.__className + '.type_cb_change')

        curr_tab = self.tabs.currentIndex()

        if self.type_CB[curr_tab].currentIndex() == 0:
            # show rows for type 1
            self.set_type_one_columns()
            self.joncsDef_M.setType(curr_tab + 1, 1)

        else:
            # show rows for type 2
            self.set_type_two_columns()
            self.joncsDef_M.setType(curr_tab + 1, 2)

        self.pm.set_file_saved(False)

    def set_type_one_columns(self):
        """
        :method: Enables disables table columns to be accurate for type
                 one tables
        """
        curr_tab = self.tabs.currentIndex()
        self.table[curr_tab].hideColumn(ProcModel.JoncsDefModel.pBECol)

        self.table[curr_tab].showColumn(ProcModel.JoncsDefModel.pCACol)
        self.table[curr_tab].showColumn(ProcModel.JoncsDefModel.pCBCol)
        self.table[curr_tab].showColumn(ProcModel.JoncsDefModel.pCCCol)
        self.table[curr_tab].showColumn(ProcModel.JoncsDefModel.pCDCol)
        self.table[curr_tab].hideColumn(ProcModel.JoncsDefModel.TypeCol)

    def set_type_two_columns(self):
        """
        :method: Enables disables table columns to be accurate for type
                 two tables
        """
        curr_tab = self.tabs.currentIndex()
        self.table[curr_tab].showColumn(ProcModel.JoncsDefModel.pBECol)

        self.table[curr_tab].hideColumn(ProcModel.JoncsDefModel.pCACol)
        self.table[curr_tab].hideColumn(ProcModel.JoncsDefModel.pCBCol)
        self.table[curr_tab].hideColumn(ProcModel.JoncsDefModel.pCCCol)
        self.table[curr_tab].hideColumn(ProcModel.JoncsDefModel.pCDCol)
        self.table[curr_tab].hideColumn(ProcModel.JoncsDefModel.TypeCol)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        """
        logging.debug(self.__className + '.sort_btn_press')

        if self.tabs.count() > 0:
            curr_tab = self.tabs.currentIndex()
            self.proxyModel[curr_tab].sort(
                ProcModel.JoncsDefModel.OrderNumCol,
                Qt.AscendingOrder)
            self.proxyModel[curr_tab].setDynamicSortFilter(False)

    def btn_press(self, q):
        """
        :method: Handling of all pressed buttons.
        """
        logging.debug(self.__className + '.btn_press')
        if q == 'Apply':
            pass

        elif q == 'Ok':
            self.close()

        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className
                          + '.btn_press unrecognized button press '
                          + q)
