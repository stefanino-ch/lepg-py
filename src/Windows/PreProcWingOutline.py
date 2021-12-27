'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget,\
                            QSizePolicy
from Windows.gui_elements.WindowHelpBar import WindowHelpBar
from Windows.gui_elements.WindowBtnBar import WindowBtnBar


class PreProcWingOutline(QMdiSubWindow):
    '''
    :class: Window to display the wing outline calculated by the
            PreProcessor.
    '''

    __className = 'PreProcWingOutline'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()

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
                windowLayout
                     Gen Table
                     LE Table
                     TE Table
                     Vault Table
                    ---------------------------
                                helpBar | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')

        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 400)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Wing outline"))

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('preproc/wingOutline.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)

        self.win.setLayout(self.windowLayout)

    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className+'.btnPress')
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
