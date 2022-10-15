"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
                            QHBoxLayout, QVBoxLayout, QComboBox, QLabel

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class CalageVar(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'CalageVar'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.btnBar = None
        self.usage_cb = None
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.pm = ProcModel()

        self.calageVar_M = ProcModel.CalageVarModel()
        self.calageVar_M.usageUpd.connect(self.usage_update)
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
                    Table
                    Table
                    Table
                    -------------------------
                        help_bar  | btn_bar

        Naming:
            Conf is always one as there is only one configuration possible
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(600, 200)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Calage variation "))

        usage_l = QLabel(_('Type'))
        self.usage_cb = QComboBox()
        self.usage_cb.addItem(_("None"))
        self.usage_cb.addItem(_("Type 1"))
        self.usage_cb.currentIndexChanged.connect(self.usage_cb_change)
        usage_ly = QHBoxLayout()
        usage_ly.addWidget(usage_l)
        usage_ly.addWidget(self.usage_cb)
        usage_ly.addStretch()

        self.window_ly.addLayout(usage_ly)

        one_t = TableView()
        one_t.setModel(self.calageVar_M)
        one_t.verticalHeader().setVisible(False)
        one_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        one_t.hideColumn(0)
        for i in range(ProcModel.CalageVarModel.PosACol,
                       ProcModel.CalageVarModel.NumPosStepsCol + 1):
            one_t.hideColumn(i)
        one_t.hideColumn(self.calageVar_M.columnCount() - 2)
        one_t.hideColumn(self.calageVar_M.columnCount() - 1)

        one_t.setFixedHeight(2
                             + one_t.horizontalHeader().height()
                             + one_t.rowHeight(0))
        one_t_ly = QHBoxLayout()
        one_t_ly.addWidget(one_t)
        one_t_ly.addStretch()
        one_t_ly.addStretch()
        self.window_ly.addLayout(one_t_ly)

        one_t.en_int_validator(ProcModel.CalageVarModel.NumRisersCol,
                               ProcModel.CalageVarModel.NumRisersCol,
                               2, 6)

        one_t.set_help_bar(self.helpBar)
        one_t.set_help_text(ProcModel.CalageVarModel.NumRisersCol,
                            _('CalageVar-NumRisersDesc'))

        two_t = TableView()
        two_t.setModel(self.calageVar_M)
        two_t.verticalHeader().setVisible(False)
        two_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(0, ProcModel.CalageVarModel.NumRisersCol + 1):
            two_t.hideColumn(i)
        for i in range(ProcModel.CalageVarModel.MaxNegAngCol,
                       ProcModel.CalageVarModel.NumPosStepsCol + 1):
            two_t.hideColumn(i)
        two_t.hideColumn(self.calageVar_M.columnCount() - 2)
        two_t.hideColumn(self.calageVar_M.columnCount() - 1)

        two_t.setFixedHeight(2
                             + two_t.horizontalHeader().height()
                             + two_t.rowHeight(0))
        two_t_ly = QHBoxLayout()
        two_t_ly.addWidget(two_t)
        self.window_ly.addLayout(two_t_ly)

        two_t.en_double_validator(ProcModel.CalageVarModel.PosACol,
                                  ProcModel.CalageVarModel.PosFCol,
                                  0, 100, 2)

        two_t.set_help_bar(self.helpBar)
        two_t.set_help_text(ProcModel.CalageVarModel.PosACol,
                            _('CalageVar-PosADesc'))
        two_t.set_help_text(ProcModel.CalageVarModel.PosBCol,
                            _('CalageVar-PosBDesc'))
        two_t.set_help_text(ProcModel.CalageVarModel.PosCCol,
                            _('CalageVar-PosCDesc'))
        two_t.set_help_text(ProcModel.CalageVarModel.PosDCol,
                            _('CalageVar-PosDDesc'))
        two_t.set_help_text(ProcModel.CalageVarModel.PosECol,
                            _('CalageVar-PosEDesc'))
        two_t.set_help_text(ProcModel.CalageVarModel.PosFCol,
                            _('CalageVar-PosFDesc'))

        three_t = TableView()
        three_t.setModel(self.calageVar_M)
        three_t.verticalHeader().setVisible(False)
        three_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(0, ProcModel.CalageVarModel.PosFCol + 1):
            three_t.hideColumn(i)
        three_t.hideColumn(self.calageVar_M.columnCount() - 2)
        three_t.hideColumn(self.calageVar_M.columnCount() - 1)

        three_t.setFixedHeight(2
                               + three_t.horizontalHeader().height()
                               + three_t.rowHeight(0))
        three_t_ly = QHBoxLayout()
        three_t_ly.addWidget(three_t)
        self.window_ly.addLayout(three_t_ly)

        three_t.en_double_validator(ProcModel.CalageVarModel.MaxNegAngCol,
                                    ProcModel.CalageVarModel.MaxNegAngCol,
                                    -45, 0, 2)
        three_t.en_int_validator(ProcModel.CalageVarModel.NumNegStepsCol,
                                 ProcModel.CalageVarModel.NumNegStepsCol,
                                 1, 100)
        three_t.en_double_validator(ProcModel.CalageVarModel.MaxPosAngCol,
                                    ProcModel.CalageVarModel.MaxPosAngCol,
                                    0, 45, 2)
        three_t.en_int_validator(ProcModel.CalageVarModel.NumPosStepsCol,
                                 ProcModel.CalageVarModel.NumPosStepsCol,
                                 1, 100)

        three_t.set_help_bar(self.helpBar)
        three_t.set_help_text(ProcModel.CalageVarModel.MaxNegAngCol,
                              _('CalageVar-MaxNegAngDesc'))
        three_t.set_help_text(ProcModel.CalageVarModel.NumNegStepsCol,
                              _('CalageVar-NumNegStepsDesc'))
        three_t.set_help_text(ProcModel.CalageVarModel.MaxPosAngCol,
                              _('CalageVar-MaxPosAngDesc'))
        three_t.set_help_text(ProcModel.CalageVarModel.NumPosStepsCol,
                              _('CalageVar-NumPosStepsDesc'))

        self.usage_update()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/calageVar.html')

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
        logging.debug(self.__className + '.usage_update')

        if self.calageVar_M.isUsed():
            self.usage_cb.setCurrentIndex(1)
        else:
            self.usage_cb.setCurrentIndex(0)

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        logging.debug(self.__className + '.usage_cb_change')
        if self.usage_cb.currentIndex() == 0:
            self.calageVar_M.setIsUsed(False)
        else:
            self.calageVar_M.setIsUsed(True)

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
