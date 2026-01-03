"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
                            QSpinBox, QLabel, QTabWidget, QHBoxLayout, \
                            QVBoxLayout, QPushButton, QComboBox, QGridLayout

from data.ProcModel import ProcModel
from data.procModel.IntradosColsConfModel import IntradosColsConfModel
from data.procModel.IntradosColsDetModel import IntradosColsDetModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class IntradColors(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit intrados (lower sail) colors data
    """

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()

        self.usage_cb = None
        self.helpBar = None
        self.windowLayout = None
        self.btnBar = None
        self.tabs = None
        self.numConf_s = None
        self.win = None

        self.pm = ProcModel()

        self.intradColsConf_M = IntradosColsConfModel()
        self.intradColsConf_M.usageUpd.connect(self.model_usage_changed)
        self.intradColsConf_M.numRowsForConfigChanged. \
            connect(self.model_num_configs_changed)

        self.intradColsDet_M = IntradosColsDetModel()
        self.intradColsDet_M.numRowsForConfigChanged.connect(self.update_tabs)

        self.confProxyModel = []

        self.detProxyModel = []
        self.numDet_s = []
        self.det_t = []

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
                    Type combo box
                    numConfSpin
                    Tabs
                        configTable
                        numDetSpin
                        detailTable
                    -------------------------
                            help_bar  | btn_bar
        """
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(400, 400)
        self.windowLayout = QVBoxLayout()
        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Colors lower sail"))

        usage_l = QLabel(_('Type'))
        self.usage_cb = QComboBox()
        self.usage_cb.addItem(_("None"))
        self.usage_cb.addItem(_("cols_old_style"))
        self.usage_cb.addItem(_("cols_new_style"))
        self.usage_cb.currentIndexChanged.connect(self.usage_cb_change)

        num_conf_l = QLabel(_('Number of configs'))
        self.numConf_s = QSpinBox()
        self.numConf_s.setRange(0, ValidationValues.MaxNumRibs)
        self.numConf_s.setValue(self.intradColsConf_M.num_configs())
        conf_edit = self.numConf_s.lineEdit()
        conf_edit.setReadOnly(True)
        self.numConf_s.valueChanged.connect(self.conf_spin_change)
        self.numConf_s.setEnabled(False)

        window_header_g_lo = QGridLayout()
        window_header_g_lo.addWidget(usage_l, 0, 0, Qt.AlignmentFlag.AlignRight)
        window_header_g_lo.addWidget(self.usage_cb,0,1)
        window_header_g_lo.addWidget(num_conf_l, 1, 0, Qt.AlignmentFlag.AlignRight)
        window_header_g_lo.addWidget(self.numConf_s, 1, 1)

        window_header_h_lo = QHBoxLayout()
        window_header_h_lo.addLayout(window_header_g_lo)
        window_header_h_lo.addStretch()

        self.windowLayout.addLayout(window_header_h_lo)

        self.tabs = QTabWidget()
        self.windowLayout.addWidget(self.tabs)

        # check if there's already data
        if self.intradColsConf_M.type() != 0:
            self.model_usage_changed()

        if self.intradColsConf_M.num_configs() > 0:
            self.model_num_configs_changed()

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
        self.btnBar.set_help_page('proc/intradosColors.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(sort_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottom_layout)

        self.win.setLayout(self.windowLayout)

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage cb has been changed
        :return: na
        """
        self.intradColsConf_M.set_type(self.usage_cb.currentIndex())
        self.pm.set_file_saved(False)

    def model_usage_changed(self):
        """
        :method: Updates the window after a change of the usage information in the model
        :return: na
        """
        intrados_type = self.intradColsConf_M.type()
        self.usage_cb.blockSignals(True)
        self.usage_cb.setCurrentIndex(intrados_type)
        self.usage_cb.blockSignals(False)

        match intrados_type:
            case 0:
                # section not used
                self.numConf_s.setValue(0)
                self.numConf_s.setEnabled(False)
            case 1:
                # old style setup
                self.numConf_s.setEnabled(True)
                for table in self.det_t:
                    table.hideColumn(self.intradColsDet_M.DistTeRightCol)
                    table.hideColumn(self.intradColsDet_M.SeamCol)
            case 2:
                # new style setup
                self.numConf_s.setEnabled(True)
                for table in self.det_t:
                    table.showColumn(self.intradColsDet_M.DistTeRightCol)
                    table.showColumn(self.intradColsDet_M.SeamCol)

    def conf_spin_change(self):
        """
        :method: Called upon manual changes of the config spin. Does assure
                 all elements will follow the user configuration.
        """
        self.intradColsConf_M.set_num_configs(self.numConf_s.value())
        self.pm.set_file_saved(False)

    def model_num_configs_changed(self):
        """
        :method: Called upon changes of the configs model. Does assure all GUI
                 elements will follow the changes.
        """
        current_num_configs = self.intradColsConf_M.num_configs()

        self.numConf_s.blockSignals(True)
        self.numConf_s.setValue(current_num_configs)
        self.numConf_s.blockSignals(False)

        diff = abs(current_num_configs - self.tabs.count())
        if diff != 0:
            # we have to update the tabs
            i = 0
            if current_num_configs > self.tabs.count():
                # add tabs
                while i < diff:
                    self.add_tab()
                    i += 1
            else:
                # remove tabs
                while i < diff:
                    self.remove_tab()
                    i += 1

    def det_spin_change(self):
        """
        :method: Called upon manual changes of the detail spin. Does assure
                 all elements will follow the user configuration.
        """
        self.intradColsDet_M. \
            set_num_rows_for_config(
                self.tabs.currentIndex() + 1,
                self.numDet_s[self.tabs.currentIndex()].value())
        self.pm.set_file_saved(False)

    def add_tab(self):
        """
        :method: Creates a new tab including all its widgets.
        """
        curr_num_tabs = self.tabs.count()

        tab_widget = QWidget()
        tab_layout = QVBoxLayout()

        # Configuration 
        conf_table = TableView()
        self.confProxyModel.append(QSortFilterProxyModel())
        self.confProxyModel[curr_num_tabs].setSourceModel(self.intradColsConf_M)
        self.confProxyModel[curr_num_tabs].setFilterKeyColumn(IntradosColsConfModel.ConfigNumCol)
        self.confProxyModel[curr_num_tabs].setFilterRegularExpression(QRegularExpression(str(curr_num_tabs + 1)))

        conf_table.setModel(self.confProxyModel[curr_num_tabs])
        conf_table.verticalHeader().setVisible(False)
        conf_table.hideColumn(self.intradColsConf_M.OrderNumCol)
        conf_table.hideColumn(self.intradColsConf_M.columnCount() - 1)
        conf_table.hideColumn(self.intradColsConf_M.columnCount() - 2)

        conf_table.en_int_validator(
            IntradosColsConfModel.FirstRibCol,
            IntradosColsConfModel.FirstRibCol, 1, ValidationValues.MaxNumRibs)

        conf_table.set_help_bar(self.helpBar)
        conf_table.set_help_text(IntradosColsConfModel.FirstRibCol,
                                 _('IntradCols-FirstRibDesc'))

        conf_layout = QHBoxLayout()
        conf_layout.addWidget(conf_table)
        conf_layout.addStretch()
        conf_table.setFixedWidth(2
                                 + conf_table.columnWidth(
                                    IntradosColsConfModel.FirstRibCol))
        conf_table.setFixedHeight(2
                                  + conf_table.horizontalHeader().height()
                                  + conf_table.rowHeight(0))
        tab_layout.addLayout(conf_layout)

        # Data lines
        num_det_l = QLabel(_('Number of config lines'))
        num_det_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_det_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                            QSizePolicy.Policy.Fixed))

        self.numDet_s.append(QSpinBox())
        self.numDet_s[curr_num_tabs].setRange(1, ValidationValues.Proc.MaxNumColorLines)
        self.numDet_s[curr_num_tabs].setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.numDet_s[curr_num_tabs].valueChanged.connect(self.det_spin_change)
        det_edit = self.numDet_s[curr_num_tabs].lineEdit()
        det_edit.setReadOnly(True)

        det_num_layout = QHBoxLayout()
        det_num_layout.addWidget(num_det_l)
        det_num_layout.addWidget(self.numDet_s[curr_num_tabs])
        det_num_layout.addStretch()
        tab_layout.addLayout(det_num_layout)

        # add here the code for the details table
        self.det_t.append(TableView())
        self.detProxyModel.append(QSortFilterProxyModel())
        self.detProxyModel[curr_num_tabs].setSourceModel(self.intradColsDet_M)
        self.detProxyModel[curr_num_tabs].setFilterKeyColumn(IntradosColsDetModel.ConfigNumCol)
        self.detProxyModel[curr_num_tabs].setFilterRegularExpression(QRegularExpression(str(curr_num_tabs + 1)))

        self.det_t[curr_num_tabs].setModel(self.detProxyModel[curr_num_tabs])
        self.det_t[curr_num_tabs].verticalHeader().setVisible(False)
        self.det_t[curr_num_tabs].horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        match self.usage_cb.currentIndex():
            case 1:# old style
                self.det_t[curr_num_tabs].hideColumn(self.intradColsDet_M.DistTeRightCol)
                self.det_t[curr_num_tabs].hideColumn(self.intradColsDet_M.SeamCol)
            case 2:
                self.det_t[curr_num_tabs].showColumn(self.intradColsDet_M.DistTeRightCol)
                self.det_t[curr_num_tabs].showColumn(self.intradColsDet_M.SeamCol)

        self.det_t[curr_num_tabs].hideColumn(self.intradColsDet_M.columnCount() - 1)
        self.det_t[curr_num_tabs].hideColumn(self.intradColsDet_M.columnCount() - 2)
        tab_layout.addWidget(self.det_t[curr_num_tabs])

        self.det_t[curr_num_tabs].en_int_validator(IntradosColsDetModel.OrderNumCol,
                                   IntradosColsDetModel.OrderNumCol,
                                   1, ValidationValues.Proc.MaxNumColorLines)
        self.det_t[curr_num_tabs].en_double_validator(IntradosColsDetModel.DistTeCol,
                                      IntradosColsDetModel.DistTeRightCol,
                                      ValidationValues.WingChordMin_perc,
                                      ValidationValues.WingChordMax_perc,
                                      2)
        self.det_t[curr_num_tabs].en_double_validator(IntradosColsDetModel.SeamCol,
                                                      IntradosColsDetModel.SeamCol,
                                                      ValidationValues.Proc.MinSewingAllowance_mm,
                                                      ValidationValues.Proc.MaxSewingAllowance_mm)

        self.det_t[curr_num_tabs].set_help_bar(self.helpBar)
        self.det_t[curr_num_tabs].set_help_text(IntradosColsDetModel.OrderNumCol,
                                _('OrderNumDesc'))
        self.det_t[curr_num_tabs].set_help_text(IntradosColsDetModel.DistTeCol,
                                _('IntradCols-DistTeDesc'))
        self.det_t[curr_num_tabs].set_help_text(IntradosColsDetModel.DistTeRightCol,
                                _('IntradCols-DistTeRightDesc'))
        self.det_t[curr_num_tabs].set_help_text(IntradosColsDetModel.SeamCol,
                                _('IntradCols-Seam'))
        # then setup spin
        if self.detProxyModel[curr_num_tabs].rowCount() == 0:
            # a new tab was created from the gui
            self.intradColsDet_M.set_num_rows_for_config(curr_num_tabs + 1, 1)
        # a new tab was added based on file load. The model has
        # been updated already before.
        self.numDet_s[curr_num_tabs].setValue(
            self.detProxyModel[curr_num_tabs].rowCount())
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
        self.confProxyModel.pop(num_tabs - 1)
        self.detProxyModel.pop(num_tabs - 1)
        self.numDet_s.pop(num_tabs - 1)
        self.intradColsDet_M.set_num_rows_for_config(num_tabs, 0)

    def update_tabs(self):
        """
        :method: called upon changes of the details model. Does assure all
                 GUI elements will follow the changes.
        """
        i = 0
        while i < self.tabs.count():
            if self.numDet_s[i].value != self.intradColsDet_M. \
                    num_rows_for_config(i + 1):
                self.numDet_s[i].setValue(self.intradColsDet_M.
                                          num_rows_for_config(i + 1))
            i += 1

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        """
        if self.tabs.count() > 0:
            curr_tab = self.tabs.currentIndex()
            self.detProxyModel[curr_tab].sort(
                IntradosColsDetModel.OrderNumCol,
                Qt.SortOrder.AscendingOrder)
            self.detProxyModel[curr_tab].setDynamicSortFilter(False)

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
            logging.error('.btn_press unrecognized button press ' + q)
