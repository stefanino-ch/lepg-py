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
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class NoseMylars(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Brake line details  
    """

    __className = 'NoseMylars'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.numLines_s = None
        self.helpBar = None
        self.window_ly = None
        self.btnBar = None
        self.proxyModel = None
        self.wrapper = None
        self.win = None

        self.pm = ProcModel()
        self.noseMylars_M = ProcModel.NoseMylarsModel()
        self.noseMylars_M.numRowsForConfigChanged. \
            connect(self.model_size_changed)
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
        self.win.setMinimumSize(700, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Nose mylars"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.noseMylars_M)

        num_lines_l = QLabel(_('Number of configs'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))

        self.numLines_s = QSpinBox()
        self.numLines_s.setRange(0, 999)
        self.numLines_s.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                  QSizePolicy.Policy.Fixed))
        self.numLines_s.valueChanged.connect(self.num_lines_change)
        num_lines_edit = self.numLines_s.lineEdit()
        num_lines_edit.setReadOnly(True)

        num_lines_layout = QHBoxLayout()
        num_lines_layout.addWidget(num_lines_l)
        num_lines_layout.addWidget(self.numLines_s)
        num_lines_layout.addStretch()
        self.window_ly.addLayout(num_lines_layout)
        ###############

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.noseMylars_M)

        table_t = TableView()
        table_t.setModel(self.proxyModel)
        table_t.verticalHeader().setVisible(False)
        table_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_t.hideColumn(self.noseMylars_M.columnCount() - 1)
        table_t.hideColumn(self.noseMylars_M.columnCount() - 2)
        self.window_ly.addWidget(table_t)

        table_t.en_int_validator(ProcModel.NoseMylarsModel.OrderNumCol,
                                 ProcModel.NoseMylarsModel.LastRibCol,
                                 1, 999)
        table_t.en_double_validator(ProcModel.NoseMylarsModel.xOneCol,
                                    ProcModel.NoseMylarsModel.vTwoCol,
                                    1, 100, 1)

        table_t.set_help_bar(self.helpBar)
        table_t.set_help_text(ProcModel.NoseMylarsModel.OrderNumCol,
                              _('OrderNumDesc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.FirstRibCol,
                              _('NoseMylars-FirstRibDesc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.LastRibCol,
                              _('NoseMylars-LastRibDesc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.xOneCol,
                              _('NoseMylars-x1Desc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.uOneCol,
                              _('NoseMylars-u1Desc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.uTwoCol,
                              _('NoseMylars-u2Desc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.xTwoCol,
                              _('NoseMylars-x2Desc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.vOneCol,
                              _('NoseMylars-v1Desc'))
        table_t.set_help_text(ProcModel.NoseMylarsModel.vTwoCol,
                              _('NoseMylars-v2Desc'))

        sort_btn = QPushButton(_('Sort by order_num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                           QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.noseMylars_M.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/noseMylars.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(sort_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def model_size_changed(self):
        """
        :method: Called after the model has been changed it's size. Herein we 
                 assure the GUI follows the model.
        """
        logging.debug(self.__className + '.model_size_changed')
        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.noseMylars_M.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all 
                 elements will follow the user configuration. 
        """
        logging.debug(self.__className + '.num_lines_change')
        self.noseMylars_M.set_num_rows_for_config(1, self.numLines_s.value())
        self.pm.set_file_saved(False)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort 
                 based on the numbers in the OrderNum column.
        """
        logging.debug(self.__className + '.sort_btn_press')

        self.proxyModel.sort(ProcModel.NoseMylarsModel.OrderNumCol,
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
