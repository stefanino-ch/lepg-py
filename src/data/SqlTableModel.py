"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtCore import pyqtSignal, QSortFilterProxyModel, QRegExp
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class SqlTableModel(QSqlTableModel):
    """
    :class: Inherits QSqlTableModel and adds a few specific methods, partially
            sw related, partially to work around some Qt limitations
    """
    __className = 'SqlTableModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    didSelect = pyqtSignal()
    '''
    :signal: Emitted as soon select() was executed on the model.
             You must know about this fact if you have mappers to LineEdits
             in place, as the mapping must be redone after every select().
    '''

    numDetailsChanged = pyqtSignal(int, int)
    numRowsForConfigChanged = pyqtSignal(int, int)

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Constructor
        """
        logging.debug(self.__className+'.__init__')
        super().__init__()

    def add_rows(self, row, count):
        """
        :method: Add one or multiple rows to the model
        :param row: Row after which the new rows must be inserted
        :param count: Rhe number of new rows to be inserted

        Thanks to https://stackoverflow.com/questions/47318601/
        inserting-row-into-qsqltablemodel#47319440 for the example
        about how to insert.
        """
        logging.debug(self.__className + '.add_rows')

        QSqlDatabase.database().transaction()
        for i in range(0, count):
            num_rows = self.rowCount()
            record = self.record()
            record.setValue("ID", num_rows+1)
            record.setValue("RibNum", num_rows+1)
            # -1 is set to indicate that it will be added to the last row
            if not self.insertRecord(row+i, record):
                logging.critical(self.__className + '.add_rows insertRecord Err type: %s'
                                 % self.lastError().type())
                logging.critical(self.__className + '.add_rows insertRecord Err text: %s'
                                 % self.lastError().text())
                QSqlDatabase.database().rollback()
                return False

        if not QSqlDatabase.database().commit():
            logging.critical(self.__className + '.add_rows commit Err type: %s'
                             % self.lastError().type())
            logging.critical(self.__className + '.add_rows commit Err text: %s'
                             % self.lastError().text())
            return False
        return True

    def remove_rows_at_end(self, num_to_remove):
        """
        :method: Removes one or multiple rows from the end of the table
        :param num_to_remove: Number of rows to remove
        """
        logging.debug(self.__className+'.remove_rows_at_end')

        i = 0
        res = 0
        start = self.rowCount()-1
        while i < num_to_remove:
            res = self.removeRows(start-i, 1)
            i += 1
        self.select()  # use as less selects as possible
        return res

    def select(self, *args, **kwargs):
        """
        :method: Overwritten class method. Needed to get a signal back after
                 a select()
        :emits didSelect: The signal telling the consumers that a select()
                          was done on the model
        """
        logging.debug(self.__className+'.select')

        res = QSqlTableModel.select(self, *args, **kwargs)
        # Now we must tell the rest of the app that a row has been removed.
        self.didSelect.emit()
        return res

    def sort_table(self, row, order):
        """
        :method: Forces the model to sort
        :param row: Row which is used to sort
        :param order: Qt.AscendingOrder or Qt.DescendingOrder
        """
        logging.debug(self.__className+'.sort_table')
        self.setSort(row, order)
        self.select()

    def setup_rib_rows(self, half_num_ribs):
        """
        :method: Compares the number of rows currently with what it should be.
                 Add/ removes rows accordingly
        :param half_num_ribs: The number of rows to be achieved.
        """
        logging.debug(self.__className+'.setup_rib_rows')
        self.submitAll()

        num_rows = self.rowCount()
        if num_rows > half_num_ribs:
            num_to_remove = num_rows - half_num_ribs
            self.remove_rows_at_end(num_to_remove)
        elif num_rows < half_num_ribs:
            num_to_add = half_num_ribs - num_rows
            self.add_rows(num_rows, num_to_add)

    def set_num_configs(self, must_num_configs):
        """
        :method: Assures the model will hold at least one row for each config
                 based on the parameter passed
        :param must_num_configs: Number of configs the model must provide
        """
        logging.debug(self.__className+'.set_num_configs')
        curr_num_configs = self.num_configs()

        diff = abs(must_num_configs - curr_num_configs)
        if diff != 0:
            # do it only if really the number has changed
            i = 0
            if must_num_configs > curr_num_configs:
                # add config lines
                while i < diff:
                    self.set_num_rows_for_config(curr_num_configs + 1 + i, 1)
                    # emit the change signal
                    self.numRowsForConfigChanged.emit(curr_num_configs+1+i, 1)
                    i += 1
            else:
                # remove config lines
                while i < diff:
                    self.set_num_rows_for_config(curr_num_configs - i, 0)
                    # emit the change signal
                    self.numRowsForConfigChanged.emit(curr_num_configs-i, 0)
                    i += 1

    def num_configs(self):
        """
        :method: Reads from a table how many configurations
                 are saved.
        :return: Number of different configs
        """
        logging.debug(self.__className+'.num_configs')

        query = QSqlQuery()
        query.prepare("Select ConfigNum FROM %s ORDER BY ConfigNum ASC"
                      % self.tableName())
        query.exec()
        order_num = 0
        while query.next():
            order_num = query.value(0)

        return order_num

    def add_row_for_config(self, config_num):
        """
        :method: Adds a row to the model. Sets Columns *ConfigNum* and
                 *OrderNum*
        :parm config_num: Number of the config for which the row must be added.
        :attention: The two columns *ConfigNum* and *OrderNum* must exist for
                    proper functionality
        """
        logging.debug(self.__className+'.add_row_for_config')

        curr_num_rows = self.num_rows_for_config(config_num)

        query = QSqlQuery()
        query.prepare("INSERT into %s (ConfigNum, OrderNum) Values( :conf, :order);" % self.tableName())
        query.bindValue(":conf", config_num)
        query.bindValue(":order", curr_num_rows+1)
        res = query.exec()
        if not res:
            logging.critical(self.__className
                             + '.addRowsForConfig insertRecord Err type: %s'
                             % self.lastError().type())
            logging.critical(self.__className
                             + '.addRowsForConfig insertRecord Err text: %s'
                             % self.lastError().text())
        # to a select() to assure the model is updated properly
        self.select()

    def remove_row_for_config(self, config_num):
        """
        :method: Removes the last row of a specific config from the model
        :param config_num: Number of the config for which the row must
                          be deleted.
        """
        logging.debug(self.__className+'.remove_row_for_config')

        query = QSqlQuery()
        query.prepare("Select ConfigNum, OrderNum FROM %s WHERE ConfigNum = :conf ORDER BY OrderNum ASC"
                      % self.tableName())
        query.bindValue(":conf", str(config_num))
        query.exec()
        order_num = 0
        while query.next():
            order_num = query.value(1)

        if order_num > 0:
            query.prepare("DELETE FROM %s WHERE (ConfigNum = :conf AND OrderNum = :order);"
                          % self.tableName())
            query.bindValue(":conf", str(config_num))
            query.bindValue(":order", str(order_num))
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

    def set_num_rows_for_config(self, config_num, must_num_rows):
        """
        :method: Assures the model will be setup to hold the correct number
                 of rows based on parameters passed
        :param config_num: Number of the config for which the row must
                          be deleted
        :param must_num_rows: Number of rows the model must provide.
        """
        logging.debug(self.__className+'.set_num_rows_for_config')

        curr_num_rows = self.num_rows_for_config(config_num)
        diff = abs(must_num_rows - curr_num_rows)

        if diff != 0:
            # do it only if really the number has changed
            i = 0
            if must_num_rows > curr_num_rows:
                # add config lines
                while i < diff:
                    self.add_row_for_config(config_num)
                    i += 1
            else:
                # remove config lines
                while i < diff:
                    self.remove_row_for_config(config_num)
                    i += 1

            # emit the change signal
            self.numRowsForConfigChanged.emit(config_num,
                                              self.num_rows_for_config(config_num))

    def num_rows_for_config(self, config_num):
        """
        :method: Use this to check how many rows a specific config
                 holds currently
        :param config_num: Number of the config for which the number of rows
                          must be returned.
        :return: Current number of rows.
        :attention: To use this method the model must have the variable
                    *ConfigNumCol* defined.
        """
        logging.debug(self.__className+'.num_rows_for_config')

        if hasattr(self, 'ConfigNumCol'):
            proxy_model = QSortFilterProxyModel()
            proxy_model.setSourceModel(self)
            proxy_model.setFilterKeyColumn(self.ConfigNumCol)
            proxy_model.setFilterRegExp(QRegExp(str(config_num)))
            return proxy_model.rowCount()
        else:
            logging.critical(self.__className+'.num_rows_for_config: ConfigNumCol not defined')
            return
