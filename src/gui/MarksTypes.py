"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
                            QSpinBox, QLabel, QHBoxLayout, QVBoxLayout

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class MarksTypes(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'MarksTypes'
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
        self.numLines_s = None
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.pm = ProcModel()

        self.marksT_M = ProcModel.MarksTypesModel()
        self.marksT_M.numRowsForConfigChanged.connect(self.model_size_changed)
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
        self.win.setMinimumSize(900, 400)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Marks types"))

        num_lines_l = QLabel(_('Number of marks'))
        num_lines_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, 
                                              QSizePolicy.Policy.Fixed))

        self.numLines_s = QSpinBox()
        self.numLines_s.setRange(0, 10)
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

        marks_types_t = TableView()
        marks_types_t.setModel(self.marksT_M)
        marks_types_t.verticalHeader().setVisible(False)
        marks_types_t.horizontalHeader().\
            setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        marks_types_t.hideColumn(self.marksT_M.columnCount() - 1)
        marks_types_t.hideColumn(self.marksT_M.columnCount() - 2)
        marks_types_t.hideColumn(0)
        self.window_ly.addWidget(marks_types_t)

        marks_types_t.en_reg_exp_validator(
            ProcModel.MarksTypesModel.TypeCol, 
            ProcModel.MarksTypesModel.TypeCol,
            "^[a-zA-Z0-9_.-]*$")
        marks_types_t.en_int_validator(
            ProcModel.MarksTypesModel.FormOneCol, 
            ProcModel.MarksTypesModel.FormOneCol, 
            1, 3)
        marks_types_t.en_double_validator(
            ProcModel.MarksTypesModel.FormOnePOneCol,
            ProcModel.MarksTypesModel.FormOnePTwoCol, 
            0, 100, 2)
        marks_types_t.en_int_validator(
            ProcModel.MarksTypesModel.FormTwoCol, 
            ProcModel.MarksTypesModel.FormTwoCol, 
            1, 3)
        marks_types_t.en_double_validator(
            ProcModel.MarksTypesModel.FormTwoPOneCol,
            ProcModel.MarksTypesModel.FormTwoPTwoCol, 
            0, 100, 2)

        marks_types_t.set_help_bar(self.helpBar)
        marks_types_t.set_help_text(ProcModel.MarksTypesModel.TypeCol,
                                    _('MarksTypes-TypeDesc'))
        marks_types_t.set_help_text(ProcModel.MarksTypesModel.FormOneCol,
                                    _('MarksTypes-FormOneDesc'))
        marks_types_t.set_help_text(ProcModel.MarksTypesModel.FormOnePOneCol,
                                    _('MarksTypes-FormOnePOneDesc'))
        marks_types_t.set_help_text(ProcModel.MarksTypesModel.FormOnePTwoCol,
                                    _('MarksTypes-FormOnePTwoDesc'))
        marks_types_t.set_help_text(ProcModel.MarksTypesModel.FormTwoCol,
                                    _('MarksTypes-FormTwoDesc'))
        marks_types_t.set_help_text(ProcModel.MarksTypesModel.FormTwoPOneCol,
                                    _('MarksTypes-FormTwoPOneDesc'))
        marks_types_t.set_help_text(ProcModel.MarksTypesModel.FormTwoPTwoCol,
                                    _('MarksTypes-FormTwoPTwoDesc'))

        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.marksT_M.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, 
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/marksTypes.html')

        bottom_layout = QHBoxLayout()
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
        logging.debug(self.__className + '.model_size_changed')
        self.numLines_s.blockSignals(True)
        self.numLines_s.setValue(self.marksT_M.num_rows_for_config(1))
        self.numLines_s.blockSignals(False)

    def num_lines_change(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all 
                 elements will follow the user configuration.
        """
        logging.debug(self.__className + '.num_lines_change')
        self.marksT_M.set_num_rows_for_config(1, self.numLines_s.value())
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
