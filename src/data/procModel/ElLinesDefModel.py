"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class ElLinesDefModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the Elastic lines deformation parameters. (2nd part of elastic
            lines correction)
    """
    __className = 'ElLinesDefModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    OrderNumCol = 0
    ''':attr: used here for the number of lines'''
    DefLowCol = 1
    ''':attr: Number of the col holding the deformation in the lower level'''
    DefMidCol = 2
    ''':attr: Number of the col holding the deformation in the medium level'''
    DefHighCol = 3
    ''':attr: Number of the col holding the deformation in the higher level'''
    ConfigNumCol = 4
    ''':attr: num of column for config number (always 1)'''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists ElasticLinesDef;")
        query.exec("create table if not exists ElasticLinesDef ("
                   "OrderNum INTEGER,"
                   "DefLow REAL,"
                   "DefMid REAL,"
                   "DefHigh REAL,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("ElasticLinesDef")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Num lines per rib"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Def in lower level"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Def in mid level"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Def in higher level"))

        self.set_num_rows_for_config(1, 5)

    def update_row(self, config_num, order_num, def_low, def_mid, def_high):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE ElasticLinesDef SET "
                      "DefLow= :defLow, "
                      "DefMid= :defMid, "
                      "DefHigh= :defHigh "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":defLow", def_low)
        query.bindValue(":defMid", def_mid)
        query.bindValue(":defHigh", def_high)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def getRow(self, configNum, orderNum):
        """
        :method: reads values back from the internal database for a specific config and order number
        :param configNum: Configuration number. Starting with 1
        :param orderNum: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "OrderNum, "
                      "DefLow, "
                      "DefMid, "
                      "DefHigh "
                      "FROM ElasticLinesDef WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
