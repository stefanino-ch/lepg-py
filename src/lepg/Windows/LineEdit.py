'''
Created on 28.12.2019

@author: User
'''
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QLineEdit

class LineEdit(QLineEdit):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        
        self.__helpBar = None
        self.__helpText = '' 
        self.installEventFilter(self)
    
    def eventFilter(self, source, event):
        if self.__helpBar != None:
            if event.type() == QEvent.Enter:
                self.__helpBar.setText(self.__helpText)
    
            elif event.type() == QEvent.Leave:
                self.__helpBar.clearText()
                
        return super(LineEdit, self).eventFilter(source, event)

    def setHelpBar(self, helpBar):
        '''
        TODO: add description
        '''
        self.__helpBar = helpBar
        
    def setHelpText(self, helpText):
        self.__helpText = helpText