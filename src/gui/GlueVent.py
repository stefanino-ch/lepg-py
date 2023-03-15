"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
                            QHBoxLayout, QVBoxLayout, QComboBox, QLabel
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar

from data.ProcModel import ProcModel
from data.procModel.GlueVentModel import GlueVentModel

from Singleton.Singleton import Singleton

from gui.GlobalDefinition import ValidationValues


class GlueVent(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Glue vent data
    """

    __className = 'GlueVent'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        self.btn_bar = None
        self.usage_cb = None
        self.help_bar = None
        self.window_ly = None
        self.win = None

        super().__init__()

        self.pm = ProcModel()

        self.glueVent_M = GlueVentModel()
        self.glueVent_M.usageUpd.connect(self.usage_update)
        self.build_window()

    def closeEvent(self, event):  # @UnusedVariable
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

        self.help_bar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Glue vent"))

        usage_l = QLabel(_('Type'))
        self.usage_cb = QComboBox()
        self.usage_cb.addItem(_("Defaults"))
        self.usage_cb.addItem(_("User defined"))
        self.usage_cb.currentIndexChanged.connect(self.usage_cb_change)
        usage_lo = QHBoxLayout()
        usage_lo.addWidget(usage_l)
        usage_lo.addWidget(self.usage_cb)
        usage_lo.addStretch()

        self.window_ly.addLayout(usage_lo)

        one_t = TableView()
        one_t.setModel(self.glueVent_M)
        one_t.verticalHeader().setVisible(False)
        one_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        one_t.hideColumn(self.glueVent_M.columnCount() - 1)
        one_t.hideColumn(self.glueVent_M.columnCount() - 2)
        self.window_ly.addWidget(one_t)

        one_t.en_int_validator(
            GlueVentModel.OrderNumCol,
            GlueVentModel.OrderNumCol,
            1,
            ValidationValues.MaxNumRibs,
            GlueVentModel.paramLength)

        one_t.en_double_validator(
            GlueVentModel.TypeCol,
            GlueVentModel.TypeCol,
            ValidationValues.Proc.MinGlueVentParamNum,
            ValidationValues.Proc.MaxGlueVentParamNum,
            0,
            GlueVentModel.paramLength)

        one_t.en_double_validator(
            GlueVentModel.ParamACol,
            GlueVentModel.ParamCCol,
            0,
            100,
            2,
            GlueVentModel.paramLength)

        one_t.set_help_bar(self.help_bar)
        one_t.set_help_text(
            GlueVentModel.OrderNumCol,
            _('GlueVent-AirfoilNumDesc'))
        one_t.set_help_text(
            GlueVentModel.TypeCol,
            _('GlueVent-VentParamDesc'))
        one_t.set_help_text(
            GlueVentModel.ParamACol,
            _('GlueVent-ParamADesc'))
        one_t.set_help_text(
            GlueVentModel.ParamBCol,
            _('GlueVent-ParamBDesc'))
        one_t.set_help_text(
            GlueVentModel.ParamCCol,
            _('GlueVent-ParamCDesc'))

        self.usage_update()

        #############################
        # Commons for all windows
        self.btn_bar = WindowBtnBar(0b0101)
        self.btn_bar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Fixed))
        self.btn_bar.my_signal.connect(self.btn_press)
        self.btn_bar.set_help_page('proc/glueVent.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_bar)
        bottom_layout.addWidget(self.btn_bar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def usage_update(self):
        """
        :method: Updates the GUI as soon in the model the usage
                 flag has been changed
        """
        if self.glueVent_M.is_used():
            self.usage_cb.setCurrentIndex(1)
        else:
            self.usage_cb.setCurrentIndex(0)

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        if self.usage_cb.currentIndex() == 0:
            self.glueVent_M.set_is_used(False)
        else:
            self.glueVent_M.set_is_used(True)
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
            logging.error(self.__className + '.btn_press unrecognized button press ' + q)
