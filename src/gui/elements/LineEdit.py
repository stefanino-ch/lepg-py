"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to

https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-
using-qvalidator/ for the qvalidator explanations
"""
import logging
from PyQt6.QtCore import QEvent, QRegularExpression
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QValidator, QIntValidator, QDoubleValidator, \
                         QRegularExpressionValidator


class LineEdit(QLineEdit):
    """
    :class: Subclasses QLineEdit to add additional functionality.
    """
    __className = 'LineEdit'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    __hasIntValidator = False
    ''':attr: True if IntValidator has been set.'''

    __hasDoubleValidator = False
    ''':attr: True if DoubleValidator has been set.'''

    __hasRegExpValidator = False
    ''':attr: True if RegExpValidator has been set.'''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className+'.__init__')

        super().__init__()
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
                self.__helpBar.set_text(self.__helpText)

            elif event.type() == QEvent.Leave:
                self.__helpBar.clear_text()

            # elif event.type() == QEvent.KeyRelease:
            #     self.checkContent()

        return super(LineEdit, self).eventFilter(source, event)

    def setHelpBar(self, helpBar):
        """
        :method: Configure the help bar of a specific window where the user
                 help text shall be displayed during program execution.
        :param helpBar: Instance of the respective help bar to work with
        """
        logging.debug(self.__className+'.set_help_bar')
        self.__helpBar = helpBar

    def setHelpText(self, helpText):
        """
        :method: Herein you set the help text for each LineEdit which shall
                 be displayed if the mouse pointer is located above the
                 LineEdit or during data edit.
        :param helpText: Help text to be displayed
        """
        logging.debug(self.__className+'.set_help_text')
        self.__helpText = helpText

    def enableIntValidator(self, bottom, top):
        """
        :method: Creates an IntValidator and sets it for the current line edit.
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        """
        logging.debug(self.__className+'.en_int_validator')
        self.validator = QIntValidator(bottom, top)
        self.setValidator(self.validator)
        self.__hasIntValidator = True

    def enableDoubleValidator(self, bottom, top, decimals=0):
        '''
        :method: Creates an DoubleValidator and sets it for the
                 current line edit.
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        :param decimals: number of decimals to be checked
        '''
        logging.debug(self.__className+'.en_double_validator')
        self.validator = QDoubleValidator(bottom, top, decimals)
        self.setValidator(self.validator)
        self.__hasDoubleValidator = True

    def enableRegExpValidator(self, regexp):
        """
        Creates an RegExpValidator and sets it to the current line edit.

        :param regexp: the RegExp to be applied to the validator.
        """
        logging.debug(self.__className+'.en_reg_exp_validator')
        rx = QRegExp(regexp)
        self.validator = QRegExpValidator(rx, self)
        self.setValidator(self.validator)
        self.__hasRegExpValidator = True

    def checkContent(self):
        """
        :method: Does check the content of a line edit with the help of the
                 applied validator. Depending on the check result the
                 background of the line edit is changed.
        """
        logging.debug(self.__className+'.checkContent')
        if self.__hasDoubleValidator or self.__hasIntValidator:
            state = self.validator.validate(self.text(), 0)[0]
            if state == QValidator.Acceptable:
                color = '#c4df9b'
            elif state == QValidator.Intermediate:
                color = '#fff79a'
            else:
                color = '#f6989d'
            self.setStyleSheet('QLineEdit {background-color: %s }' % color)

        elif self.__hasRegExpValidator:
            state = self.validator.validate(self.text(), 0)[0]
            if state == QRegExpValidator.Acceptable:
                color = '#c4df9b'
            elif state == QRegExpValidator.Intermediate:
                color = '#fff79a'
            else:
                color = '#f6989d'
            self.setStyleSheet('QLineEdit {background-color: %s }' % color)

    def setText(self, *args, **kwargs):
        """
        :method: Calls first the super class to set the text and triggers
                 afterwards the value check making sure the background is set
                 according to the verification result.
        """
        logging.debug(self.__className+'.set_text')
        QLineEdit.setText(self, *args, **kwargs)
        return
