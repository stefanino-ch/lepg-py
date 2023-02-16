"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class BrakeLengthModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the Marks parameters.
    """
    __className = 'BrakeLengthModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    s1Col = 0
    ''':attr: Number of the col holding the s1 value'''
    s2Col = 1
    ''':attr: Number of the col holding the s2 value'''
    s3Col = 2
    ''':attr: Number of the col holding the s3 value'''
    s4Col = 3
    ''':attr: Number of the col holding the s4 value'''
    s5Col = 4
    ''':attr: Number of the col holding the s5 value'''
    d1Col = 5
    ''':attr: Number of the col holding the d1 value'''
    d2Col = 6
    ''':attr: Number of the col holding the d2 value'''
    d3Col = 7
    ''':attr: Number of the col holding the d3 value'''
    d4Col = 8
    ''':attr: Number of the col holding the d4 value'''
    d5Col = 9
    ''':attr: Number of the col holding the d5 value'''

    def create_table(self):
        """
        :method: Creates initially the empty Brake length table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists BrakeLength;")
        query.exec("create table if not exists BrakeLength ("
                   "s1 INTEGER,"
                   "s2 INTEGER,"
                   "s3 INTEGER,"
                   "s4 INTEGER,"
                   "s5 INTEGER,"
                   "d1 INTEGER,"
                   "d2 INTEGER,"
                   "d3 INTEGER,"
                   "d4 INTEGER,"
                   "d5 INTEGER,"
                   "ID INTEGER PRIMARY KEY);")
        query.exec("INSERT into BrakeLength (ID) Values( '1' );")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("BrakeLength")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("s1 [\u0025]"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("s2 [\u0025]"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("s3 [\u0025]"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("s4 [\u0025]"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("s5 [\u0025]"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("d1 [cm]"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("d2 [cm]"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("d3 [cm]"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("d4 [cm]"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("d5 [cm]"))

    def get_row(self):
        """
        :method: reads values back from the internal database
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "s1, "
                      "s2, "
                      "s3, "
                      "s4, "
                      "s5, "
                      "d1, "
                      "d2, "
                      "d3, "
                      "d4, "
                      "d5 "
                      "FROM BrakeLength")
        query.exec()
        query.next()

        return query.value
