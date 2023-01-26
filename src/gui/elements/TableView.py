'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to 

https://stackoverflow.com/questions/20064975/how-to-catch-mouse-over-event-of-qtablewidget-item-in-pyqt

https://stackoverflow.com/questions/13449971/pyside-pyqt4-how-to-set-a-validator-when-editing-a-cell-in-a-qtableview

https://overthere.co.uk/2012/07/29/using-qstyleditemdelegate-on-a-qtableview/

https://stackoverflow.com/questions/66091468/qtableview-crashes-as-soon-two-validators-with-qstyleditemdelegate-are-set/66091520#66091520
'''
import logging
from PyQt5.QtCore import QEvent, QModelIndex, QPersistentModelIndex, QRegExp
from PyQt5.QtWidgets import QTableView, QStyledItemDelegate, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator

class ValidatedIntItemDelegate(QStyledItemDelegate):
    '''
    :class: creates a delegate limiting the input to a specific int range.
    ''' 
    __className = 'ValidatedIntItemDelegate'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    def __init__(self, bottom, top):
        '''
        :method: Constructor
        :param bottom: lower border of the valid range
        :param top: upper border of the valid range
        '''
        logging.debug(self.__className+'.__init__')
        QStyledItemDelegate.__init__(self)
        self.bottom = bottom
        self.top = top
    
    def createEditor(self, widget, option, index): # @UnusedVariable
        logging.debug(self.__className+'.createEditor')
        editor = QLineEdit(widget)
        validator = QIntValidator(self.bottom, self.top)
        editor.setValidator(validator)
        return editor 

class ValidatedDoubleItemDelegate(QStyledItemDelegate):
    '''
    :class: creates a delegate limiting the input to a specific double range.
    '''
    __className = 'ValidatedDoubleItemDelegate'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    def __init__(self, bottom, top, decimals=0):
        '''
        :method: Constructor
        :param bottom: lower border of the valid range
        :param top: upper border of the valid range
        :param decimals: number of decimals allowed
        '''
        logging.debug(self.__className+'.__init__')
        QStyledItemDelegate.__init__(self)
        self.bottom = bottom
        self.top = top
        self.decimals = decimals
    
    def createEditor(self, widget, option, index): # @UnusedVariable
        logging.debug(self.__className+'.createEditor')
        editor = QLineEdit(widget)
        validator =  QDoubleValidator(self.bottom, self.top, self.decimals)
        editor.setValidator(validator)
        return editor
    
class ValidatedRegExpItemDelegate(QStyledItemDelegate):
    '''
    :class: creates a delegate limiting the input to a specific RegExp.
    '''
    __className = 'ValidatedRegExpItemDelegate'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    def __init__(self, regexp):
        '''
        :method: Constructor
        :param regexp: lower border of the valid range
        '''
        logging.debug(self.__className+'.__init__')
        QStyledItemDelegate.__init__(self)
        self.regexp = regexp
    
    def createEditor(self, widget, option, index): # @UnusedVariable
        logging.debug(self.__className+'.createEditor')
        editor = QLineEdit(widget)
        rx = QRegExp(self.regexp)
        validator =  QRegExpValidator( rx , self)
        editor.setValidator(validator)
        return editor

class TableView(QTableView):
    '''
    :class: Subclasses QLineEdit to add additional functionality 
    '''
    __className = 'TableView'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    
    def __init__(self, *args, **kwargs):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        QTableView.__init__(self, *args, **kwargs)
        
        self.__helpBar = None
        self.__helpText = [''] 
        self._last_index = QPersistentModelIndex()
        self.setMouseTracking(True)
        self.viewport().installEventFilter(self)
        
        self.intDelegate = []
        self.doubleDelegate = []
        self.regExpDelegate = []
    
    def eventFilter(self, widget, event):
        '''
        :method: Catches specific events and controls (the updates of the help window and the validation of the user inputs).
        '''
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QEvent.Leave:
                index = QModelIndex()
                if self.__helpBar != None:
                    self.__helpBar.clearText()
            if index != self._last_index:
                column = index.column()
                if (self.__helpBar != None) and column >= 0:
                    self.__helpBar.setText(self.__helpText[column])
                self._last_index = QPersistentModelIndex(index)
        return QTableView.eventFilter(self, widget, event)

    def setHelpBar(self, helpBar): 
        '''
        :method: Configure the help bar of a specific window where the user help text shall be displayed during program execution. 
        :param helpBar: Instance of the respecitive help bar to work with
        '''
        logging.debug(self.__className+'.setHelpBar')
        self.__helpBar = helpBar
        
    def setHelpText(self, column, helpText):
        '''
        :method: Herein you set the help text for each LineEdit which shall be displayed if the mouse pointer is located above the LineEdit or during data edit.   
        :param column: number of the column for which the text will be set. 
        :param helpText: Help text to be displayed
        '''
        logging.debug(self.__className+'.set_help_text')
        length = len(self.__helpText)
        if length <= column:
            # add columns
            missingCols = (column - length) + 1
            i=0
            while i < missingCols:
                self.__helpText.append('')
                i += 1
        self.__helpText[column] = helpText
    
    def enableIntValidator(self, firstCol, lastCol, bottom, top):
        '''
        :method: Limits one ore multiple columns to a specific int input range
        :param firstRow: first row of the table where the validator should be set
        :param lastRow: last row of the table where the validator should be set
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        '''
        logging.debug(self.__className+'.enable_int_validator')
        self.intDelegate.append( ValidatedIntItemDelegate(bottom, top) )
        index = len(self.intDelegate)-1
        
        i = firstCol
        while i<= lastCol:
            self.setItemDelegateForColumn(i, self.intDelegate[index])
            i += 1

            
    def enableDoubleValidator(self, firstCol, lastCol, bottom, top, decimals=0):
        '''
        :method: Limits one ore multiple columns to a specific double input range
        :param firstRow: first row of the table where the validator should be set
        :param lastRow: last row of the table where the validator should be set
        :param bottom: lower value of validation border
        :param top: upper value of validation border
        :param decimals: number of decimals allowed
        '''
        logging.debug(self.__className+'.enable_double_validator')
        self.doubleDelegate.append( ValidatedDoubleItemDelegate(bottom, top, decimals) )
        index = len(self.doubleDelegate)-1
        
        i = firstCol
        while i<= lastCol:
            self.setItemDelegateForColumn(i, self.doubleDelegate[index])
            i += 1
        
    def enableRegExpValidator(self, firstCol, lastCol, regexp):
        '''
        :method: Limits one ore multiple columns to a specific RegExp
        :param firstRow: first row of the table where the validator should be set
        :param lastRow: last row of the table where the validator should be set
        :param regexp: the RegExp to be applied to the validator.
        '''
        logging.debug(self.__className+'.enable_reg_exp_validator')
        self.regExpDelegate.append( ValidatedRegExpItemDelegate(regexp) )
        index = len(self.regExpDelegate)-1
        
        i = firstCol
        while i<= lastCol:
            self.setItemDelegateForColumn(i, self.regExpDelegate[index])
            i += 1
