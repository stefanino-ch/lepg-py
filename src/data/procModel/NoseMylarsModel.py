"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class NoseMylarsModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the DXF layer names
    """
    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    FirstRibCol = 1
    ''':attr: Number of the col holding the first rib'''
    LastRibCol = 2
    ''':attr: Number of the col holding the last rib'''
    xOneCol = 3
    ''':attr: Number of the col holding the 1st param of 2nd row'''
    uOneCol = 4
    ''':attr: Number of the col holding the 2nd param of 2nd row'''
    uTwoCol = 5
    ''':attr: Number of the col holding the 3rd param of 2nd row'''
    xTwoCol = 6
    ''':attr: Number of the col holding the 4th param of 2nd row'''
    vOneCol = 7
    ''':attr: Number of the col holding the 5th param of 2nd row'''
    vTwoCol = 8
    ''':attr: Number of the col holding the 1st param of 3rd row'''
    ConfigNumCol = 9
    ''':attr: num of column for config number (always 1)'''

    def createTable(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists NoseMylars;")
        query.exec("create table if not exists NoseMylars ("
                   "OrderNum INTEGER, "
                   "FirstRib INTEGER, "
                   "LastRib INTEGER, "
                   "x_one REAL, "
                   "uOne REAL, "
                   "uTwo REAL, "
                   "x_two REAL, "
                   "vOne REAL, "
                   "vTwo REAL, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("NoseMylars")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("First Rib"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Last Rib"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("X1"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("U1"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("U2"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("X2"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("V1"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("V2"))

    def updateRow(self, configNum, orderNum, firstRib, lastRib, xOne, uOne, uTwo, xTwo, vOne, vTwo):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE NoseMylars SET "
                      "FirstRib= :first_rib, "
                      "LastRib= :last_rib, "
                      "x_one= :x_one, "
                      "uOne= :uOne, "
                      "uTwo= :uTwo, "
                      "x_two= :x_two, "
                      "vOne= :vOne, "
                      "vTwo= :vTwo "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":first_rib", firstRib)
        query.bindValue(":last_rib", lastRib)
        query.bindValue(":x_one", xOne)
        query.bindValue(":uOne", uOne)
        query.bindValue(":uTwo", uTwo)
        query.bindValue(":x_two", xTwo)
        query.bindValue(":vOne", vOne)
        query.bindValue(":vTwo", vTwo)
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
                      "OrderNum, "
                      "FirstRib, "
                      "LastRib, "
                      "x_one, "
                      "uOne, "
                      "uTwo, "
                      "x_two, "
                      "vOne, "
                      "vTwo "
                      "FROM NoseMylars WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
