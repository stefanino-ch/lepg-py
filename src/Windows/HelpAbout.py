'''
@Author: Stefan Feuz; http://www.laboratoridenvol.com
@License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy
from PyQt5.QtWidgets import QLabel

from __init__ import __version__

from Windows.WindowBtnBar import WindowBtnBar

class HelpAbout(QMdiSubWindow):
    '''
    Window displaying 
        The help about information
    '''
    __className = 'HelpAbout'

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
                    helpAboutTitleL
                    helpAboutTextL
                    helpAboutDevL
                    helpAboutLicL
                    
                    btnBar
        '''
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
                
        self.windowGrid = QGridLayout()
        self.__winGridRow = 0

        #############################
        # Add window specifics here
        self.setWindowTitle("Help about")
        
        self.helpAboutTitleL = QLabel(_('lepg-py'))
        #set font
        self.font = QFont()
        self.font.setPointSize(20);
        self.font.setBold(True);
        self.helpAboutTitleL.setFont(self.font);
        
        
        self.windowGrid.addWidget(self.helpAboutTitleL, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        self.helpAboutTextL = QLabel(_('A graphical frontend to lepg\nCurrent Version \t\t\t%s') %(__version__))
        self.windowGrid.addWidget(self.helpAboutTextL, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        self.helpAboutDevL = QLabel(_('Developers: \nStefan Feuz'))
        self.windowGrid.addWidget(self.helpAboutDevL, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        self.helpAboutLicL = QLabel(_('General Public License GNU GPL 3.0'))
        self.windowGrid.addWidget(self.helpAboutLicL, self.__winGridRow, 0, Qt.AlignLeft)
        self.__winGridRow += 1
        
        #############################
        # Rest of standard window setups
        self.btnBar = WindowBtnBar( 0b0100 )
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        
        self.windowGrid.addWidget(self.btnBar, self.__winGridRow ,0, Qt.AlignRight)
        self.__winGridRow += 1
        
        self.win.setLayout(self.windowGrid)
            
    def btnPress(self, q):
        if q == 'Ok':
            self.close()
        else:
            logging.error(self.__className+'.btnPress unrecognized button press '+q)
        