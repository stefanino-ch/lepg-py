"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class ThreeDShLoDetModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the 3d Shaping data for
            the lower panels
    """
    OrderNumCol = 0
    '''
    :attr: Num of column for ordering the individual lines
           of a config
    '''

    IniPointCol = 1
    '''
    :attr: Number of the col holding initial point of the zone
           of influence
    '''

    CutPointCol = 2
    '''
    :attr: Number of the col holding position of the point where the
           cut is set
    '''

    DepthCol = 3
    '''
    :attr: Number of the col holding the shaping depth
    '''

    ConfigNumCol = 4
    '''
    :attr: num of column for config number
    '''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists ThreeDShapingLoDetail;")
        query.exec("create table if not exists ThreeDShapingLoDetail ("
                   "OrderNum INTEGER, "
                   "IniPoint INTEGER, "
                   "CutPoint INTEGER, "
                   "Depth REAL, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("ThreeDShapingLoDetail")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Ini P"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Cut P"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Depth"))

    def update_row(self, config_num, order_num, ini_point, cut_point, depth):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here
                 as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE ThreeDShapingLoDetail SET "
                      "IniPoint= :ini_point, "
                      "CutPoint= :cut_point, "
                      "Depth= :depth "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":ini_point", ini_point)
        query.bindValue(":cut_point", cut_point)
        query.bindValue(":depth", depth)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def get_row(self, config_num, order_num):
        """
        :method: Reads values back from the internal database for a
                 specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "IniPoint, "
                      "CutPoint, "
                      "Depth "
                      "FROM ThreeDShapingLoDetail WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
