'''
@Author: Stefan Feuz; http://www.laboratoridenvol.com
@License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMdiSubWindow,\
                            QWidget,\
                            QGridLayout,\
                            QTextEdit,\
                            QSizePolicy

from gui.elements.WindowBtnBar import WindowBtnBar


class ProcessorOutput(QMdiSubWindow):
    '''
    :class: Window displaying the output of both of the processors
    '''
    __className = 'ProcessorOutput'

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
        :method: Builds the window.

        Structure::

            win
                windowGrid
                    debugOut

                    btn_bar
        '''
        self.setWindowIcon(QIcon('gui\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(700, 400)

        self.windowGrid = QGridLayout()
        self.__winGridRow = 0

        #############################
        # Add window specifics here
        self.setWindowTitle("Processor output")

        self.debugOut = QTextEdit()
        self.font = QFont("TypeWriter")
        self.font.setPointSize(8)
        self.font.setFixedPitch(True)
        self.debugOut.setFont(self.font)

        self.windowGrid.addWidget(self.debugOut,
                                  self.__winGridRow,
                                  0)
        self.__winGridRow += 1

        #############################
        # Rest of standard window setups
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/procOutput.html')

        self.windowGrid.addWidget(self.btnBar,
                                  self.__winGridRow,
                                  0,
                                  Qt.AlignRight)
        self.__winGridRow += 1

        self.win.setLayout(self.windowGrid)

    def appendText(self, string):
        '''
        :method: Does append text at the end of the message view.
        '''
        self.debugOut.append(string)

    def btnPress(self, q):
        '''
        :method: Handles button functionality within the window.
        '''
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__className
                          + '.btn_press unrecognized button press '
                          + q)
