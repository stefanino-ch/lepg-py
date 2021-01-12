'''
Window displaying
    the output of both of the processors
    

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.Qt import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QGridLayout, QTextEdit, QSizePolicy

from Windows.WindowBtnBar import WindowBtnBar

class ProcessorOutput(QMdiSubWindow):
    '''
    Window displaying
        the output of both of the processors
    '''
    __className = 'ProcessorOutput'

    def __init__(self):
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.buildWindow()
    
    def closeEvent(self, event):  # @UnusedVariable
        logging.debug(self.__className+'.closeEvent')
    
    def buildWindow(self):
        '''
        Builds the window. 
        
        Structure:
            win
                windowGrid
                    debugOut
                    
                    btnBar
        '''
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
                
        self.windowGrid = QGridLayout()
        self.__winGridRow = 0

        #############################
        # Add window specifics here
        self.setWindowTitle("Processor output")
        
        self.debugOut = QTextEdit()
        self.font = QFont("TypeWriter")
        self.font.setPointSize(8)
        self.font.setFixedPitch(True)
        self.debugOut.setFont(self.font);
        self.debugOut.setFixedWidth(650)
        
        self.windowGrid.addWidget(self.debugOut, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        #############################
        # Rest of standard window setups
        self.btnBar = WindowBtnBar( 0b0100 )
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        
        self.windowGrid.addWidget(self.btnBar, self.__winGridRow ,0, Qt.AlignRight)
        self.__winGridRow += 1
        
        self.win.setLayout(self.windowGrid)
    
    def appendText(self, string):
        self.debugOut.append(string)
            
    def btnPress(self, q):
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__className+'.btnPress unrecognized button press '+q)
        
