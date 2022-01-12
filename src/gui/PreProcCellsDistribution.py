"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView, \
    QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QSpinBox

from data.PreProcModel import PreProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from Singleton.Singleton import Singleton


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
        :method: Constructor
        """
        self.win = None
        self.window_ly = None
        self.help_bar = None
        self.usage_cb = None
        self.num_lines_s = None
        self.num_lines_l = None
        self.one_t = None
        self.btn_bar = None
        logging.debug(self.__className+'.__init__')
        super().__init__()

        self.ppm = PreProcModel()
        self.cellsDistr_M = PreProcModel.CellsDistrModel()
        self.cellsDistr_M.didSelect.connect(self.model_change)
        self.build_window()
    
    def closeEvent(self, event):  # @UnusedVariable
        """
        :method: Called at the time the user closes the window.
        """
        logging.debug(self.__className+'.closeEvent') 
        
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
        logging.debug(self.__className + '.build_window')
        
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
        usage_l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
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
        self.num_lines_l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.num_lines_s = QSpinBox()
        self.num_lines_s.setRange(1, 999)
        self.num_lines_s.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
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
        self.one_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.one_t.hideColumn(self.cellsDistr_M.columnCount() - 1)
        self.one_t.hideColumn(self.cellsDistr_M.columnCount() - 2)

        self.window_ly.addWidget(self.one_t)
        
        self.one_t.enableIntValidator(PreProcModel.CellsDistrModel.OrderNumCol,
                                      PreProcModel.CellsDistrModel.OrderNumCol,
                                      1, 999)
        self.one_t.enableDoubleValidator(PreProcModel.CellsDistrModel.CoefCol,
                                         PreProcModel.CellsDistrModel.CoefCol,
                                         0, 1, 1)
        self.one_t.enableDoubleValidator(PreProcModel.CellsDistrModel.WidthCol,
                                         PreProcModel.CellsDistrModel.WidthCol,
                                         1, 500, 1)
        self.one_t.enableIntValidator(PreProcModel.CellsDistrModel.NumCellsCol,
                                      PreProcModel.CellsDistrModel.NumCellsCol,
                                      1, 999)
          
        self.one_t.setHelpBar(self.help_bar)
        self.one_t.setHelpText(PreProcModel.CellsDistrModel.OrderNumCol, _('PreProc-CellNumDesc'))
        self.one_t.setHelpText(PreProcModel.CellsDistrModel.CoefCol, _('PreProc-DistrCoefDesc'))
        self.one_t.setHelpText(PreProcModel.CellsDistrModel.WidthCol, _('PreProc-WidthDesc'))
        self.one_t.setHelpText(PreProcModel.CellsDistrModel.NumCellsCol, _('PreProc-NumCellsDesc'))

        self.model_change()
        
        #############################
        # Commons for all windows
        self.btn_bar = WindowBtnBar(0b0101)
        self.btn_bar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
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
        logging.debug(self.__className+'.usage_update')
        
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
        logging.debug(self.__className+'.usage_cb_change')
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
        logging.debug(self.__className+'.num_lines_change')
        self.cellsDistr_M.set_num_rows_for_config(1, self.num_lines_s.value())

        self.ppm.set_file_saved(False)
            
    def btn_press(self, q):
        """
        :method: Handling of all pressed buttons.
        """
        logging.debug(self.__className+'.btn_press')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btn_press unrecognized button press '+q)
            
    def set_type_one_columns(self):
        """
        :method: shows/ hides the spinbox and the table columns to for type 1 data
        """
        logging.debug(self.__className+'.set_type_one_columns')
        
        self.num_lines_l.setVisible(False)
        self.num_lines_s.setVisible(False)
        
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.OrderNumCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.DistrTypeCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.CoefCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.WidthCol)
        self.one_t.showColumn(PreProcModel.CellsDistrModel.NumCellsCol)

    def set_type_two_thr_columns(self):
        """
        :method: shows/ hides the spinbox and the table columns to for type 2 and 3 data
        """
        logging.debug(self.__className+'.set_type_two_thr_columns')
        
        self.num_lines_l.setVisible(False)
        self.num_lines_s.setVisible(False)
        
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.OrderNumCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.DistrTypeCol)
        self.one_t.showColumn(PreProcModel.CellsDistrModel.CoefCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.WidthCol)
        self.one_t.showColumn(PreProcModel.CellsDistrModel.NumCellsCol)
        
    def set_type_fou_columns(self):
        """
        :method: shows/ hides the spinbox and the table columns to for type 4 data
        """
        logging.debug(self.__className+'.set_type_fou_columns')
        
        self.num_lines_s.blockSignals(True)
        self.num_lines_s.setValue(self.cellsDistr_M.num_rows_for_config(1))
        self.num_lines_s.blockSignals(False)
        
        self.num_lines_l.setVisible(True)
        self.num_lines_s.setVisible(True)
        
        self.one_t.showColumn(PreProcModel.CellsDistrModel.OrderNumCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.DistrTypeCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.CoefCol)
        self.one_t.showColumn(PreProcModel.CellsDistrModel.WidthCol)
        self.one_t.hideColumn(PreProcModel.CellsDistrModel.NumCellsCol)
    