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


class TwoDDxfModel(QMdiSubWindow):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'TwoDDxfModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.btnBar = None
        self.usage_cb = None
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.pm = ProcModel()

        self.twoDDxf_M = ProcModel.TwoDDxfModel()
        self.twoDDxf_M.usageUpd.connect(self.usage_update)
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

        Naming:
            Conf is always one as there is only one configuration possible
        """
        logging.debug(self.__className + '.build_window')

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

        one_t = TableView()
        one_t.setModel(self.twoDDxf_M)
        one_t.verticalHeader().setVisible(False)
        one_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        one_t.hideColumn(self.twoDDxf_M.columnCount() - 1)
        one_t.hideColumn(self.twoDDxf_M.columnCount() - 2)
        one_t.hideColumn(0)
        one_t.setFixedHeight(2
                             + one_t.horizontalHeader().height()
                             + 6 * one_t.rowHeight(0))
        self.window_ly.addWidget(one_t)

        one_t.enableRegExpValidator(ProcModel.TwoDDxfModel.LineNameCol,
                                    ProcModel.TwoDDxfModel.LineNameCol,
                                    "^[a-zA-Z0-9_.-]*$")
        one_t.enableIntValidator(ProcModel.TwoDDxfModel.ColorCodeCol,
                                 ProcModel.TwoDDxfModel.ColorCodeCol,
                                 0, 255)
        one_t.enableRegExpValidator(ProcModel.TwoDDxfModel.LineNameCol,
                                    ProcModel.TwoDDxfModel.LineNameCol,
                                    "^[a-zA-Z0-9_.-]*$")

        one_t.setHelpBar(self.helpBar)
        one_t.setHelpText(ProcModel.TwoDDxfModel.LineNameCol,
                          _('TwoDDxf-LineNameDesc'))
        one_t.setHelpText(ProcModel.TwoDDxfModel.ColorCodeCol,
                          _('TwoDDxf-ColorCodeDesc'))
        one_t.setHelpText(ProcModel.TwoDDxfModel.ColorNameCol,
                          _('TwoDDxf-ColorNameDesc'))

        self.usage_update()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/twoDDxf.html')

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

        if self.twoDDxf_M.isUsed():
            self.usage_cb.setCurrentIndex(1)
        else:
            self.usage_cb.setCurrentIndex(0)

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        logging.debug(self.__className + '.usage_cb_change')
        if self.usage_cb.currentIndex() == 0:
            self.twoDDxf_M.setIsUsed(False)
        else:
            self.twoDDxf_M.setIsUsed(True)
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
