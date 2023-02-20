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

    paramLength = {
        1: 7,
        2: 8,
        3: 8
    }
    ''':attr: defines the length (number of values) for the individual parameter lines'''

    def create_table(self):
        """
        :method: Creates initially the empty lightening details table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists LightDet;")
        query.exec("create table if not exists LightDet ("
                   "OrderNum INTEGER,"
                   "light_typ INTEGER,"
                   "dist_le REAL,"
                   "dist_chord REAL,"
                   "hor_axis REAL,"
                   "vert_axis REAL,"
                   "rot_angle REAL,"
                   "opt_1 REAL,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")
        query.exec("INSERT into LightDet (ConfigNum, OrderNum) Values( '1', '1' );")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
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

    def update_row(self, config_num, order_num, light_typ, dist_le, dist_chord,
                   hor_axis, vert_axis, rot_angle, opt_1):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE LightDet SET light_typ= :light, "
                      "dist_le= :dist, dist_chord= :dis, hor_axis= :hor, "
                      "vert_axis= :vert, rot_angle= :rot, opt_1= :opt1 "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":light", light_typ)
        query.bindValue(":dist", dist_le)
        query.bindValue(":dis", dist_chord)
        query.bindValue(":hor", hor_axis)
        query.bindValue(":vert", vert_axis)
        query.bindValue(":rot", rot_angle)
        query.bindValue(":opt1", opt_1)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def get_row(self, config_num, order_num):
        """
        :method: reads values back from the internal database for a specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "light_typ, "
                      "dist_le, "
                      "dist_chord, "
                      "hor_axis, "
                      "vert_axis, "
                      "rot_angle, "
                      "opt_1 "
                      "FROM LightDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
