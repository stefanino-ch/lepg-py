"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
import platform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy,\
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QGroupBox
from gui.elements.LineEdit import LineEdit
from gui.elements.CheckBox import CheckBox
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from ConfigReader.ConfigReader import ConfigReader
from Singleton.Singleton import Singleton


class SetupProcessors(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display and setup pre-proc and proc settings.
    """

    __className = 'SetupProcessors'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        super().__init__()

        self.proc_e = None
        self.proc_grp = None
        self.outline_chkb = None
        self.pre_proc_e = None
        self.pre_proc_grp_ly = None
        self.pre_proc_grp = None
        self.helpBar = None
        self.window_ly = None
        self.win = None
        self.proc_grp_ly = None
        self.btn_bar = None

        logging.debug(self.__className+'.__init__')

        self.config_reader = ConfigReader()
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
                windowGrid
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
        self.win.setMinimumSize(500, 150)

        self.window_ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Setup processors"))

        self.pre_proc_grp = QGroupBox(_('Pre-processor'))
        self.pre_proc_grp_ly = QVBoxLayout()
        self.pre_proc_grp.setLayout(self.pre_proc_grp_ly)
        self.window_ly.addWidget(self.pre_proc_grp)

        self.pre_proc_e = LineEdit()
        self.pre_proc_e.setReadOnly(True)
        self.pre_proc_e.set_help_bar(self.helpBar)
        self.pre_proc_e.set_help_text(_('SetupProc-PreProcPathNameDesc'))
        self.pre_proc_e.setText(self.config_reader.get_pre_proc_path_name())

        pre_proc_btn = QPushButton(_('Change'))
        pre_proc_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                               QSizePolicy.Fixed))
        pre_proc_btn.clicked.connect(self.pre_proc_btn_press)

        pre_proc_ly = QHBoxLayout()
        pre_proc_ly.addWidget(self.pre_proc_e)
        pre_proc_ly.addWidget(pre_proc_btn)
        self.pre_proc_grp_ly.addLayout(pre_proc_ly)

        self.outline_chkb = CheckBox(_('Open wing outline after processing'))
        self.outline_chkb.setHelpBar(self.helpBar)
        self.outline_chkb.setHelpText(_('SetupProc-PreProcWingOutline'))
        self.outline_chkb.stateChanged.connect(self.outline_chkb_change)
        self.pre_proc_grp_ly.addWidget(self.outline_chkb)

        self.proc_grp = QGroupBox(_('Processor (lep)'))
        self.proc_grp_ly = QHBoxLayout()
        self.proc_grp.setLayout(self.proc_grp_ly)
        self.window_ly.addWidget(self.proc_grp)

        self.proc_e = LineEdit()
        self.proc_e.setReadOnly(True)
        self.proc_e.set_help_bar(self.helpBar)
        self.proc_e.set_help_text(_('SetupProc-ProcPathNameDesc'))
        self.proc_e.setText(self.config_reader.get_proc_path_name())

        proc_btn = QPushButton(_('Change'))
        proc_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                           QSizePolicy.Fixed))
        proc_btn.clicked.connect(self.proc_btn_press)
        self.proc_grp_ly.addWidget(self.proc_e)
        self.proc_grp_ly.addWidget(proc_btn)

        self.outline_chkb.setChecked(
            self.config_reader.get_check_for_updates())

        #############################
        # Commons for all windows
        self.btn_bar = WindowBtnBar(0b0101)
        self.btn_bar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                               QSizePolicy.Fixed))
        self.btn_bar.my_signal.connect(self.btn_press)
        self.btn_bar.setHelpPage('setup/processors.html')

        bottom_ly = QHBoxLayout()
        bottom_ly.addStretch()
        bottom_ly.addWidget(self.helpBar)
        bottom_ly.addWidget(self.btn_bar)
        self.window_ly.addLayout(bottom_ly)

        self.win.setLayout(self.window_ly)

    def pre_proc_btn_press(self):
        """
        :method: Called at the time the user select the pre-proc change
                 button. Does prepare and execute the according file
                 change dialog.
        """
        logging.debug(self.__className + '.pre_proc_btn_press')

        # Do platform specific if here as the PreProx extensions are different
        if platform.system() == "Windows":
            filename = QFileDialog.getOpenFileName(
                            None,
                            _('Select Pre-Processor'),
                            "",
                            "Executable (*.exe)")
        elif platform.system() == "Linux":
            filename = QFileDialog.getOpenFileName(
                            None,
                            _('Select Pre_Processor'),
                            "",
                            "Compiled Fortran (*.out)")
        elif platform.system() == "Darwin":
            filename = QFileDialog.getOpenFileName(
                            None,
                            _('Select Pre_Processor'),
                            "",
                            "Compiled Fortran (*.o)")
        else:
            logging.error("Sorry, your operating system is not supported yet")
            return

        if filename != ('', ''):
            # User has really selected a file, if it had aborted the
            # dialog an empty tuple is returned
            # Write the info to the config reader
            logging.debug(self.__className
                          + '.setupPreProcLocation Path and Name '
                          + filename[0])

            self.pre_proc_e.setText(filename[0])
            self.config_reader.set_pre_proc_path_name(filename[0])

    def outline_chkb_change(self):
        """
        :method: Called at the time the pre-processor show outline checkbox
                 is changed. Does set up the config reader property.
        """
        self.config_reader.set_pre_proc_show_outline(
            self.outline_chkb.isChecked())

    def proc_btn_press(self):
        """
        :method: Called at the time the user select the proc change button.
                 Does prepare and execute the according file change dialog.
        """
        logging.debug(self.__className + '.proc_btn_press')

        # Do platform specific if here as the PreProx extensions are different
        if platform.system() == "Windows":
            filename = QFileDialog.getOpenFileName(
                            None,
                            _('Select Processor'),
                            "",
                            "Executable (*.exe)")
        elif platform.system() == "Linux":
            filename = QFileDialog.getOpenFileName(
                            None,
                            _('Select Processor'),
                            "",
                            "Compiled Fortran (*.out)")
        elif platform.system() == "Darwin":
            filename = QFileDialog.getOpenFileName(
                None,
                _('Select Processor'),
                "",
                "Compiled Fortran (*.o)")
        else:
            logging.error("Sorry, your operating system is not supported yet")
            return

        if filename != ('', ''):
            # User has really selected a file, if it had aborted the
            # dialog an empty tuple is returned.
            # Write the info to the config reader
            logging.debug(self.__className
                          + '.setupProcLocation Path and Name '
                          + filename[0])

            self.proc_e.setText(filename[0])
            self.config_reader.set_proc_path_name(filename[0])

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
