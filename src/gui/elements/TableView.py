"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to the authors of

https://stackoverflow.com/questions/20064975/how-to-catch-mouse-over-event-of-qtablewidget-item-in-pyqt

https://stackoverflow.com/questions/13449971/pyside-pyqt4-how-to-set-a-validator-when-editing-a-cell-in-a-qtableview

https://overthere.co.uk/2012/07/29/using-qstyleditemdelegate-on-a-qtableview/

https://stackoverflow.com/questions/66091468/qtableview-crashes-as-soon-two-validators-with-qstyleditemdelegate-are-set/66091520#66091520

https://stackoverflow.com/questions/10219739/set-color-to-a-qtableview-row

https://stackoverflow.com/questions/75344157/how-to-update-cell-background-color-of-an-inactive-qtableview-qstyleditemdelega
"""
from PyQt6.QtCore import QEvent, QModelIndex, QPersistentModelIndex, Qt, QRegularExpression
from PyQt6.QtWidgets import QTableView, QStyledItemDelegate, QStyle
from PyQt6.QtGui import QIntValidator, QDoubleValidator, \
    QRegularExpressionValidator, QBrush, QValidator, QColor, QPalette

from gui.elements.LineEdit import LineEdit
from gui.GlobalDefinition import BackgroundColorDefinition, BackgroundHighlight


def get_param_length(index, param_length_dict):
    """
    :method: Reads for the line defined with index the effective number of parameters which must be defined
    :param index: Index of the element defining the line for which the number of parameters must be found.
    :param param_length_dict: The dictionary containing parameter num and number of parameters.
    """

    # If there is no param_length_dict all parameters must be checked
    if param_length_dict is None:
        return 99

    # Here we assume the parameter number is always on the 2nd column!
    # If the Index.column is 0 or 1 no further checks are needed
    if index.column() <= 1:
        return 2

    param_num = index.siblingAtColumn(1).data(Qt.ItemDataRole.DisplayRole)

    # Check if the parameter is a valid integer
    if isinstance(param_num, int):

        # Check if the key is part of the length information dict
        if param_num in param_length_dict.keys():
            param_length = param_length_dict[param_num]

            return param_length

    return 0


def validate(index, validator):
    """
    :method: Runs a validator and returns based on validation results the background color for the cell.
    :param index: Index of the element to be validated.
    :param validator: The validator to be used.
    """
    state = validator.validate(str(index.data(Qt.ItemDataRole.DisplayRole)), 0)[0]
    if state == QValidator.State.Acceptable:
        return QBrush(QColor(BackgroundColorDefinition.valAcceptable))
    elif state == QValidator.State.Intermediate:
        return QBrush(QColor(BackgroundColorDefinition.valIntermediate))
    else:
        return QBrush(QColor(BackgroundColorDefinition.valInvalid))


class ValidatedIntItemDelegate(QStyledItemDelegate):
    """
    :class: Creates a delegate limiting the input to a specific int range.
    """
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
        """
        :method: Derives the background color based on parameter value and number of parameters expected based on
                 the data edited
        :param index: Index of the element.
        """
        param_length = get_param_length(index, self.param_length_dict)
        if index.column() >= param_length:
            return QBrush(QColor(BackgroundColorDefinition.valNotUsed))

        return validate(index, self.validator)

    def initStyleOption(self, option, index):
        """
        :method: Changes mainly the background color based on value and position.
        :param option:
        :param index: Index of the element.
        """

        super(ValidatedIntItemDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = self.calculate_color_for_column(index)

        if option.backgroundBrush.style() and option.state & QStyle.StateFlag.State_Selected:
            color = option.backgroundBrush.color()
            option.palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight,
                                    color.darker(BackgroundHighlight.BackgroundHighlightActive))
            option.palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight,
                                    color.darker(BackgroundHighlight.BackgroundHighlightInactive))


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
        """
        :method: Derives the background color based on parameter value and number of parameters expected based on
                 the data edited
        :param index: Index of the element.
        """
        param_length = get_param_length(index, self.param_length_dict)
        if index.column() >= param_length:
            return QBrush(QColor(BackgroundColorDefinition.valNotUsed))

        return validate(index, self.validator)

    def initStyleOption(self, option, index):
        """
        :method: Changes mainly the background color based on value and position.
        :param option:
        :param index: Index of the element.
        """
        super(ValidatedDoubleItemDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = self.calculate_color_for_column(index)

        if option.backgroundBrush.style() and option.state & QStyle.StateFlag.State_Selected:
            color = option.backgroundBrush.color()
            option.palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight,
                                    color.darker(BackgroundHighlight.BackgroundHighlightActive))
            option.palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight,
                                    color.darker(BackgroundHighlight.BackgroundHighlightInactive))


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
        self.rx = QRegularExpression(regexp)
        self.param_length_dict = param_length_dict
        self.editor = None
        self.validator = QRegularExpressionValidator(self.rx, self)
    
    def createEditor(self, parent, option, index):
        self.editor = LineEdit(parent)
        self.editor.en_reg_exp_validator(self.rx)
        return self.editor

    def calculate_color_for_column(self, index):
        """
        :method: Derives the background color based on parameter value and number of parameters expected based on
                 the data edited
        :param index: Index of the element.
        """
        param_length = get_param_length(index, self.param_length_dict)
        if index.column() >= param_length:
            return QBrush(QColor(BackgroundColorDefinition.valNotUsed))

        return validate(index, self.validator)

    def initStyleOption(self, option, index):
        """
        :method: Changes mainly the background color based on value and position.
        :param option:
        :param index: Index of the element.
        """
        super(ValidatedRegExpItemDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = self.calculate_color_for_column(index)

        if option.backgroundBrush.style() and option.state & QStyle.StateFlag.State_Selected:
            color = option.backgroundBrush.color()
            option.palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight,
                                    color.darker(BackgroundHighlight.BackgroundHighlightActive))
            option.palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight,
                                    color.darker(BackgroundHighlight.BackgroundHighlightInactive))


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

        # https://www.youtube.com/watch?v=BH19o9GlN20
        # self.selectionChanged.connect(self.on_selectionChanged)
        # self.

    # def on_selectionChanged(self, selected, deselected):
    #     print(selected, deselected)

    # https://programtalk.com/python-examples/PyQt4.QtGui.QItemSelectionModel.Deselect/
    
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
