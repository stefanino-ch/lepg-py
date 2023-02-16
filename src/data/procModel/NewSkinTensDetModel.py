"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class NewSkinTensDetModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all detail data related to New skin tension.
    """
    __className = 'NewSkinTensionDetModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    TopDistLECol = 1
    ''':attr: Distance in % of chord on the leading edge of extrados'''
    TopWideCol = 2
    ''':attr: Extrados over-wide corresponding in % of chord'''
    BottDistTECol = 3
    ''':attr: Distance in % of chord on trailing edge'''
    BottWideCol = 4
    ''':attr: Intrados over-wide corresponding in % of chord'''
    ConfigNumCol = 5
    ''':attr: number of the column holding the config number'''

    def createTable(self):
        """
        :method: Creates initially the empty Skin tension table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists NewSkinTensDet;")
        query.exec("create table if not exists NewSkinTensDet ("
                   "OrderNum INTEGER, "
                   "TopDistLE REAL, "
                   "TopWide REAL, "
                   "BotDistTE REAL, "
                   "BotWide REAL, "
                   "ConfigNum INTEGER, "
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("NewSkinTensDet")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Top dist LE"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Top widening"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Bott dist TE"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Bott widening"))

    def updateRow(self, configNum, orderNum, topDistLE, topWide, botDistTE, botWide):
        """
        :method: updates a specific row with the parameters passed.
        """
        query = QSqlQuery()
        query.prepare("UPDATE NewSkinTensDet SET "
                      "TopDistLE= :topDis, "
                      "TopWide= :topWide, "
                      "BotDistTE= :botDis, "
                      "BotWide= :botWide  "
                      "WHERE (ConfigNum = :config AND OrderNum= :order);")
        query.bindValue(":topDis", topDistLE)
        query.bindValue(":topWide", topWide)
        query.bindValue(":botDis", botDistTE)
        query.bindValue(":botWide", botWide)
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
                      "TopDistLE, "
                      "TopWide, "
                      "BotDistTE, "
                      "BotWide "
                      "FROM NewSkinTensDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
