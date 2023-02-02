"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class HvVhRibsModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the lines parameters.
    """
    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a config'''
    TypeCol = 1
    ''':attr: Number of the col holding the rib type info'''
    IniRibCol = 2
    ''':attr: Number of the col holding initial rib of the configuration'''
    ParamACol = 3
    ''':attr: Number of the col holding param A'''
    ParamBCol = 4
    ''':attr: Number of the col holding param B'''
    ParamCCol = 5
    ''':attr: Number of the col holding param C'''
    ParamDCol = 6
    ''':attr: Number of the col holding param D'''
    ParamECol = 7
    ''':attr: Number of the col holding param E'''
    ParamFCol = 8
    ''':attr: Number of the col holding param F'''
    ParamGCol = 9
    ''':attr: Number of the col holding param G'''
    ParamHCol = 10
    ''':attr: Number of the col holding param H'''
    ParamICol = 11
    ''':attr: Number of the col holding param I'''
    ConfigNumCol = 12
    ''':attr: num of column for config number'''

    paramLength = {
        1: 7,
        2: 10,
        3: 8,
        4: 10,
        5: 10,
        6: 12,
        11: 7,
        12: 10,
        13: 8,
        14: 10,
        15: 10,
        16: 12
    }
    ''':attr: defines the length (number of values) for the individual parameter lines'''

    def create_table(self):
        """
        :method: Creates initially the empty Lines table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists HvVhRibs;")
        query.exec("create table if not exists HvVhRibs ("
                   "OrderNum INTEGER,"
                   "Type INTEGER,"
                   "IniRib INTEGER,"
                   "ParamA INTEGER,"
                   "ParamB INTEGER,"
                   "ParamC INTEGER,"
                   "ParamD REAL,"
                   "ParamE REAL,"
                   "ParamF REAL,"
                   "ParamG REAL,"
                   "ParamH REAL,"
                   "ParamI REAL,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("HvVhRibs")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(self.OrderNumCol, Qt.Orientation.Horizontal, _("Order num"))
        self.setHeaderData(self.TypeCol, Qt.Orientation.Horizontal, _("Type"))
        self.setHeaderData(self.IniRibCol, Qt.Orientation.Horizontal, _("Ini Rib"))
        self.setHeaderData(self.ParamACol, Qt.Orientation.Horizontal, _("Param A"))
        self.setHeaderData(self.ParamBCol, Qt.Orientation.Horizontal, _("Param B"))
        self.setHeaderData(self.ParamCCol, Qt.Orientation.Horizontal, _("Param C"))
        self.setHeaderData(self.ParamDCol, Qt.Orientation.Horizontal, _("Param D"))
        self.setHeaderData(self.ParamECol, Qt.Orientation.Horizontal, _("Param E"))
        self.setHeaderData(self.ParamFCol, Qt.Orientation.Horizontal, _("Param F"))
        self.setHeaderData(self.ParamGCol, Qt.Orientation.Horizontal, _("Param G"))
        self.setHeaderData(self.ParamHCol, Qt.Orientation.Horizontal, _("Param H"))
        self.setHeaderData(self.ParamICol, Qt.Orientation.Horizontal, _("Param I"))

    def update_row(self, config_num, order_num, typ, ini_rib, param_a, param_b, param_c, param_d, param_e, param_f,
                   param_g, param_h=0, param_i=0):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE HvVhRibs SET "
                      "Type= :typ, "
                      "IniRib= :ini_rib, "
                      "ParamA= :param_a, "
                      "ParamB= :param_b, "
                      "ParamC= :param_c, "
                      "ParamD= :param_d, "
                      "ParamE= :param_e, "
                      "ParamF= :param_f, "
                      "ParamG= :param_g, "
                      "ParamH= :param_h, "
                      "ParamI= :param_i "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":typ", typ)
        query.bindValue(":ini_rib", ini_rib)
        query.bindValue(":param_a", param_a)
        query.bindValue(":param_b", param_b)
        query.bindValue(":param_c", param_c)
        query.bindValue(":param_d", param_d)
        query.bindValue(":param_e", param_e)
        query.bindValue(":param_f", param_f)
        query.bindValue(":param_g", param_g)
        query.bindValue(":param_h", param_h)
        query.bindValue(":param_i", param_i)
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
                      "Type, "
                      "IniRib, "
                      "ParamA, "
                      "ParamB, "
                      "ParamC, "
                      "ParamD, "
                      "ParamE, "
                      "ParamF, "
                      "ParamG, "
                      "ParamH, "
                      "ParamI "
                      "FROM HvVhRibs WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
