"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class AnchorPointsModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data related to the Anchor points.
    """
    __className = 'AnchorPointsModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    RibNumCol = 0
    ''':attr: Number of the rib number column'''
    NumAnchCol = 1
    ''':attr: Number of the column holding the number of anchors'''
    PosACol = 2
    ''':attr: Number the column holding Pos A'''
    PosBCol = 3
    ''':attr: Number the column holding Pos B'''
    PosCCol = 4
    ''':attr: Number the column holding Pos C'''
    PosDCol = 5
    ''':attr: Number the column holding Pos D'''
    PosECol = 6
    ''':attr: Number the column holding Pos E'''
    PosFCol = 7
    ''':attr: Number the column holding Pos F'''

    def createAnchorPointsTable(self):
        """
        :method: Creates initially the empty anchor points table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists AnchorPoints;")
        query.exec("create table if not exists AnchorPoints ("
                   "RibNum INTEGER,"
                   "NumAnchors INTEGER,"
                   "PosA REAL,"
                   "PosB REAL,"
                   "PosC REAL,"
                   "PosD REAL,"
                   "PosE REAL,"
                   "PosF REAL,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createAnchorPointsTable()
        self.setTable("AnchorPoints")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Rib Num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Num Anchors"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Pos A"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Pos B"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Pos C"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Pos D"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Pos E"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Pos F"))

    def getRow(self, ribNum):
        """
        :method: Reads values back from the internal database
        :param ribNum: Rib number. Starting with 1.
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "NumAnchors, "
                      "PosA, "
                      "PosB, "
                      "PosC, "
                      "PosD, "
                      "PosE, "
                      "PosF "
                      "FROM AnchorPoints WHERE (RibNum = :rib)")
        query.bindValue(":rib", ribNum)
        query.exec()
        query.next()
        return query.value
