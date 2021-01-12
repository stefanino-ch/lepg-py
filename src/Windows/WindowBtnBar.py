'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''

import os
import webbrowser


from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from ConfigReader.ConfigReader import ConfigReader

class WindowBtnBar(QWidget):
    '''
    :class: Displays the standard buttons under each data window. 
    
    Button Layout::
    
        [Apply] [Ok] [Cancel]
                     [Help]
                     
    Bitmask controlling which buttons will be displayed::
    
        Apply    0b1000
        Ok       0b0100
        Cancel   0b0010
        Help     0b0001
    '''
    my_signal = pyqtSignal(str)
    '''
    :Signal: Will be emitted upon button press. The Strind indicates the name of the pressed button. 
    '''
    
    def __init__(self, buttons = 0b1111):
        '''
        :class: Constructor
        
        :param buttons: A bitmask defining which of the buttons shall be displayed. 
        '''
        super().__init__()
        
        self.__helpPage = 'index.html'
        '''
        :attr: the user help page which will be opened if not an individual file was configured
        '''
        
        layout = QGridLayout()
        
        # Define GUI elements and connects
        if buttons & 0b1000 : 
            self.applyBtn = QPushButton('Apply')
            self.applyBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            self.applyBtn.clicked.connect(self.applyBtnPress)
            layout.addWidget(self.applyBtn,0,0)
        
        if buttons & 0b0100 :
            self.okBtn = QPushButton('Ok')
            self.okBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            self.okBtn.clicked.connect(self.okBtnPress)
            layout.addWidget(self.okBtn,0,1)
        
        if buttons & 0b0010 :
            self.cancelBtn = QPushButton('Cancel')
            self.cancelBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            self.cancelBtn.clicked.connect(self.cancelBtnPress)
            layout.addWidget(self.cancelBtn,0,2)
        
        if buttons & 0b0001 :
            self.helpBtn = QPushButton('Help')
            self.helpBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            self.helpBtn.clicked.connect(self.helpBtnPress)
            layout.addWidget(self.helpBtn,1,2)
        
        # Explanation
        self.setLayout(layout)
        
    def applyBtnPress(self):
        '''
        :class: Called if the *Apply* button is pressed
        '''
        self.my_signal.emit('Apply')
        
    def okBtnPress(self):
        '''
        :class: Called if the *Ok* button is pressed
        '''
        self.my_signal.emit('Ok')
        
    def cancelBtnPress(self):
        '''
        :class: Called if the *Cancel* button is pressed
        '''
        self.my_signal.emit('Cancel')
        
    def helpBtnPress(self):
        '''
        :class: Called if the *Help* button is pressed
        '''
        config = ConfigReader()
        webbrowser.open( os.path.join(os.getcwd(), 'userHelp', config.getLanguage(), self.__helpPage) )
    
    def setHelpPage(self, helpPage):
        '''
        :class: Set the html page to be displayed upon *Help* button press.
        :param helpPage: the name of the .html file to be opened if the Help Button is pressed. If not set, the main index.html will be opened.
        '''
        self.__helpPage = helpPage
