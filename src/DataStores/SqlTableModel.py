'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class SqlTableModel(QSqlTableModel):
    '''
    :class: inherits QSqlTableModel and adds a few specific methods, partially sw related, partially to work around some Qt limitations 
    '''
    __className = 'SqlTableModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    
    didSelect = pyqtSignal()
    '''
    :signal: emitted as soon select() was executed on the model. You must know about this fact if you have mappers to LineEdits in place, as the mapping must be redone after every select().
    '''
        
    def __init__(self, parent=None): # @UnusedVariable
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
    
    def removeRowsAtEnd(self, numToRemove):
        '''
        :method: removes one or multiple rows from the end of the table
        :param numToRemove: number of rows to remove
        '''
        logging.debug(self.__className+'.removeRowsAtEnd')
        
        i=0
        start = self.rowCount()-1
        while i < numToRemove:
            res = self.removeRows( start-i , 1)
            i+=1
        self.select() # use as less selects as possible
        return res
    
    def addRows(self, row, count):
        '''
        :method: add one or multiple rows to the model
        :param row: row after which the new rows must be inserted
        :param count: the number of new rows to be inserted
        
        Thanks to https://stackoverflow.com/questions/47318601/inserting-row-into-qsqltablemodel#47319440
        for the example about how to insert.
        '''
        logging.debug(self.__className+ '.addRows')
        
        QSqlDatabase.database().transaction()             
        for i in range( 0, count ):
            numRows = self.rowCount()
            record = self.record()
            record.setValue("ID", numRows+1);
            #-1 is set to indicate that it will be added to the last row*/
            if not self.insertRecord(row+i, record):
                logging.critical(self.__className + '.addRows insertRecord Err type: %s' %self.lastError().type())
                logging.critical(self.__className + '.addRows insertRecord Err text: %s' %self.lastError().text())
                QSqlDatabase.database().rollback()
                return False
            
        if not QSqlDatabase.database().commit():
            logging.critical(self.__className + '.addRows commit Err type: %s' %self.lastError().type())
            logging.critical(self.__className + '.addRows commit Err text: %s' %self.lastError().text())
            return False
        return True
    
    def select(self, *args, **kwargs):
        '''
        :method: overwritten class method. Needed to get a signal back after a select().
        :emits didSelect: the signal telling the consumers that a select() was done on the model
        '''
        logging.debug(self.__className+'.select')
        
        res = QSqlTableModel.select(self, *args, **kwargs)
        self.didSelect.emit()   # Now we must tell the rest of the app that a row has been removed.
        return res
    
    def sortTable(self, row, order):
        '''
        :method: forces the model to sort
        :param: row which is used to sort
        :param order: Qt.AscendingOrder or Qt.DescendingOrder
        '''
        logging.debug(self.__className+'.sortTable')
        self.setSort(row, order)
        self.select()
        
    def setupRibRows(self, halfNumRibs):
        '''
        :method: compares the number of rows currently with what it should be. Add/ removes rows accordingly.
        :param halfNumRibs: the number of rows to be achieved. 
        ''' 
        logging.debug(self.__className+'.setupRibRows')
        self.submitAll()
        
        numRows = self.rowCount()
        if numRows > halfNumRibs:
            numToRemove = numRows-halfNumRibs
            self.removeRowsAtEnd(numToRemove)
        elif numRows < halfNumRibs:
            numToAdd = halfNumRibs - numRows
            self.addRows(numRows, numToAdd)
