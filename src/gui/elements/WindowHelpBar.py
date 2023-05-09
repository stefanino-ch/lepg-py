"""
@Author: Stefan Feuz; http://www.laboratoridenvol.com
@License: General Public License GNU GPL 3.0
"""
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPalette, QColor


class WindowHelpBar(QWidget):
    """
    :class: Displays the standard window showing the user help text.
    """

    def __init__(self):
        """
        :method: Constructor
        """
        super().__init__()

        # Define GUI elements and connects
        self.helpWindow = QLabel()
        self.helpWindow.setFixedSize(300, 75)

        palette = QPalette(self.helpWindow.palette())
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))

        self.helpWindow.setPalette(palette)
        self.helpWindow.setAutoFillBackground(True)

        # Explanation
        layout = QGridLayout()
        layout.addWidget(self.helpWindow, 0, 0)

        self.setLayout(layout)

    def set_text(self, help_text):
        """
        :method: Displays a text message in the help window
        :parameter help_text: Text to be displayed
        """
        self.helpWindow.setText(help_text)

    def clear_text(self):
        """
        :method: Clears the help window.
        """
        self.helpWindow.setText('')
