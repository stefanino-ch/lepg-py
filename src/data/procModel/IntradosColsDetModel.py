"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class IntradosColsDetModel(SqlTableModel, metaclass=Singleton):
    """
    :class: provides a SqlTableModel holding all detail data related to the Intrados colors
    """
    __className = 'IntradosColsDetModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a config'''
    DistTeCol = 1
    ''':attr: number of the column holding the first rib of the config'''
    ConfigNumCol = 2
    ''':attr: number of the column holding the config number'''

    def createTable(self):
        """
        :method: Creates initially the empty table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists IntradColsDet;")
        query.exec("create table if not exists IntradColsDet ("
                   "OrderNum INTEGER,"
                   "DistTe INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("IntradColsDet")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order Num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Dist TE"))

    def updateRow(self, configNum, orderNum, distTe):
        query = QSqlQuery()
        query.prepare(
            "UPDATE IntradColsDet SET DistTe= :distTe WHERE (ConfigNum = :config  AND OrderNum = :order);")
        query.bindValue(":distTe", distTe)
        query.bindValue(":config", configNum)
        query.bindValue(":order", orderNum)
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
                      "DistTe "
                      "FROM IntradColsDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
