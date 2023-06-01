"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QGridLayout, QLabel, QWidget, QHeaderView

from data.procModel.SewingAllowancesModel import SewingAllowancesModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class SewingAllowances(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Sewing allowances data
    """

    __className = 'SewingAllowances'
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

        self.sewAll_M = SewingAllowancesModel()
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
                         upperP_T
                         lower_p_t
                         ribs_t
                         vRibsT
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
        self.setWindowTitle(_("Sewing allowances"))

        edit_grid_l = QGridLayout()

        # upper panel
        upper_p_l = QLabel(_('Upper panel'))
        upper_p_l.setAlignment(Qt.AlignmentFlag.AlignRight)

        upper_p_t = TableView()
        upper_p_t.setModel(self.sewAll_M)
        upper_p_t.hideRow(1)
        upper_p_t.hideRow(2)
        upper_p_t.hideRow(3)
        # hide the ID column which is always at the end of the model
        upper_p_t.hideColumn(self.sewAll_M.columnCount() - 1)
        upper_p_t.verticalHeader().setVisible(False)
        upper_p_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        upper_p_t.set_help_bar(self.helpBar)

        upper_p_t.set_help_text(SewingAllowancesModel.EdgeSeamCol,
                                _('SewingAllowances-EdgeSeamDesc'))
        upper_p_t.set_help_text(SewingAllowancesModel.LeSeemCol,
                                _('SewingAllowances-LeSeamDesc'))
        upper_p_t.set_help_text(SewingAllowancesModel.TeSeemCol,
                                _('SewingAllowances-TeSeamDesc'))

        upper_p_t.en_int_validator(SewingAllowancesModel.EdgeSeamCol,
                                   SewingAllowancesModel.TeSeemCol,
                                   ValidationValues.Proc.MinSewingAllowance_mm,
                                   ValidationValues.Proc.MaxSewingAllowance_mm)
        upper_p_t.setFixedHeight(2
                                 + upper_p_t.horizontalHeader().height()
                                 + upper_p_t.rowHeight(0))

        edit_grid_l.addWidget(upper_p_l, 0, 0)
        edit_grid_l.addWidget(upper_p_t, 0, 1)
        edit_grid_l.addWidget(QWidget(), 0, 3)

        # lower panel
        lower_p_l = QLabel(_('Lower panel'))
        lower_p_l.setAlignment(Qt.AlignmentFlag.AlignRight)

        lower_p_t = TableView()
        lower_p_t.setModel(self.sewAll_M)
        lower_p_t.hideRow(0)
        lower_p_t.hideRow(2)
        lower_p_t.hideRow(3)
        # hide the ID column which is always at the end of the model
        lower_p_t.hideColumn(self.sewAll_M.columnCount() - 1)
        lower_p_t.verticalHeader().setVisible(False)
        lower_p_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lower_p_t.set_help_bar(self.helpBar)

        lower_p_t.set_help_text(SewingAllowancesModel.EdgeSeamCol,
                                _('SewingAllowances-EdgeSeamDesc'))
        lower_p_t.set_help_text(SewingAllowancesModel.LeSeemCol,
                                _('SewingAllowances-LeSeamDesc'))
        lower_p_t.set_help_text(SewingAllowancesModel.TeSeemCol,
                                _('SewingAllowances-TeSeamDesc'))

        lower_p_t.en_int_validator(SewingAllowancesModel.EdgeSeamCol,
                                   SewingAllowancesModel.TeSeemCol,
                                   ValidationValues.Proc.MinSewingAllowance_mm,
                                   ValidationValues.Proc.MaxSewingAllowance_mm)
        lower_p_t.setFixedHeight(2
                                 + upper_p_t.horizontalHeader().height()
                                 + upper_p_t.rowHeight(0))

        edit_grid_l.addWidget(lower_p_l, 1, 0)
        edit_grid_l.addWidget(lower_p_t, 1, 1)
        edit_grid_l.addWidget(QWidget(), 1, 3)

        # ribs panel
        ribs_l = QLabel(_('Ribs'))
        ribs_l.setAlignment(Qt.AlignmentFlag.AlignRight)

        ribs_t = TableView()
        ribs_t.setModel(self.sewAll_M)
        ribs_t.hideRow(0)
        ribs_t.hideRow(1)
        ribs_t.hideRow(3)
        ribs_t.hideColumn(1)
        ribs_t.hideColumn(2)
        # hide the ID column which is always at the end of the model
        ribs_t.hideColumn(self.sewAll_M.columnCount() - 1)
        ribs_t.verticalHeader().setVisible(False)
        ribs_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        ribs_t.set_help_bar(self.helpBar)

        ribs_t.set_help_text(SewingAllowancesModel.EdgeSeamCol,
                             _('SewingAllowances-RibsSeemDesc'))

        ribs_t.en_int_validator(SewingAllowancesModel.EdgeSeamCol,
                                SewingAllowancesModel.EdgeSeamCol,
                                ValidationValues.Proc.MinSewingAllowance_mm,
                                ValidationValues.Proc.MaxSewingAllowance_mm)
        ribs_t.setFixedHeight(2
                              + upper_p_t.horizontalHeader().height()
                              + upper_p_t.rowHeight(0))

        edit_grid_l.addWidget(ribs_l, 2, 0)
        edit_grid_l.addWidget(ribs_t, 2, 1)
        edit_grid_l.addWidget(QWidget(), 2, 3)

        # ribs panel
        v_ribs_l = QLabel(_('V-Ribs'))
        v_ribs_l.setAlignment(Qt.AlignmentFlag.AlignRight)

        v_ribs_t = TableView()
        v_ribs_t.setModel(self.sewAll_M)
        v_ribs_t.hideRow(0)
        v_ribs_t.hideRow(1)
        v_ribs_t.hideRow(2)
        v_ribs_t.hideColumn(1)
        v_ribs_t.hideColumn(2)
        # hide the ID column which is always at the end of the model
        v_ribs_t.hideColumn(self.sewAll_M.columnCount() - 1)
        v_ribs_t.verticalHeader().setVisible(False)
        v_ribs_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        v_ribs_t.set_help_bar(self.helpBar)

        v_ribs_t.set_help_text(SewingAllowancesModel.EdgeSeamCol,
                               _('SewingAllowances-V-RibsSeemDesc'))

        v_ribs_t.en_int_validator(SewingAllowancesModel.EdgeSeamCol,
                                  SewingAllowancesModel.EdgeSeamCol,
                                  ValidationValues.Proc.MinSewingAllowance_mm,
                                  ValidationValues.Proc.MaxSewingAllowance_mm)
        v_ribs_t.setFixedHeight(2
                                + upper_p_t.horizontalHeader().height()
                                + upper_p_t.rowHeight(0))

        edit_grid_l.addWidget(v_ribs_l, 3, 0)
        edit_grid_l.addWidget(v_ribs_t, 3, 1)
        edit_grid_l.addWidget(QWidget(), 3, 3)

        self.window_ly.addLayout(edit_grid_l)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/sewingAllowances.html')

        bottom_ly = QHBoxLayout()
        bottom_ly.addStretch()
        bottom_ly.addWidget(self.helpBar)
        bottom_ly.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_ly)

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