"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class ThreeDShPrintModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the Print data for 3d Shaping
    """
    OrderNumCol = 0
    '''
    :attr: Num of column for ordering the individual lines
           of a config
    '''
    NameCol = 1
    '''
    :attr: Number of the col holding the layer name
    '''
    DrawCol = 2
    '''
    :attr: Number of the col holding the info if the layer shall
           be drawn
    '''
    FirstPanelCol = 3
    '''
    :attr: Number of the col holding the number of the first panel
           to print
    '''
    LastPanelCol = 4
    '''
    :attr: Number of the col holding the number of the last panel
           to print
    '''
    SymmetricCol = 5
    '''
    :attr: Number of the col holding the symmetric information
    '''
    ConfigNumCol = 6
    '''
    :attr: num of column for config number
    '''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists ThreeDShapingPrint;")
        query.exec("create table if not exists ThreeDShapingPrint ("
                   "OrderNum INTEGER, "
                   "Name TEXT, "
                   "Draw INTEGER, "
                   "FirstPanel INTEGER, "
                   "LastPanel INTEGER, "
                   "Symmetric INTEGER, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("ThreeDShapingPrint")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.set_num_configs(1)
        self.set_num_rows_for_config(1, 5)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Name"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Draw"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("First panel"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Last panel"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Symmetric"))

    def update_row(self, config_num, order_num, name, draw,
                   first_panel, last_panel, symmetric):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here
                 as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE ThreeDShapingPrint SET "
                      "Name= :name, "
                      "Draw= :draw, "
                      "FirstPanel= :firstPanel, "
                      "LastPanel= :lastPanel, "
                      "Symmetric= :symmetric "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":name", name)
        query.bindValue(":draw", draw)
        query.bindValue(":firstPanel", first_panel)
        query.bindValue(":lastPanel", last_panel)
        query.bindValue(":symmetric", symmetric)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def get_row(self, config_num, order_num):
        """
        :method: Reads values back from the internal database for a
                 specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "Name, "
                      "Draw, "
                      "FirstPanel, "
                      "LastPanel, "
                      "Symmetric "
                      "FROM ThreeDShapingPrint WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
