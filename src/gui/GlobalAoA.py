"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, \
                            QSizePolicy, QHeaderView

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class GlobalAoA(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit global AoA data
    """

    __className = 'GlobalAoA'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.globAoA_M = ProcModel.GlobAoAModel()
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
                    calage_t
                    length_T
                ---------------------------
                            help_bar | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(250, 200)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Global AoA"))

        calage_t = TableView()
        calage_t.setModel(self.globAoA_M)
        # hide the ID column which is always at the end of the model
        calage_t.hideColumn(self.globAoA_M.columnCount() - 1)
        calage_t.verticalHeader().setVisible(False)
        calage_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        calage_t.set_help_bar(self.helpBar)
        calage_t.hideColumn(3)
        calage_t.hideColumn(4)
        calage_t.hideColumn(5)

        calage_t.set_help_text(ProcModel.GlobAoAModel.FinesseCol,
                               _('GlobalAoA-FinesseDesc'))
        calage_t.set_help_text(ProcModel.GlobAoAModel.CentOfPressCol,
                               _('GlobalAoA-CenterOfPressureDesc'))
        calage_t.set_help_text(ProcModel.GlobAoAModel.CalageCol,
                               _('GlobalAoA-CalageDesc'))

        calage_t.en_double_validator(ProcModel.GlobAoAModel.FinesseCol,
                                     ProcModel.GlobAoAModel.FinesseCol,
                                     0, 100, 2)
        calage_t.en_int_validator(ProcModel.GlobAoAModel.CentOfPressCol,
                                  ProcModel.GlobAoAModel.CalageCol,
                                  0, 100)

        calage_t.setFixedHeight(2
                                + calage_t.horizontalHeader().height()
                                + calage_t.rowHeight(0))

        self.windowLayout.addWidget(calage_t)

        #####
        lenght_t = TableView()
        lenght_t.setModel(self.globAoA_M)
        # hide the ID column which is always at the end of the model
        lenght_t.hideColumn(self.globAoA_M.columnCount() - 1)
        lenght_t.verticalHeader().setVisible(False)
        lenght_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lenght_t.set_help_bar(self.helpBar)
        lenght_t.hideColumn(0)
        lenght_t.hideColumn(1)
        lenght_t.hideColumn(2)

        lenght_t.set_help_text(ProcModel.GlobAoAModel.RisersCol,
                               _('GlobalAoA-RisersDesc'))
        lenght_t.set_help_text(ProcModel.GlobAoAModel.LinesCol,
                               _('GlobalAoA-LinesDesc'))
        lenght_t.set_help_text(ProcModel.GlobAoAModel.KarabinersCol,
                               _('GlobalAoA-KarabinersDesc'))

        lenght_t.en_int_validator(ProcModel.GlobAoAModel.RisersCol,
                                  ProcModel.GlobAoAModel.LinesCol,
                                  0, 2000)
        lenght_t.en_int_validator(ProcModel.GlobAoAModel.KarabinersCol,
                                  ProcModel.GlobAoAModel.KarabinersCol,
                                  0, 100)

        lenght_t.setFixedHeight(2
                                + lenght_t.horizontalHeader().height()
                                + lenght_t.rowHeight(0))

        self.windowLayout.addWidget(lenght_t)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/globalAoA.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottom_layout)

        self.win.setLayout(self.windowLayout)

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
