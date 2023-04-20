"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class PartsSeparationModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the parts' separation
            settings.
    """
    __isUsed = False
    '''
    :attr: Helps to remember if the section is in use or not
    '''
    usageUpd = pyqtSignal()
    '''
    :signal: Emitted as soon the usage flag is changed
    '''
    OrderNumCol = 0
    '''
    :attr: Num of column for ordering the individual lines of a config
    '''
    Panel_x_col = 1
    '''
    :attr: Multiplication factor for x-direction panels separation
    '''
    Panel_x_min_col = 2
    '''
    :attr: Multiplication factor for x-direction panels minimum separation
    '''
    Panel_y_col = 3
    '''
    :attr: Multiplication factor for y-direction panels separation 
    '''
    Rib_x_col = 4
    '''
    :attr: Multiplication factor for x-direction ribs separation
    '''
    Rib_y_col = 5
    '''
    :attr: Multiplication factor for y-direction ribs separation
    '''
    Rib_1y_col = 6
    '''
    :attr: Parameter still not used
    '''
    Param7_col = 7
    '''
    :attr: Parameter still not used
    '''
    Param8_col = 8
    '''
    :attr: Parameter still not used
    '''
    Param9_col = 9
    '''
    :attr: Parameter still not used
    '''
    Param10_col = 10
    '''
    :attr: Parameter still not used
    '''
    ConfigNumCol = 11
    '''
    :attr: Num of column for config number (always 1)
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("PartsSeparation")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.set_num_rows_for_config(1, 1)

        self.setHeaderData(self.OrderNumCol,
                           Qt.Orientation.Horizontal,
                           _("Order num"))
        self.setHeaderData(self.Panel_x_col,
                           Qt.Orientation.Horizontal,
                           _("panel_x"))
        self.setHeaderData(self.Panel_x_min_col,
                           Qt.Orientation.Horizontal,
                           _("panel_x_min"))
        self.setHeaderData(self.Panel_y_col,
                           Qt.Orientation.Horizontal,
                           _("panel_y"))
        self.setHeaderData(self.Rib_x_col,
                           Qt.Orientation.Horizontal,
                           _("rib_x"))
        self.setHeaderData(self.Rib_y_col,
                           Qt.Orientation.Horizontal,
                           _("rib_y"))
        self.setHeaderData(self.Rib_1y_col,
                           Qt.Orientation.Horizontal,
                           _("rib_1y"))
        self.setHeaderData(self.Param7_col,
                           Qt.Orientation.Horizontal,
                           _("parameter7"))
        self.setHeaderData(self.Param8_col,
                           Qt.Orientation.Horizontal,
                           _("parameter8"))
        self.setHeaderData(self.Param9_col,
                           Qt.Orientation.Horizontal,
                           _("parameter9"))
        self.setHeaderData(self.Param10_col,
                           Qt.Orientation.Horizontal,
                           _("parameter10"))

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists PartsSeparation;")
        query.exec("create table if not exists PartsSeparation ("
                   "OrderNum INTEGER, "
                   "panel_x REAL, "
                   "panel_x_min REAL, "
                   "panel_y REAL, "
                   "rib_x REAL, "
                   "rib_y REAL, "
                   "rib_1y REAL, "
                   "param7 REAL, "
                   "param8 REAL, "
                   "param9 REAL, "
                   "param10 REAL, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num,
                   panel_x, panel_x_min, panel_y,
                   rib_x, rib_y,
                   rib_1y, param7, param8, param9, param10):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here
                 as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE PartsSeparation SET "
                      "panel_x= :panel_x, "
                      "panel_x_min= :panel_x_min, "
                      "panel_y= :panel_y, "
                      "rib_x= :rib_x, "
                      "rib_y= :rib_y, "
                      "rib_1y= :rib_1y, "
                      "param7= :param7, "
                      "param8= :param8, "
                      "param9= :param9, "
                      "param10= :param10 "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":panel_x", panel_x)
        query.bindValue(":panel_x_min", panel_x_min)
        query.bindValue(":panel_y", panel_y)
        query.bindValue(":rib_x", rib_x)
        query.bindValue(":rib_y", rib_y)
        query.bindValue(":rib_1y", rib_1y)
        query.bindValue(":param7", param7)
        query.bindValue(":param8", param8)
        query.bindValue(":param9", param9)
        query.bindValue(":param10", param10)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # assure the model is updated properly

    def set_is_used(self, is_used):
        """
        :method: Set the usage flag of the section
        :param is_used: True if section is in use, False otherwise
        :type is_used: bool
        """
        self.__isUsed = is_used
        self.usageUpd.emit()

    def is_used(self):
        """
        :method: Returns the information if the section is in use or not
        :returns: True if section is in use, false otherwise
        :rtype: bool
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
                      "panel_x, "
                      "panel_x_min, "
                      "panel_y, "
                      "rib_x, "
                      "rib_y, "
                      "rib_1y, "
                      "param7, "
                      "param8, "
                      "param9, "
                      "param10 "
                      "FROM PartsSeparation WHERE (ConfigNum = :config) "
                      "ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        return query.record()
