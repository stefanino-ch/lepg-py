"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class AirfoilsModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data related to the individual ribs.
    """
    __className = 'AirfoilsModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    RibNumCol = 0
    ''':attr: number of the rib number column'''
    AirfNameCol = 1
    ''':attr: number of the rib name column'''
    IntakeStartCol = 2
    ''':attr: number of the intake start column'''
    IntakeEndCol = 3
    ''':attr: number of the intake end column'''
    OpenCloseCol = 4
    ''':attr: number of the column for the open/ close config'''
    DisplacCol = 5
    ''':attr: number of the column for the displacement'''
    RelWeightCol = 6
    ''':attr: number of the column for the relative weight '''
    rrwCol = 7
    ''':attr: number of the column for the rrw config'''

    def create_table(self):
        """
        :method: Creates initially the empty anchor points table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists Airfoils;")
        query.exec("create table if not exists Airfoils ("
                   "RibNum INTEGER,"
                   "AirfName TEXT,"
                   "IntakeStart REAL,"
                   "IntakeEnd REAL,"
                   "OpenClose INTEGER,"
                   "Displac REAL,"
                   "RelWeight REAL,"
                   "rrw REAL,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("Airfoils")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Rib Num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Name"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Intake Start"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Intake End"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Open-close"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Displac"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Rel weight"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("rrw"))

    def get_row(self, rib_num):
        """
        :method: reads values back from the internal database
        :param rib_num: Rib number. Starting with 1.
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "AirfName, "
                      "IntakeStart, "
                      "IntakeEnd, "
                      "OpenClose, "
                      "Displac, "
                      "RelWeight, "
                      "rrw "
                      "FROM Airfoils WHERE (RibNum = :rib)")
        query.bindValue(":rib", rib_num)
        query.exec()
        query.next()
        return query.value
