"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QCheckBox


class CheckBox(QCheckBox):
    """
        :class: Subclasses QCheckBox to add additional functionality.
        """
    __className = 'LineEdit'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self, *args, **kwargs):
        """
        :method: Constructor
        """
        super().__init__(*args, **kwargs)
        self.__helpBar = None
        self.__helpText = ''
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        """
        :method: Catches specific events and controls the updates of the help
                 window and the validation of the user inputs.
        """
        if self.__helpBar is not None:
            if event.type() == QEvent.Type.Enter:
                self.__helpBar.set_text(self.__helpText)

            elif event.type() == QEvent.Type.Leave:
                self.__helpBar.clear_text()

        return super(CheckBox, self).eventFilter(source, event)

    def set_help_bar(self, help_bar):
        """
        :method: Configure the help bar of a specific window where the user
                 help text shall be displayed during program execution.
        :param help_bar: Instance of the respective help bar to work with
        """
        self.__helpBar = help_bar

    def set_help_text(self, help_text):
        """
        :method: Herein you set the help text for each element which shall
                 be displayed if the mouse pointer is located over it.
        :param help_text: Help text to be displayed
        """
        self.__helpText = help_text
