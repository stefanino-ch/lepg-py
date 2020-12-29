'''
The onw implementation of QLineEdit with some program specific enhancements. 

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QLineEdit

class LineEdit(QLineEdit):
    '''
    The onw implementation of QLineEdit with some program specific enhancements. 
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
        Herein you set the help bar of a specific window where the user help text
        shall be displayed during program execution. 
        
        @param helpBar: Instance of the respecitive help bar to work with
        '''
        self.__helpBar = helpBar
        
    def setHelpText(self, helpText):
        '''
        Herein you set the help text for each LineEdit which shall be displayed if 
        the mouse pointer is located above the LineEdit or during data edit.   
        
        @param helpText: Help text to be displayed
        '''
        self.__helpText = helpText