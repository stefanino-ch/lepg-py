"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QGridLayout, QLabel, QWidget

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class SeewingAllowances(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Seewing allowances data
    """

    __className = 'SeewingAllowances'
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
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.sewAll_M = ProcModel.SewingAllowancesModel()
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
                    edit_grid_l
                         upperP_T
                         lower_p_t
                         ribs_t
                         vRibsT
                ---------------------------
                            help_bar | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(450, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Sewing allowances"))

        edit_grid_l = QGridLayout()

        # upper panel
        upper_p_l = QLabel(_('Upper panel'))
        upper_p_l.setAlignment(Qt.AlignRight)

        upper_p_t = TableView()
        upper_p_t.setModel(self.sewAll_M)
        upper_p_t.hideRow(1)
        upper_p_t.hideRow(2)
        upper_p_t.hideRow(3)
        # hide the ID column which is always at the end of the model
        upper_p_t.hideColumn(self.sewAll_M.columnCount() - 1)
        upper_p_t.verticalHeader().setVisible(False)
        upper_p_t.setHelpBar(self.helpBar)

        # TODO: Hilfetexte englisch fehlen
        # TODO: deutsche Spaltentitel
        # TODO: resizing komisch
        upper_p_t.setHelpText(ProcModel.SewingAllowancesModel.EdgeSeamCol,
                              _('SewingAllowances-EdgeSeamDesc'))
        upper_p_t.setHelpText(ProcModel.SewingAllowancesModel.LeSeemCol,
                              _('SewingAllowances-LeSeamDesc'))
        upper_p_t.setHelpText(ProcModel.SewingAllowancesModel.TeSeemCol,
                              _('SewingAllowances-TeSeamDesc'))

        upper_p_t.enableIntValidator(
            ProcModel.SewingAllowancesModel.EdgeSeamCol,
            ProcModel.SewingAllowancesModel.TeSeemCol,
            1, 100)
        upper_p_t.setFixedHeight(2
                                 + upper_p_t.horizontalHeader().height()
                                 + upper_p_t.rowHeight(0))
        upper_p_t.setFixedWidth(2
                                + upper_p_t.columnWidth(0)
                                + upper_p_t.columnWidth(1)
                                + upper_p_t.columnWidth(2))

        edit_grid_l.addWidget(upper_p_l, 0, 0)
        edit_grid_l.addWidget(upper_p_t, 0, 1)
        edit_grid_l.addWidget(QWidget(), 0, 3)

        # lower panel
        lower_p_l = QLabel(_('Lower panel'))
        lower_p_l.setAlignment(Qt.AlignRight)

        lower_p_t = TableView()
        lower_p_t.setModel(self.sewAll_M)
        lower_p_t.hideRow(0)
        lower_p_t.hideRow(2)
        lower_p_t.hideRow(3)
        # hide the ID column which is always at the end of the model
        lower_p_t.hideColumn(self.sewAll_M.columnCount() - 1)
        lower_p_t.verticalHeader().setVisible(False)
        lower_p_t.setHelpBar(self.helpBar)

        lower_p_t.setHelpText(ProcModel.SewingAllowancesModel.EdgeSeamCol,
                              _('SewingAllowances-EdgeSeamDesc'))
        lower_p_t.setHelpText(ProcModel.SewingAllowancesModel.LeSeemCol,
                              _('SewingAllowances-LeSeamDesc'))
        lower_p_t.setHelpText(ProcModel.SewingAllowancesModel.TeSeemCol,
                              _('SewingAllowances-TeSeamDesc'))

        lower_p_t.enableIntValidator(
            ProcModel.SewingAllowancesModel.EdgeSeamCol,
            ProcModel.SewingAllowancesModel.TeSeemCol,
            1, 100)
        lower_p_t.setFixedHeight(2
                                 + upper_p_t.horizontalHeader().height()
                                 + upper_p_t.rowHeight(0))
        lower_p_t.setFixedWidth(2
                                + upper_p_t.columnWidth(0)
                                + upper_p_t.columnWidth(1)
                                + upper_p_t.columnWidth(2))

        edit_grid_l.addWidget(lower_p_l, 1, 0)
        edit_grid_l.addWidget(lower_p_t, 1, 1)
        edit_grid_l.addWidget(QWidget(), 1, 3)

        # ribs panel
        ribs_l = QLabel(_('Ribs'))
        ribs_l.setAlignment(Qt.AlignRight)

        ribs_t = TableView()
        ribs_t.setModel(self.sewAll_M)
        ribs_t.hideRow(0)
        ribs_t.hideRow(1)
        ribs_t.hideRow(3)
        ribs_t.hideColumn(1)
        ribs_t.hideColumn(2)
        # hide the ID column which is always at the end of the model
        ribs_t.hideColumn(self.sewAll_M.columnCount() - 1)
        ribs_t.verticalHeader().setVisible(False)
        ribs_t.setHelpBar(self.helpBar)

        ribs_t.setHelpText(ProcModel.SewingAllowancesModel.EdgeSeamCol,
                           _('SewingAllowances-RibsSeemDesc'))

        ribs_t.enableIntValidator(ProcModel.SewingAllowancesModel.EdgeSeamCol,
                                  ProcModel.SewingAllowancesModel.EdgeSeamCol,
                                  1, 100)
        ribs_t.setFixedHeight(2
                              + upper_p_t.horizontalHeader().height()
                              + upper_p_t.rowHeight(0))
        ribs_t.setFixedWidth(2 + upper_p_t.columnWidth(0))

        edit_grid_l.addWidget(ribs_l, 2, 0)
        edit_grid_l.addWidget(ribs_t, 2, 1)
        edit_grid_l.addWidget(QWidget(), 2, 3)

        # ribs panel
        v_ribs_l = QLabel(_('V-Ribs'))
        v_ribs_l.setAlignment(Qt.AlignRight)

        v_ribs_t = TableView()
        v_ribs_t.setModel(self.sewAll_M)
        v_ribs_t.hideRow(0)
        v_ribs_t.hideRow(1)
        v_ribs_t.hideRow(2)
        v_ribs_t.hideColumn(1)
        v_ribs_t.hideColumn(2)
        # hide the ID column which is always at the end of the model
        v_ribs_t.hideColumn(self.sewAll_M.columnCount() - 1)
        v_ribs_t.verticalHeader().setVisible(False)
        v_ribs_t.setHelpBar(self.helpBar)

        v_ribs_t.setHelpText(ProcModel.SewingAllowancesModel.EdgeSeamCol,
                             _('SewingAllowances-V-RibsSeemDesc'))

        v_ribs_t.enableIntValidator(
            ProcModel.SewingAllowancesModel.EdgeSeamCol,
            ProcModel.SewingAllowancesModel.EdgeSeamCol,
            1, 100)
        v_ribs_t.setFixedHeight(2
                                + upper_p_t.horizontalHeader().height()
                                + upper_p_t.rowHeight(0))
        v_ribs_t.setFixedWidth(2 + upper_p_t.columnWidth(0))

        edit_grid_l.addWidget(v_ribs_l, 3, 0)
        edit_grid_l.addWidget(v_ribs_t, 3, 1)
        edit_grid_l.addWidget(QWidget(), 3, 3)

        self.window_ly.addLayout(edit_grid_l)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/seewingAllowances.html')

        bottom_ly = QHBoxLayout()
        bottom_ly.addStretch()
        bottom_ly.addWidget(self.helpBar)
        bottom_ly.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_ly)

        self.win.setLayout(self.window_ly)

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
