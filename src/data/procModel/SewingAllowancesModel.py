"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class SewingAllowancesModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the Sewing allowances parameters.
    """
    EdgeSeamCol = 0
    ''':attr: Number of the col holding the Edge seem values'''
    LeSeemCol = 1
    ''':attr: Number of the col holding the LE seem values'''
    TeSeemCol = 2
    ''':attr: Number of the col holding the TE seem values'''

    def createTable(self):
        """
        :method: Creates initially the empty Sewing allowances table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists SewingAllowances;")
        query.exec("create table if not exists SewingAllowances ("
                   "EdgeSeam Integer,"
                   "LESeem Integer,"
                   "TESeem Integer,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("SewingAllowances")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Edge seem [mm]"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("LE seem [mm]"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("TE seem [mm]"))

        self.add_rows(-1, 4)

    def updateRow(self, row, edgeSeam, leSeem=0, teSeem=0):
        """
        :method: updates a specific row with the parameters passed.
        """
        query = QSqlQuery()
        query.prepare(
            "UPDATE SewingAllowances SET EdgeSeam= :edgeSeam, LESeem= :lESeem, TESeem= :tESeem WHERE (ID = :id);")
        query.bindValue(":edgeSeam", edgeSeam)
        query.bindValue(":lESeem", leSeem)
        query.bindValue(":tESeem", teSeem)
        query.bindValue(":id", row)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def getRow(self, configNum):
        """
        :method: reads values back from the internal database for a specific config number
        :param configNum: Rib number. Starting with 1.
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "EdgeSeam, "
                      "LESeem, "
                      "TESeem "
                      "FROM SewingAllowances WHERE (ID = :config)")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        return query.value
