'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtCore import pyqtSignal, QSortFilterProxyModel, QRegExp
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

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
    
    numDetailsChanged = pyqtSignal(int, int)
    numRowsForConfigChanged = pyqtSignal(int, int)
        
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


    def setNumConfigs(self, mustNumConfigs):
        '''
        :method: Assures the model will hold at least one row for each config based on the parameter passed. 
        :param mustNumConfigs: Number of configs the model must provide.
        '''
        logging.debug(self.__className+'.setNumConfigs')
        currNumConfigs = self.numConfigs()
        
        diff = abs(mustNumConfigs-currNumConfigs)
        if diff != 0:
            # do it only if really the number has changed
            i = 0
            if mustNumConfigs > currNumConfigs:
                # add config lines
                while i < diff:
                    self.setNumRowsForConfig(currNumConfigs+1+i, 1)
                    self.numRowsForConfigChanged.emit(currNumConfigs+1+i, 1)  # emit the change signal
                    i += 1
            else:
                # remove config lines
                while i < diff:
                    self.setNumRowsForConfig(currNumConfigs-i, 0)
                    self.numRowsForConfigChanged.emit(currNumConfigs-i, 0)  # emit the change signal
                    i += 1


    def numConfigs(self):
        '''
        :method: reads from a table how many different configurations are saved.
        :return: number of different configs
        '''
        logging.debug(self.__className+'.numConfigs')
                
        # TODO: Add transaction
        query = QSqlQuery()
        query.prepare("Select ConfigNum FROM %s ORDER BY ConfigNum ASC" %(self.tableName()) )
        query.exec()
        orderNum = 0
        while (query.next()):
            orderNum = query.value(0)
        
        return orderNum


    def addRowForConfig(self, configNum):
        '''
        :method: Adds a row to the model. Sets Columns *ConfigNum* and *OrderNum*
        :parm configNum: Number of the config for which the row must be added.
        :attention: The two columns *ConfigNum* and *OrderNum* must exist for proper funtionality
        '''
        logging.debug(self.__className+'.addRowForConfig')

        currNumRows = self.numRowsForConfig(configNum)
        
        # TODO: Add transaction
        query = QSqlQuery()
        query.prepare("INSERT into %s (ConfigNum, OrderNum) Values( :conf, :order);" %(self.tableName()))
        query.bindValue(":conf", configNum)
        query.bindValue(":order", currNumRows+1)
        res = query.exec()
        if not res:
                logging.critical(self.__className + '.addRowsForConfig insertRecord Err type: %s' %self.lastError().type())
                logging.critical(self.__className + '.addRowsForConfig insertRecord Err text: %s' %self.lastError().text())
        self.select() # to a select() to assure the model is updated properly

    def removeRowForConfig(self, configNum):
        '''
        :method: Removes the last row of a specific config from the model.
        :param configNum: Number of the config for which the row must be deleted.  
        '''
        logging.debug(self.__className+'.removeRowForConfig')
        
        # TODO: Add transaction
        query = QSqlQuery()
        query.prepare("Select ConfigNum, OrderNum FROM %s WHERE ConfigNum = :conf ORDER BY OrderNum ASC" %(self.tableName()) )
        query.bindValue(":conf", str(configNum))
        query.exec()
        orderNum = 0
        while (query.next()):
            orderNum = query.value(1)
        
        if orderNum>0:
            query.prepare("DELETE FROM %s WHERE (ConfigNum = :conf AND OrderNum = :order);" %(self.tableName()) )
            query.bindValue(":conf", str(configNum))
            query.bindValue(":order", str(orderNum))
            query.exec()
            self.select() # to a select() to assure the model is updated properly


    def setNumRowsForConfig(self, configNum, mustNumRows):
        '''
        :method: Assures the model will be setup to hold the correct number of rows based on parameters passed. 
        :param configNum: Number of the config for which the row must be deleted.
        :param mustNumRows: Number of rows the model must provide.
        '''
        logging.debug(self.__className+'.setNumRowsForConfig')
        
        currNumRows = self.numRowsForConfig(configNum)
        diff = abs(mustNumRows-currNumRows)
        
        
        if diff != 0:
            # do it only if really the number has changed
            i = 0
            if mustNumRows > currNumRows:
                # add config lines
                while i < diff:
                    self.addRowForConfig(configNum)
                    i += 1
            else:
                # remove config lines
                while i < diff:
                    self.removeRowForConfig( configNum )
                    i += 1
            
            # emit the change signal
            self.numRowsForConfigChanged.emit(configNum, self.numRowsForConfig(configNum))

            
    def numRowsForConfig(self, configNum):
            '''
            :method: Use this to check how many rows a specific config holds currently.
            :param configNum: Number of the config for which the number of rows must be returned.
            :return: Current number of rows.
            :attention: To use this method the model must have the variable *ConfigNumCol* defined. 
            '''
            logging.debug(self.__className+'.numRowsForConfig')
            
            if hasattr(self, 'ConfigNumCol'):
                proxyModel = QSortFilterProxyModel()
                proxyModel.setSourceModel(self)
                proxyModel.setFilterKeyColumn( self.ConfigNumCol )
                proxyModel.setFilterRegExp( QRegExp( str(configNum) ) )
                return proxyModel.rowCount()
            else:
                logging.critical(self.__className+'.numRowsForConfig: ConfigNumCol not defined')
                return
