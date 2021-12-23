'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
import platform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QLabel, \
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QCheckBox
from Windows.LineEdit import LineEdit
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from ConfigReader.ConfigReader import ConfigReader


class SetupProcessors(QMdiSubWindow):
    '''
    :class: Window to display and setup pre-proc and proc settings.
    '''

    __className = 'SetupProcessors'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()

        self.confRdr = ConfigReader()

        self.buildWindow()

    def closeEvent(self, event):  # @UnusedVariable
        '''
        :method: Called at the time the user closes the window.
        '''
        logging.debug(self.__className+'.closeEvent')

    def buildWindow(self):
        '''
        :method: Creates the window including all GUI elements.

        Structure::

            win
                windowGrid
                     Labels    | Edit fields
                     ...       | ...
                    -------------------------
                                | helpBar
                                | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')

        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(400, 150)

        self.window_Ly = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Setup processors"))

        preProc_L = QLabel(_('Pre-Processor'))
        self.window_Ly.addWidget(preProc_L)

        self.preProc_E = LineEdit()
        self.preProc_E.setReadOnly(True)
        self.preProc_E.setHelpBar(self.helpBar)
        self.preProc_E.setHelpText(_('SetupProc-PreProcPathNameDesc'))
        self.preProc_E.setText(self.confRdr.getPreProcPathName())

        preProc_Btn = QPushButton(_('Change'))
        preProc_Btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        preProc_Btn.clicked.connect(self.preProcBtnPress)

        preProc_Ly = QHBoxLayout()
        preProc_Ly.addWidget(self.preProc_E)
        preProc_Ly.addWidget(preProc_Btn)
        self.window_Ly.addLayout(preProc_Ly)

        showWingOutl_chkB = QCheckBox(_('Open wing outline after processing'))
        self.window_Ly.addWidget(showWingOutl_chkB)

        proc_L = QLabel(_('Processor (lep)'))
        self.window_Ly.addWidget(proc_L)

        self.proc_E = LineEdit()
        self.proc_E.setReadOnly(True)
        self.proc_E.setHelpBar(self.helpBar)
        self.proc_E.setHelpText(_('SetupProc-ProcPathNameDesc'))
        self.proc_E.setText(self.confRdr.getProcPathName())

        proc_Btn = QPushButton(_('Change'))
        proc_Btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                           QSizePolicy.Fixed))
        proc_Btn.clicked.connect(self.procBtnPress)
        proc_Ly = QHBoxLayout()
        proc_Ly.addWidget(self.proc_E)
        proc_Ly.addWidget(proc_Btn)

        self.window_Ly.addLayout(proc_Ly)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('setup/processors.html')

        bottom_Ly = QHBoxLayout()
        bottom_Ly.addStretch()
        bottom_Ly.addWidget(self.helpBar)
        bottom_Ly.addWidget(self.btnBar)
        self.window_Ly.addLayout(bottom_Ly)

        self.win.setLayout(self.window_Ly)

    def preProcBtnPress(self):
        '''
        :method: Called at the time the user select the pre-proc change
                 button. Does prepare and execute the according file
                 change dialog.
        '''
        logging.debug(self.__className + '.preProcBtnPress')

        # Do platform specific if here as the PreProx extensions are different
        if platform.system() == "Windows":
            fileName = QFileDialog.getOpenFileName(
                            None,
                            _('Select Pre_Processor'),
                            "",
                            "Executable (*.exe)")
        elif platform.system() == "Linux":
            fileName = QFileDialog.getOpenFileName(
                            None,
                            _('Select Pre_Processor'),
                            "",
                            "Compiled Fortran (*.o *.out)")
        else:
            logging.error("Sorry, your operating system is not supported yet")
            return

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the
            # dialog an empty tuple is retured
            # Write the info to the config reader
            logging.debug(self.__className
                          + '.setupPreProcLocation Path and Name '
                          + fileName[0])

            self.preProc_E.setText(fileName[0])
            self.confRdr.setPreProcPathName(fileName[0])

    def procBtnPress(self):
        '''
        :method: Called at the time the user select the proc change button.
                 Does prepare and execute the according file change dialog.
        '''
        logging.debug(self.__className + '.procBtnPress')

        # Do platform specific if here as the PreProx extensions are different
        if platform.system() == "Windows":
            fileName = QFileDialog.getOpenFileName(
                            None,
                            _('Select Processor'),
                            "",
                            "Executable (*.exe)")
        elif platform.system() == "Linux":
            fileName = QFileDialog.getOpenFileName(
                            None,
                            _('Select Processor'),
                            "",
                            "Compiled Fortran (*.o *.out)")
        else:
            logging.error("Sorry, your operating system is not supported yet")
            return

        if fileName != ('', ''):
            # User has really selected a file, if it would have aborted the
            # dialog an empty tuple is retured.
            # Write the info to the config reader
            logging.debug(self.__className
                          + '.setupProcLocation Path and Name '
                          + fileName[0])

            self.proc_E.setText(fileName[0])
            self.confRdr.setProcPathName(fileName[0])

    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className + '.btnPress')
        if q == 'Apply':
            pass

        elif q == 'Ok':
            self.close()

        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className
                          + '.btnPress unrecognized button press '
                          + q)
