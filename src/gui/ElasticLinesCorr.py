"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, \
                            QLabel, QDataWidgetMapper, QVBoxLayout, \
                            QHBoxLayout, QHeaderView

from Singleton.Singleton import Singleton
from data.ProcModel import ProcModel
from gui.elements.LineEdit import LineEdit
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar


class ElasticLinesCorr(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit the Basic Data
    """

    __className = 'ElasticLinesCorr'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.btnBar = None
        self.fiveLineE_E = None
        self.fiveLineD_E = None
        self.fiveLineC_E = None
        self.fiveLineB_E = None
        self.fiveLineA_E = None
        self.fourLineD_E = None
        self.fourLineC_E = None
        self.fourLineB_E = None
        self.fourLineA_E = None
        self.threeLineC_E = None
        self.threeLineB_E = None
        self.threeLineA_E = None
        self.twoLineB_E = None
        self.twoLineA_E = None
        self.load_E = None
        self.wrapper = None
        self.grid_ly = None
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.elLinesCorr_M = ProcModel.ElLinesCorrModel()
        self.elLinesDef_M = ProcModel.ElLinesDefModel()

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
                windowGrid
                     Labels    | Edit fields
                     ...       | ...
                    -------------------------
                                | help_bar
                                | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(300, 300)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here

        self.setWindowTitle(_("Elastic lines correction"))

        self.grid_ly = QGridLayout()
        __gridRow = 0

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.elLinesCorr_M)

        load_l = QLabel(_('In flight load [kg]'))
        load_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.load_E = LineEdit()
        self.wrapper.addMapping(self.load_E,
                                ProcModel.ElLinesCorrModel.LoadCol)
        self.load_E.enableDoubleValidator(0, 500, 2)
        self.load_E.setHelpText(_('ElLinesCorr-LoadDesc'))
        self.load_E.setHelpBar(self.helpBar)
        self.grid_ly.addWidget(load_l, __gridRow, 0)
        self.grid_ly.addWidget(self.load_E, __gridRow, 1)
        __gridRow += 1

        self.grid_ly.addWidget(QLabel(_('Load distr [%]')), __gridRow, 1)
        self.grid_ly.addWidget(QLabel(_('Load distr [%]')), __gridRow, 2)
        self.grid_ly.addWidget(QLabel(_('Load distr [%]')), __gridRow, 3)
        self.grid_ly.addWidget(QLabel(_('Load distr [%]')), __gridRow, 4)
        self.grid_ly.addWidget(QLabel(_('Load distr [%]')), __gridRow, 5)
        __gridRow += 1

        # Two Lines
        two_line_t_l = QLabel(_('Two Lines'))
        two_line_t_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.twoLineA_E = LineEdit()
        self.wrapper.addMapping(self.twoLineA_E,
                                ProcModel.ElLinesCorrModel.TwoLineDistACol)
        self.twoLineA_E.enableDoubleValidator(0, 100, 2)
        self.twoLineA_E.setHelpText(_('ElLinesCorr-TwoLineDistDesc'))
        self.twoLineA_E.setHelpBar(self.helpBar)

        self.twoLineB_E = LineEdit()
        self.wrapper.addMapping(self.twoLineB_E,
                                ProcModel.ElLinesCorrModel.TwoLineDistBCol)
        self.twoLineB_E.enableDoubleValidator(0, 100, 2)
        self.twoLineB_E.setHelpText(_('ElLinesCorr-TwoLineDistDesc'))
        self.twoLineB_E.setHelpBar(self.helpBar)

        self.grid_ly.addWidget(two_line_t_l, __gridRow, 0)
        self.grid_ly.addWidget(self.twoLineA_E, __gridRow, 1)
        self.grid_ly.addWidget(self.twoLineB_E, __gridRow, 2)
        __gridRow += 1

        # Three Lines
        three_line_t_l = QLabel(_('Three Lines'))
        three_line_t_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.threeLineA_E = LineEdit()
        self.wrapper.addMapping(self.threeLineA_E,
                                ProcModel.ElLinesCorrModel.ThreeLineDistACol)
        self.threeLineA_E.enableDoubleValidator(0, 100, 2)
        self.threeLineA_E.setHelpText(_('ElLinesCorr-ThreeLineDistDesc'))
        self.threeLineA_E.setHelpBar(self.helpBar)

        self.threeLineB_E = LineEdit()
        self.wrapper.addMapping(self.threeLineB_E,
                                ProcModel.ElLinesCorrModel.ThreeLineDistBCol)
        self.threeLineB_E.enableDoubleValidator(0, 100, 2)
        self.threeLineB_E.setHelpText(_('ElLinesCorr-ThreeLineDistDesc'))
        self.threeLineB_E.setHelpBar(self.helpBar)

        self.threeLineC_E = LineEdit()
        self.wrapper.addMapping(self.threeLineC_E,
                                ProcModel.ElLinesCorrModel.ThreeLineDistCCol)
        self.threeLineC_E.enableDoubleValidator(0, 100, 2)
        self.threeLineC_E.setHelpText(_('ElLinesCorr-ThreeLineDistDesc'))
        self.threeLineC_E.setHelpBar(self.helpBar)

        self.grid_ly.addWidget(three_line_t_l, __gridRow, 0)
        self.grid_ly.addWidget(self.threeLineA_E, __gridRow, 1)
        self.grid_ly.addWidget(self.threeLineB_E, __gridRow, 2)
        self.grid_ly.addWidget(self.threeLineC_E, __gridRow, 3)
        __gridRow += 1

        # Four Lines
        four_line_t_l = QLabel(_('Four Lines'))
        four_line_t_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fourLineA_E = LineEdit()
        self.wrapper.addMapping(self.fourLineA_E,
                                ProcModel.ElLinesCorrModel.FourLineDistACol)
        self.fourLineA_E.enableDoubleValidator(0, 100, 2)
        self.fourLineA_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineA_E.setHelpBar(self.helpBar)

        self.fourLineB_E = LineEdit()
        self.wrapper.addMapping(self.fourLineB_E,
                                ProcModel.ElLinesCorrModel.FourLineDistBCol)
        self.fourLineB_E.enableDoubleValidator(0, 100, 2)
        self.fourLineB_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineB_E.setHelpBar(self.helpBar)

        self.fourLineC_E = LineEdit()
        self.wrapper.addMapping(self.fourLineC_E,
                                ProcModel.ElLinesCorrModel.FourLineDistCCol)
        self.fourLineC_E.enableDoubleValidator(0, 100, 2)
        self.fourLineC_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineC_E.setHelpBar(self.helpBar)

        self.fourLineD_E = LineEdit()
        self.wrapper.addMapping(self.fourLineD_E,
                                ProcModel.ElLinesCorrModel.FourLineDistDCol)
        self.fourLineD_E.enableDoubleValidator(0, 100, 2)
        self.fourLineD_E.setHelpText(_('ElLinesCorr-FourLineDistDesc'))
        self.fourLineD_E.setHelpBar(self.helpBar)

        self.grid_ly.addWidget(four_line_t_l, __gridRow, 0)
        self.grid_ly.addWidget(self.fourLineA_E, __gridRow, 1)
        self.grid_ly.addWidget(self.fourLineB_E, __gridRow, 2)
        self.grid_ly.addWidget(self.fourLineC_E, __gridRow, 3)
        self.grid_ly.addWidget(self.fourLineD_E, __gridRow, 4)
        __gridRow += 1

        # Five Lines
        five_line_t_l = QLabel(_('Five Lines'))
        five_line_t_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fiveLineA_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineA_E,
                                ProcModel.ElLinesCorrModel.FiveLineDistACol)
        self.fiveLineA_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineA_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineA_E.setHelpBar(self.helpBar)

        self.fiveLineB_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineB_E,
                                ProcModel.ElLinesCorrModel.FiveLineDistBCol)
        self.fiveLineB_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineB_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineB_E.setHelpBar(self.helpBar)

        self.fiveLineC_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineC_E,
                                ProcModel.ElLinesCorrModel.FiveLineDistCCol)
        self.fiveLineC_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineC_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineC_E.setHelpBar(self.helpBar)

        self.fiveLineD_E = LineEdit()
        self.wrapper.addMapping(self.fiveLineD_E,
                                ProcModel.ElLinesCorrModel.FiveLineDistDCol)
        self.fiveLineD_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineD_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineD_E.setHelpBar(self.helpBar)

        self.fiveLineE_E = LineEdit()
        self.wrapper.addMapping(
            self.fiveLineE_E, ProcModel.ElLinesCorrModel.FiveLineDistECol)
        self.fiveLineD_E.enableDoubleValidator(0, 100, 2)
        self.fiveLineE_E.setHelpText(_('ElLinesCorr-FiveLineDistDesc'))
        self.fiveLineE_E.setHelpBar(self.helpBar)

        self.grid_ly.addWidget(five_line_t_l, __gridRow, 0)
        self.grid_ly.addWidget(self.fiveLineA_E, __gridRow, 1)
        self.grid_ly.addWidget(self.fiveLineB_E, __gridRow, 2)
        self.grid_ly.addWidget(self.fiveLineC_E, __gridRow, 3)
        self.grid_ly.addWidget(self.fiveLineD_E, __gridRow, 4)
        self.grid_ly.addWidget(self.fiveLineE_E, __gridRow, 5)
        __gridRow += 1

        self.window_ly.addLayout(self.grid_ly)

        def_t = TableView()
        def_t.setModel(self.elLinesDef_M)
        def_t.verticalHeader().setVisible(False)
        def_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        def_t.hideColumn(self.elLinesDef_M.columnCount() - 1)
        def_t.hideColumn(self.elLinesDef_M.columnCount() - 2)
        def_t.setFixedHeight(2
                             + def_t.horizontalHeader().height()
                             + 5 * def_t.rowHeight(0))
        self.window_ly.addWidget(def_t)

        def_t.en_int_validator(ProcModel.ElLinesDefModel.OrderNumCol,
                               ProcModel.ElLinesDefModel.OrderNumCol,
                               1, 5)
        def_t.en_double_validator(ProcModel.ElLinesDefModel.DefLowCol,
                                  ProcModel.ElLinesDefModel.DefHighCol,
                                  0, 10, 2)

        def_t.set_help_bar(self.helpBar)
        def_t.set_help_text(ProcModel.ElLinesDefModel.OrderNumCol,
                            _('ElLinesCorr-NumOfLinesDesc'))
        def_t.set_help_text(ProcModel.ElLinesDefModel.DefLowCol,
                            _('ElLinesCorr-LowColDesc'))
        def_t.set_help_text(ProcModel.ElLinesDefModel.DefMidCol,
                            _('ElLinesCorr-MidColDesc'))
        def_t.set_help_text(ProcModel.ElLinesDefModel.DefHighCol,
                            _('ElLinesCorr-HigColDesc'))

        self.wrapper.toFirst()
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/elasticLinesCorr.html')

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
