"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, \
                            QSizePolicy, QHeaderView, QPushButton
from data.procModel.AirfoilsModel import AirfoilsModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton
from gui.GlobalDefinition import ValidationValues, Regex


class Airfoils(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit airfoils data  
    """

    __className = 'Airfoils'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        self.btnBar = None
        self.sortBtn = None
        self.table = None
        self.helpBar = None
        self.windowLayout = None
        self.win = None
        super().__init__()

        self.airf_M = AirfoilsModel()
        self.build_window()

    def closeEvent(self, event):
        """
        :method: Called at the time the user closes the window.
        """

    def build_window(self):
        """
        :method: Creates the window including all GUI elements. 
        
        Layout::
        
            Data
            Buttons
            
        Structure:: 
        
            window
                window_ly
                     Table
                    ---------------------------
                     SortBtn | help_bar | btn_bar
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 300)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Airfoils"))

        self.table = TableView()
        self.table.setModel(self.airf_M)
        # hide the ID column which is always at the end of the model
        self.table.hideColumn(self.airf_M.columnCount() - 1)  
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.en_int_validator(AirfoilsModel.RibNumCol,
                                    AirfoilsModel.RibNumCol,
                                    1, ValidationValues.MaxNumRibs)

        self.table.en_reg_exp_validator(AirfoilsModel.AirfNameCol,
                                        AirfoilsModel.AirfNameCol,
                                        Regex.AirfoilsNameString)

        self.table.en_double_validator(AirfoilsModel.IntakeStartCol,
                                       AirfoilsModel.IntakeEndCol,
                                       ValidationValues.WingChordMin_perc,
                                       ValidationValues.WingChordMax_perc,
                                       3)

        self.table.en_int_validator(AirfoilsModel.OpenCloseCol,
                                    AirfoilsModel.OpenCloseCol,
                                    0, 1)

        self.table.en_double_validator(AirfoilsModel.DisplacCol,
                                       AirfoilsModel.DisplacCol,
                                       ValidationValues.Proc.DisplacementMin_cm,
                                       ValidationValues.Proc.DisplacementMax_cm,
                                       3)

        self.table.en_double_validator(AirfoilsModel.RelWeightCol,
                                       AirfoilsModel.rrwCol,
                                       ValidationValues.Proc.RelativeWeightMin,
                                       ValidationValues.Proc.RelativeWeightMax,
                                       3)

        self.table.set_help_bar(self.helpBar)
        self.table.set_help_text(AirfoilsModel.RibNumCol,
                                 _('Proc-RibNumDesc'))
        self.table.set_help_text(AirfoilsModel.AirfNameCol,
                                 _('Proc-AirfoilNameDesc'))
        self.table.set_help_text(AirfoilsModel.IntakeStartCol,
                                 _('Proc-IntakeStartDesc'))
        self.table.set_help_text(AirfoilsModel.IntakeEndCol,
                                 _('Proc-IntakeEnDesc'))
        self.table.set_help_text(AirfoilsModel.OpenCloseCol,
                                 _('Proc-OpenCloseDesc'))
        self.table.set_help_text(AirfoilsModel.DisplacCol,
                                 _('Proc-DisplacDesc'))
        self.table.set_help_text(AirfoilsModel.RelWeightCol,
                                 _('Proc-RelWeightDesc'))
        self.table.set_help_text(AirfoilsModel.rrwCol,
                                 _('Proc-rrwDesc'))

        self.windowLayout.addWidget(self.table)

        self.sortBtn = QPushButton(_('Sort by Rib Number'))
        self.sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, 
                                               QSizePolicy.Policy.Fixed))
        self.sortBtn.clicked.connect(self.sort_btn_press)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, 
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/airfoils.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.sortBtn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.helpBar)
        bottom_layout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottom_layout)

        self.win.setLayout(self.windowLayout)

    def sort_btn_press(self):
        """
        : method : handles the sort of the table by rib number
        """
        self.airf_M.sort_table(AirfoilsModel.RibNumCol,
                               Qt.SortOrder.AscendingOrder)

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
