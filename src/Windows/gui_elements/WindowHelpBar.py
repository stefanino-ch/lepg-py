'''
@Author: Stefan Feuz; http://www.laboratoridenvol.com
@License: General Public License GNU GPL 3.0
'''
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor


class WindowHelpBar(QWidget):
    '''
    :class: Displays the standard window showing the user help text.
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        super().__init__()

        # Define GUI elements and connects
        self.helpWindow = QLabel()
        self.helpWindow.setFixedSize(300, 75)

        palette = QPalette(self.helpWindow.palette())
        palette.setColor(QPalette.Background, QColor('white'))
        self.helpWindow.setPalette(palette)
        self.helpWindow.setAutoFillBackground(True)

        # Explanation
        layout = QGridLayout()
        layout.addWidget(self.helpWindow, 0, 0)

        self.setLayout(layout)

    def setText(self, helpText):
        '''
        :method: Displays a text message in the help window.
        :parameter helpText: Text to be displayed
        '''
        self.helpWindow.setText(helpText)

    def clearText(self):
        '''
        :method: Clears the help window.
        '''
        self.helpWindow.setText('')
