"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class TwoDDxfModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the DXF layer names
    """
    __isUsed = False
    ''' :attr: Helps to remember if the section is in use or not'''

    usageUpd = pyqtSignal()
    '''
    :signal: emitted as soon the usage flag is changed
    '''
    OrderNumCol = 0
    '''
    :attr: Num of column for ordering the individual
           lines of a config
    '''
    LineNameCol = 1
    ''':attr: Number of the col holding the fixed line name '''
    ColorCodeCol = 2
    ''':attr: Number of the col holding the color code'''
    ColorNameCol = 3
    ''':attr: Number of the col holding the optional color name'''
    ConfigNumCol = 4
    ''':attr: num of column for config number (always 1)'''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("TwoDDxf")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.set_num_rows_for_config(1, 6)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Line name"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Color code"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Color name"))

        # TODO Color name is optional, reader does not take this
        #      into account currently
        # TODO prefill table with correct names.

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists TwoDDxf;")
        query.exec("create table if not exists TwoDDxf ("
                   "OrderNum INTEGER,"
                   "LineName TEXT,"
                   "ColorCode INTEGER,"
                   "ColorName TEXT,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, line_name,
                   color_code, color_name):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE TwoDDxf SET "
                      "LineName= :line_name, "
                      "ColorCode= :color_code, "
                      "ColorName= :color_name "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":line_name", line_name)
        query.bindValue(":color_code", color_code)
        query.bindValue(":color_name", color_name)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def set_is_used(self, is_used):
        """
        :method: Set the usage flag of the section
        :param is_used: True if section is in use, False otherwise.
        """
        self.__isUsed = is_used
        self.usageUpd.emit()

    def is_used(self):
        """
        :method: Returns the information if the section is in use or not
        :returns: True if section is in use, false otherwise
        """
        return self.__isUsed

    def get_row(self, config_num, order_num):
        """
        :method: Reads values back from the internal database for
                 a specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "LineName, "
                      "ColorCode, "
                      "ColorName "
                      "FROM TwoDDxf WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
