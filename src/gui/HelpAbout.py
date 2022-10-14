"""
@Author: Stefan Feuz; http://www.laboratoridenvol.com
@License: General Public License GNU GPL 3.0
"""
import logging
import __init__

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy

from gui.elements.WindowBtnBar import WindowBtnBar
from Singleton.Singleton import Singleton


class HelpAbout(QMdiSubWindow, metaclass=Singleton):
    """
    Window displaying
        The help about information
    """
    __className = 'HelpAbout'

    def __init__(self):
        self.helpAboutLicL = None
        self.helpAboutDevL = None
        self.helpAboutTextL = None
        self.font = None
        self.helpAboutTitleL = None
        self.__winGridRow = None
        self.windowGrid = None
        self.win = None
        self.btnBar = None
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.build_window()

    def closeEvent(self, event):  # @UnusedVariable
        logging.debug(self.__className + '.closeEvent')

    def build_window(self):
        """
        Builds the window.

        Structure:
            window
                windowGrid
                    helpAboutTitleL
                    helpAboutTextL
                    helpAboutDevL
                    helpAboutLicL

                    btn_bar
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)

        self.windowGrid = QGridLayout()
        self.__winGridRow = 0

        #############################
        # Add window specifics here
        self.setWindowTitle(_("About lepg-py"))

        self.helpAboutTitleL = QLabel(_('lepg-py'))
        # set font
        self.font = QFont()
        self.font.setPointSize(20)
        self.font.setBold(True)
        self.helpAboutTitleL.setFont(self.font)

        self.windowGrid.addWidget(self.helpAboutTitleL,
                                  self.__winGridRow,
                                  0,
                                  Qt.AlignLeft)
        self.__winGridRow += 1

        self.helpAboutTextL = QLabel(_('A graphical frontend to lep\n'
                                       'Current Version \t\t\t%s')
                                     % getattr(__init__, '__version__'))
        self.windowGrid.addWidget(self.helpAboutTextL,
                                  self.__winGridRow, 0,
                                  Qt.AlignLeft)
        self.__winGridRow += 1

        self.helpAboutDevL = QLabel(_('Developers: \nStefan Feuz'))
        self.windowGrid.addWidget(self.helpAboutDevL,
                                  self.__winGridRow, 0,
                                  Qt.AlignLeft)
        self.__winGridRow += 1

        self.helpAboutLicL = QLabel(_('General Public License GNU GPL 3.0'))
        self.windowGrid.addWidget(self.helpAboutLicL,
                                  self.__winGridRow, 0,
                                  Qt.AlignLeft)
        self.__winGridRow += 1

        #############################
        # Rest of standard window setups
        self.btnBar = WindowBtnBar(0b0100)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Fixed))
        self.btnBar.my_signal.connect(self.btn_press)

        self.windowGrid.addWidget(self.btnBar,
                                  self.__winGridRow, 0, Qt.AlignmentFlag.AlignRight)
        self.__winGridRow += 1

        self.win.setLayout(self.windowGrid)

    def btn_press(self, q):
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__className
                          + '.btn_press unrecognized button press '
                          + q)
