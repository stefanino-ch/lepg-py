"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
                            QSpinBox, QLabel, QHBoxLayout, QVBoxLayout, \
                            QPushButton, QDataWidgetMapper

from data.ProcModel import ProcModel
from data.procModel.HvVhRibsModel import HvVhRibsModel

from gui.elements.LineEdit import LineEdit
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class HvVhRibs(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Brake line details  
    """

    __className = 'HvVhRibs'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.helpBar = None
        self.windowLayout = None
        self.btnBar = None
        self.proxyModel = None
        self.numLines_S = None
        self.wrapper = None
        self.win = None

        self.pm = ProcModel()
        self.wing_M = ProcModel.WingModel()

        self.ribs_M = HvVhRibsModel()
        self.ribs_M.numRowsForConfigChanged.connect(self.model_size_changed)

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
                    xSpacing
                    ySpacing
                    numLinesSpin
                    Table
                    -------------------------
                        OrderBtn  help_bar  | btn_bar
                            
        Naming:
            Conf is always one as there is only one configuration possible
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
        self.setWindowTitle(_("HV VH Ribs"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.wing_M)

        x_sp_l = QLabel(_('x Spacing'))
        x_sp_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        x_sp_e = LineEdit()
        x_sp_e.setFixedWidth(40)
        self.wrapper.addMapping(x_sp_e, ProcModel.WingModel.xSpacingCol)
        x_sp_e.en_double_validator(0, 100, 1)
        x_sp_e.set_help_text(_('HvVhRibs-xSpacingDesc'))
        x_sp_e.set_help_bar(self.helpBar)
        x_sp_layout = QHBoxLayout()
        x_sp_layout.addWidget(x_sp_l)
        x_sp_layout.addWidget(x_sp_e)
        x_sp_layout.addStretch()
        self.windowLayout.addLayout(x_sp_layout)

        y_sp_l = QLabel(_('y Spacing'))
        y_sp_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        y_sp_e = LineEdit()
        y_sp_e.setFixedWidth(40)
        self.wrapper.addMapping(y_sp_e, ProcModel.WingModel.ySpacingCol)
        y_sp_e.en_double_validator(0, 100, 1)
        y_sp_e.set_help_text(_('HvVhRibs-ySpacingDesc'))
        y_sp_e.set_help_bar(self.helpBar)
        y_sp_layout = QHBoxLayout()
        y_sp_layout.addWidget(y_sp_l)
        y_sp_layout.addWidget(y_sp_e)
        y_sp_layout.addStretch()
        self.windowLayout.addLayout(y_sp_layout)

        self.wrapper.toFirst()

        ###############
        num_lines_l = QLabel(_('Number of configs'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))

        self.numLines_S = QSpinBox()
        self.numLines_S.setRange(0, 999)
        self.numLines_S.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                  QSizePolicy.Policy.Fixed))
        self.numLines_S.valueChanged.connect(self.num_lines_change)
        num_lines_edit = self.numLines_S.lineEdit()
        num_lines_edit.setReadOnly(True)
        self.numLines_S.setValue(self.ribs_M.num_rows_for_config(1))

        num_lines_layout = QHBoxLayout()
        num_lines_layout.addWidget(num_lines_l)
        num_lines_layout.addWidget(self.numLines_S)
        num_lines_layout.addStretch()
        self.windowLayout.addLayout(num_lines_layout)
        ###############

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.ribs_M)

        ribs_t = TableView()
        ribs_t.setModel(self.proxyModel)
        ribs_t.verticalHeader().setVisible(False)
        ribs_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        ribs_t.hideColumn(self.ribs_M.columnCount() - 1)
        ribs_t.hideColumn(self.ribs_M.columnCount() - 2)
        self.windowLayout.addWidget(ribs_t)

        ribs_t.en_int_validator(HvVhRibsModel.TypeCol,
                                HvVhRibsModel.TypeCol,
                                1, 16)
        ribs_t.en_int_validator(HvVhRibsModel.IniRibCol,
                                HvVhRibsModel.IniRibCol,
                                1, 999)
        ribs_t.en_int_validator(HvVhRibsModel.ParamACol,
                                HvVhRibsModel.ParamACol,
                                1, 6)
        ribs_t.en_int_validator(HvVhRibsModel.ParamBCol,
                                HvVhRibsModel.ParamCCol,
                                1, 100)
        ribs_t.en_double_validator(HvVhRibsModel.ParamDCol,
                                   HvVhRibsModel.ParamICol,
                                   1, 100, 1)

        ribs_t.set_help_bar(self.helpBar)
        ribs_t.set_help_text(HvVhRibsModel.OrderNumCol,
                             _('OrderNumDesc'))
        ribs_t.set_help_text(HvVhRibsModel.TypeCol,
                             _('HvVhRibs-TypeDesc'))
        ribs_t.set_help_text(HvVhRibsModel.IniRibCol,
                             _('HvVhRibs-IniRibDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamACol,
                             _('HvVhRibs-ParamADesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamBCol,
                             _('HvVhRibs-ParamBDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamCCol,
                             _('HvVhRibs-ParamCDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamDCol,
                             _('HvVhRibs-ParamDDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamECol,
                             _('HvVhRibs-ParamEDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamFCol,
                             _('HvVhRibs-ParamFDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamGCol,
                             _('HvVhRibs-ParamGDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamHCol,
                             _('HvVhRibs-ParamHDesc'))
        ribs_t.set_help_text(HvVhRibsModel.ParamICol,
                             _('HvVhRibs-ParamIDesc'))

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
        self.btnBar.setHelpPage('proc/hVvHribs.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(sort_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottom_layout)

        self.win.setLayout(self.windowLayout)

    def model_size_changed(self):
        """
        :method: Called after the model has been changed it's size. Herein we
                 assure the GUI follows the model.
        """
        logging.debug(self.__className + '.model_size_changed')
        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue(self.ribs_M.num_rows_for_config(1))
        self.numLines_S.blockSignals(False)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all 
                 elements will follow the user configuration. 
        """
        logging.debug(self.__className + '.num_lines_change')
        self.ribs_M.set_num_rows_for_config(1, self.numLines_S.value())
        self.pm.set_file_saved(False)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort 
                 based on the numbers in the OrderNum column.
        """
        logging.debug(self.__className + '.sort_btn_press')

        self.proxyModel.sort(HvVhRibsModel.OrderNumCol,
                             Qt.SortOrder.AscendingOrder)
        self.proxyModel.setDynamicSortFilter(False)

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
