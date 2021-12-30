"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QCheckBox


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
        logging.debug(self.__className + '.__init__')

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
            if event.type() == QEvent.Enter:
                self.__helpBar.setText(self.__helpText)

            elif event.type() == QEvent.Leave:
                self.__helpBar.clearText()

        return super(CheckBox, self).eventFilter(source, event)

    def setHelpBar(self, helpBar):
        """
        :method: Configure the help bar of a specific window where the user
                 help text shall be displayed during program execution.
        :param helpBar: Instance of the respective help bar to work with
        """
        logging.debug(self.__className+'.setHelpBar')
        self.__helpBar = helpBar

    def setHelpText(self, helpText):
        """
        :method: Herein you set the help text for each element which shall
                 be displayed if the mouse pointer is located over it.
        :param helpText: Help text to be displayed
        """
        logging.debug(self.__className+'.setHelpText')
        self.__helpText = helpText