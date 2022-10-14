"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

import logging

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QMdiSubWindow,
                             QWidget,
                             QSizePolicy,
                             QHeaderView,
                             QSpinBox,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton,
                             QDataWidgetMapper,
                             )

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class AddRibPoints(QMdiSubWindow):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'AddRibPoints'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self, metaclass=Singleton):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.proxyModel = None
        self.helpBar = None
        self.windowLayout = None
        self.win = None
        self.btnBar = None
        self.wrapper = None
        self.numLines_s = None

        self.pm = ProcModel()

        self.addRibPts_M = ProcModel.AddRibPointsModel()
        self.addRibPts_M.numRowsForConfigChanged.connect(self.model_size_changed)
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
        self.win.setMinimumSize(550, 400)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Additional rib points"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.addRibPts_M)

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
        self.windowLayout.addLayout(num_lines_layout)
        ###############

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.addRibPts_M)

        ribs_t = TableView()
        ribs_t.setModel(self.proxyModel)
        ribs_t.verticalHeader().setVisible(False)
        ribs_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        ribs_t.hideColumn(self.addRibPts_M.columnCount() - 1)
        ribs_t.hideColumn(self.addRibPts_M.columnCount() - 2)
        self.windowLayout.addWidget(ribs_t)

        ribs_t.en_int_validator(ProcModel.AddRibPointsModel.OrderNumCol,
                                ProcModel.AddRibPointsModel.OrderNumCol,
                                1, 999)
        ribs_t.en_double_validator(ProcModel.AddRibPointsModel.XCoordCol,
                                   ProcModel.AddRibPointsModel.YCoordCol,
                                   1, 100, 2)

        ribs_t.set_help_bar(self.helpBar)
        ribs_t.set_help_text(ProcModel.AddRibPointsModel.OrderNumCol,
                             _('OrderNumDesc'))
        ribs_t.set_help_text(ProcModel.AddRibPointsModel.XCoordCol,
                             _('AddRibPts-XCoordDesc'))
        ribs_t.set_help_text(ProcModel.AddRibPointsModel.YCoordCol,
                             _('AddRibPts-YCoordDesc'))

        sort_btn = QPushButton(_('Sort by order_num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                           QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.addRibPts_M.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/addRibPoints.html')

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
        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.addRibPts_M.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all
                 elements will follow the user configuration.
        """
        logging.debug(self.__className + '.num_lines_change')
        self.addRibPts_M.set_num_rows_for_config(1, self.numLines_s.value())
        self.pm.set_file_saved(False)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        """
        logging.debug(self.__className + '.sort_btn_press')

        self.proxyModel.sort(ProcModel.AddRibPointsModel.OrderNumCol,
                             Qt.AscendingOrder)
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
