'''
Displays the standard window showing the user help text.

@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor

class WindowHelpBar(QWidget):
    '''
    Displays the standard window showing the user help text.
    '''

    def __init__(self):
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