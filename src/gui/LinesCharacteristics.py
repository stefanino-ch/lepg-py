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
from data.procModel.LinesCharacteristicsModel import LinesCharacteristicsModel

from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import Regex, ValidationValues


class LinesCharacteristics(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit lines characteristics details
    """

    __className = 'LinesCharacteristics'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()

        self.numLines_s = None
        self.helpBar = None
        self.window_ly = None
        self.btnBar = None
        self.proxyModel = None
        self.wrapper = None
        self.win = None

        self.pm = ProcModel()
        self.lines_char_m = LinesCharacteristicsModel()
        self.lines_char_m.numRowsForConfigChanged.connect(self.model_size_changed)
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
                    numLinesSpin
                    Table
                    -------------------------
                        OrderBtn  help_bar  | btn_bar
                            
        Naming:
            Conf is always one as there is only one configuration possible
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1000, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Lines characteristics"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.lines_char_m)

        num_lines_l = QLabel(_('Number of configs'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))

        self.numLines_s = QSpinBox()
        self.numLines_s.setRange(0, 999)
        self.numLines_s.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                  QSizePolicy.Policy.Fixed))
        self.numLines_s.valueChanged.connect(self.num_lines_change)
        num_lines_edit = self.numLines_s.lineEdit()
        num_lines_edit.setReadOnly(True)

        num_lines_layout = QHBoxLayout()
        num_lines_layout.addWidget(num_lines_l)
        num_lines_layout.addWidget(self.numLines_s)
        num_lines_layout.addStretch()
        self.window_ly.addLayout(num_lines_layout)
        ###############

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.lines_char_m)

        table_t = TableView()
        table_t.setModel(self.proxyModel)
        table_t.verticalHeader().setVisible(False)
        table_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_t.hideColumn(self.lines_char_m.columnCount() - 1)
        table_t.hideColumn(self.lines_char_m.columnCount() - 2)
        self.window_ly.addWidget(table_t)

        table_t.en_int_validator(LinesCharacteristicsModel.OrderNumCol,
                                 LinesCharacteristicsModel.OrderNumCol,
                                 1,
                                 ValidationValues.MaxNumRibs)

        table_t.en_int_validator(LinesCharacteristicsModel.LineTypeCol,
                                 LinesCharacteristicsModel.LineTypeCol,
                                 1,
                                 ValidationValues.Proc.LinesCharTypeMax_num)

        table_t.en_reg_exp_validator(LinesCharacteristicsModel.LineFormCol,
                                     LinesCharacteristicsModel.LineFormCol,
                                     Regex.LinesCharLineForm)

        table_t.en_double_validator(LinesCharacteristicsModel.LineDiamCol,
                                    LinesCharacteristicsModel.BDiamCol,
                                    ValidationValues.Proc.LinesCharMinDiam,
                                    ValidationValues.Proc.LinesCharMaxDiam,
                                    2)

        table_t.en_reg_exp_validator(LinesCharacteristicsModel.LineLabelCol,
                                     LinesCharacteristicsModel.LineLabelCol,
                                     Regex.LinesCharLineLabel)

        table_t.en_int_validator(LinesCharacteristicsModel.MinBreakStrCol,
                                 LinesCharacteristicsModel.MinBreakStrCol,
                                 ValidationValues.Proc.LinesCharMinBreakStr,
                                 ValidationValues.Proc.LinesCharMaxBreakStr)

        table_t.en_reg_exp_validator(LinesCharacteristicsModel.MatTypeCol,
                                     LinesCharacteristicsModel.MatTypeCol,
                                     Regex.LinesCharMatType)

        table_t.en_double_validator(LinesCharacteristicsModel.WeightPerMCol,
                                    LinesCharacteristicsModel.WeightPerMCol,
                                    ValidationValues.Proc.LinesCharMinWeightPerM,
                                    ValidationValues.Proc.LinesCharMaxWeightPerM,
                                    2)

        table_t.en_reg_exp_validator(LinesCharacteristicsModel.LoopTypeCol,
                                     LinesCharacteristicsModel.LoopTypeCol,
                                     Regex.LinesCharLoopType)

        table_t.en_double_validator(LinesCharacteristicsModel.LoopLengthCol,
                                    LinesCharacteristicsModel.LoopLengthCol,
                                    ValidationValues.Proc.LinesCharMinLoopLength_cm,
                                    ValidationValues.Proc.LinesCharMaxLoopLength_cm,
                                    2)

        table_t.en_int_validator(LinesCharacteristicsModel.LineCadColorCol,
                                 LinesCharacteristicsModel.LineCadColorCol,
                                 ValidationValues.Proc.MinDxfColorNum,
                                 ValidationValues.Proc.MaxDxfColorNum)


        table_t.set_help_bar(self.helpBar)
        table_t.set_help_text(LinesCharacteristicsModel.OrderNumCol,
                              _('OrderNumDesc'))
        table_t.set_help_text(LinesCharacteristicsModel.LineTypeCol,
                              _('LinesCharacteristics-LineType'))
        table_t.set_help_text(LinesCharacteristicsModel.LineFormCol,
                              _('LinesCharacteristics-LineForm'))
        table_t.set_help_text(LinesCharacteristicsModel.LineDiamCol,
                              _('LinesCharacteristics-LineDiameter'))
        table_t.set_help_text(LinesCharacteristicsModel.BDiamCol,
                              _('LinesCharacteristics-BDim'))
        table_t.set_help_text(LinesCharacteristicsModel.LineLabelCol,
                              _('LinesCharacteristics-LineLabel'))
        table_t.set_help_text(LinesCharacteristicsModel.MinBreakStrCol,
                              _('LinesCharacteristics-MinBreakStr'))
        table_t.set_help_text(LinesCharacteristicsModel.MatTypeCol,
                              _('LinesCharacteristics-MatType'))
        table_t.set_help_text(LinesCharacteristicsModel.WeightPerMCol,
                              _('LinesCharacteristics-WeightPerM'))
        table_t.set_help_text(LinesCharacteristicsModel.LoopTypeCol,
                              _('LinesCharacteristics-LoopType'))
        table_t.set_help_text(LinesCharacteristicsModel.LoopLengthCol,
                              _('LinesCharacteristics-LoopLength'))
        table_t.set_help_text(LinesCharacteristicsModel.LineCadColorCol,
                              _('LinesCharacteristics-LineCadColor'))

        sort_btn = QPushButton(_('Sort by order_num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                           QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.lines_char_m.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/lineCharacteristics.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(sort_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_layout)

        self.win.setLayout(self.window_ly)

    def model_size_changed(self):
        """
        :method: Called after the model has been changed it's size. Herein we 
                 assure the GUI follows the model.
        """
        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.lines_char_m.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all 
                 elements will follow the user configuration. 
        """
        self.lines_char_m.set_num_rows_for_config(1, self.numLines_s.value())
        self.pm.set_file_saved(False)

        if self.numLines_s.value() == 0:
            self.lines_char_m.set_is_used(False)
        else:
            self.lines_char_m.set_is_used(True)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort 
                 based on the numbers in the OrderNum column.
        """
        self.proxyModel.sort(LinesCharacteristicsModel.OrderNumCol,
                             Qt.SortOrder.AscendingOrder)
        self.proxyModel.setDynamicSortFilter(False)

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
