"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QSpinBox, QLabel, QTabWidget, QHBoxLayout, \
    QVBoxLayout, QPushButton

from data.ProcModel import ProcModel
from data.procModel.LightConfModel import LightConfModel
from data.procModel.LightDetModel import LightDetModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class RibHoles(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit airfoils holes data
    """

    __className = 'RibHoles'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()

        self.btnBar = None
        self.tabs = None
        self.numConf_S = None
        self.window_ly = None
        self.helpBar = None
        self.win = None
        self.confProxyModel = []
        self.detProxyModel = []
        self.numDet_S = []

        self.pm = ProcModel()
        self.lightC_M = LightConfModel()
        self.lightC_M.numRowsForConfigChanged.connect(self.model_num_configs_changed)

        self.lightD_M = LightDetModel()
        self.lightD_M.numRowsForConfigChanged.connect(self.update_tabs)

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
                    numConfSpin

                    Tabs
                        configTable
                        numDetSpin
                        detailTable
                    -------------------------
                            help_bar  | btn_bar
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Edit rib holes (rib lightening)"))

        num_conf_l = QLabel(_('Number of configurations'))
        num_conf_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_conf_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                             QSizePolicy.Policy.Fixed))
        self.numConf_S = QSpinBox()
        self.numConf_S.setRange(0, 999)
        self.numConf_S.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                 QSizePolicy.Policy.Fixed))
        self.numConf_S.setValue(self.lightC_M.num_configs())
        conf_edit = self.numConf_S.lineEdit()
        conf_edit.setReadOnly(True)
        self.numConf_S.valueChanged.connect(self.conf_spin_change)

        num_conf_layout = QHBoxLayout()
        num_conf_layout.addWidget(num_conf_l)
        num_conf_layout.addWidget(self.numConf_S)
        num_conf_layout.addStretch()
        self.window_ly.addLayout(num_conf_layout)

        self.tabs = QTabWidget()
        self.window_ly.addWidget(self.tabs)

        # check if there's already data
        if self.lightC_M.num_configs() > 0:
            self.model_num_configs_changed()

        sort_btn = QPushButton(_('Sort by Order Num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/ribHoles.html')

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
        self.lightC_M.set_num_configs(self.numConf_S.value())
        self.pm.set_file_saved(False)

    def model_num_configs_changed(self):
        """
        :method: Called upon changes of the configs model. Does assure all GUI elements will follow the changes.
        """
        current_num_configs = self.lightC_M.num_configs()

        self.numConf_S.blockSignals(True)
        self.numConf_S.setValue(current_num_configs)
        self.numConf_S.blockSignals(False)

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
        self.lightD_M.set_num_rows_for_config(self.tabs.currentIndex() + 1,
                                              self.numDet_S[self.tabs.currentIndex()].value())
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
        self.confProxyModel[curr_num_tabs].setSourceModel(self.lightC_M)
        self.confProxyModel[curr_num_tabs]. \
            setFilterKeyColumn(LightConfModel.ConfigNumCol)
        self.confProxyModel[curr_num_tabs]. \
            setFilterRegularExpression(QRegularExpression(str(curr_num_tabs + 1)))

        conf_table.setModel(self.confProxyModel[curr_num_tabs])
        conf_table.verticalHeader().setVisible(False)
        conf_table.hideColumn(self.lightC_M.OrderNumCol)
        conf_table.hideColumn(self.lightC_M.columnCount() - 1)
        conf_table.hideColumn(self.lightC_M.columnCount() - 2)

        conf_table.en_int_validator(LightConfModel.InitialRibCol,
                                    LightConfModel.FinalRibCol,
                                    1,
                                    ValidationValues.MaxNumRibs)

        conf_table.set_help_bar(self.helpBar)
        conf_table.set_help_text(LightConfModel.InitialRibCol,
                                 _('Proc-InitialRibDesc'))
        conf_table.set_help_text(LightConfModel.FinalRibCol,
                                 _('Proc-FinalRibDesc'))

        conf_layout = QHBoxLayout()
        conf_layout.addWidget(conf_table)
        conf_layout.addStretch()
        conf_table.setFixedWidth(2
                                 + conf_table.columnWidth(
                                    LightConfModel.InitialRibCol)
                                 + conf_table.columnWidth(
                                    LightConfModel.FinalRibCol))
        conf_table.setFixedHeight(2
                                  + conf_table.horizontalHeader().height()
                                  + conf_table.rowHeight(0))
        tab_layout.addLayout(conf_layout)

        # Data lines
        num_det_l = QLabel(_('Number of configuration lines'))
        num_det_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_det_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                            QSizePolicy.Policy.Fixed))
        tab_layout.addWidget(num_det_l)
        self.numDet_S.append(QSpinBox())
        self.numDet_S[curr_num_tabs].setRange(1, ValidationValues.MaxNumRibs)
        self.numDet_S[curr_num_tabs].setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Fixed,
                        QSizePolicy.Policy.Fixed))
        self.numDet_S[curr_num_tabs].valueChanged.connect(self.det_spin_change)
        det_edit = self.numDet_S[curr_num_tabs].lineEdit()
        det_edit.setReadOnly(True)

        det_num_layout = QHBoxLayout()
        det_num_layout.addWidget(num_det_l)
        det_num_layout.addWidget(self.numDet_S[curr_num_tabs])
        det_num_layout.addStretch()
        tab_layout.addLayout(det_num_layout)

        # add here the code for the details table
        det_table = TableView()
        self.detProxyModel.append(QSortFilterProxyModel())
        self.detProxyModel[curr_num_tabs].setSourceModel(self.lightD_M)
        self.detProxyModel[curr_num_tabs]. \
            setFilterKeyColumn(LightDetModel.ConfigNumCol)
        self.detProxyModel[curr_num_tabs]. \
            setFilterRegularExpression(QRegularExpression(str(curr_num_tabs + 1)))

        det_table.setModel(self.detProxyModel[curr_num_tabs])
        det_table.verticalHeader().setVisible(False)
        det_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        det_table.hideColumn(self.lightD_M.columnCount() - 1)
        det_table.hideColumn(self.lightD_M.columnCount() - 2)
        tab_layout.addWidget(det_table)

        det_table.en_int_validator(LightDetModel.OrderNumCol,
                                   LightDetModel.OrderNumCol,
                                   1,
                                   ValidationValues.MaxNumRibs)

        det_table.en_int_validator(LightDetModel.LightTypCol,
                                   LightDetModel.LightTypCol,
                                   1,
                                   3,
                                   LightDetModel.paramLength)

        det_table.en_double_validator(LightDetModel.DistLECol,
                                      LightDetModel.VertAxisCol,
                                      ValidationValues.WingChordMin_perc,
                                      ValidationValues.WingChordMax_perc,
                                      3,
                                      LightDetModel.paramLength)

        det_table.en_double_validator(LightDetModel.RotAngleCol,
                                      LightDetModel.RotAngleCol,
                                      0, 360, 3,
                                      LightDetModel.paramLength)

        det_table.en_double_validator(LightDetModel.Opt1Col,
                                      LightDetModel.Opt1Col,
                                      ValidationValues.Proc.RibHolesOpt1Min,
                                      ValidationValues.Proc.RibHolesOpt1Max,
                                      3,
                                      LightDetModel.paramLength)

        det_table.set_help_bar(self.helpBar)
        det_table.set_help_text(LightDetModel.OrderNumCol,
                                _('OrderNumDesc'))
        det_table.set_help_text(LightDetModel.LightTypCol,
                                _('RibHoles-LightTypeDesc'))
        det_table.set_help_text(LightDetModel.DistLECol,
                                _('RibHoles-DistLEDesc'))
        det_table.set_help_text(LightDetModel.DisChordCol,
                                _('RibHoles-DisChordDesc'))
        det_table.set_help_text(LightDetModel.HorAxisCol,
                                _('RibHoles-HorAxisDesc'))
        det_table.set_help_text(LightDetModel.VertAxisCol,
                                _('RibHoles-VertAxisDesc'))
        det_table.set_help_text(LightDetModel.RotAngleCol,
                                _('RibHoles-RotAngleDesc'))
        det_table.set_help_text(LightDetModel.Opt1Col,
                                _('RibHoles-Opt1Desc'))

        # then setup spin
        if self.detProxyModel[curr_num_tabs].rowCount() == 0:
            # a new tab was created from the gui
            self.lightD_M.set_num_rows_for_config(curr_num_tabs + 1, 1)
        # A new tab was added based on file load.
        # The model has been updated already before.
        self.numDet_S[curr_num_tabs].setValue(
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
        self.numDet_S.pop(num_tabs - 1)
        self.lightD_M.set_num_rows_for_config(num_tabs, 0)

    def update_tabs(self):
        """
        :method: called upon changes of the details model. Does assure all GUI elements will follow the changes.
        """
        i = 0
        while i < self.tabs.count():
            if self.numDet_S[i].value != self.lightD_M.num_rows_for_config(i + 1):
                self.numDet_S[i].setValue(self.lightD_M.num_rows_for_config(i + 1))
            i += 1

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        """
        if self.tabs.count() > 0:
            curr_tab = self.tabs.currentIndex()
            self.detProxyModel[curr_tab]. \
                sort(LightDetModel.OrderNumCol,
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
            logging.error(self.__className
                          + '.btn_press unrecognized button press ' + q)
