"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to the authors of

https://stackoverflow.com/questions/20064975/how-to-catch-mouse-over-event-of-qtablewidget-item-in-pyqt

https://stackoverflow.com/questions/13449971/pyside-pyqt4-how-to-set-a-validator-when-editing-a-cell-in-a-qtableview

https://overthere.co.uk/2012/07/29/using-qstyleditemdelegate-on-a-qtableview/

https://stackoverflow.com/questions/66091468/qtableview-crashes-as-soon-two-validators-with-qstyleditemdelegate-are-set/66091520#66091520

https://stackoverflow.com/questions/10219739/set-color-to-a-qtableview-row
"""
from PyQt6.QtCore import QEvent, QModelIndex, QPersistentModelIndex, Qt
from PyQt6.QtWidgets import QTableView, QStyledItemDelegate
from PyQt6.QtGui import QIntValidator, QDoubleValidator, \
    QRegularExpressionValidator, QBrush, QValidator, QColor

from gui.elements.LineEdit import LineEdit
from gui.ColorDefinition import ColorDefinition


def get_param_length(index, param_length_dict):
    # TODO: Doc

    # Here we assume the parameter number is always on the 2nd column!
    # If the Index.column is 0 or 1 no further checks are needed
    if index.column() <= 1:
        return 2

    param_num = index.siblingAtColumn(1).data(Qt.ItemDataRole.DisplayRole)

    # Check if the parameter is a valid integer
    if isinstance(param_num, int):

        # Check if we have length information for this parameter
        if param_length_dict is not None:

            # Check if the key is part of the length information dict
            if param_num in param_length_dict.keys():
                param_length = param_length_dict[param_num]

                return param_length

    return 0


def validate(index, validator):
    # Todo: Doc

    state = validator.validate(str(index.data(Qt.ItemDataRole.DisplayRole)), 0)[0]
    if state == QValidator.State.Acceptable:
        return QBrush(QColor(ColorDefinition.valAcceptable))
    elif state == QValidator.State.Intermediate:
        return QBrush(QColor(ColorDefinition.valIntermediate))
    else:
        return QBrush(QColor(ColorDefinition.valInvalid))


class ValidatedIntItemDelegate(QStyledItemDelegate):
    """
    :class: Creates a delegate limiting the input to a specific int range.
    """
    __className = 'ValidatedIntItemDelegate'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    def __init__(self, bottom, top, param_length_dict=None):
        """
        :method: Class initialization
        :param bottom: lower border of the valid range
        :param top: upper border of the valid range
        """
        QStyledItemDelegate.__init__(self)
        self.bottom = bottom
        self.top = top
        self.param_length_dict = param_length_dict
        self.editor = None
        self.validator = QIntValidator(bottom, top)
    
    def createEditor(self, parent, option, index):
        self.editor = LineEdit(parent)
        self.editor.en_int_validator(self.bottom, self.top)
        return self.editor

    def calculate_color_for_column(self, index):
        # TODO: Doc

        param_length = get_param_length(index, self.param_length_dict)
        if index.column() >= param_length:
            return QBrush(QColor(ColorDefinition.valNotUsed))

        return validate(index, self.validator)

    def initStyleOption(self, option, index):
        # TODO: Doc

        super(ValidatedIntItemDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = self.calculate_color_for_column(index)


class ValidatedDoubleItemDelegate(QStyledItemDelegate):
    """
    :class: Creates a delegate limiting the input to a specific double range.
    """
    def __init__(self, bottom, top, decimals=0, param_length_dict=None):
        """
        :method: Class initialization
        :param bottom: lower border of the valid range
        :param top: upper border of the valid range
        :param decimals: number of decimals allowed
        """
        QStyledItemDelegate.__init__(self)
        self.bottom = bottom
        self.top = top
        self.decimals = decimals
        self.param_length_dict = param_length_dict
        self.editor = None
        self.validator = QDoubleValidator(bottom, top, decimals)
    
    def createEditor(self, parent, option, index):
        self.editor = LineEdit(parent)
        self.editor.en_double_validator(self.bottom, self.top, self.decimals)
        return self.editor

    def calculate_color_for_column(self, index):
        # TODO: Doc

        param_length = get_param_length(index, self.param_length_dict)
        if index.column() >= param_length:
            return QBrush(QColor(ColorDefinition.valNotUsed))

        return validate(index, self.validator)

    def initStyleOption(self, option, index):
        # TODO: Doc

        super(ValidatedDoubleItemDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = self.calculate_color_for_column(index)


class ValidatedRegExpItemDelegate(QStyledItemDelegate):
    """
    :class: Creates a delegate limiting the input to a specific RegExp.
    """
    def __init__(self, regexp, param_length_dict=None):
        """
        :method: Class initialization
        :param regexp: lower border of the valid range
        """
        QStyledItemDelegate.__init__(self)
        self.regexp = regexp
        self.param_length_dict = param_length_dict
        self.editor = None
        self.validator = QRegularExpressionValidator(regexp, self)
    
    def createEditor(self, parent, option, index):
        self.editor = LineEdit(parent)
        self.editor.en_reg_exp_validator(self.regexp)
        return self.editor

    def calculate_color_for_column(self, index):
        # TODO: Doc

        param_length = get_param_length(index, self.param_length_dict)
        if index.column() >= param_length:
            return QBrush(QColor(ColorDefinition.valNotUsed))

        return validate(index, self.validator)

    def initStyleOption(self, option, index):
        # TODO: Doc

        super(ValidatedRegExpItemDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = self.calculate_color_for_column(index)


class TableView(QTableView):
    """
    :class: Subclasses QLineEdit to add additional functionality
    """
    def __init__(self, *args, **kwargs):
        """
        :method: Class initialization
        """
        QTableView.__init__(self, *args, **kwargs)
        
        self.__helpBar = None
        self.__helpText = ['']
        self.__paramLength = None
        self._last_index = QPersistentModelIndex()
        self.setMouseTracking(True)
        self.viewport().installEventFilter(self)
        
        self.intDelegate = []
        self.doubleDelegate = []
        self.regExpDelegate = []
    
    def eventFilter(self, widget, event):
        """
        :method: Catches specific events and controls (the updates of the help
        window and the validation of the user inputs).
        """
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QEvent.Type.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QEvent.Type.Leave:
                index = QModelIndex()
                if self.__helpBar is not None:
                    self.__helpBar.clear_text()
            if index != self._last_index:
                column = index.column()
                if (self.__helpBar is not None) and column >= 0:
                    self.__helpBar.set_text(self.__helpText[column])
                self._last_index = QPersistentModelIndex(index)
        return QTableView.eventFilter(self, widget, event)

    def set_help_bar(self, help_bar):
        """
        :method: Configure the help bar of a specific window where the user
                    help text shall be displayed during program execution
        :param help_bar: Instance of the respective help bar to work with
        """
        self.__helpBar = help_bar
        
    def set_help_text(self, column, help_text):
        """
        :method: Herein you set the help text for each LineEdit which shall be
                    displayed if the mouse pointer is located above the
                    LineEdit or during data edit
        :param column: number of the column for which the text will be set
        :param help_text: Help text to be displayed
        """
        length = len(self.__helpText)
        if length <= column:
            # add columns
            missing_cols = (column - length) + 1
            i = 0
            while i < missing_cols:
                self.__helpText.append('')
                i += 1
        self.__helpText[column] = help_text
    
    def en_int_validator(self, first_col, last_col, bottom, top, param_length_dict=None):
        """
        :method: Limits one or multiple columns to a specific int input range
        :param first_col: first col of the table where the validator should be set
        :param last_col: last col of the table where the validator should be set
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        :param param_length_dict: dictionary containing the length (number of values) for the individual parameter lines
        """
        self.intDelegate.append(ValidatedIntItemDelegate(bottom, top, param_length_dict))
        index = len(self.intDelegate)-1
        
        i = first_col
        while i <= last_col:
            self.setItemDelegateForColumn(i, self.intDelegate[index])
            i += 1

    def en_double_validator(self, first_ol, last_col, bottom, top, decimals=0, param_length_dict=None):
        """
        :method: Limits one or multiple columns to a specific double
                    input range
        :param first_ol: first col of the table where the validator
                    should be set
        :param last_col: last col of the table where the validator
                    should be set
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        :param decimals: number of decimals allowed
        :param param_length_dict: dictionary containing the length (number of values) for the individual parameter lines
        """
        self.doubleDelegate.append(
            ValidatedDoubleItemDelegate(bottom, top, decimals, param_length_dict))
        index = len(self.doubleDelegate)-1
        
        i = first_ol
        while i <= last_col:
            self.setItemDelegateForColumn(i, self.doubleDelegate[index])
            i += 1
        
    def en_reg_exp_validator(self, first_col, last_col, regexp, param_length_dict=None):
        """
        :method: Limits one or multiple columns to a specific RegExp
        :param first_col: first col of the table where the validator should
                            be set
        :param last_col: last col of the table where the validator should be set
        :param regexp: the RegExp to be applied to the validator
        :param param_length_dict: dictionary containing the length (number of values) for the individual parameter lines
        """
        self.regExpDelegate.append(ValidatedRegExpItemDelegate(regexp, param_length_dict))
        index = len(self.regExpDelegate)-1
        
        i = first_col
        while i <= last_col:
            self.setItemDelegateForColumn(i, self.regExpDelegate[index])
            i += 1
