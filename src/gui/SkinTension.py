"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, \
    QSizePolicy, QHeaderView

from data.procModel.SkinTensionModel import SkinTensionModel
from data.procModel.SkinTensionParamsModel import SkinTensionParamsModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class SkinTension(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Skin tension data
    """

    __className = 'SkinTension'
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

        self.skinTens_M = SkinTensionModel()
        self.skinTensParams_M = SkinTensionParamsModel()
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
                     params_table
                    ---------------------------
                                help_bar | btn_bar
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Skin tension"))

        table = TableView()
        table.setModel(self.skinTens_M)
        # hide the ID column which is always at the end of the model
        table.hideColumn(self.skinTens_M.columnCount() - 1)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table.en_double_validator(SkinTensionModel.TopDistLECol,
                                  SkinTensionModel.BottWideCol,
                                  ValidationValues.WingChordMin_perc,
                                  ValidationValues.WingChordMax_perc,
                                  3)

        table.set_help_bar(self.helpBar)

        table.set_help_text(SkinTensionModel.TopDistLECol,
                            _('SkinTension-TopDistLEDesc'))
        table.set_help_text(SkinTensionModel.TopWideCol,
                            _('SkinTension-TopOverWideDesc'))
        table.set_help_text(SkinTensionModel.BottDistTECol,
                            _('SkinTension-BottDistTEDesc'))
        table.set_help_text(SkinTensionModel.BottWideCol,
                            _('SkinTension-BottOverWideDesc'))

        table.setFixedHeight(2
                             + table.horizontalHeader().height()
                             + 6 * table.rowHeight(0))
        self.window_ly.addWidget(table)

        params_table = TableView()
        params_table.setModel(self.skinTensParams_M)
        # hide the ID column which is always at the end of the model
        params_table.hideColumn(self.skinTensParams_M.columnCount() - 1)
        params_table.verticalHeader().setVisible(False)
        params_table.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        params_table.en_double_validator(
            SkinTensionParamsModel.StrainMiniRibsCol,
            SkinTensionParamsModel.StrainMiniRibsCol,
            ValidationValues.Proc.StrainMiniRibsMin,
            ValidationValues.Proc.StrainMiniRibsMax,
            5)

        params_table.en_int_validator(
            SkinTensionParamsModel.NumPointsCol,
            SkinTensionParamsModel.NumPointsCol,
            ValidationValues.Proc.NumPointsMin,
            ValidationValues.Proc.NumPointsMax)

        params_table.en_double_validator(
            SkinTensionParamsModel.CoeffCol,
            SkinTensionParamsModel.CoeffCol,
            ValidationValues.Proc.SkinTensionCoefMin,
            ValidationValues.Proc.SkinTensionCoefMax,
            1)

        params_table.set_help_bar(self.helpBar)

        params_table.set_help_text(
            SkinTensionParamsModel.StrainMiniRibsCol,
            _('SkinTension-StrainMiniRibsDesc'))
        params_table.set_help_text(
            SkinTensionParamsModel.NumPointsCol,
            _('SkinTension-NumPointsDesc'))
        params_table.set_help_text(
            SkinTensionParamsModel.CoeffCol,
            _('SkinTension-CoeffDesc'))

        params_layout = QHBoxLayout()
        params_layout.addWidget(params_table)
        params_layout.addStretch()
        params_table.setFixedWidth(2
                                   + 3 * params_table.columnWidth(0)
                                   + 2 * params_table.columnWidth(1)
                                   + 2 * params_table.columnWidth(2))
        params_table.setFixedHeight(2
                                    + params_table.horizontalHeader().height()
                                    + params_table.rowHeight(0))
        self.window_ly.addLayout(params_layout)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/skinTension.html')

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
