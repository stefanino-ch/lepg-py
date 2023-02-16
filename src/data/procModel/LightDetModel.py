"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class LightDetModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data related to the individual lightening config parameters.
    """
    # numDetailsChanged = pyqtSignal(int, int)
    '''
    :Signal: Emitted at the moment the number of data lines in the model is changed. \
    Param 1: the configuration number which has changed \
    Param2: new number of data lines
    '''

    __className = 'LightDetModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a confit'''
    LightTypCol = 1
    ''':attr: num of column for 1..3: hole type info'''
    DistLECol = 2
    ''':attr: num of column for 1..3: distance from LE to hole center in % chord '''
    DisChordCol = 3
    ''':attr: num of column for 1..3: distance from the center of hole to the chord line in % of chord'''
    HorAxisCol = 4
    '''
    :attr: num of column for 1..2: horizontal axis of the ellipse as % of chord; 
              3: triangle base as % of chord
    '''
    VertAxisCol = 5
    ''':attr: num of column for 1..2: ellipse vertical axis as % of chord; 3: triangle height as % of chord'''
    RotAngleCol = 6
    ''':attr: num of column 1..3:  for rotation angle of the ellipse'''
    Opt1Col = 7
    ''':attr: num of column 1: na; 2:  central strip width; 3: Radius of the smoothed corners'''
    ConfigNumCol = 8
    ''':attr: num of column for 1..3: config number'''

    def createTable(self):
        """
        :method: Creates initially the empty lightening details table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists LightDet;")
        query.exec("create table if not exists LightDet ("
                   "OrderNum INTEGER,"
                   "LightTyp INTEGER,"
                   "DistLE REAL,"
                   "DisChord REAL,"
                   "HorAxis REAL,"
                   "VertAxis REAL,"
                   "RotAngle REAL,"
                   "Opt1 REAL,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")
        query.exec("INSERT into LightDet (ConfigNum, OrderNum) Values( '1', '1' );")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("LightDet")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order Num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Light Typ"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Dist LE"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Dist chord"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Hor axis"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Vert axis"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Rot angle"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Opt "))

    def updateRow(self, configNum, orderNum, LightTyp, DistLE, DisChord, HorAxis, VertAxis, RotAngle, Opt1):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE LightDet SET LightTyp= :light, "
                      "DistLE= :dist, DisChord= :dis, HorAxis= :hor, "
                      "VertAxis= :vert, RotAngle= :rot, Opt1= :opt1 "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":light", LightTyp)
        query.bindValue(":dist", DistLE)
        query.bindValue(":dis", DisChord)
        query.bindValue(":hor", HorAxis)
        query.bindValue(":vert", VertAxis)
        query.bindValue(":rot", RotAngle)
        query.bindValue(":opt1", Opt1)
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
                      "LightTyp, "
                      "DistLE, "
                      "DisChord, "
                      "HorAxis, "
                      "VertAxis, "
                      "RotAngle, "
                      "Opt1 "
                      "FROM LightDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
