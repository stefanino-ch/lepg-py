"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class SkinTensionModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data related to Skin tension.
    """
    TopDistLECol = 0
    ''':attr: Distance in % of chord on the leading edge of extrados'''
    TopWideCol = 1
    ''':attr: Extrados over-wide corresponding in % of chord'''
    BottDistTECol = 2
    ''':attr: Distance in % of chord on trailing edge'''
    BottWideCol = 3
    ''':attr: Intrados over-wide corresponding in % of chord'''

    def createTable(self):
        """
        :method: Creates initially the empty Skin tension table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists SkinTension;")
        query.exec("create table if not exists SkinTension ("
                   "TopDistLE REAL,"
                   "TopWide REAL,"
                   "BottDistTE REAL,"
                   "BottWide REAL,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("SkinTension")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.add_rows(-1, 6)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Top dist LE"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Top widening"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Bott dist TE"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Bott widening"))

    def updateRow(self, row, topDistLE, topWide, bottDistTE, bottWide):
        """
        :method: updates a specific row with the parameters passed.
        """
        query = QSqlQuery()
        query.prepare(
            "UPDATE SkinTension SET TopDistLE= :topDis, TopWide= :topWide, BottDistTE= :bottDis, BottWide= :bottWide  WHERE (ID = :id);")
        query.bindValue(":topDis", topDistLE)
        query.bindValue(":topWide", topWide)
        query.bindValue(":bottDis", bottDistTE)
        query.bindValue(":bottWide", bottWide)
        query.bindValue(":id", row)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def getRow(self, configNum):
        """
        :method: reads values back from the internal database for a specific config number
        :param configNum: Configuration number. Starting with 1.
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "TopDistLE, "
                      "TopWide, "
                      "BottDistTE, "
                      "BottWide "
                      "FROM SkinTension WHERE (ID = :config)")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        return query.value
