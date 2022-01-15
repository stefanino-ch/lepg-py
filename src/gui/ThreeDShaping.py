"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QSpinBox, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class ThreeDShaping(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit airfoils holes data
    """

    __className = 'ThreeDShaping'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        self.btnBar = None
        self.tabs = None
        self.numConf_s = None
        self.helpBar = None
        self.window_ly = None
        self.win = None
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.threeDShConf_M = ProcModel.ThreeDShConfModel()
        self.threeDShConf_M.numRowsForConfigChanged.\
            connect(self.model_num_configs_changed)

        self.threeDShUpDet_M = ProcModel.ThreeDShUpDetModel()
        self.threeDShUpDet_M.numRowsForConfigChanged.connect(self.update_tabs)

        self.threeDShLoDet_M = ProcModel.ThreeDShLoDetModel()
        self.threeDShLoDet_M.numRowsForConfigChanged.connect(self.update_tabs)

        self.threeDShPr_M = ProcModel.ThreeDShPrintModel()

        self.pm = ProcModel()

        self.rib_PM = []
        self.upC_PM = []
        self.loC_PM = []

        self.numUpC_s = []
        self.numLoC_s = []

        self.build_window()

    def closeEvent(self, event):
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
                    numConfSpin

                    Tabs
                        ribTable
                        numUpSpin
                        upTable
                        numLoSpin
                        loTable

                    print_table
                    -------------------------
                            help_bar  | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(750, 600)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("3D shaping"))

        num_conf_l = QLabel(_('Number of groups'))
        num_conf_l.setAlignment(Qt.AlignRight)
        num_conf_l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                             QSizePolicy.Fixed))
        self.numConf_s = QSpinBox()
        self.numConf_s.setRange(0, 999)
        self.numConf_s.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                                 QSizePolicy.Fixed))
        self.numConf_s.setValue(self.threeDShConf_M.num_configs())
        conf_edit = self.numConf_s.lineEdit()
        conf_edit.setReadOnly(True)
        self.numConf_s.valueChanged.connect(self.conf_spin_change)

        num_conf_layout = QHBoxLayout()
        num_conf_layout.addWidget(num_conf_l)
        num_conf_layout.addWidget(self.numConf_s)
        num_conf_layout.addStretch()
        self.window_ly.addLayout(num_conf_layout)

        self.tabs = QTabWidget()
        self.window_ly.addWidget(self.tabs)

        # check if there's already data
        if self.threeDShConf_M.num_configs() > 0:
            self.model_num_configs_changed()

        print_table = TableView()
        print_table.setModel(self.threeDShPr_M)
        print_table.verticalHeader().setVisible(False)
        print_table.hideColumn(self.threeDShPr_M.OrderNumCol)
        print_table.hideColumn(self.threeDShPr_M.columnCount() - 2)
        print_table.hideColumn(self.threeDShPr_M.columnCount() - 1)

        # TODO: remove currently not supported rows
        print_table.setHelpBar(self.helpBar)
        print_table.setHelpText(ProcModel.ThreeDShPrintModel.NameCol,
                                _('3DShPrint-NameDesc'))
        print_table.setHelpText(ProcModel.ThreeDShPrintModel.DrawCol,
                                _('3DShPrint-DrawDesc'))
        print_table.setHelpText(ProcModel.ThreeDShPrintModel.FirstPanelCol,
                                _('3DShPrint-FirstPanelDesc'))
        print_table.setHelpText(ProcModel.ThreeDShPrintModel.LastPanelCol,
                                _('3DShPrint-LastPanelDesc'))
        print_table.setHelpText(ProcModel.ThreeDShPrintModel.SymmetricCol,
                                _('3DShPrint-SymmetricDesc'))

        print_layout = QHBoxLayout()
        print_layout.addWidget(print_table)
        print_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        print_table.setFixedHeight(2
                                   + print_table.horizontalHeader().height()
                                   + 5 * print_table.rowHeight(0))
        self.window_ly.addLayout(print_layout)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/threeDShaping.html')

        bottom_layout = QHBoxLayout()

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def conf_spin_change(self):
        """
        :method: Called upon manual changes of the config spin. Does assure all
                 elements will follow the user configuration.
        """
        logging.debug(self.__className + '.conf_spin_change')
        self.threeDShConf_M.set_num_configs(self.numConf_s.value())
        self.pm.set_file_saved(False)

    def model_num_configs_changed(self):
        """
        :method: Called upon changes of the configs model. Does assure all GUI
                 elements will follow the changes.
        """
        logging.debug(self.__className + '.model_num_configs_changed')

        current_num_configs = self.threeDShConf_M.num_configs()

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

    def add_tab(self):
        """
        :method: Creates a new tab including all its widgets.
        """
        logging.debug(self.__className + '.add_tab')

        curr_num_tabs = self.tabs.count()

        tab_widget = QWidget()
        tab_ly = QVBoxLayout()

        # Configuration 
        rib_table = TableView()
        self.rib_PM.append(QSortFilterProxyModel())
        self.rib_PM[curr_num_tabs].setSourceModel(self.threeDShConf_M)
        self.rib_PM[curr_num_tabs].\
            setFilterKeyColumn(ProcModel.ThreeDShConfModel.ConfigNumCol)
        self.rib_PM[curr_num_tabs].\
            setFilterRegExp(QRegExp(str(curr_num_tabs + 1)))
        rib_table.setModel(self.rib_PM[curr_num_tabs])
        rib_table.verticalHeader().setVisible(False)
        rib_table.hideColumn(self.threeDShConf_M.OrderNumCol)
        rib_table.hideColumn(self.threeDShConf_M.columnCount() - 1)
        rib_table.hideColumn(self.threeDShConf_M.columnCount() - 2)

        rib_table.enableIntValidator(ProcModel.ThreeDShConfModel.FirstRibCol,
                                     ProcModel.ThreeDShConfModel.LastRibCol,
                                     1, 999)

        rib_table.setHelpBar(self.helpBar)
        rib_table.setHelpText(ProcModel.ThreeDShConfModel.FirstRibCol,
                              _('3DSh-FirstRibDesc'))
        rib_table.setHelpText(ProcModel.ThreeDShConfModel.LastRibCol,
                              _('3DSh-LastRibDesc'))

        rib_ly = QHBoxLayout()
        rib_ly.addWidget(rib_table)
        rib_ly.addStretch()
        rib_table.setFixedWidth(2
                                + rib_table.columnWidth(
                                    ProcModel.ThreeDShConfModel.FirstRibCol)
                                + rib_table.columnWidth(
                                    ProcModel.ThreeDShConfModel.LastRibCol))
        rib_table.setFixedHeight(2
                                 + rib_table.horizontalHeader().height()
                                 + rib_table.rowHeight(0))
        tab_ly.addLayout(rib_ly)

        # upper cuts
        num_up_c_l = QLabel(_('Number of upper cuts'))
        num_up_c_l.setAlignment(Qt.AlignRight)
        num_up_c_l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                             QSizePolicy.Fixed))
        self.numUpC_s.append(QSpinBox())
        self.numUpC_s[curr_num_tabs].setRange(0, 2)
        self.numUpC_s[curr_num_tabs].\
            setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                      QSizePolicy.Fixed))
        self.numUpC_s[curr_num_tabs].setValue(
            self.threeDShUpDet_M.num_rows_for_config(curr_num_tabs + 1))
        conf_edit = self.numUpC_s[curr_num_tabs].lineEdit()
        conf_edit.setReadOnly(True)
        self.numUpC_s[curr_num_tabs].valueChanged.connect(self.up_c_change)

        num_up_c_ly = QHBoxLayout()
        num_up_c_ly.addWidget(num_up_c_l)
        num_up_c_ly.addWidget(self.numUpC_s[curr_num_tabs])
        num_up_c_ly.addStretch()
        tab_ly.addLayout(num_up_c_ly)

        up_c_t = TableView()
        self.upC_PM.append(QSortFilterProxyModel())
        self.upC_PM[curr_num_tabs].setSourceModel(self.threeDShUpDet_M)
        self.upC_PM[curr_num_tabs].\
            setFilterKeyColumn(ProcModel.ThreeDShUpDetModel.ConfigNumCol)
        self.upC_PM[curr_num_tabs].\
            setFilterRegExp(QRegExp(str(curr_num_tabs + 1)))
        up_c_t.setModel(self.upC_PM[curr_num_tabs])
        up_c_t.verticalHeader().setVisible(False)
        up_c_t.hideColumn(self.threeDShUpDet_M.OrderNumCol)
        up_c_t.hideColumn(self.threeDShUpDet_M.columnCount() - 1)
        up_c_t.hideColumn(self.threeDShUpDet_M.columnCount() - 2)

        up_c_t.enableIntValidator(ProcModel.ThreeDShUpDetModel.IniPointCol,
                                  ProcModel.ThreeDShUpDetModel.CutPointCol,
                                  0, 100)
        up_c_t.enableDoubleValidator(ProcModel.ThreeDShUpDetModel.DepthCol,
                                     ProcModel.ThreeDShUpDetModel.DepthCol,
                                     -1, 1, 1)

        up_c_t.setHelpBar(self.helpBar)
        up_c_t.setHelpText(ProcModel.ThreeDShUpDetModel.IniPointCol,
                           _('3DSh-IniPointDesc'))
        up_c_t.setHelpText(ProcModel.ThreeDShUpDetModel.CutPointCol,
                           _('3DSh-CutPointDesc'))
        up_c_t.setHelpText(ProcModel.ThreeDShUpDetModel.DepthCol,
                           _('3DSh-DepthDesc'))

        up_c_ly = QHBoxLayout()
        up_c_ly.addWidget(up_c_t)
        up_c_ly.addStretch()
        up_c_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        up_c_t.setFixedHeight(2 + 3 * up_c_t.horizontalHeader().height())
        tab_ly.addLayout(up_c_ly)

        # lower cuts
        num_lo_c_l = QLabel(_('Number of lower cuts'))
        num_lo_c_l.setAlignment(Qt.AlignRight)
        num_lo_c_l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                             QSizePolicy.Fixed))
        self.numLoC_s.append(QSpinBox())
        self.numLoC_s[curr_num_tabs].setRange(0, 1)
        self.numLoC_s[curr_num_tabs].\
            setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                      QSizePolicy.Fixed))
        self.numLoC_s[curr_num_tabs].\
            setValue(self.threeDShLoDet_M.num_rows_for_config(curr_num_tabs + 1))
        conf_edit = self.numLoC_s[curr_num_tabs].lineEdit()
        conf_edit.setReadOnly(True)
        self.numLoC_s[curr_num_tabs].valueChanged.connect(self.lo_c_change)

        num_lo_c_ly = QHBoxLayout()
        num_lo_c_ly.addWidget(num_lo_c_l)
        num_lo_c_ly.addWidget(self.numLoC_s[curr_num_tabs])
        num_lo_c_ly.addStretch()
        tab_ly.addLayout(num_lo_c_ly)

        lo_c_t = TableView()
        self.loC_PM.append(QSortFilterProxyModel())
        self.loC_PM[curr_num_tabs].setSourceModel(self.threeDShLoDet_M)
        self.loC_PM[curr_num_tabs].\
            setFilterKeyColumn(ProcModel.ThreeDShLoDetModel.ConfigNumCol)
        self.loC_PM[curr_num_tabs].\
            setFilterRegExp(QRegExp(str(curr_num_tabs + 1)))
        lo_c_t.setModel(self.loC_PM[curr_num_tabs])
        lo_c_t.verticalHeader().setVisible(False)
        lo_c_t.hideColumn(self.threeDShLoDet_M.OrderNumCol)
        lo_c_t.hideColumn(self.threeDShLoDet_M.columnCount() - 1)
        lo_c_t.hideColumn(self.threeDShLoDet_M.columnCount() - 2)

        lo_c_t.enableIntValidator(ProcModel.ThreeDShLoDetModel.IniPointCol,
                                  ProcModel.ThreeDShLoDetModel.CutPointCol,
                                  0, 100)
        lo_c_t.enableDoubleValidator(ProcModel.ThreeDShLoDetModel.DepthCol,
                                     ProcModel.ThreeDShLoDetModel.DepthCol,
                                     -1, 1, 1)

        lo_c_t.setHelpBar(self.helpBar)
        lo_c_t.setHelpText(ProcModel.ThreeDShLoDetModel.IniPointCol,
                           _('3DSh-IniPointDesc'))
        lo_c_t.setHelpText(ProcModel.ThreeDShLoDetModel.CutPointCol,
                           _('3DSh-CutPointDesc'))
        lo_c_t.setHelpText(ProcModel.ThreeDShLoDetModel.DepthCol,
                           _('3DSh-DepthDesc'))

        lo_c_ly = QHBoxLayout()
        lo_c_ly.addWidget(lo_c_t)
        lo_c_ly.addStretch()
        lo_c_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        lo_c_t.setFixedHeight(2 + 2 * lo_c_t.horizontalHeader().height())
        tab_ly.addLayout(lo_c_ly)

        tab_widget.setLayout(tab_ly)

        i = self.tabs.addTab(tab_widget, str(curr_num_tabs + 1))
        self.tabs.setCurrentIndex(i)

    def remove_tab(self):
        """
        :method: Removes the last tab from the GUI. Does take care at the same
                 time of the class internal elements and the data model.
        """
        logging.debug(self.__className + '.remove_tab')

        num_tabs = self.tabs.count()
        self.tabs.removeTab(num_tabs - 1)
        # cleanup arrays

        self.rib_PM.pop(num_tabs - 1)
        self.upC_PM.pop(num_tabs - 1)
        self.loC_PM.pop(num_tabs - 1)

        self.numUpC_s.pop(num_tabs - 1)
        self.numLoC_s.pop(num_tabs - 1)

        # cleanup database
        self.threeDShConf_M.set_num_rows_for_config(num_tabs, 0)
        self.threeDShUpDet_M.set_num_rows_for_config(num_tabs, 0)
        self.threeDShLoDet_M.set_num_rows_for_config(num_tabs, 0)

    def update_tabs(self):
        """
        :method: called upon changes of the details models. Does assure all
                 GUI elements will follow the changes.
        """
        logging.debug(self.__className + '.update_tabs')

        i = 0
        while i < self.tabs.count():
            if self.numUpC_s[i].value != \
                    self.threeDShUpDet_M.num_rows_for_config(i + 1):
                self.numUpC_s[i].blockSignals(True)
                self.numUpC_s[i].setValue(
                    self.threeDShUpDet_M.num_rows_for_config(i + 1))
                self.numUpC_s[i].blockSignals(False)

            if self.numLoC_s[i].value != \
                    self.threeDShLoDet_M.num_rows_for_config(i + 1):
                self.numLoC_s[i].blockSignals(True)
                self.numLoC_s[i].setValue(
                    self.threeDShLoDet_M.num_rows_for_config(i + 1))
                self.numLoC_s[i].blockSignals(False)
            i += 1

    def up_c_change(self):
        """
        :method: Called upon manual changes of the number of lower cuts spin.
                 Does assure all elements will follow the user configuration.
        """
        logging.debug(self.__className + '.up_c_change')
        self.threeDShUpDet_M.set_num_rows_for_config(
            self.tabs.currentIndex() + 1,
            self.numUpC_s[self.tabs.currentIndex()].value())
        self.pm.set_file_saved(False)

    def lo_c_change(self):
        """
        :method: Called upon manual changes of the number of lower cuts spin.
                 Does assure all elements will follow the user configuration.
        """
        logging.debug(self.__className + '.lo_c_change')
        self.threeDShLoDet_M.set_num_rows_for_config(
            self.tabs.currentIndex() + 1,
            self.numLoC_s[self.tabs.currentIndex()].value())
        self.pm.set_file_saved(False)

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
