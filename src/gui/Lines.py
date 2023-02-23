"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView,\
                            QSpinBox, QLabel, QTabWidget, QHBoxLayout,\
                            QVBoxLayout, QPushButton, QDataWidgetMapper
from gui.elements.LineEdit import LineEdit
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.procModel.LinesModel import LinesModel
from data.procModel.WingModel import WingModel
from data.ProcModel import ProcModel
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class Lines(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit lines data
    """

    __className = 'Lines'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        self.tabs = None
        self.numConf_s = None
        self.btnBar = None
        self.control_e = None
        self.helpBar = None
        self.window_ly = None
        self.win = None
        self.wrapper = None
        super().__init__()

        self.pm = ProcModel()

        self.wing_M = WingModel()
        self.wing_M.dataChanged.connect(self.wing_model_data_change)

        self.lines_M = LinesModel()
        self.lines_M.numRowsForConfigChanged.connect(self.model_size_changed)

        self.proxyModel = []
        self.numLines_s = []

        self.build_window()

    def closeEvent(self, event):
        """
        :method: Called at the time the user closes the window.
        """
        pass

    def build_window(self):
        """
        :method: Creates the window including all GUI elements.

        Structure::

            window
                window_ly
                    config edit
                    numConfSpin
                    Tabs
                        numLinesSpin
                        LinesTable
                    -------------------------
                        OrderBtn | help_bar  | btn_bar

        Naming:

            conf equals plans
            details equals line paths
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1100, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Edit Lines"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.wing_M)

        control_l = QLabel(_('Lines control parameter'))
        control_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.control_e = LineEdit()
        self.control_e.setFixedWidth(40)
        self.wrapper.addMapping(self.control_e,
                                WingModel.LinesConcTypeCol)
        self.control_e.en_int_validator(ValidationValues.Proc.LinesControlParamMin,
                                        ValidationValues.Proc.LinesControlParamMax)

        self.control_e.set_help_text(_('Lines-LinesControlParamDesc'))
        self.control_e.set_help_bar(self.helpBar)

        control_layout = QHBoxLayout()
        control_layout.addWidget(control_l)
        control_layout.addWidget(self.control_e)
        control_layout.addStretch()

        self.window_ly.addLayout(control_layout)

        num_conf_l = QLabel(_('Number of Line plans'))
        num_conf_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_conf_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                             QSizePolicy.Policy.Fixed))

        self.numConf_s = QSpinBox()
        self.numConf_s.setRange(0, ValidationValues.MaxNumRibs)

        self.numConf_s.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                 QSizePolicy.Policy.Fixed))
        self.numConf_s.setValue(self.lines_M.num_configs())

        edit = self.numConf_s.lineEdit()
        edit.setReadOnly(True)
        self.numConf_s.valueChanged.connect(self.conf_spin_change)

        num_conf_layout = QHBoxLayout()
        num_conf_layout.addWidget(num_conf_l)
        num_conf_layout.addWidget(self.numConf_s)
        num_conf_layout.addStretch()
        self.window_ly.addLayout(num_conf_layout)

        self.tabs = QTabWidget()
        self.window_ly.addWidget(self.tabs)

        # check if there's already data
        if self.lines_M.num_configs() > 0:
            self.model_size_changed()

        sort_btn = QPushButton(_('Sort by order_num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                           QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        self.wrapper.toFirst()
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/lines.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(sort_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def conf_spin_change(self):
        """
        :method: Called upon manual changes of the config spin. Does assure
                 all elements will follow the user configuration.
        """
        curr_num_configs = self.lines_M.num_configs()
        must_num_configs = self.numConf_s.value()

        if curr_num_configs > must_num_configs:
            # more tabs than we should have -> remove last
            self.lines_M.set_num_rows_for_config(curr_num_configs, 0)

        if curr_num_configs < must_num_configs:
            # missing configs -> add one
            self.lines_M.set_num_rows_for_config(must_num_configs, 1)

        self.pm.set_file_saved(False)

    def model_size_changed(self):
        """
        :method: Called after the model has been changed it's size.
                 Herein we assure the GUI follows the model.
        """
        curr_num_configs = self.lines_M.num_configs()

        # config (num plans) spinbox
        if self.numConf_s.value() != curr_num_configs:
            self.numConf_s.blockSignals(True)
            self.numConf_s.setValue(curr_num_configs)
            self.numConf_s.blockSignals(False)

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
            if self.numLines_s[i].value != self.lines_M.num_rows_for_config(i + 1):
                self.numLines_s[i].blockSignals(True)
                self.numLines_s[i].setValue(self.lines_M.num_rows_for_config(i + 1))
                self.numLines_s[i].blockSignals(False)
            i += 1

    def add_tab(self):
        """
        :method: Creates a new tab including all its widgets.
        """
        curr_num_tabs = self.tabs.count()

        tab_widget = QWidget()
        tab_layout = QVBoxLayout()

        # Data lines
        num_lines_layout = QHBoxLayout()

        num_lines_l = QLabel(_('Number of Line paths'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.numLines_s.append(QSpinBox())
        self.numLines_s[curr_num_tabs].setRange(1, ValidationValues.MaxNumRibs)

        self.numLines_s[curr_num_tabs].setSizePolicy(QSizePolicy(
                                                     QSizePolicy.Policy.Fixed,
                                                     QSizePolicy.Policy.Fixed))
        self.numLines_s[curr_num_tabs].valueChanged.connect(self.num_lines_change)
        path_edit = self.numLines_s[curr_num_tabs].lineEdit()
        path_edit.setReadOnly(True)
        num_lines_layout.addWidget(num_lines_l)
        num_lines_layout.addWidget(self.numLines_s[curr_num_tabs])
        num_lines_layout.addStretch()
        tab_layout.addLayout(num_lines_layout)

        self.proxyModel.append(QSortFilterProxyModel())
        self.proxyModel[curr_num_tabs].setSourceModel(self.lines_M)
        self.proxyModel[curr_num_tabs].setFilterKeyColumn(
                                        LinesModel.ConfigNumCol)

        self.proxyModel[curr_num_tabs].setFilterRegularExpression(
                                        QRegularExpression(str(curr_num_tabs+1)))

        branch_table = TableView()
        branch_table.setModel(self.proxyModel[curr_num_tabs])
        branch_table.verticalHeader().setVisible(False)
        branch_table.horizontalHeader().setSectionResizeMode(
                                            QHeaderView.ResizeMode.Stretch)
        branch_table.hideColumn(self.lines_M.columnCount()-1)
        branch_table.hideColumn(self.lines_M.columnCount()-2)
        tab_layout.addWidget(branch_table)

        branch_table.en_int_validator(LinesModel.OrderNumCol,
                                      LinesModel.OrderNumCol,
                                      1,
                                      ValidationValues.MaxNumRibs)

        branch_table.en_int_validator(LinesModel.NumBranchesCol,
                                      LinesModel.NumBranchesCol,
                                      1,
                                      4)

        branch_table.en_int_validator(LinesModel.LevelOfRamOneCol,
                                      LinesModel.LevelOfRamOneCol,
                                      ValidationValues.Proc.NumLineLevelsMin,
                                      ValidationValues.Proc.NumLineLevelsMax)
        branch_table.en_int_validator(LinesModel.OrderLvlOneCol,
                                      LinesModel.OrderLvlOneCol,
                                      ValidationValues.Proc.LineOrderNumMin,
                                      ValidationValues.Proc.LineOrderNumMax)

        branch_table.en_int_validator(LinesModel.LevelOfRamTwoCol,
                                      LinesModel.LevelOfRamTwoCol,
                                      ValidationValues.Proc.NumLineLevelsMin,
                                      ValidationValues.Proc.NumLineLevelsMax)
        branch_table.en_int_validator(LinesModel.OrderLvlTwoCol,
                                      LinesModel.OrderLvlTwoCol,
                                      ValidationValues.Proc.LineOrderNumMin,
                                      ValidationValues.Proc.LineOrderNumMax)

        branch_table.en_int_validator(LinesModel.LevelOfRamThreeCol,
                                      LinesModel.LevelOfRamThreeCol,
                                      ValidationValues.Proc.NumLineLevelsMin,
                                      ValidationValues.Proc.NumLineLevelsMax)
        branch_table.en_int_validator(LinesModel.OrderLvlThreeCol,
                                      LinesModel.OrderLvlThreeCol,
                                      ValidationValues.Proc.LineOrderNumMin,
                                      ValidationValues.Proc.LineOrderNumMax)

        branch_table.en_int_validator(LinesModel.LevelOfRamFourCol,
                                      LinesModel.LevelOfRamFourCol,
                                      ValidationValues.Proc.NumLineLevelsMin,
                                      ValidationValues.Proc.NumLineLevelsMax)
        branch_table.en_int_validator(LinesModel.OrderLvlFourCol,
                                      LinesModel.OrderLvlFourCol,
                                      ValidationValues.Proc.LineOrderNumMin,
                                      ValidationValues.Proc.LineOrderNumMax)

        branch_table.en_int_validator(LinesModel.AnchorLineCol,
                                      LinesModel.AnchorLineCol,
                                      ValidationValues.Proc.AnchorsNumMin,
                                      ValidationValues.Proc.AnchorsNumMax)

        branch_table.en_int_validator(LinesModel.AnchorRibNumCol,
                                      LinesModel.AnchorRibNumCol,
                                      1,
                                      ValidationValues.MaxNumRibs)

        branch_table.set_help_bar(self.helpBar)
        branch_table.set_help_text(
                        LinesModel.OrderNumCol,
                        _('OrderNumDesc'))
        branch_table.set_help_text(
                        LinesModel.NumBranchesCol,
                        _('Lines-NumBranchesDesc'))
        branch_table.set_help_text(
                        LinesModel.LevelOfRamOneCol,
                        _('Lines-BranchLvlOneDesc'))
        branch_table.set_help_text(
                        LinesModel.OrderLvlOneCol,
                        _('Lines-OrderLvlOneDesc'))
        branch_table.set_help_text(
                        LinesModel.LevelOfRamTwoCol,
                        _('Lines-LevelOfRamTwoDesc'))
        branch_table.set_help_text(
                        LinesModel.OrderLvlTwoCol,
                        _('Lines-OrderLvlTwoDesc'))
        branch_table.set_help_text(
                        LinesModel.LevelOfRamThreeCol,
                        _('Lines-LevelOfRamThreeDesc'))
        branch_table.set_help_text(
                        LinesModel.OrderLvlThreeCol,
                        _('Lines-OrderLvlThreeDesc'))
        branch_table.set_help_text(
                        LinesModel.LevelOfRamFourCol,
                        _('Lines-BranchLvlFourDesc'))
        branch_table.set_help_text(
                        LinesModel.OrderLvlFourCol,
                        _('Lines-OrderLvlFourDesc'))
        branch_table.set_help_text(
                        LinesModel.AnchorLineCol,
                        _('Lines-AnchorLineDesc'))
        branch_table.set_help_text(
                        LinesModel.AnchorRibNumCol,
                        _('Lines-AnchorRibNumDesc'))

        tab_widget.setLayout(tab_layout)

        i = self.tabs.addTab(tab_widget, str(curr_num_tabs + 1))
        self.tabs.setCurrentIndex(i)

    def remove_tab(self):
        """
        :method: Removes the last tab from the GUI. Does take care at the same
                 time of the class internal elements and the data model.
        """
        num_tabs = self.tabs.count()
        self.tabs.removeTab(num_tabs - 1)
        # cleanup arrays
        self.proxyModel.pop(num_tabs-1)
        self.numLines_s.pop(num_tabs - 1)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure
                 all elements will follow the user configuration.
        """
        self.lines_M.set_num_rows_for_config(
                        self.tabs.currentIndex()+1,
                        self.numLines_s[self.tabs.currentIndex()].value())
        self.pm.set_file_saved(False)

    def wing_model_data_change(self):
        """
        :method: Called if data in wing model changes. As mappings are lost
                 upon the use of select we have potentially to re-establish
                 the mapping again.
        """
        self.wrapper.addMapping(self.control_e,
                                WingModel.LinesConcTypeCol)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        """
        if self.tabs.count() > 0:
            curr_tab = self.tabs.currentIndex()
            self.proxyModel[curr_tab].sort(LinesModel.OrderNumCol,
                                           Qt.SortOrder.AscendingOrder)
            self.proxyModel[curr_tab].setDynamicSortFilter(False)

    def btn_press(self, q):
        """
        :method: Handling of all pressed buttons.
        """
        if q == 'Apply':
            pass

        elif q == 'Ok':
            self.close()

        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className +
                          '.btn_press unrecognized button press '+q)
