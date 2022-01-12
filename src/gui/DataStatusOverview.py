"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QGroupBox

from data.PreProcModel import PreProcModel
from data.ProcModel import ProcModel
from gui.elements.WindowBtnBar import WindowBtnBar


class DataStatusOverview(QMdiSubWindow):
    """
    :class: Window displaying: Filenames, if files are saved, if data withing
            windows has been applied
    """

    __className = 'DataStatusOverview'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        self.pre_proc_saved_e = None
        self.btn_bar = None
        self.pre_proc_name_e = None
        self.proc_version_e = None
        self.proc_filename_e = None
        self.pre_proc_vers_e = None
        self.__stringLength = 50
        self.win = None
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.ppm = PreProcModel()
        self.pm = ProcModel()

        self.build_window()

        self.ppm.dataStatusUpdate.connect(self.data_changed)
        self.pm.dataStatusUpdate.connect(self.data_changed)

    def closeEvent(self, event):  # @UnusedVariable
        """
        :method: Called upon window close
        """
        logging.debug(self.__className + '.closeEvent')

    def build_window(self):
        """
        :method: Builds the window.

        Structure::

            window
                windowGrid
                    ---------------------------------
                    pre_proc_grp
                        preProcG
                            all labels for PreProc
                    ---------------------------------
                    ProcF
                        ProcG
                            all labels for Proc
                    ---------------------------------
                    btn_bar
        """
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)

        self.win.setMinimumWidth(450)

        window_ly = QVBoxLayout()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Data Status Overview"))

        pre_proc_grp = QGroupBox()
        pre_proc_grp.setTitle(_("Pre Processor"))
        window_ly.addWidget(pre_proc_grp)

        ##
        pre_proc_gly = QGridLayout()
        pre_proc_grp.setLayout(pre_proc_gly)

        ##
        pre_proc_filename_l = QLabel(_('Filename'))
        self.pre_proc_name_e = QLineEdit(
            self.shorten_path(self.ppm.get_file_name()))
        self.pre_proc_name_e.setReadOnly(True)
        self.pre_proc_name_e.setAlignment(Qt.AlignRight)

        pre_proc_gly.addWidget(pre_proc_filename_l, 0, 0)
        pre_proc_gly.addWidget(self.pre_proc_name_e, 0, 1)
        ##
        pre_proc_vers_l = QLabel(_('File version'))
        self.pre_proc_vers_e = QLineEdit()
        self.pre_proc_vers_e.setReadOnly(True)
        self.pre_proc_vers_e.setText(self.ppm.get_file_version())

        pre_proc_gly.addWidget(pre_proc_vers_l, 1, 0)
        pre_proc_gly.addWidget(self.pre_proc_vers_e, 1, 1)

        pre_proc_saved_l = QLabel(_('File saved'))
        self.pre_proc_saved_e = QLineEdit()
        self.pre_proc_saved_e.setReadOnly(True)
        self.pre_proc_saved_e.setText(self.ppm.file_saved_char())

        pre_proc_gly.addWidget(pre_proc_saved_l, 2, 0)
        pre_proc_gly.addWidget(self.pre_proc_saved_e, 2, 1)

        #############################
        proc_grp = QGroupBox()
        proc_grp.setTitle(_("Processor"))
        window_ly.addWidget(proc_grp)

        ##
        proc_gly = QGridLayout()
        proc_grp.setLayout(proc_gly)

        ##
        proc_filename_l = QLabel(_('Filename'))
        self.proc_filename_e = QLineEdit(
            self.shorten_path(self.pm.get_file_name()))
        self.proc_filename_e.setReadOnly(True)
        self.proc_filename_e.setAlignment(Qt.AlignRight)

        proc_gly.addWidget(proc_filename_l, 0, 0)
        proc_gly.addWidget(self.proc_filename_e, 0, 1)
        ##
        proc_version_l = QLabel(_('File version'))
        self.proc_version_e = QLineEdit(self.pm.get_file_version())
        self.proc_version_e.setReadOnly(True)

        proc_gly.addWidget(proc_version_l, 1, 0)
        proc_gly.addWidget(self.proc_version_e, 1, 1)

        #############################
        # Rest of standard window setups
        self.btn_bar = WindowBtnBar(0b0100)
        self.btn_bar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                               QSizePolicy.Fixed))
        self.btn_bar.my_signal.connect(self.btn_press)

        bottom_ly = QHBoxLayout()
        bottom_ly.addStretch()
        bottom_ly.addWidget(self.btn_bar)
        window_ly.addLayout(bottom_ly)

        self.win.setLayout(window_ly)

    def shorten_path(self, path):
        """
        :method: does shorten the path strings in a way that the filename at
                 the end and only part of the path is shown
        :parameter path: the full path to be shortened
        :returns: the short form of the path
        """
        if len(path) > self.__stringLength:
            return '...' + path[-(self.__stringLength - 3):]
        else:
            return path

    def data_changed(self, n, q):
        """
        :method: Updates the status information displayed in the window
        """
        if n == 'PreProcModel':
            if q == 'FileNamePath':
                self.pre_proc_name_e.setText(
                    self.shorten_path(self.ppm.get_file_name()))

            elif q == 'FileVersion':
                self.pre_proc_vers_e.setText(self.ppm.get_file_version())

            elif q == 'SaveStatus':
                self.pre_proc_saved_e.setText(self.ppm.file_saved_char())

        elif n == 'ProcModel':
            if q == 'FileNamePath':
                self.proc_filename_e.setText(self.shorten_path(self.pm.get_file_name()))

            elif q == 'FileVersion':
                self.proc_version_e.setText(self.pm.get_file_version())

    def btn_press(self, q):
        """
        :method: Takes care about the button events from the window
        """
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__className
                          + '.btn_press unrecognized button press ' + q)
