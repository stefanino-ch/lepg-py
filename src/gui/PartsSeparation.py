"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar


class PartsSeparation(QMdiSubWindow):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'PartsSeparation'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.btn_bar = None
        self.usage_cb = None
        self.help_bar = None
        self.window_ly = None
        self.win = None

        self.pm = ProcModel()

        self.parts_sep_m = ProcModel.PartsSeparationModel()
        self.parts_sep_m.usageUpd.connect(self.usage_update)
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
                    -------------------------
                        help_bar  | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(600, 200)

        self.window_ly = QVBoxLayout()

        self.help_bar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Parts separation"))

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

        one_t = TableView()
        one_t.setModel(self.parts_sep_m)
        one_t.verticalHeader().setVisible(False)
        one_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        one_t.hideColumn(0)
        for i in range(ProcModel.PartsSeparationModel.Param6_col,
                       ProcModel.PartsSeparationModel.Param10_col+1):
            one_t.hideColumn(i)
        one_t.hideColumn(self.parts_sep_m.columnCount() - 2)
        one_t.hideColumn(self.parts_sep_m.columnCount() - 1)

        one_t.setFixedHeight(2
                             + one_t.horizontalHeader().height()
                             + one_t.rowHeight(0))
        self.window_ly.addWidget(one_t)

        one_t.enableDoubleValidator(ProcModel.PartsSeparationModel.Panel_x_col,
                                    ProcModel.PartsSeparationModel.Rib_y_col,
                                    0, 10, 2)

        one_t.setHelpBar(self.help_bar)
        one_t.setHelpText(ProcModel.PartsSeparationModel.Panel_x_col,
                          _('PartsSep-Panel_x_Desc'))
        one_t.setHelpText(ProcModel.PartsSeparationModel.Panel_x_min_col,
                          _('PartsSep-Panel_x_min_Desc'))
        one_t.setHelpText(ProcModel.PartsSeparationModel.Panel_y_col,
                          _('PartsSep-Panel_y_Desc'))
        one_t.setHelpText(ProcModel.PartsSeparationModel.Rib_x_col,
                          _('PartsSep-Rib_x_Desc'))
        one_t.setHelpText(ProcModel.PartsSeparationModel.Rib_y_col,
                          _('PartsSep-Rib_y_Desc'))

        self.usage_update()

        #############################
        # Commons for all windows
        self.btn_bar = WindowBtnBar(0b0101)
        self.btn_bar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                               QSizePolicy.Fixed))
        self.btn_bar.my_signal.connect(self.btn_press)
        self.btn_bar.setHelpPage('proc/partsSeparation.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_bar)
        bottom_layout.addWidget(self.btn_bar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def usage_update(self):
        """
        :method: Updates the GUI as soon in the model the usage flag has
                 been changed
        """
        logging.debug(self.__className + '.usage_update')

        if self.parts_sep_m.is_used():
            self.usage_cb.setCurrentIndex(1)
        else:
            self.usage_cb.setCurrentIndex(0)

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        logging.debug(self.__className + '.usage_cb_change')
        if self.usage_cb.currentIndex() == 0:
            self.parts_sep_m.set_is_used(False)
        else:
            self.parts_sep_m.set_is_used(True)
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
