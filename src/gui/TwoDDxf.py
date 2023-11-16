"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel

from data.ProcModel import ProcModel
from data.procModel.TwoDDxfModel import TwoDDxfModel

from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import Regex, ValidationValues


class TwoDDxf(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'TwoDDxf'
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

        self.twoDDxf_M = TwoDDxfModel()
        self.twoDDxf_M.usageUpd.connect(self.usage_update)
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
        self.win.setMinimumSize(500, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("2D DXF Options"))

        usage_l = QLabel(_('Type'))
        self.usage_cb = QComboBox()
        self.usage_cb.addItem(_("Defaults"))
        self.usage_cb.addItem(_("User defined"))
        self.usage_cb.currentIndexChanged.connect(self.usage_cb_change)
        usage_ly = QHBoxLayout()
        usage_ly.addWidget(usage_l)
        usage_ly.addWidget(self.usage_cb)
        usage_ly.addStretch()

        self.window_ly.addLayout(usage_ly)

        self.one_t = TableView()
        self.one_t.setModel(self.twoDDxf_M)
        self.one_t.verticalHeader().setVisible(False)
        self.one_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.one_t.hideColumn(self.twoDDxf_M.columnCount() - 1)
        self.one_t.hideColumn(self.twoDDxf_M.columnCount() - 2)
        self.one_t.hideColumn(0)
        self.one_t.setFixedHeight(2
                                 + self.one_t.horizontalHeader().height()
                                 + 6 * self.one_t.rowHeight(0))
        self.window_ly.addWidget(self.one_t)

        self.one_t.en_reg_exp_validator(TwoDDxfModel.LineNameCol,
                                       TwoDDxfModel.LineNameCol,
                                       Regex.TwoDDxfLayerNames)
        self.one_t.en_int_validator(TwoDDxfModel.ColorCodeCol,
                                   TwoDDxfModel.ColorCodeCol,
                                   ValidationValues.Proc.MinTwoDDxfColorNum,
                                   ValidationValues.Proc.MaxTwoDDxfColorNum)
        self.one_t.en_reg_exp_validator(TwoDDxfModel.ColorNameCol,
                                       TwoDDxfModel.ColorNameCol,
                                       Regex.TwoDDxfColorDesc)

        self.one_t.set_help_bar(self.helpBar)
        self.one_t.set_help_text(TwoDDxfModel.LineNameCol,
                                _('TwoDDxf-LineNameDesc'))
        self.one_t.set_help_text(TwoDDxfModel.ColorCodeCol,
                                _('TwoDDxf-ColorCodeDesc'))
        self.one_t.set_help_text(TwoDDxfModel.ColorNameCol,
                                _('TwoDDxf-ColorNameDesc'))

        self.usage_update()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/twoDDxf.html')

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
        if self.twoDDxf_M.is_used():
            self.usage_cb.setCurrentIndex(1)
            self.one_t.setEnabled(True)
        else:
            self.usage_cb.setCurrentIndex(0)
            self.one_t.setEnabled(False)

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        if self.usage_cb.currentIndex() == 0:
            self.twoDDxf_M.set_is_used(False)
        else:
            self.twoDDxf_M.set_is_used(True)
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
