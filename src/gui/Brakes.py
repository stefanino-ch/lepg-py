"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
                            QSpinBox, QLabel, QHBoxLayout, QVBoxLayout, \
                            QPushButton, QDataWidgetMapper

from data.ProcModel import ProcModel
from gui.elements.LineEdit import LineEdit
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class Brakes(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'Brakes'
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
        self.proxyModel = None
        self.numLines_S = None
        self.wrapper = None
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.pm = ProcModel()

        self.wing_M = ProcModel.WingModel()

        self.brakes_M = ProcModel.BrakesModel()
        self.brakes_M.numRowsForConfigChanged.connect(self.model_size_changed)

        self.brakeL_M = ProcModel.BrakeLengthModel()

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
                        numLinesSpin
                        LinesTable
                    -------------------------
                        OrderBtn  help_bar  | btn_bar

        Naming:

            conf is always one as there is only one brake line configuration allowed
            details equals brake line paths
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1100, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Edit Brake lines"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.wing_M)

        length_l = QLabel(_('Brake length [cm]'))
        length_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        length_e = LineEdit()
        length_e.setFixedWidth(40)
        self.wrapper.addMapping(length_e, ProcModel.WingModel.BrakeLengthCol)
        length_e.enableIntValidator(0, 20000)
        length_e.setHelpText(_('Brakes-LineLengthDesc'))
        length_e.setHelpBar(self.helpBar)

        length_layout = QHBoxLayout()
        length_layout.addWidget(length_l)
        length_layout.addWidget(length_e)
        length_layout.addStretch()
        self.window_ly.addLayout(length_layout)

        self.wrapper.toFirst()

        ###############
        num_lines_l = QLabel(_('Number of Brake paths'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        self.numLines_S = QSpinBox()
        self.numLines_S.setRange(1, 999)
        self.numLines_S.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.numLines_S.valueChanged.connect(self.num_lines_change)
        num_lines_edit = self.numLines_S.lineEdit()
        num_lines_edit.setReadOnly(True)

        num_lines_layout = QHBoxLayout()
        num_lines_layout.addWidget(num_lines_l)
        num_lines_layout.addWidget(self.numLines_S)
        num_lines_layout.addStretch()
        self.window_ly.addLayout(num_lines_layout)
        ###############

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.brakes_M)

        brakes_t = TableView()
        brakes_t.setModel(self.proxyModel)
        brakes_t.verticalHeader().setVisible(False)
        brakes_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        brakes_t.hideColumn(self.brakes_M.columnCount() - 1)
        brakes_t.hideColumn(self.brakes_M.columnCount() - 2)
        self.window_ly.addWidget(brakes_t)

        brakes_t.en_int_validator(ProcModel.BrakesModel.OrderNumCol, ProcModel.BrakesModel.OrderNumCol, 1, 999)
        brakes_t.en_int_validator(ProcModel.BrakesModel.NumBranchesCol, ProcModel.BrakesModel.NumBranchesCol, 1, 4)
        brakes_t.en_int_validator(ProcModel.BrakesModel.BranchLvlOneCol, ProcModel.BrakesModel.OrderLvlFourCol, 1, 99)
        brakes_t.en_int_validator(ProcModel.BrakesModel.AnchorLineCol, ProcModel.BrakesModel.AnchorLineCol, 1, 6)
        # TODO: update max num ribs
        brakes_t.en_double_validator(ProcModel.BrakesModel.AnchorRibNumCol, ProcModel.BrakesModel.AnchorRibNumCol, 1,
                                     999, 1)

        brakes_t.set_help_bar(self.helpBar)
        brakes_t.set_help_text(ProcModel.BrakesModel.OrderNumCol, _('OrderNumDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.NumBranchesCol, _('Brakes-NumBranchesDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.BranchLvlOneCol, _('Brakes-BranchLvlOneDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.OrderLvlOneCol, _('Brakes-OrderLvlOneDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.LevelOfRamTwoCol, _('Brakes-LevelOfRamTwoDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.OrderLvlTwoCol, _('Brakes-OrderLvlTwoDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.LevelOfRamThreeCol, _('Brakes-LevelOfRamThreeDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.OrderLvlThreeCol, _('Brakes-OrderLvlThreeDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.BranchLvlFourCol, _('Brakes-BranchLvlFourDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.OrderLvlFourCol, _('Brakes-OrderLvlFourDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.AnchorLineCol, _('Brakes-AnchorLineDesc'))
        brakes_t.set_help_text(ProcModel.BrakesModel.AnchorRibNumCol, _('Brakes-AnchorRibNumDesc'))

        center_dist_t = TableView()
        center_dist_t.setModel(self.brakeL_M)
        center_dist_t.verticalHeader().setVisible(False)
        center_dist_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for c in range(5, self.brakeL_M.columnCount()):
            center_dist_t.hideColumn(c)
        center_dist_t.setFixedHeight(2 + center_dist_t.horizontalHeader().height() + center_dist_t.rowHeight(0))
        center_dist_layout = QHBoxLayout()
        center_dist_layout.addWidget(center_dist_t)
        center_dist_layout.addStretch()
        self.window_ly.addLayout(center_dist_layout)

        center_dist_t.en_int_validator(ProcModel.BrakeLengthModel.s1Col, ProcModel.BrakeLengthModel.s5Col, 0, 100)

        center_dist_t.set_help_bar(self.helpBar)
        center_dist_t.set_help_text(ProcModel.BrakeLengthModel.s1Col, _('Brakes-s1Desc'))
        center_dist_t.set_help_text(ProcModel.BrakeLengthModel.s2Col, _('Brakes-s2Desc'))
        center_dist_t.set_help_text(ProcModel.BrakeLengthModel.s3Col, _('Brakes-s3Desc'))
        center_dist_t.set_help_text(ProcModel.BrakeLengthModel.s4Col, _('Brakes-s4Desc'))
        center_dist_t.set_help_text(ProcModel.BrakeLengthModel.s5Col, _('Brakes-s5Desc'))

        length_inc_t = TableView()
        length_inc_t.setModel(self.brakeL_M)
        length_inc_t.verticalHeader().setVisible(False)
        length_inc_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for c in range(0, 5):
            length_inc_t.hideColumn(c)
        length_inc_t.hideColumn(self.brakeL_M.columnCount() - 1)
        length_inc_t.setFixedHeight(2 + length_inc_t.horizontalHeader().height() + length_inc_t.rowHeight(0))
        length_inc_layout = QHBoxLayout()
        length_inc_layout.addWidget(length_inc_t)
        length_inc_layout.addStretch()
        self.window_ly.addLayout(length_inc_layout)

        length_inc_t.en_int_validator(ProcModel.BrakeLengthModel.d1Col, ProcModel.BrakeLengthModel.d5Col, 0, 100)

        length_inc_t.set_help_bar(self.helpBar)
        length_inc_t.set_help_text(ProcModel.BrakeLengthModel.d1Col, _('Brakes-d1Desc'))
        length_inc_t.set_help_text(ProcModel.BrakeLengthModel.d2Col, _('Brakes-d2Desc'))
        length_inc_t.set_help_text(ProcModel.BrakeLengthModel.d3Col, _('Brakes-d3Desc'))
        length_inc_t.set_help_text(ProcModel.BrakeLengthModel.d4Col, _('Brakes-d4Desc'))
        length_inc_t.set_help_text(ProcModel.BrakeLengthModel.d5Col, _('Brakes-d5Desc'))

        sort_btn = QPushButton(_('Sort by order_num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        if self.brakes_M.num_configs() > 0:
            self.model_size_changed()

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.setHelpPage('proc/brakes.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(sort_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def model_size_changed(self):
        """
        :method: Called after the model has been changed it's size. Herein we assure the GUI follows the model.
        """
        logging.debug(self.__className + '.model_size_changed')

        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue(self.brakes_M.num_rows_for_config(1))
        self.numLines_S.blockSignals(False)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all
                 elements will follow the user configuration.
        """
        logging.debug(self.__className + '.num_lines_change')
        self.brakes_M.set_num_rows_for_config(1, self.numLines_S.value())
        self.pm.set_file_saved(False)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        """
        logging.debug(self.__className + '.sort_btn_press')

        self.proxyModel.sort(ProcModel.BrakesModel.OrderNumCol, Qt.AscendingOrder)
        self.proxyModel.setDynamicSortFilter(False)

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
            logging.error(self.__className + '.btn_press unrecognized button press ' + q)
