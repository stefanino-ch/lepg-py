"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QVBoxLayout, \
    QHeaderView, QHBoxLayout

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class BasicData(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit the Basic Data
    """

    __className = 'ProcBasicData'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.win = None
        self.window_ly = None
        self.helpBar = None
        self.numbers_t = None
        self.alpha_t = None
        self.type_t = None
        self.btnBar = None

        self.wing_M = ProcModel.WingModel()
        self.wing_M.dataChanged.connect(self.check_num_cells_ribs)

        self.build_window()

    def closeEvent(self, event):  # @UnusedVariable
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
                     Tables
                    -------------------------
                                | help_bar
                                | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(400, 300)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Basic Data"))

        # Brand name
        brand_name_t = TableView()
        brand_name_t.setModel(self.wing_M)

        for i in range(ProcModel.WingModel.WingNameCol,
                       self.wing_M.columnCount()):
            brand_name_t.hideColumn(i)
        brand_name_t.verticalHeader().setVisible(False)
        brand_name_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)
        brand_name_t.setFixedHeight(2
                                    + brand_name_t.horizontalHeader().height()
                                    + brand_name_t.rowHeight(0))

        brand_name_t.setHelpBar(self.helpBar)
        brand_name_t.setHelpText(ProcModel.WingModel.BrandNameCol,
                                 _('Proc-BrandNameDesc'))

        brand_name_t.enableRegExpValidator(ProcModel.WingModel.BrandNameCol,
                                           ProcModel.WingModel.BrandNameCol,
                                           "(.|\s)*\S(.|\s)*")

        self.window_ly.addWidget(brand_name_t)

        # Wing name
        wing_name_t = TableView()
        wing_name_t.setModel(self.wing_M)

        wing_name_t.hideColumn(0)
        for i in range(ProcModel.WingModel.DrawScaleCol,
                       self.wing_M.columnCount()):
            wing_name_t.hideColumn(i)
        wing_name_t.verticalHeader().setVisible(False)
        wing_name_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)
        wing_name_t.setFixedHeight(2
                                   + wing_name_t.horizontalHeader().height()
                                   + wing_name_t.rowHeight(0))

        wing_name_t.setHelpBar(self.helpBar)
        wing_name_t.setHelpText(ProcModel.WingModel.WingNameCol,
                                _('Proc-WingNameDesc'))

        wing_name_t.enableRegExpValidator(ProcModel.WingModel.WingNameCol,
                                          ProcModel.WingModel.WingNameCol,
                                          "(.|\s)*\S(.|\s)*")

        self.window_ly.addWidget(wing_name_t)

        # Scales
        scales_t = TableView()
        scales_t.setModel(self.wing_M)

        for i in range(ProcModel.WingModel.BrandNameCol,
                       ProcModel.WingModel.WingNameCol + 1):
            scales_t.hideColumn(i)
        for i in range(ProcModel.WingModel.NumCellsCol,
                       self.wing_M.columnCount()):
            scales_t.hideColumn(i)
        scales_t.verticalHeader().setVisible(False)
        scales_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        scales_t.setFixedHeight(2 + scales_t.horizontalHeader().height()
                                + scales_t.rowHeight(0))

        scales_t.setHelpBar(self.helpBar)
        scales_t.setHelpText(ProcModel.WingModel.DrawScaleCol,
                             _('Proc-DrawScaleDesc'))
        scales_t.setHelpText(ProcModel.WingModel.WingScaleCol,
                             _('Proc-WingScaleDesc'))

        scales_t.enableDoubleValidator(ProcModel.WingModel.DrawScaleCol,
                                       ProcModel.WingModel.WingScaleCol,
                                       0, 10, 2)

        self.window_ly.addWidget(scales_t)

        # numbers
        self.numbers_t = TableView()
        self.numbers_t.setModel(self.wing_M)

        for i in range(ProcModel.WingModel.BrandNameCol,
                       ProcModel.WingModel.WingScaleCol + 1):
            self.numbers_t.hideColumn(i)
        for i in range(ProcModel.WingModel.AlphaMaxTipCol,
                       self.wing_M.columnCount()):
            self.numbers_t.hideColumn(i)
        self.numbers_t.verticalHeader().setVisible(False)
        self.numbers_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)
        self.numbers_t.setFixedHeight(
            2
            + self.numbers_t.horizontalHeader().height()
            + self.numbers_t.rowHeight(0))

        self.numbers_t.setHelpBar(self.helpBar)
        self.numbers_t.setHelpText(ProcModel.WingModel.NumCellsCol,
                                   _('Proc-NumCellsDesc'))
        self.numbers_t.setHelpText(ProcModel.WingModel.NumRibsCol,
                                   _('Proc-NumRibsDesc'))

        self.numbers_t.enableIntValidator(ProcModel.WingModel.NumCellsCol,
                                          ProcModel.WingModel.NumRibsCol,
                                          1, 999)

        self.window_ly.addWidget(self.numbers_t)

        # alpha max and param
        self.alpha_t = TableView()
        self.alpha_t.setModel(self.wing_M)

        for i in range(ProcModel.WingModel.BrandNameCol,
                       ProcModel.WingModel.NumRibsCol + 1):
            self.alpha_t.hideColumn(i)
        for i in range(ProcModel.WingModel.ParaTypeCol,
                       self.wing_M.columnCount()):
            self.alpha_t.hideColumn(i)
        self.alpha_t.verticalHeader().setVisible(False)
        self.alpha_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)
        self.alpha_t.setFixedHeight(2
                                    + self.alpha_t.horizontalHeader().height()
                                    + self.alpha_t.rowHeight(0))

        self.alpha_t.setHelpBar(self.helpBar)
        self.alpha_t.setHelpText(ProcModel.WingModel.AlphaModeCol,
                                 _('Proc-AlphaModeDesc'))
        self.alpha_t.setHelpText(ProcModel.WingModel.AlphaMaxCentCol,
                                 _('Proc-AlphaMaxCentDesc'))
        self.alpha_t.setHelpText(ProcModel.WingModel.AlphaMaxTipCol,
                                 _('Proc-AlphaMaxTipDesc'))

        self.alpha_t.enableDoubleValidator(ProcModel.WingModel.AlphaMaxTipCol,
                                           ProcModel.WingModel.AlphaMaxTipCol,
                                           -10, -10, 1)
        self.alpha_t.enableIntValidator(ProcModel.WingModel.AlphaModeCol,
                                        ProcModel.WingModel.ParaParamCol,
                                        0, 2)
        self.alpha_t.enableDoubleValidator(ProcModel.WingModel.AlphaMaxCentCol,
                                           ProcModel.WingModel.AlphaMaxCentCol,
                                           -10, -10, 1)

        self.window_ly.addWidget(self.alpha_t)

        # para type and param
        self.type_t = TableView()
        self.type_t.setModel(self.wing_M)

        for i in range(ProcModel.WingModel.BrandNameCol,
                       ProcModel.WingModel.AlphaMaxCentCol + 1):
            self.type_t.hideColumn(i)
        for i in range(ProcModel.WingModel.LinesConcTypeCol,
                       self.wing_M.columnCount()):
            self.type_t.hideColumn(i)
        self.type_t.verticalHeader().setVisible(False)
        self.type_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.Stretch)
        self.type_t.setFixedHeight(2
                                   + self.type_t.horizontalHeader().height()
                                   + self.type_t.rowHeight(0))

        self.type_t.setHelpBar(self.helpBar)
        self.type_t.setHelpText(ProcModel.WingModel.ParaTypeCol,
                                _('Proc-ParaTypeDesc'))
        self.type_t.setHelpText(ProcModel.WingModel.ParaParamCol,
                                _('Proc-ParaParamDesc'))

        self.type_t.enableRegExpValidator(ProcModel.WingModel.ParaTypeCol,
                                          ProcModel.WingModel.ParaTypeCol,
                                          "(.|\s)*\S(.|\s)*")
        self.type_t.enableIntValidator(ProcModel.WingModel.ParaParamCol,
                                       ProcModel.WingModel.ParaParamCol,
                                       0, 1)

        self.window_ly.addWidget(self.type_t)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/basicData.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def check_num_cells_ribs(self, q):
        """
        :method: The difference between NumCells and NumRibs must be 1, if
                 this is not the case we have a nonsense setup
        """
        logging.debug(self.__className + '.check_num_cells_ribs')

        if q.column() == self.wing_M.NumRibsCol \
                or q.column() == self.wing_M.NumCellsCol:
            try:
                num_cells = int(self.wing_M.index(
                    0,
                    self.wing_M.NumCellsCol).data())
                num_ribs = int(self.wing_M.index(
                    0,
                    self.wing_M.NumRibsCol).data())
            except:
                return

            cells = isinstance(num_cells, int)
            ribs = isinstance(num_ribs, int)

            if cells and ribs:
                diff = abs(num_cells - num_ribs)
                if diff == 1:
                    self.numbers_t.setStyleSheet(self.styleSheet())
                else:
                    self.numbers_t.setStyleSheet("border: 1px solid red")

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
