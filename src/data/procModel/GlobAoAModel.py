"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class GlobAoAModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the global AoA parameters.
    """
    __className = 'GlobAoAModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    FinesseCol = 0
    ''':attr: Number of the col holding the finesse value'''
    CentOfPressCol = 1
    ''':attr: Number of the col holding the center of pressure value'''
    CalageCol = 2
    ''':attr: Number of the col holding the calage value'''
    RisersCol = 3
    ''':attr: Number of the col holding the risers length value'''
    LinesCol = 4
    ''':attr: Number of the col holding the lines length value'''
    KarabinersCol = 5
    ''':attr: Number of the col holding the karabiners length value'''

    def createTable(self):
        """
        :method: Creates initially the empty GlobalAoA table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists GlobalAoA;")
        query.exec("create table if not exists GlobalAoA ("
                   "Finesse REAL,"
                   "CentOfPress INTEGER,"
                   "Calage INTEGER,"
                   "Risers INTEGER,"
                   "Lines INTEGER,"
                   "Karabiners INTEGER,"
                   "ID INTEGER PRIMARY KEY);")
        query.exec("INSERT into GlobalAoA (ID) Values( '1' );")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("GlobalAoA")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Finesse [deg]"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Center of Pressure"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Calage"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Risers [cm]"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Lines [cm]"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Karabiners [cm]"))

    def getRow(self):
        """
        :method: reads values back from the internal database
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "Finesse, "
                      "CentOfPress, "
                      "Calage, "
                      "Risers, "
                      "Lines, "
                      "Karabiners "
                      "FROM GlobalAoA")
        query.exec()
        query.next()
        return query.value
