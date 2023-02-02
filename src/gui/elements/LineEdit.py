"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to the authors of

https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-
using-qvalidator/ for the qvalidator explanations
"""
from PyQt6.QtCore import QEvent, QRegularExpression
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QValidator, QIntValidator, QDoubleValidator, \
                         QRegularExpressionValidator
from gui.ColorDefinition import ColorDefinition


class LineEdit(QLineEdit):
    """
    :class: Subclasses QLineEdit to add additional functionality.
    """
    __hasIntValidator = False
    ''':attr: True if IntValidator has been set.'''

    __hasDoubleValidator = False
    ''':attr: True if DoubleValidator has been set.'''

    __hasRegExpValidator = False
    ''':attr: True if RegExpValidator has been set.'''

    def __init__(self, parent=None):
        """
        :method: Class initialization
        """
        super().__init__(parent)
        self.__helpBar = None
        self.__helpText = ''
        self.validator = None

        self.installEventFilter(self)
        self.textChanged.connect(self.check_content)

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

            # elif event.type() == QEvent.KeyRelease:
            #     self.check_content()

        return super(LineEdit, self).eventFilter(source, event)

    def set_help_bar(self, help_bar):
        """
        :method: Configure the help bar of a specific window where the user
                 help text shall be displayed during program execution.
        :param help_bar: Instance of the respective help bar to work with
        """
        self.__helpBar = help_bar

    def set_help_text(self, help_text):
        """
        :method: Herein you set the help text for each LineEdit which shall
                 be displayed if the mouse pointer is located above the
                 LineEdit or during data edit.
        :param help_text: Help text to be displayed
        """
        self.__helpText = help_text

    def en_int_validator(self, bottom, top):
        """
        :method: Creates an IntValidator and sets it for the current line edit.
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        """
        self.validator = QIntValidator(bottom, top)
        self.__hasIntValidator = True
        self.check_content()

    def en_double_validator(self, bottom, top, decimals=0):
        """
        :method: Creates an DoubleValidator and sets it for the
                 current line edit.
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        :param decimals: number of decimals to be checked
        """
        self.validator = QDoubleValidator(bottom, top, decimals)
        self.__hasDoubleValidator = True
        self.check_content()

    def en_reg_exp_validator(self, regexp):
        """
        Creates an RegExpValidator and sets it to the current line edit.

        :param regexp: the RegExp to be applied to the validator.
        """
        rx = QRegularExpression(regexp)
        self.validator = QRegularExpressionValidator(rx, self)
        self.__hasRegExpValidator = True
        self.check_content()

    def check_content(self):
        """
        :method: Does check the content of a line edit with the help of the
                 applied validator. Depending on the check result the
                 background of the line edit is changed.
        """
        if self.__hasDoubleValidator or self.__hasIntValidator:
            state = self.validator.validate(self.text(), 0)[0]
            if state == QValidator.State.Acceptable:
                color = ColorDefinition.valAcceptable
            elif state == QValidator.State.Intermediate:
                color = ColorDefinition.valIntermediate
            else:
                color = ColorDefinition.valInvalid
            self.setStyleSheet('QLineEdit {background-color: %s }' % color)

        elif self.__hasRegExpValidator:
            state = self.validator.validate(self.text(), 0)[0]
            if state == QRegularExpressionValidator.State.Acceptable:
                color = ColorDefinition.valAcceptable
            elif state == QRegularExpressionValidator.State.Intermediate:
                color = ColorDefinition.valIntermediate
            else:
                color = ColorDefinition.valInvalid
            self.setStyleSheet('QLineEdit {background-color: %s }' % color)

    def setText(self, *args, **kwargs):
        """
        :method: Calls first the super class to set the text and triggers
                 afterwards the value check making sure the background is set
                 according to the verification result.
        """
        QLineEdit.setText(self, *args, **kwargs)
        return
