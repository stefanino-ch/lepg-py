"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget,\
                            QSizePolicy, QHeaderView, QPushButton

from data.procModel.AnchorPointsModel import AnchorPointsModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class AnchorPoints(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit anchor points data
    """

    __className = 'AnchorPoints'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()

        self.btnBar = None
        self.sortBtn = None
        self.table = None
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.anchPoints_M = AnchorPointsModel()
        self.build_window()

    def closeEvent(self, event):
        """
        :method: Called at the time the user closes the window.
        """
        pass

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
                    ---------------------------
                     SortBtn | help_bar | btn_bar
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 300)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Anchor points"))

        self.table = TableView()
        self.table.setModel(self.anchPoints_M)
        # hide the ID column which is always at the end of the model
        self.table.hideColumn(self.anchPoints_M.columnCount() - 1)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.en_int_validator(AnchorPointsModel.RibNumCol,
                                    AnchorPointsModel.RibNumCol,
                                    1, ValidationValues.MaxNumRibs)

        self.table.en_int_validator(AnchorPointsModel.NumAnchCol,
                                    AnchorPointsModel.NumAnchCol,
                                    ValidationValues.Proc.NumAnchorsMin,
                                    ValidationValues.Proc.NumAnchorsMax)

        self.table.en_double_validator(AnchorPointsModel.PosACol,
                                       AnchorPointsModel.PosFCol,
                                       ValidationValues.WingChordMin_perc,
                                       ValidationValues.WingChordMax_perc,
                                       3)

        self.table.set_help_bar(self.helpBar)
        self.table.set_help_text(AnchorPointsModel.RibNumCol,
                                 _('AnchPoints-RibNumDesc'))
        self.table.set_help_text(AnchorPointsModel.NumAnchCol,
                                 _('AnchPoints-NumAnchorsDesc'))
        self.table.set_help_text(AnchorPointsModel.PosACol,
                                 _('AnchPoints-PosADesc'))
        self.table.set_help_text(AnchorPointsModel.PosBCol,
                                 _('AnchPoints-PosBDesc'))
        self.table.set_help_text(AnchorPointsModel.PosCCol,
                                 _('AnchPoints-PosCDesc'))
        self.table.set_help_text(AnchorPointsModel.PosDCol,
                                 _('AnchPoints-PosDDesc'))
        self.table.set_help_text(AnchorPointsModel.PosECol,
                                 _('AnchPoints-PosEDesc'))
        self.table.set_help_text(AnchorPointsModel.PosFCol,
                                 _('AnchPoints-PosFDesc'))

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
        self.btnBar.set_help_page('proc/anchorPoints.html')

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
        self.anchPoints_M.sort_table(AnchorPointsModel.RibNumCol,
                                     Qt.SortOrder.AscendingOrder)

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
