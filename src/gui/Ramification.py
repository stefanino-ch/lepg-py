"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QGridLayout, QLabel, QWidget, QHeaderView

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class Ramification(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Seewing allowances data
    """

    __className = 'Ramification'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.ramif_M = ProcModel.RamificationModel()
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
                    edit_grid_l
                        three_line_rows_t
                        FourLineRows_T
                        ThreeBrakeRows_T
                        four_brake_rows_t
                ---------------------------
                            help_bar | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(450, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Ramification"))

        edit_grid_l = QGridLayout()

        # 3 line rows
        three_line_rows_l = QLabel(_('3 Line rows'))
        three_line_rows_l.setAlignment(Qt.AlignRight)

        three_line_rows_t = TableView()
        three_line_rows_t.setModel(self.ramif_M)
        three_line_rows_t.hideRow(1)
        three_line_rows_t.hideRow(2)
        three_line_rows_t.hideRow(3)

        three_line_rows_t.hideColumn(0)  # hide the OrderNum column
        three_line_rows_t.hideColumn(1)  # hide the Rows column
        # hide the ID column
        three_line_rows_t.hideColumn(self.ramif_M.columnCount() - 1)
        # hide the Config column
        three_line_rows_t.hideColumn(self.ramif_M.columnCount() - 2)
        # hide the Config column
        three_line_rows_t.hideColumn(self.ramif_M.columnCount() - 3)

        three_line_rows_t.verticalHeader().setVisible(False)
        three_line_rows_t.setHelpBar(self.helpBar)

        three_line_rows_t.setHelpText(
            ProcModel.RamificationModel.ThirdToSailCol,
            _('Ramification-3L-ThirdLineToSailDesc'))

        three_line_rows_t.enableIntValidator(
            ProcModel.RamificationModel.ThirdToSailCol,
            ProcModel.RamificationModel.ThirdToSailCol,
            1, 2000)

        three_line_rows_t.setFixedHeight(
            2
            + three_line_rows_t.horizontalHeader().height()
            + three_line_rows_t.rowHeight(0))
        three_line_rows_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)

        edit_grid_l.addWidget(three_line_rows_l, 0, 0)
        edit_grid_l.addWidget(three_line_rows_t, 0, 1)
        edit_grid_l.addWidget(QWidget(), 0, 2)
        edit_grid_l.addWidget(QWidget(), 0, 3)

        # 4 line rows
        four_line_rows_l = QLabel(_('4 Line rows'))
        four_line_rows_l.setAlignment(Qt.AlignRight)

        four_line_rows_t = TableView()
        four_line_rows_t.setModel(self.ramif_M)
        four_line_rows_t.hideRow(0)
        four_line_rows_t.hideRow(2)
        four_line_rows_t.hideRow(3)

        four_line_rows_t.hideColumn(0)  # hide the OrderNum column
        four_line_rows_t.hideColumn(1)  # hide the Rows column
        # hide the ID column
        four_line_rows_t.hideColumn(self.ramif_M.columnCount() - 1)
        # hide the Config column
        four_line_rows_t.hideColumn(self.ramif_M.columnCount() - 2)

        four_line_rows_t.verticalHeader().setVisible(False)
        four_line_rows_t.setHelpBar(self.helpBar)

        four_line_rows_t.setHelpText(
            ProcModel.RamificationModel.ThirdToSailCol,
            _('Ramification-4L-ThirdLineToSailDesc'))
        four_line_rows_t.setHelpText(
            ProcModel.RamificationModel.FourthToSailCol,
            _('Ramification-4L-FourthLineToSailDesc'))

        four_line_rows_t.enableIntValidator(
            ProcModel.RamificationModel.ThirdToSailCol,
            ProcModel.RamificationModel.ThirdToSailCol,
            1, 2000)
        four_line_rows_t.enableIntValidator(
            ProcModel.RamificationModel.FourthToSailCol,
            ProcModel.RamificationModel.FourthToSailCol,
            1, 2000)

        four_line_rows_t.setFixedHeight(
            2
            + four_line_rows_t.horizontalHeader().height()
            + four_line_rows_t.rowHeight(1))
        four_line_rows_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)

        edit_grid_l.addWidget(four_line_rows_l, 1, 0)
        edit_grid_l.addWidget(four_line_rows_t, 1, 1, 1, 2)
        edit_grid_l.addWidget(QWidget(), 1, 3)

        # 3 brake rows
        three_brake_rows_l = QLabel(_('3 Brake rows'))
        three_brake_rows_l.setAlignment(Qt.AlignRight)

        three_brake_rows_t = TableView()
        three_brake_rows_t.setModel(self.ramif_M)
        three_brake_rows_t.hideRow(0)
        three_brake_rows_t.hideRow(1)
        three_brake_rows_t.hideRow(3)

        three_brake_rows_t.hideColumn(0)  # hide the OrderNum column
        three_brake_rows_t.hideColumn(1)  # hide the Rows column
        # hide the ID column
        three_brake_rows_t.hideColumn(self.ramif_M.columnCount() - 1)
        # hide the Config column
        three_brake_rows_t.hideColumn(self.ramif_M.columnCount() - 2)
        # hide the Config column
        three_brake_rows_t.hideColumn(self.ramif_M.columnCount() - 3)
        three_brake_rows_t.verticalHeader().setVisible(False)
        three_brake_rows_t.setHelpBar(self.helpBar)

        three_brake_rows_t.setHelpText(
            ProcModel.RamificationModel.ThirdToSailCol,
            _('Ramification-3L-ThirdBrakeToSailDesc'))

        three_brake_rows_t.enableIntValidator(
            ProcModel.RamificationModel.ThirdToSailCol,
            ProcModel.RamificationModel.ThirdToSailCol,
            1, 2000)

        three_brake_rows_t.setFixedHeight(
            2
            + three_brake_rows_t.horizontalHeader().height()
            + three_brake_rows_t.rowHeight(2))
        three_brake_rows_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)

        edit_grid_l.addWidget(three_brake_rows_l, 2, 0)
        edit_grid_l.addWidget(three_brake_rows_t, 2, 1)
        edit_grid_l.addWidget(QWidget(), 2, 2)
        edit_grid_l.addWidget(QWidget(), 2, 3)

        # 4 brake rows
        four_brake_rows_l = QLabel(_('4 Brake rows'))
        four_brake_rows_l.setAlignment(Qt.AlignRight)

        four_brake_rows_t = TableView()
        four_brake_rows_t.setModel(self.ramif_M)
        four_brake_rows_t.hideRow(0)
        four_brake_rows_t.hideRow(1)
        four_brake_rows_t.hideRow(2)

        four_brake_rows_t.hideColumn(0)  # hide the OrderNum column
        four_brake_rows_t.hideColumn(1)  # hide the Rows column
        # hide the ID column
        four_brake_rows_t.hideColumn(self.ramif_M.columnCount() - 1)
        # hide the Config column
        four_brake_rows_t.hideColumn(self.ramif_M.columnCount() - 2)
        four_brake_rows_t.verticalHeader().setVisible(False)
        four_brake_rows_t.setHelpBar(self.helpBar)

        four_brake_rows_t.setHelpText(
            ProcModel.RamificationModel.ThirdToSailCol,
            _('Ramification-4L-ThirdBrakeToSailDesc'))
        four_brake_rows_t.setHelpText(
            ProcModel.RamificationModel.FourthToSailCol,
            _('Ramification-4L-FourthBrakeToSailDesc'))

        four_brake_rows_t.enableIntValidator(
            ProcModel.RamificationModel.ThirdToSailCol,
            ProcModel.RamificationModel.ThirdToSailCol,
            1, 2000)
        four_brake_rows_t.enableIntValidator(
            ProcModel.RamificationModel.FourthToSailCol,
            ProcModel.RamificationModel.FourthToSailCol,
            1, 2000)

        four_brake_rows_t.setFixedHeight(2
                                         + four_brake_rows_t.horizontalHeader().height()
                                         + four_brake_rows_t.rowHeight(3))
        four_brake_rows_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)

        edit_grid_l.addWidget(four_brake_rows_l, 3, 0)
        edit_grid_l.addWidget(four_brake_rows_t, 3, 1, 1, 2)
        edit_grid_l.addWidget(QWidget(), 3, 3)

        self.window_ly.addLayout(edit_grid_l)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/ramification.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def btn_press(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
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
