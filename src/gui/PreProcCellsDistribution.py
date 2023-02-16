"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
                            QHBoxLayout, QVBoxLayout, QComboBox, QLabel, \
                            QSpinBox

from Singleton.Singleton import Singleton
from data.PreProcModel import PreProcModel
from data.preProcModel.CellsDistrModel import CellsDistrModel
from gui.GlobalDefinition import ValidationValues
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar


class PreProcCellsDistribution(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit the cells' distribution data
            for the pre-processor
    """

    __className = 'PreProcCellsDistribution'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        self.win = None
        self.window_ly = None
        self.help_bar = None
        self.usage_cb = None
        self.num_lines_s = None
        self.num_lines_l = None
        self.one_t = None
        self.btn_bar = None
        super().__init__()

        self.ppm = PreProcModel()
        self.cellsDistr_M = CellsDistrModel()
        self.cellsDistr_M.didSelect.connect(self.model_change)
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
                    usage_cb
                    num_lines_s
                    Table
                    -------------------------
                        help_bar  | btn_bar

        Naming:
            Conf is always one as there is only one configuration possible
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(450, 200)

        self.window_ly = QVBoxLayout()

        self.help_bar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Pre-Processor cells distribution"))

        usage_l = QLabel(_('Type'))
        usage_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                          QSizePolicy.Policy.Fixed))
        self.usage_cb = QComboBox()
        self.usage_cb.addItem(_("1: uniform "))
        self.usage_cb.addItem(_("2: linear"))
        self.usage_cb.addItem(_("3: prop to chord"))
        self.usage_cb.addItem(_("4: explicit"))
        self.usage_cb.currentIndexChanged.connect(self.usage_cb_change)
        usage_ly = QHBoxLayout()
        usage_ly.addWidget(usage_l)
        usage_ly.addWidget(self.usage_cb)
        usage_ly.addStretch()

        self.window_ly.addLayout(usage_ly)

        self.num_lines_l = QLabel(_('Num cells'))
        self.num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                   QSizePolicy.Policy.Fixed))
        self.num_lines_s = QSpinBox()
        self.num_lines_s.setRange(1, ValidationValues.MaxNumCells)
        self.num_lines_s.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                   QSizePolicy.Policy.Fixed))
        self.num_lines_s.valueChanged.connect(self.num_lines_change)
        num_lines_edit = self.num_lines_s.lineEdit()
        num_lines_edit.setReadOnly(True)
        num_lines_ly = QHBoxLayout()
        num_lines_ly.addWidget(self.num_lines_l)
        num_lines_ly.addWidget(self.num_lines_s)
        num_lines_ly.addStretch()

        self.window_ly.addLayout(num_lines_ly)

        self.one_t = TableView()
        self.one_t.setModel(self.cellsDistr_M)
        self.one_t.verticalHeader().setVisible(False)
        self.one_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.one_t.hideColumn(self.cellsDistr_M.columnCount() - 1)
        self.one_t.hideColumn(self.cellsDistr_M.columnCount() - 2)

        self.window_ly.addWidget(self.one_t)

        self.one_t.en_int_validator(CellsDistrModel.OrderNumCol,
                                    CellsDistrModel.OrderNumCol,
                                    1, ValidationValues.MaxNumCells)

        self.one_t.en_double_validator(CellsDistrModel.CoefCol,
                                       CellsDistrModel.CoefCol,
                                       0, 1, 1)

        self.one_t.en_double_validator(CellsDistrModel.WidthCol,
                                       CellsDistrModel.WidthCol,
                                       1, ValidationValues.HalfWingSpanMax_cm, 1)

        self.one_t.en_int_validator(CellsDistrModel.NumCellsCol,
                                    CellsDistrModel.NumCellsCol,
                                    1, ValidationValues.MaxNumCells)

        self.one_t.set_help_bar(self.help_bar)
        self.one_t.set_help_text(CellsDistrModel.OrderNumCol,
                                 _('PreProc-CellNumDesc'))
        self.one_t.set_help_text(CellsDistrModel.CoefCol,
                                 _('PreProc-DistrCoefDesc'))
        self.one_t.set_help_text(CellsDistrModel.WidthCol,
                                 _('PreProc-WidthDesc'))
        self.one_t.set_help_text(CellsDistrModel.NumCellsCol,
                                 _('PreProc-NumCellsDesc'))

        self.model_change()

        #############################
        # Commons for all windows
        self.btn_bar = WindowBtnBar(0b0101)
        self.btn_bar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Fixed))
        self.btn_bar.my_signal.connect(self.btn_press)
        self.btn_bar.setHelpPage('preproc/cell_distribution.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_bar)
        bottom_layout.addWidget(self.btn_bar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def model_change(self):
        """
        :method: Updates the GUI as soon the model changes
        """
        type_n = self.cellsDistr_M.get_type(1, 1)

        if type_n == 1:
            self.usage_cb.blockSignals(True)
            self.usage_cb.setCurrentIndex(0)
            self.usage_cb.blockSignals(False)

            self.set_type_one_columns()

        elif type_n == 2:
            self.usage_cb.blockSignals(True)
            self.usage_cb.setCurrentIndex(1)
            self.usage_cb.blockSignals(False)

            self.set_type_two_thr_columns()

        elif type_n == 3:
            self.usage_cb.blockSignals(True)
            self.usage_cb.setCurrentIndex(2)
            self.usage_cb.blockSignals(False)

            self.set_type_two_thr_columns()

        elif type_n == 4:
            self.usage_cb.blockSignals(True)
            self.usage_cb.setCurrentIndex(3)
            self.usage_cb.blockSignals(False)

            self.set_type_fou_columns()

    def usage_cb_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        if self.usage_cb.currentIndex() == 0:
            self.cellsDistr_M.set_num_rows_for_config(1, 1)
            self.cellsDistr_M.update_type(1, 1, 1)

        elif self.usage_cb.currentIndex() == 1:
            self.cellsDistr_M.set_num_rows_for_config(1, 1)
            self.cellsDistr_M.update_type(1, 1, 2)

        elif self.usage_cb.currentIndex() == 2:
            self.cellsDistr_M.set_num_rows_for_config(1, 1)
            self.cellsDistr_M.update_type(1, 1, 3)

        elif self.usage_cb.currentIndex() == 3:
            self.cellsDistr_M.update_type(1, 1, 4)

        self.ppm.set_file_saved(False)

    def num_lines_change(self):
        """
        :method: Updates the model as soon the usage CB has been changed
        """
        self.cellsDistr_M.set_num_rows_for_config(1, self.num_lines_s.value())

        self.ppm.set_file_saved(False)

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
                          + '.btn_press unrecognized button press ' + q)

    def set_type_one_columns(self):
        """
        :method: Shows/ hides the spinbox and the table columns to for
                 type 1 data
        """
        self.num_lines_l.setVisible(False)
        self.num_lines_s.setVisible(False)

        self.one_t.hideColumn(CellsDistrModel.OrderNumCol)
        self.one_t.hideColumn(CellsDistrModel.DistrTypeCol)
        self.one_t.hideColumn(CellsDistrModel.CoefCol)
        self.one_t.hideColumn(CellsDistrModel.WidthCol)
        self.one_t.showColumn(CellsDistrModel.NumCellsCol)

    def set_type_two_thr_columns(self):
        """
        :method: Shows/ hides the spinbox and the table columns to for type
                 2 and 3 data
        """
        self.num_lines_l.setVisible(False)
        self.num_lines_s.setVisible(False)

        self.one_t.hideColumn(CellsDistrModel.OrderNumCol)
        self.one_t.hideColumn(CellsDistrModel.DistrTypeCol)
        self.one_t.showColumn(CellsDistrModel.CoefCol)
        self.one_t.hideColumn(CellsDistrModel.WidthCol)
        self.one_t.showColumn(CellsDistrModel.NumCellsCol)

    def set_type_fou_columns(self):
        """
        :method: Shows/ hides the spinbox and the table columns to for type
                 4 data
        """
        self.num_lines_s.blockSignals(True)
        self.num_lines_s.setValue(self.cellsDistr_M.num_rows_for_config(1))
        self.num_lines_s.blockSignals(False)

        self.num_lines_l.setVisible(True)
        self.num_lines_s.setVisible(True)

        self.one_t.showColumn(CellsDistrModel.OrderNumCol)
        self.one_t.hideColumn(CellsDistrModel.DistrTypeCol)
        self.one_t.hideColumn(CellsDistrModel.CoefCol)
        self.one_t.showColumn(CellsDistrModel.WidthCol)
        self.one_t.hideColumn(CellsDistrModel.NumCellsCol)
