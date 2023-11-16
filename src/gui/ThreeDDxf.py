"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel

from data.ProcModel import ProcModel
from data.procModel.ThreeDDxfModel import ThreeDDxfModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import Regex, ValidationValues


class ThreeDDxf(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'ThreeDDxfModel'
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

        self.threeDDxf_M = ThreeDDxfModel()
        self.threeDDxf_M.usageUpd.connect(self.usage_update)
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
        self.setWindowTitle(_("3D DXF Options"))

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
        self.one_t.setModel(self.threeDDxf_M)
        self.one_t.verticalHeader().setVisible(False)
        self.one_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.one_t.hideColumn(self.threeDDxf_M.columnCount() - 1)
        self.one_t.hideColumn(self.threeDDxf_M.columnCount() - 2)
        self.one_t.hideColumn(2)
        self.one_t.hideColumn(0)
        for cell in range(6, 9):
            self.one_t.hideRow(cell)
        self.one_t.setFixedHeight(2
                                 + self.one_t.horizontalHeader().height()
                                 + 6 * self.one_t.rowHeight(0))
        self.window_ly.addWidget(self.one_t)

        self.one_t.en_reg_exp_validator(ThreeDDxfModel.LineNameCol,
                                       ThreeDDxfModel.LineNameCol,
                                       Regex.ThreeDDxfLayerNames)

        self.one_t.en_int_validator(ThreeDDxfModel.ColorCodeCol,
                                   ThreeDDxfModel.ColorCodeCol,
                                   ValidationValues.Proc.MinThreeDDxfColorNum,
                                   ValidationValues.Proc.MaxThreeDDxfColorNum)

        self.one_t.en_reg_exp_validator(ThreeDDxfModel.ColorNameCol,
                                       ThreeDDxfModel.ColorNameCol,
                                       Regex.ThreeDDxfColorDesc)

        self.one_t.set_help_bar(self.helpBar)
        self.one_t.set_help_text(ThreeDDxfModel.LineNameCol,
                                _('ThreeDDxf-LineNameDesc'))
        self.one_t.set_help_text(ThreeDDxfModel.ColorCodeCol,
                                _('ThreeDDxf-ColorCodeDesc'))
        self.one_t.set_help_text(ThreeDDxfModel.ColorNameCol,
                                _('ThreeDDxf-ColorNameDesc'))

        self.two_t = TableView()
        self.two_t.setModel(self.threeDDxf_M)
        self.two_t.verticalHeader().setVisible(False)
        self.two_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.two_t.hideColumn(self.threeDDxf_M.columnCount() - 1)
        self.two_t.hideColumn(self.threeDDxf_M.columnCount() - 2)
        self.two_t.hideColumn(0)
        for cell in range(0, 6):
            self.two_t.hideRow(cell)
        self.two_t.setFixedHeight(2
                                 + self.two_t.horizontalHeader().height()
                                 + 3 * self.two_t.rowHeight(6))
        self.window_ly.addWidget(self.two_t)

        self.two_t.en_reg_exp_validator(ThreeDDxfModel.LineNameCol,
                                       ThreeDDxfModel.LineNameCol,
                                       Regex.ThreeDDxfLayerNamesPlus)

        self.two_t.en_int_validator(ThreeDDxfModel.UnifilarCol,
                                   ThreeDDxfModel.UnifilarCol,
                                   0, 1)

        self.two_t.en_int_validator(ThreeDDxfModel.ColorCodeCol,
                                   ThreeDDxfModel.ColorCodeCol,
                                   ValidationValues.Proc.MinThreeDDxfColorNum,
                                   ValidationValues.Proc.MaxThreeDDxfColorNum)

        self.two_t.en_reg_exp_validator(ThreeDDxfModel.ColorNameCol,
                                       ThreeDDxfModel.ColorNameCol,
                                       Regex.ThreeDDxfColorDesc)

        self.two_t.set_help_bar(self.helpBar)
        self.two_t.set_help_text(ThreeDDxfModel.LineNameCol,
                                _('ThreeDDxf-LineNameDesc'))
        self.two_t.set_help_text(ThreeDDxfModel.UnifilarCol,
                                _('ThreeDDxf-UnifilarDesc'))
        self.two_t.set_help_text(ThreeDDxfModel.ColorCodeCol,
                                _('ThreeDDxf-ColorCodeDesc'))
        self.two_t.set_help_text(ThreeDDxfModel.ColorNameCol,
                                _('ThreeDDxf-ColorNameDesc'))

        self.usage_update()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/threeDDxf.html')

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
        if self.threeDDxf_M.is_used():
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
            self.threeDDxf_M.set_is_used(False)
        else:
            self.threeDDxf_M.set_is_used(True)
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
