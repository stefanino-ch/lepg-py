"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QLabel, QComboBox, QCheckBox
from gui.elements.WindowBtnBar import WindowBtnBar
from ConfigReader.ConfigReader import ConfigReader


class SetupUpdateChecking(QMdiSubWindow):
    """
    :class: Window to display and edit the Basic Data
    """

    __className = 'SetupUpdateChecking'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        self.window_ly = None
        self.btn_bar = None
        self.branch_cb = None
        self.update_chkb = None
        self.win = None

        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.confRdr = ConfigReader()

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
                     Labels    | Edit fields
                     ...       | ...
                    -------------------------
                                | help_bar
                                | btn_bar
        """
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(300, 150)

        self.window_ly = QGridLayout()
        __winGRowL = 0
        __winGRowR = 0
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Setup update checking"))
        
        update_l = QLabel(_('Perform update checks at start'))
        update_l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.update_chkb = QCheckBox()
        self.update_chkb.toggled.connect(self.update_chkb_change)
        self.window_ly.addWidget(update_l, __winGRowL, 0)
        self.window_ly.addWidget(self.update_chkb, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        branch_l = QLabel(_('Branch'))
        branch_l.setAlignment(Qt.AlignRight)
        self.branch_cb = QComboBox()
        self.branch_cb.addItem(_("stable"))
        self.branch_cb.addItem(_("latest"))
        if self.confRdr.get_track_branch() == 'stable':
            self.branch_cb.setCurrentIndex(0)
        else:
            self.branch_cb.setCurrentIndex(1)
            
        self.branch_cb.currentIndexChanged.connect(self.branch_cb_change)
        self.branch_cb.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.window_ly.addWidget(branch_l, __winGRowL, 0)
        self.window_ly.addWidget(self.branch_cb, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        if self.confRdr.get_check_for_updates() is True:
            self.update_chkb.setChecked(True)
            self.branch_cb.setEnabled(True)
        else:
            self.update_chkb.setChecked(False)
            self.branch_cb.setEnabled(False)

        #############################
        # Commons for all windows
        self.btn_bar = WindowBtnBar(0b0101)
        self.btn_bar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btn_bar.my_signal.connect(self.btn_press)
        self.btn_bar.setHelpPage('setup/updateCheck.html')

        self.window_ly.addWidget(self.btn_bar, __winGRowR, 1, Qt.AlignRight)
        __winGRowR += 1
        
        self.win.setLayout(self.window_ly)

    def update_chkb_change(self):
        """
        :method: Called at the time the user alters the update checkbox
        """ 
        logging.debug(self.__className + '.update_chkb_change')
        
        if self.update_chkb.isChecked():
            self.confRdr.set_check_for_updates('yes')
            self.branch_cb.setEnabled(True)
        else:
            self.confRdr.set_check_for_updates('no')
            self.branch_cb.setEnabled(False)
        
    def branch_cb_change(self):
        """
        :method: Called at the time the user alters the branch combo box.
        """
        logging.debug(self.__className + '.branch_cb_change')
        
        if self.branch_cb.currentIndex() == 0:
            self.confRdr.set_track_branch('stable')
        else:
            self.confRdr.set_track_branch('latest')
    
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
            logging.error(self.__className + '.btn_press unrecognized button press '+q)
    