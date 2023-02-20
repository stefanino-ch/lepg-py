"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, \
                            QSizePolicy, QHeaderView, QPushButton

from gui.GlobalDefinition import ValidationValues
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from data.procModel.RibModel import RibModel


class Geometry(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit geometry data
    """

    __className = 'Geometry'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        self.btnBar = None
        self.sortBtn = None
        self.table = None
        self.helpBar = None
        self.window_ly = None
        self.win = None
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.rib_M = RibModel()
        self.build_window()

    def closeEvent(self, event):  # @UnusedVariable
        """
        :method: Called at the time the user closes the window.
        """
        logging.debug(self.__className + '.closeEvent')

    def build_window(self):
        """
        :method: Creates the window including all GUI elements.

        Layout::

            Data
            Buttons

        Structure::

            window
                window_ly
                     Table
                    --------------------------
                    SortBtn | help_bar | btn_bar

        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 300)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Geometry"))

        self.table = TableView()
        self.table.setModel(self.rib_M)
        # hide the ID column which is always at the end of the model
        self.table.hideColumn(self.rib_M.columnCount() - 1)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.set_help_bar(self.helpBar)

        self.table.en_int_validator(RibModel.RibNumCol,
                                    RibModel.RibNumCol,
                                    1, ValidationValues.MaxNumRibs)
        self.table.en_double_validator(RibModel.xribCol,
                                       RibModel.xribCol,
                                       0, ValidationValues.HalfWingSpanMax_cm, 3)
        self.table.en_double_validator(RibModel.yLECol,
                                       RibModel.yTECol,
                                       0, ValidationValues.WingChordMax_cm, 3)
        self.table.en_double_validator(RibModel.xpCol,
                                       RibModel.xpCol,
                                       0, ValidationValues.WingChordMax_cm, 3)
        self.table.en_double_validator(RibModel.zCol,
                                       RibModel.zCol,
                                       0, ValidationValues.WingZMax_cm, 3)

        self.table.en_double_validator(RibModel.betaCol,
                                       RibModel.betaCol,
                                       ValidationValues.Proc.RibVerticalAngleMin_deg,
                                       ValidationValues.Proc.RibVerticalAngleMax_deg,
                                       3)

        self.table.en_double_validator(RibModel.RPCol,
                                       RibModel.RPCol,
                                       ValidationValues.Proc.RibRotationPointMin_chord,
                                       ValidationValues.Proc.RibRotationPointMax_chord,
                                       3)

        self.table.en_double_validator(RibModel.WashinCol,
                                       RibModel.WashinCol,
                                       ValidationValues.Proc.WashinMin,
                                       ValidationValues.Proc.WashinMax,
                                       3)

        self.table.en_double_validator(RibModel.RotZCol,
                                       RibModel.RotZCol,
                                       ValidationValues.Proc.RotZColMin,
                                       ValidationValues.Proc.RotZColMax,
                                       3)

        self.table.en_double_validator(RibModel.PosZCol,
                                       RibModel.PosZCol,
                                       ValidationValues.Proc.RibRotationPointMin_chord,
                                       ValidationValues.Proc.RibRotationPointMax_chord,
                                       3)

        self.table.set_help_text(RibModel.RibNumCol,
                                 _('Proc-RibNumDesc'))
        self.table.set_help_text(RibModel.xribCol,
                                 _('Proc-xribDesc'))
        self.table.set_help_text(RibModel.yLECol,
                                 _('Proc-yLEDesc'))
        self.table.set_help_text(RibModel.yTECol,
                                 _('Proc-yTEDesc'))
        self.table.set_help_text(RibModel.xpCol,
                                 _('Proc-xpDesc'))
        self.table.set_help_text(RibModel.zCol,
                                 _('Proc-zDesc'))
        self.table.set_help_text(RibModel.betaCol,
                                 _('Proc-betaDesc'))
        self.table.set_help_text(RibModel.RPCol,
                                 _('Proc-RPDesc'))
        self.table.set_help_text(RibModel.WashinCol,
                                 _('Proc-WashinDesc'))
        self.table.set_help_text(RibModel.RotZCol,
                                 _('Proc-RotZDesc'))
        self.table.set_help_text(RibModel.PosZCol,
                                 _('Proc-PosZDesc'))

        self.window_ly.addWidget(self.table)

        self.sortBtn = QPushButton(_('Sort by Rib Number'))
        self.sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Fixed))
        self.sortBtn.clicked.connect(self.sort_btn_press)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/geometry.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.sortBtn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)

        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def sort_btn_press(self):
        """
        : method : handles the sort of the table by rib number
        """
        logging.debug(self.__className + '.sort_btn_press')
        self.rib_M.sort_table(RibModel.RibNumCol,
                              Qt.SortOrder.AscendingOrder)

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
            logging.error(self.__className +
                          '.btn_press unrecognized button press ' +
                          q)
