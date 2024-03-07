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
from data.procModel.SpecialParametersModel import SpecialParametersModel

from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton

from gui.GlobalDefinition import Regex, ValidationValues


class SpecialParameters(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit special parameters details
    """

    __className = 'SpecialParameters'
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
        self.spec_param_m = SpecialParametersModel()
        self.spec_param_m.numRowsForConfigChanged.connect(self.model_size_changed)
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
        self.win.setMinimumSize(500, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Special parameters"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.spec_param_m)

        num_lines_l = QLabel(_('Number of configs'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))

        self.numLines_s = QSpinBox()
        self.numLines_s.setRange(0, ValidationValues.Proc.SpecParams_MaxNumParams)

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
        self.proxyModel.setSourceModel(self.spec_param_m)

        table_t = TableView()
        table_t.setModel(self.proxyModel)
        table_t.verticalHeader().setVisible(False)
        table_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_t.hideColumn(self.spec_param_m.columnCount() - 1)
        table_t.hideColumn(self.spec_param_m.columnCount() - 2)
        self.window_ly.addWidget(table_t)

        table_t.en_int_validator(SpecialParametersModel.OrderNumCol,
                                 SpecialParametersModel.OrderNumCol,
                                 1,
                                 ValidationValues.Proc.SpecParams_MaxNumParams)

        table_t.en_int_validator(SpecialParametersModel.code_Col,
                                 SpecialParametersModel.code_Col,
                                 1000,
                                 9999)

        table_t.en_double_validator(SpecialParametersModel.value_Col,
                                    SpecialParametersModel.value_Col,
                                    0,
                                    9999,
                                    2)

        table_t.set_help_bar(self.helpBar)
        table_t.set_help_text(SpecialParametersModel.OrderNumCol,
                              _('OrderNumDesc'))
        table_t.set_help_text(SpecialParametersModel.code_Col,
                              _('SpecialParameters-Code'))
        table_t.set_help_text(SpecialParametersModel.value_Col,
                              _('SpecialParameters-Value'))

        sort_btn = QPushButton(_('Sort by order_num'))
        sort_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                           QSizePolicy.Policy.Fixed))
        sort_btn.clicked.connect(self.sort_btn_press)

        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.spec_param_m.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('expert/specialParameters.html')

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
        self.numLines_s.setValue(self.spec_param_m.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all 
                 elements will follow the user configuration. 
        """
        self.spec_param_m.set_num_rows_for_config(1, self.numLines_s.value())
        self.pm.set_file_saved(False)

        if self.numLines_s.value() == 0:
            self.spec_param_m.set_is_used(False)
        else:
            self.spec_param_m.set_is_used(True)

    def sort_btn_press(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort 
                 based on the numbers in the OrderNum column.
        """
        self.proxyModel.sort(SpecialParametersModel.OrderNumCol,
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
