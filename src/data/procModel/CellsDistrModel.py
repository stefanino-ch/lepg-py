"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from Singleton.Singleton import Singleton
from data.SqlTableModel import SqlTableModel


class CellsDistrModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all for cells distribution.
    """
    OrderNumCol = 0
    DistrTypeCol = 1
    CoefCol = 2
    WidthCol = 3
    NumCellsCol = 4
    ConfigNumCol = 5

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("PreProcCellsDistr")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Cell Num"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Coef"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Width"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Num cells"))

        self.set_num_rows_for_config(1, 1)

    def create_table(self):
        """
        :method: Creates initially the table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists PreProcCellsDistr;")
        query.exec("create table if not exists PreProcCellsDistr ("
                   "OrderNum INTEGER, "
                   "DistrType INTEGER, "
                   "Coef REAL, "
                   "Width REAL, "
                   "NumCells INTEGER, "
                   "ConfigNum INTEGER, "
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, distr_type, coef, width,
                   num_cells):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE PreProcCellsDistr SET "
                      "DistrType = :distr_type, "
                      "Coef = :coef, "
                      "Width = :width, "
                      "NumCells = :num_cells "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":distr_type", distr_type)
        query.bindValue(":coef", coef)
        query.bindValue(":width", width)
        query.bindValue(":num_cells", num_cells)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)

        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def get_row(self, config_num, order_num):
        """
        :method: Reads values back from the internal database for a
                 config and order number
        :param config_num: Starting with 1
        :param order_num: Starting with 1
        :return: values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "DistrType, "
                      "Coef, "
                      "Width, "
                      "NumCells "
                      "FROM PreProcCellsDistr "
                      "WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()
        return query.value

    def update_type(self, config_num, order_num, distr_type):
        # TODO: doc

        query = QSqlQuery()
        query.prepare("UPDATE PreProcCellsDistr SET "
                      "DistrType= :typeN "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":typeN", distr_type)

        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def get_type(self, config_num, order_num):
        """
        :method: Reads type value back from the internal database for
                 a config and order number
        :param config_num: Starting with 1
        :param order_num: Starting with 1
        :return: type value
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "DistrType "
                      "FROM PreProcCellsDistr "
                      "WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()

        if query.value(0) == '':
            return 1
        else:
            return query.value(0)
