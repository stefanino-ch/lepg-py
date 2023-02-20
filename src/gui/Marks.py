"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, \
                            QSizePolicy, QHeaderView

from data.ProcModel import ProcModel
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar
from Singleton.Singleton import Singleton


class Marks(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and edit Seewing allowances data
    """

    __className = 'Marks'
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
        self.helpBar = None
        self.window_ly = None
        self.win = None

        self.marks_M = ProcModel.MarksModel()
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
                window_ly
                    marks_t
                ---------------------------
                            help_bar | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(250, 200)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Marks"))

        marks_t = TableView()
        marks_t.setModel(self.marks_M)
        # hide the ID column which is always at the end of the model
        marks_t.hideColumn(self.marks_M.columnCount() - 1)
        marks_t.verticalHeader().setVisible(False)
        marks_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        marks_t.set_help_bar(self.helpBar)

        marks_t.set_help_text(ProcModel.MarksModel.MarksSpCol,
                              _('Marks-MarksSpacingDesc'))
        marks_t.set_help_text(ProcModel.MarksModel.PointRadCol,
                              _('Marks-PointRadiusDesc'))
        marks_t.set_help_text(ProcModel.MarksModel.PointDisplCol,
                              _('Marks-PointsDisplacementDesc'))

        marks_t.en_double_validator(ProcModel.MarksModel.MarksSpCol,
                                    ProcModel.MarksModel.PointDisplCol,
                                    0, 10, 2)

        marks_t.setFixedHeight(2
                               + marks_t.horizontalHeader().height()
                               + marks_t.rowHeight(0))

        self.window_ly.addWidget(marks_t)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)
        self.btnBar.set_help_page('proc/marks.html')

        bottom_ly = QHBoxLayout()
        bottom_ly.addStretch()
        bottom_ly.addWidget(self.helpBar)
        bottom_ly.addWidget(self.btnBar)
        self.window_ly.addLayout(bottom_ly)

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
