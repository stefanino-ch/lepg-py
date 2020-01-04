'''
Created on 07.12.2019

@author: User
'''
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor

class WindowHelpBar(QWidget):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        
        [ Help Window       ]
        
        [Apply] [Ok] [Cancel]
                     [Help]
        '''
        super().__init__()
        
        # Define GUI elements and connects
        self.helpWindow = QLabel()
        self.helpWindow.setFixedSize(300,75)
        
        palette = QPalette(self.helpWindow.palette())
        palette.setColor(QPalette.Background, QColor('white'))
        self.helpWindow.setPalette(palette)
        self.helpWindow.setAutoFillBackground(True)
               
        # Explanation
        layout = QGridLayout()
        layout.addWidget(self.helpWindow,0,0)
        
        self.setLayout(layout)
        
    def setText(self, helpText):
        self.helpWindow.setText(helpText)
        
    def clearText(self):
        self.helpWindow.setText('')