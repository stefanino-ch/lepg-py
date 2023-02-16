"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class RibModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data related to the
            individual ribs.
    """
    RibNumCol = 0
    ''':attr: number of the rib number column'''
    xribCol = 1
    ''':attr: number of the column providing rib X coordinate'''
    yLECol = 2
    '''
    :attr: number of the column providing Y coordinate of the
           leading edge
    '''
    yTECol = 3
    '''
    :attr: number of the column providing Y coordinate of the
           trailing edge
    '''
    xpCol = 4
    '''
    :attr: number of the column providing X' coordinate of the rib
           in its final position in space
    '''
    zCol = 5
    '''
    :attr: number of the column providing Z coordinate of the rib in
           its final position in space
    '''
    betaCol = 6
    '''
    :attr: number of the column providing the angle "beta" of the
           rib to the vertical (degrees)
    '''
    RPCol = 7
    '''
    :attr: number of the column providing RP percentage of chord to
              be held on the relative torsion of the airfoils
    '''
    WashinCol = 8
    '''
    :attr: number of the column providing washin in degrees defined
           manually (if parameter is set to "0")
    '''
    RotZCol = 9
    '''
    :attr: number of the column providing the rotation angle in z
           axis.
    '''
    PosZCol = 10
    '''
    :attr: number of the column holding the position of the z-axis
           rotation point
    '''

    def createRibTable(self):
        """
        :method: Creates initially the empty rib table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists Rib;")
        query.exec("create table if not exists Rib ("
                   "RibNum INTEGER,"
                   "xrib REAL,"
                   "yLE REAL,"
                   "yTE REAL,"
                   "xp REAL,"
                   "z REAL,"
                   "beta REAL,"
                   "RP REAL,"
                   "Washin REAL,"
                   "Rot_Z REAL,"
                   "Pos_Z REAL,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createRibTable()
        self.setTable("Rib")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(self.RibNumCol, Qt.Orientation.Horizontal, _("Rib Num"))
        self.setHeaderData(self.RPCol, Qt.Orientation.Horizontal, _("RP"))
        self.setHeaderData(self.WashinCol, Qt.Orientation.Horizontal, _("Washin"))
        self.setHeaderData(self.RotZCol, Qt.Orientation.Horizontal, _("Z Rotation"))
        self.setHeaderData(self.PosZCol, Qt.Orientation.Horizontal, _("Z Position"))

    def updateRow(self, ribNum, xrib, yLE, yTE, xp, z, beta, RP, Washin,
                  rotZ, posZ):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE Rib SET "
                      "xrib = :xrib, "
                      "yLE = :yLE, "
                      "yTE = :yTE, "
                      "xp = :xp, "
                      "z = :z, "
                      "beta = :beta, "
                      "RP = :RP, "
                      "Washin = :Washin, "
                      "Rot_Z = :rotZ, "
                      "Pos_Z = :posZ "
                      "WHERE (RibNum = :ribNum);")
        query.bindValue(":xrib", xrib)
        query.bindValue(":yLE", yLE)
        query.bindValue(":yTE", yTE)
        query.bindValue(":xp", xp)
        query.bindValue(":z", z)
        query.bindValue(":beta", beta)
        query.bindValue(":RP", RP)
        query.bindValue(":Washin", Washin)
        query.bindValue(":ribNum", ribNum)
        query.bindValue(":rotZ", rotZ)
        query.bindValue(":posZ", posZ)
        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def getRow(self, ribNum):
        """
        :method: reads values back from the internal database
        :param ribNum: Rib number. Starting with 1.
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "xrib, "
                      "yLE, "
                      "yTE, "
                      "xp, "
                      "z, "
                      "beta, "
                      "RP, "
                      "Washin, "
                      "Rot_Z, "
                      "Pos_Z "
                      "FROM Rib WHERE (RibNum = :rib)")
        query.bindValue(":rib", ribNum)
        query.exec()
        query.next()
        return query.value
