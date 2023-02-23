"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, \
                            QSizePolicy, QHeaderView

from data.procModel.GlobalAoAModel import GlobalAoAModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


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
        super().__init__()

        self.win = None
        self.windowLayout = None
        self.helpBar = None
        self.btnBar = None
        self.globAoA_M = GlobalAoAModel()
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
                    calage_t
                    length_T
                ---------------------------
                            help_bar | btn_bar
        """
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

        calage_t.set_help_text(GlobalAoAModel.FinesseCol,
                               _('GlobalAoA-FinesseDesc'))
        calage_t.set_help_text(GlobalAoAModel.CentOfPressCol,
                               _('GlobalAoA-CenterOfPressureDesc'))
        calage_t.set_help_text(GlobalAoAModel.CalageCol,
                               _('GlobalAoA-CalageDesc'))

        calage_t.setFixedHeight(2
                                + calage_t.horizontalHeader().height()
                                + calage_t.rowHeight(0))

        calage_t.en_double_validator(GlobalAoAModel.FinesseCol,
                                     GlobalAoAModel.FinesseCol,
                                     ValidationValues.Proc.FinesseMin_deg,
                                     ValidationValues.Proc.FinesseMax_deg,
                                     2)

        calage_t.en_int_validator(GlobalAoAModel.CentOfPressCol,
                                  GlobalAoAModel.CalageCol,
                                  ValidationValues.WingChordMin_perc,
                                  ValidationValues.WingChordMax_perc)

        calage_t.en_double_validator(GlobalAoAModel.RisersCol,
                                     GlobalAoAModel.RisersCol,
                                     ValidationValues.Proc.RisersBasicLengthMin_cm,
                                     ValidationValues.Proc.RisersBasicLengthMax_cm,
                                     2)

        calage_t.en_double_validator(GlobalAoAModel.LinesCol,
                                     GlobalAoAModel.LinesCol,
                                     ValidationValues.Proc.LinesBasicLengthMin_cm,
                                     ValidationValues.Proc.LinesBasicLengthMax_cm,
                                     2)

        calage_t.en_double_validator(GlobalAoAModel.KarabinersCol,
                                     GlobalAoAModel.KarabinersCol,
                                     ValidationValues.Proc.KarabinersSeparationMin_cm,
                                     ValidationValues.Proc.KarabinersSeparationMax_cm,
                                     2)

        self.windowLayout.addWidget(calage_t)

        #####
        length_t = TableView()
        length_t.setModel(self.globAoA_M)
        # hide the ID column which is always at the end of the model
        length_t.hideColumn(self.globAoA_M.columnCount() - 1)
        length_t.verticalHeader().setVisible(False)
        length_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        length_t.set_help_bar(self.helpBar)
        length_t.hideColumn(0)
        length_t.hideColumn(1)
        length_t.hideColumn(2)

        length_t.set_help_text(GlobalAoAModel.RisersCol,
                               _('GlobalAoA-RisersDesc'))
        length_t.set_help_text(GlobalAoAModel.LinesCol,
                               _('GlobalAoA-LinesDesc'))
        length_t.set_help_text(GlobalAoAModel.KarabinersCol,
                               _('GlobalAoA-KarabinersDesc'))

        length_t.en_int_validator(GlobalAoAModel.RisersCol,
                                  GlobalAoAModel.LinesCol,
                                  0, 2000)
        length_t.en_int_validator(GlobalAoAModel.KarabinersCol,
                                  GlobalAoAModel.KarabinersCol,
                                  0, 100)

        length_t.setFixedHeight(2
                                + length_t.horizontalHeader().height()
                                + length_t.rowHeight(0))

        self.windowLayout.addWidget(length_t)

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
