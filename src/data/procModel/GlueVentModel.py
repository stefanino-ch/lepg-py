"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class GlueVentModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the glue vent parameters.
    """
    __className = 'GlueVentModel'
    '''
    :attr: Does help to indicate the source of the log messages.
    '''
    __isUsed = False
    '''
    :attr: Helps to remember if the section is in use or not
    '''

    usageUpd = pyqtSignal()
    '''
    :signal: emitted as soon the usage flag is changed
    '''

    OrderNumCol = 0
    '''
    :attr: Num of column for ordering the individual lines of a config
    '''
    VentParamCol = 1
    '''
    :attr: Number of the col holding the vent parameter
    '''
    ParamACol = 2
    '''
    :attr: Number of the col holding the additional parameter A (1)
    '''
    ParamBCol = 3
    '''
    :attr: Number of the col holding the additional parameter B (2)
    '''
    ParamCCol = 4
    '''
    :attr: Number of the col holding the additional parameter C (3)
    '''
    ConfigNumCol = 5
    ''':attr: num of column for config number (always 1)'''

    def __init__(self, parent=None):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("GlueVent")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(self.OrderNumCol,
                           Qt.Orientation.Horizontal,
                           _("Airfoil num"))
        self.setHeaderData(self.VentParamCol,
                           Qt.Orientation.Horizontal,
                           _("Vent param"))
        self.setHeaderData(self.ParamACol,
                           Qt.Orientation.Horizontal,
                           _("Opt param 1"))
        self.setHeaderData(self.ParamCCol,
                           Qt.Orientation.Horizontal,
                           _("Opt param 2"))
        self.setHeaderData(self.ParamBCol,
                           Qt.Orientation.Horizontal,
                           _("Opt param 3"))

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists GlueVent;")
        query.exec("create table if not exists GlueVent ("
                   "OrderNum INTEGER, "
                   "VentParam REAL, "
                   "ParamA INTEGER, "
                   "ParamB INTEGER, "
                   "ParamC INTEGER, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num,
                   vent_param, param_a, param_b, param_c):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here
                 as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE GlueVent SET "
                      "VentParam= :vent_param, "
                      "ParamA= :param_a, "
                      "ParamB= :param_b, "
                      "ParamC= :param_c "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.bindValue(":vent_param", vent_param)
        query.bindValue(":param_a", param_a)
        query.bindValue(":param_b", param_b)
        query.bindValue(":param_c", param_c)
        query.exec()
        self.select()  # assure the model is updated properly

    def set_is_used(self, is_used):
        """
        :method: Set the usage flag of the section
        :param is_used: True if section is in use, False otherwise
        """
        self.__isUsed = is_used
        self.usageUpd.emit()

    def is_used(self):
        """
        :method: Returns the information if the section is in use or not
        :returns: True if section is in use, false otherwise
        """
        return self.__isUsed

    def get_row(self, config_num, order_num):
        """
        :method: Reads values back from the internal database for a
                 specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1

        :return: Values read from internal database
        :rtype: QRecord
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "OrderNum, "
                      "VentParam, "
                      "ParamA, "
                      "ParamB, "
                      "ParamC "
                      "FROM GlueVent WHERE (ConfigNum = :config) "
                      "ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.record()
