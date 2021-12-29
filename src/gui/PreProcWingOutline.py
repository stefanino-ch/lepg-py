"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget,\
                            QSizePolicy
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar


class PreProcWingOutline(QMdiSubWindow):
    """
    :class: Window to display the wing outline calculated by the
            PreProcessor.
    """

    __className = 'PreProcWingOutline'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        super().__init__()

        self.__open_pre_proc_file = False  # type: bool
        self.button_bar = None
        self.help_bar = None
        self.window_ly = None
        self.window = None
        
        logging.debug(self.__className + '.__init__')
        
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

                    ---------------------------
                                help_bar | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.window = QWidget()
        self.setWidget(self.window)
        self.window.setMinimumSize(900, 400)

        self.window_ly = QVBoxLayout()

        self.help_bar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Wing outline"))

        #############################
        # Commons for all windows
        self.button_bar = WindowBtnBar(0b0101)
        self.button_bar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                                  QSizePolicy.Fixed))
        self.button_bar.my_signal.connect(self.button_press)
        self.button_bar.setHelpPage('preproc/wingOutline.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_bar)
        bottom_layout.addWidget(self.button_bar)
        self.window_ly.addLayout(bottom_layout)

        self.window.setLayout(self.window_ly)

    def open_pre_proc_file(self, open_pre_proc_file=False):
        """
        :method: Control what data source will be read at the time the window
                 is opened
        :param open_pre_proc_file:
                 False do not open a file, show the empty window
                 True open the file from the pre-processor folder
        """
        self.__open_pre_proc_file = open_pre_proc_file

    def button_press(self, q):
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
            logging.error(self.__className
                          + '.btn_press unrecognized button press '
                          + q)
