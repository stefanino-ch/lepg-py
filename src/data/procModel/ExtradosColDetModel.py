"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class ExtradosColDetModel(SqlTableModel, metaclass=Singleton):
    """
    :class: provides a SqlTableModel holding all detail data related to the Extrados colors
    """
    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a config'''
    DistTeCol = 1
    ''':attr: number of the column holding the distance from trailing edge'''
    DistTeRightCol = 2
    ''':attr: number of the column holding the distance from trailing edge on the right side'''
    SeamCol = 3
    ''':attr: number of the column holding seam width'''
    ConfigNumCol = 4
    ''':attr: number of the column holding the config number'''

    @staticmethod
    def create_table():
        """
        :method: Creates initially the empty table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists ExtradColsDet;")
        query.exec("create table if not exists ExtradColsDet ("
                   "OrderNum INTEGER,"
                   "DistTe INTEGER,"
                   "DistTeRight INTEGER,"
                   "Seam INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("ExtradColsDet")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order Num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Dist TE"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Dist TE right"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Seam"))

    def update_row(self, config_num, order_num, dist_te, dist_te_right, seam):
        query = QSqlQuery()
        query.prepare("UPDATE ExtradColsDet "
                      "SET DistTe= :distTe, "
                      "DistTeRight= :distTeRight, "
                      "Seam= :seam "
                      "WHERE (ConfigNum = :config  AND OrderNum = :order);")
        query.bindValue(":distTe", dist_te)
        query.bindValue(":distTeRight", dist_te_right)
        query.bindValue(":seam", seam)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    @staticmethod
    def get_row(config_num, order_num):
        """
        :method: reads values back from the internal database for a specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "DistTe, "
                      "DistTeRight, "
                      "Seam "
                      "FROM ExtradColsDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
