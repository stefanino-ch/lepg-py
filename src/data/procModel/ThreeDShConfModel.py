"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class ThreeDShConfModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the 3d Shaping configuration
    """
    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    FirstRibCol = 1
    ''':attr: Number of the col holding the first rib'''
    LastRibCol = 2
    ''':attr: Number of the col holding the last rib'''
    ConfigNumCol = 3
    ''':attr: num of column for config number'''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists ThreeDShapingConf;")
        query.exec("create table if not exists ThreeDShapingConf ("
                   "OrderNum INTEGER, "
                   "FirstRib INTEGER, "
                   "LastRib INTEGER, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("ThreeDShapingConf")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("First Rib"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Last Rib"))

    def update_row(self, config_num, order_num, first_rib, last_rib):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """

        query = QSqlQuery()
        query.prepare("UPDATE ThreeDShapingConf SET "
                      "FirstRib= :first_rib, "
                      "LastRib= :last_rib "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":first_rib", first_rib)
        query.bindValue(":last_rib", last_rib)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def get_row(self, config_num, order_num):
        """
        :method: reads values back from the internal database for a specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "OrderNum, "
                      "FirstRib, "
                      "LastRib "
                      "FROM ThreeDShapingConf WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
