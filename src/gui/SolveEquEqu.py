"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel

from data.ProcModel import ProcModel
from data.procModel.SolveEquEquModel import SolveEquEquModel

from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class SolveEquEqu(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Solve Equilibrium Equations data
    """

    __className = 'SolveEquEqu'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()

        self.btnBar = None
        self.usage_cb = None
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.pm = ProcModel()

        self.solve_equ_equ_m = SolveEquEquModel()
        self.solve_equ_equ_m.usageUpd.connect(self.usage_update)
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
                    Table
                    -------------------------
                        help_bar  | btn_bar

        Naming:
            Conf is always one as there is only one configuration possible
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(500, 300)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Solve Equilibrium Equations"))

        usage_l = QLabel(_('Type'))
        self.usage_cb = QComboBox()
        self.usage_cb.addItem(_("None"))
        self.usage_cb.addItem(_("User defined"))
        self.usage_cb.currentIndexChanged.connect(self.usage_cb_change)
        usage_ly = QHBoxLayout()
        usage_ly.addWidget(usage_l)
        usage_ly.addWidget(self.usage_cb)
        usage_ly.addStretch()

        self.window_ly.addLayout(usage_ly)

        self.one_t = TableView()
        self.one_t.setModel(self.solve_equ_equ_m)
        self.one_t.verticalHeader().setVisible(False)
        self.one_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.one_t.hideColumn(0)
        for i in range(SolveEquEquModel.Splilot_Col, SolveEquEquModel.ConfigNumCol+1):
            self.one_t.hideColumn(i)
        self.one_t.hideColumn(SolveEquEquModel.ID_Col)

        self.one_t.setFixedHeight(2 + (2 * self.one_t.horizontalHeader().height()))

        self.window_ly.addWidget(self.one_t)

        self.one_t.en_double_validator(SolveEquEquModel.g_Col,
                                       SolveEquEquModel.g_Col,
                                       ValidationValues.Proc.SolveEquEqu_g_min,
                                       ValidationValues.Proc.SolveEquEqu_g_max,
                                       3)
        self.one_t.en_double_validator(SolveEquEquModel.ro_Col,
                                       SolveEquEquModel.ro_Col,
                                       ValidationValues.Proc.SolveEquEqu_ro_min,
                                       ValidationValues.Proc.SolveEquEqu_ro_max,
                                       3)
        self.one_t.en_double_validator(SolveEquEquModel.mu_Col,
                                       SolveEquEquModel.mu_Col,
                                       ValidationValues.Proc.SolveEquEqu_mu_min,
                                       ValidationValues.Proc.SolveEquEqu_mu_max,
                                       3)
        self.one_t.en_double_validator(SolveEquEquModel.V_Col,
                                       SolveEquEquModel.V_Col,
                                       ValidationValues.Proc.SolveEquEqu_V_min,
                                       ValidationValues.Proc.SolveEquEqu_V_max,
                                       1)
        self.one_t.en_double_validator(SolveEquEquModel.Alpha_Col,
                                       SolveEquEquModel.Alpha_Col,
                                       ValidationValues.Proc.AlphaMaxCentMin,
                                       ValidationValues.Proc.AlphaMaxCentMax,
                                       2)
        self.one_t.en_double_validator(SolveEquEquModel.Cl_Col,
                                       SolveEquEquModel.Cl_Col,
                                       ValidationValues.Proc.SolveEquEqu_cl_min,
                                       ValidationValues.Proc.SolveEquEqu_cl_max,
                                       5)
        self.one_t.en_double_validator(SolveEquEquModel.cle_Col,
                                       SolveEquEquModel.cle_Col,
                                       ValidationValues.Proc.SolveEquEqu_cle_min,
                                       ValidationValues.Proc.SolveEquEqu_cle_max,
                                       1)
        self.one_t.en_double_validator(SolveEquEquModel.Cd_Col,
                                       SolveEquEquModel.Cd_Col,
                                       ValidationValues.Proc.SolveEquEqu_Cd_min,
                                       ValidationValues.Proc.SolveEquEqu_Cd_max,
                                       5)
        self.one_t.en_double_validator(SolveEquEquModel.cde_Col,
                                       SolveEquEquModel.cde_Col,
                                       ValidationValues.Proc.SolveEquEqu_cde_min,
                                       ValidationValues.Proc.SolveEquEqu_cde_max,
                                       1)
        self.one_t.en_double_validator(SolveEquEquModel.Cm_Col,
                                       SolveEquEquModel.Cm_Col,
                                       ValidationValues.Proc.SolveEquEqu_cm_min,
                                       ValidationValues.Proc.SolveEquEqu_cm_max,
                                       1)

        self.one_t.set_help_bar(self.helpBar)
        self.one_t.set_help_text(SolveEquEquModel.g_Col,
                            _('SolveEquEqu-g'))
        self.one_t.set_help_text(SolveEquEquModel.ro_Col,
                            _('SolveEquEqu-ro'))
        self.one_t.set_help_text(SolveEquEquModel.mu_Col,
                            _('SolveEquEqu-mu'))
        self.one_t.set_help_text(SolveEquEquModel.V_Col,
                            _('SolveEquEqu-V'))
        self.one_t.set_help_text(SolveEquEquModel.Alpha_Col,
                            _('SolveEquEqu-Alpha'))
        self.one_t.set_help_text(SolveEquEquModel.Cl_Col,
                            _('SolveEquEqu-Cl'))
        self.one_t.set_help_text(SolveEquEquModel.cle_Col,
                            _('SolveEquEqu-cle'))
        self.one_t.set_help_text(SolveEquEquModel.Cd_Col,
                            _('SolveEquEqu-Cd'))
        self.one_t.set_help_text(SolveEquEquModel.cde_Col,
                            _('SolveEquEqu-cde'))
        self.one_t.set_help_text(SolveEquEquModel.Cm_Col,
                            _('SolveEquEqu-Cm'))


        self.two_t = TableView()
        self.two_t.setModel(self.solve_equ_equ_m)
        self.two_t.verticalHeader().setVisible(False)
        self.two_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for i in range(0, SolveEquEquModel.Splilot_Col):
            self.two_t.hideColumn(i)
        self.two_t.hideColumn(self.solve_equ_equ_m.columnCount() - 1)
        self.two_t.hideColumn(self.solve_equ_equ_m.columnCount() - 2)

        self.two_t.setFixedHeight(2 + (2 * self.two_t.horizontalHeader().height()))

        self.window_ly.addWidget(self.two_t)

        self.two_t.en_double_validator(SolveEquEquModel.Splilot_Col,
                                       SolveEquEquModel.Splilot_Col,
                                       ValidationValues.Proc.SolveEquEqu_Spilot_min,
                                       ValidationValues.Proc.SolveEquEqu_Spilot_max,
                                       3)
        self.two_t.en_double_validator(SolveEquEquModel.Cdplilot_Col,
                                       SolveEquEquModel.Cdplilot_Col,
                                       ValidationValues.Proc.SolveEquEqu_Cdpilot_min,
                                       ValidationValues.Proc.SolveEquEqu_Cdpilot_max,
                                       1)
        self.two_t.en_double_validator(SolveEquEquModel.Mw_Col,
                                       SolveEquEquModel.Mw_Col,
                                       ValidationValues.Proc.SolveEquEqu_Mw_min,
                                       ValidationValues.Proc.SolveEquEqu_Mw_max,
                                       1)
        self.two_t.en_double_validator(SolveEquEquModel.Mp_Col,
                                       SolveEquEquModel.Mp_Col,
                                       ValidationValues.Proc.SolveEquEqu_Mp_min,
                                       ValidationValues.Proc.SolveEquEqu_Mp_max,
                                       1)
        self.two_t.en_double_validator(SolveEquEquModel.Pmc_Col,
                                       SolveEquEquModel.Pmc_Col,
                                       ValidationValues.Proc.SolveEquEqu_Pmc_min,
                                       ValidationValues.Proc.SolveEquEqu_Pmc_max,
                                       1)
        self.two_t.en_double_validator(SolveEquEquModel.Mql_Col,
                                       SolveEquEquModel.Mql_Col,
                                       ValidationValues.Proc.SolveEquEqu_Mql_min,
                                       ValidationValues.Proc.SolveEquEqu_Mql_max,
                                       1)
        self.two_t.en_double_validator(SolveEquEquModel.Ycp_Col,
                                       SolveEquEquModel.Ycp_Col,
                                       ValidationValues.Proc.SolveEquEqu_Ycp_min,
                                       ValidationValues.Proc.SolveEquEqu_Ycp_max,
                                       3)
        self.two_t.en_double_validator(SolveEquEquModel.Zcp_Col,
                                       SolveEquEquModel.Zcp_Col,
                                       ValidationValues.Proc.SolveEquEqu_Zcp_min,
                                       ValidationValues.Proc.SolveEquEqu_Zcp_max,
                                       3)

        self.two_t.set_help_bar(self.helpBar)
        self.two_t.set_help_text(SolveEquEquModel.Splilot_Col,
                                 _('SolveEquEqu-Spilot'))
        self.two_t.set_help_text(SolveEquEquModel.Cdplilot_Col,
                                 _('SolveEquEqu-Cdpilot'))
        self.two_t.set_help_text(SolveEquEquModel.Mw_Col,
                                 _('SolveEquEqu-Mw'))
        self.two_t.set_help_text(SolveEquEquModel.Mp_Col,
                                 _('SolveEquEqu-Mp'))
        self.two_t.set_help_text(SolveEquEquModel.Pmc_Col,
                                 _('SolveEquEqu-Pmc'))
        self.two_t.set_help_text(SolveEquEquModel.Mql_Col,
                                 _('SolveEquEqu-Mql'))
        self.two_t.set_help_text(SolveEquEquModel.Ycp_Col,
                                 _('SolveEquEqu-Ycp'))
        self.two_t.set_help_text(SolveEquEquModel.Zcp_Col,
                                 _('SolveEquEqu-Zcp'))

        self.usage_update()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('expert/solveEquEqu.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def usage_update(self):
        """
        :method: Updates the GUI as soon in the model the usage flag has
                 been changed
        """
        if self.solve_equ_equ_m.is_used():
            self.usage_cb.setCurrentIndex(1)
            self.one_t.setEnabled(True)
            self.two_t.setEnabled(True)
        else:
            self.usage_cb.setCurrentIndex(0)
            self.one_t.setEnabled(False)
            self.two_t.setEnabled(False)

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        if self.usage_cb.currentIndex() == 0:
            self.solve_equ_equ_m.set_is_used(False)
        else:
            self.solve_equ_equ_m.set_is_used(True)
        self.pm.set_file_saved(False)

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
