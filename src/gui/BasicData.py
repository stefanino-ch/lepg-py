"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QVBoxLayout, \
                            QHeaderView, QHBoxLayout

from gui.GlobalDefinition import Regex, ValidationValues
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from data.procModel.WingModel import WingModel


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
        :method: Class initialization
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

        self.wing_M = WingModel()
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

        for i in range(WingModel.WingNameCol,
                       self.wing_M.columnCount()):
            brand_name_t.hideColumn(i)
        brand_name_t.verticalHeader().setVisible(False)
        brand_name_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        brand_name_t.setFixedHeight(2
                                    + brand_name_t.horizontalHeader().height()
                                    + brand_name_t.rowHeight(0))

        brand_name_t.set_help_bar(self.helpBar)
        brand_name_t.set_help_text(WingModel.BrandNameCol,
                                   _('Proc-BrandNameDesc'))

        brand_name_t.en_reg_exp_validator(WingModel.BrandNameCol,
                                          WingModel.BrandNameCol,
                                          Regex.BrandNameString)

        self.window_ly.addWidget(brand_name_t)

        # Wing name
        wing_name_t = TableView()
        wing_name_t.setModel(self.wing_M)

        wing_name_t.hideColumn(0)
        for i in range(WingModel.DrawScaleCol,
                       self.wing_M.columnCount()):
            wing_name_t.hideColumn(i)
        wing_name_t.verticalHeader().setVisible(False)
        wing_name_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        wing_name_t.setFixedHeight(2
                                   + wing_name_t.horizontalHeader().height()
                                   + wing_name_t.rowHeight(0))

        wing_name_t.set_help_bar(self.helpBar)
        wing_name_t.set_help_text(WingModel.WingNameCol,
                                  _('Proc-WingNameDesc'))

        wing_name_t.en_reg_exp_validator(WingModel.WingNameCol,
                                         WingModel.WingNameCol,
                                         Regex.WingNameString)

        self.window_ly.addWidget(wing_name_t)

        # Scales
        scales_t = TableView()
        scales_t.setModel(self.wing_M)

        for i in range(WingModel.BrandNameCol,
                       WingModel.WingNameCol + 1):
            scales_t.hideColumn(i)
        for i in range(WingModel.NumCellsCol,
                       self.wing_M.columnCount()):
            scales_t.hideColumn(i)
        scales_t.verticalHeader().setVisible(False)
        scales_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        scales_t.setFixedHeight(2 + scales_t.horizontalHeader().height()
                                + scales_t.rowHeight(0))

        scales_t.set_help_bar(self.helpBar)
        scales_t.set_help_text(WingModel.DrawScaleCol,
                               _('Proc-DrawScaleDesc'))
        scales_t.set_help_text(WingModel.WingScaleCol,
                               _('Proc-WingScaleDesc'))

        scales_t.en_double_validator(WingModel.DrawScaleCol,
                                     WingModel.WingScaleCol,
                                     ValidationValues.Proc.ScaleMin,
                                     ValidationValues.Proc.ScaleMax,
                                     10)

        self.window_ly.addWidget(scales_t)

        # numbers
        self.numbers_t = TableView()
        self.numbers_t.setModel(self.wing_M)

        for i in range(WingModel.BrandNameCol,
                       WingModel.WingScaleCol + 1):
            self.numbers_t.hideColumn(i)
        for i in range(WingModel.AlphaMaxTipCol,
                       self.wing_M.columnCount()):
            self.numbers_t.hideColumn(i)
        self.numbers_t.verticalHeader().setVisible(False)
        self.numbers_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.numbers_t.setFixedHeight(
            2
            + self.numbers_t.horizontalHeader().height()
            + self.numbers_t.rowHeight(0))

        self.numbers_t.en_int_validator(WingModel.NumCellsCol,
                                        WingModel.NumRibsCol,
                                        1, ValidationValues.MaxNumCells)

        self.numbers_t.set_help_bar(self.helpBar)
        self.numbers_t.set_help_text(WingModel.NumCellsCol,
                                     _('Proc-NumCellsDesc'))
        self.numbers_t.set_help_text(WingModel.NumRibsCol,
                                     _('Proc-NumRibsDesc'))

        self.window_ly.addWidget(self.numbers_t)

        # alpha max and param
        self.alpha_t = TableView()
        self.alpha_t.setModel(self.wing_M)

        for i in range(WingModel.BrandNameCol,
                       WingModel.NumRibsCol + 1):
            self.alpha_t.hideColumn(i)
        for i in range(WingModel.ParaTypeCol,
                       self.wing_M.columnCount()):
            self.alpha_t.hideColumn(i)
        self.alpha_t.verticalHeader().setVisible(False)
        self.alpha_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.alpha_t.setFixedHeight(2
                                    + self.alpha_t.horizontalHeader().height()
                                    + self.alpha_t.rowHeight(0))

        self.alpha_t.set_help_bar(self.helpBar)
        self.alpha_t.set_help_text(WingModel.AlphaModeCol,
                                   _('Proc-AlphaModeDesc'))
        self.alpha_t.set_help_text(WingModel.AlphaMaxCentCol,
                                   _('Proc-AlphaMaxCentDesc'))
        self.alpha_t.set_help_text(WingModel.AlphaMaxTipCol,
                                   _('Proc-AlphaMaxTipDesc'))

        self.alpha_t.en_double_validator(WingModel.AlphaMaxTipCol,
                                         WingModel.AlphaMaxTipCol,
                                         ValidationValues.Proc.AlphaMaxTipMin,
                                         ValidationValues.Proc.AlphaMaxTipMax,
                                         1)
        self.alpha_t.en_int_validator(WingModel.AlphaModeCol,
                                      WingModel.ParaParamCol,
                                      0, 2)
        self.alpha_t.en_double_validator(WingModel.AlphaMaxCentCol,
                                         WingModel.AlphaMaxCentCol,
                                         ValidationValues.Proc.AlphaMaxCentMin,
                                         ValidationValues.Proc.AlphaMaxCentMax,
                                         1)

        self.window_ly.addWidget(self.alpha_t)

        # para type and param
        self.type_t = TableView()
        self.type_t.setModel(self.wing_M)

        for i in range(WingModel.BrandNameCol,
                       WingModel.AlphaMaxCentCol + 1):
            self.type_t.hideColumn(i)
        for i in range(WingModel.LinesConcTypeCol,
                       self.wing_M.columnCount()):
            self.type_t.hideColumn(i)
        self.type_t.verticalHeader().setVisible(False)
        self.type_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.type_t.setFixedHeight(2
                                   + self.type_t.horizontalHeader().height()
                                   + self.type_t.rowHeight(0))

        self.type_t.set_help_bar(self.helpBar)
        self.type_t.set_help_text(WingModel.ParaTypeCol,
                                  _('Proc-ParaTypeDesc'))
        self.type_t.set_help_text(WingModel.ParaParamCol,
                                  _('Proc-ParaParamDesc'))

        self.type_t.en_reg_exp_validator(WingModel.ParaTypeCol,
                                         WingModel.ParaTypeCol,
                                         Regex.ParaTyp)
        self.type_t.en_int_validator(WingModel.ParaParamCol,
                                     WingModel.ParaParamCol,
                                     0, 1)

        self.window_ly.addWidget(self.type_t)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/basicData.html')

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
