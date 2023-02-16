"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class SkinTensionParamsModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the three individual params of the Skin tension setup.
    """
    StrainMiniRibsCol = 0
    ''':attr: Parameter to control the mini ribs'''
    NumPointsCol = 1
    ''':attr: Number of points'''
    CoeffCol = 2
    ''':attr: The coefficient'''

    def createTable(self):
        """
        :method: Creates initially the empty Skin tension params table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists SkinTensionParams;")
        query.exec("create table if not exists SkinTensionParams ("
                   "StrainMiniRibs REAL,"
                   "NumPoints Integer,"
                   "Coeff REAL,"
                   "ID INTEGER PRIMARY KEY);")
        query.exec(
            "INSERT into SkinTensionParams (StrainMiniRibs, NumPoints, Coeff,  ID) Values( '0.0114', '1000', '1.0', 1 );")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("SkinTensionParams")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Strain mini ribs"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Num points"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Coeff"))

    def getRow(self):
        """
        :method: reads values back from the internal database
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "StrainMiniRibs, "
                      "NumPoints, "
                      "Coeff "
                      "FROM SkinTensionParams")
        query.exec()
        query.next()
        return query.value
