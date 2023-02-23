"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, \
                            QSizePolicy, QGridLayout, QLabel, QWidget, \
                            QHeaderView

from data.procModel.RamificationModel import RamificationModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class Ramification(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit ramification data
    """

    __className = 'Ramification'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()

        self.btnBar = None
        self.helpBar = None
        self.window_ly = None
        self.win = None
        self.ramif_M = RamificationModel()
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
                    edit_grid_l
                        three_line_rows_t
                        FourLineRows_T
                        ThreeBrakeRows_T
                        four_brake_rows_t
                ---------------------------
                            help_bar | btn_bar
        """
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
        three_line_rows_l.setAlignment(Qt.AlignmentFlag.AlignRight)

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
        three_line_rows_t.set_help_bar(self.helpBar)

        three_line_rows_t.set_help_text(RamificationModel.ThirdToSailCol, _('Ramification-3L-ThirdLineToSailDesc'))

        three_line_rows_t.en_double_validator(RamificationModel.ThirdToSailCol,
                                              RamificationModel.ThirdToSailCol,
                                              ValidationValues.Proc.RamificationLengthMin_cm,
                                              ValidationValues.Proc.RamificationLengthMax_cm,
                                              2)

        three_line_rows_t.setFixedHeight(2
                                         + three_line_rows_t.horizontalHeader().height()
                                         + three_line_rows_t.rowHeight(0))

        three_line_rows_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        edit_grid_l.addWidget(three_line_rows_l, 0, 0)
        edit_grid_l.addWidget(three_line_rows_t, 0, 1)
        edit_grid_l.addWidget(QWidget(), 0, 2)
        edit_grid_l.addWidget(QWidget(), 0, 3)

        # 4 line rows
        four_line_rows_l = QLabel(_('4 Line rows'))
        four_line_rows_l.setAlignment(Qt.AlignmentFlag.AlignRight)

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
        four_line_rows_t.set_help_bar(self.helpBar)

        four_line_rows_t.set_help_text(RamificationModel.ThirdToSailCol, _('Ramification-4L-ThirdLineToSailDesc'))
        four_line_rows_t.set_help_text(RamificationModel.FourthToSailCol, _('Ramification-4L-FourthLineToSailDesc'))

        four_line_rows_t.en_double_validator(RamificationModel.ThirdToSailCol,
                                             RamificationModel.ThirdToSailCol,
                                             ValidationValues.Proc.RamificationLengthMin_cm,
                                             ValidationValues.Proc.RamificationLengthMax_cm,
                                             2)
        four_line_rows_t.en_double_validator(RamificationModel.FourthToSailCol,
                                             RamificationModel.FourthToSailCol,
                                             ValidationValues.Proc.RamificationLengthMin_cm,
                                             ValidationValues.Proc.RamificationLengthMax_cm,
                                             2)

        four_line_rows_t.setFixedHeight(2
                                        + four_line_rows_t.horizontalHeader().height()
                                        + four_line_rows_t.rowHeight(1))
        four_line_rows_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        edit_grid_l.addWidget(four_line_rows_l, 1, 0)
        edit_grid_l.addWidget(four_line_rows_t, 1, 1, 1, 2)
        edit_grid_l.addWidget(QWidget(), 1, 3)

        # 3 brake rows
        three_brake_rows_l = QLabel(_('3 Brake rows'))
        three_brake_rows_l.setAlignment(Qt.AlignmentFlag.AlignRight)

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
        three_brake_rows_t.set_help_bar(self.helpBar)

        three_brake_rows_t.set_help_text(RamificationModel.ThirdToSailCol, _('Ramification-3L-ThirdBrakeToSailDesc'))

        three_brake_rows_t.en_double_validator(RamificationModel.ThirdToSailCol,
                                               RamificationModel.ThirdToSailCol,
                                               ValidationValues.Proc.RamificationLengthMin_cm,
                                               ValidationValues.Proc.RamificationLengthMax_cm,
                                               2)

        three_brake_rows_t.setFixedHeight(
            2
            + three_brake_rows_t.horizontalHeader().height()
            + three_brake_rows_t.rowHeight(2))
        three_brake_rows_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        edit_grid_l.addWidget(three_brake_rows_l, 2, 0)
        edit_grid_l.addWidget(three_brake_rows_t, 2, 1)
        edit_grid_l.addWidget(QWidget(), 2, 2)
        edit_grid_l.addWidget(QWidget(), 2, 3)

        # 4 brake rows
        four_brake_rows_l = QLabel(_('4 Brake rows'))
        four_brake_rows_l.setAlignment(Qt.AlignmentFlag.AlignRight)

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
        four_brake_rows_t.set_help_bar(self.helpBar)

        four_brake_rows_t.set_help_text(
            RamificationModel.ThirdToSailCol,
            _('Ramification-4L-ThirdBrakeToSailDesc'))
        four_brake_rows_t.set_help_text(
            RamificationModel.FourthToSailCol,
            _('Ramification-4L-FourthBrakeToSailDesc'))

        four_brake_rows_t.en_double_validator(RamificationModel.ThirdToSailCol,
                                              RamificationModel.ThirdToSailCol,
                                              ValidationValues.Proc.RamificationLengthMin_cm,
                                              ValidationValues.Proc.RamificationLengthMax_cm,
                                              2)
        four_brake_rows_t.en_double_validator(RamificationModel.FourthToSailCol,
                                              RamificationModel.FourthToSailCol,
                                              ValidationValues.Proc.RamificationLengthMin_cm,
                                              ValidationValues.Proc.RamificationLengthMax_cm,
                                              2)

        four_brake_rows_t.setFixedHeight(2
                                         + four_brake_rows_t.horizontalHeader().height()
                                         + four_brake_rows_t.rowHeight(3))
        four_brake_rows_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        edit_grid_l.addWidget(four_brake_rows_l, 3, 0)
        edit_grid_l.addWidget(four_brake_rows_t, 3, 1, 1, 2)
        edit_grid_l.addWidget(QWidget(), 3, 3)

        self.window_ly.addLayout(edit_grid_l)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/ramification.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

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
                          + '.btn_press unrecognized button press '
                          + q)
