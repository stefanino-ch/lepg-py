"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class AddRibPointsModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the parameters for the additional rib points.
    """
    __className = 'AddRibPointsModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    OrderNumCol = 0
    ''':attr: num of column used for ordering the individual lines of a config'''
    XCoordCol = 1
    ''':attr: Number of the col holding the X-Coordinate'''
    YCoordCol = 2
    ''':attr: Number of the col holding the Y-Coordinate'''
    ConfigNumCol = 3
    ''':attr: num of column for config number'''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists AddRibPoints;")
        query.exec("create table if not exists AddRibPoints ("
                   "OrderNum INTEGER,"
                   "XCoord REAL,"
                   "YCoord REAL,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("AddRibPoints")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order Num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("X-Coordinate"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Y-Coordinate"))

    def update_row(self, config_num, order_num, x_coord, y_coord):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE AddRibPoints SET "
                      "XCoord= :xCoord, "
                      "YCoord= :yCoord "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":xCoord", x_coord)
        query.bindValue(":yCoord", y_coord)
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
                      "XCoord, "
                      "YCoord "
                      "FROM AddRibPoints WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
