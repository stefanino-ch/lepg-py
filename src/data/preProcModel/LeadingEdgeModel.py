"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from Singleton.Singleton import Singleton
from data.SqlTableModel import SqlTableModel


class LeadingEdgeModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data for leading
            edge definition.
    """
    OrderNumCol = 0
    TypeCol = 1
    aOneCol = 2
    bOneCol = 3
    xOneCol = 4
    xTwoCol = 5
    xmCol = 6
    cZeroOneCol = 7
    exOneCol = 8
    cZeroTwoCol = 9
    exTwoCol = 10
    ConfigNumCol = 11

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("LeadingEdge")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Type"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("a1 [cm]"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("b1 [cm]"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("x1 [cm]"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("x2 [cm]"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("xm [cm]"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("c01 [cm]"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("ex1 [coef]"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("c02 [coef]"))
        self.setHeaderData(10, Qt.Orientation.Horizontal, _("ex2 [coef]"))

        self.set_num_rows_for_config(1, 1)

    def create_table(self):
        """
        :method: Creates initially the table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists LeadingEdge;")
        query.exec("create table if not exists LeadingEdge ("
                   "OrderNum INTEGER, "
                   "Type INTEGER, "
                   "a_one REAL, "
                   "b_one REAL, "
                   "x_one INTEGER, "
                   "x_two INTEGER, "
                   "xm INTEGER, "
                   "c_zero_one INTEGER, "
                   "ex_one REAL, "
                   "c_zero_two INTEGER, "
                   "ex_two REAL, "
                   "ConfigNum INTEGER, "
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, type_num,
                   a_one, b_one,
                   x_one, x_two, xm, c_zero_one, ex_one,
                   c_zero_two, ex_two):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE LeadingEdge SET "
                      "Type= :typeN, "
                      "a_one= :a_one, "
                      "b_one= :b_one, "
                      "x_one= :x_one, "
                      "x_two= :x_two, "
                      "xm= :xm, "
                      "c_zero_one= :c_zero_one, "
                      "ex_one= :ex_one, "
                      "c_zero_two= :c_zero_two, "
                      "ex_two= :ex_two "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":typeN", type_num)
        query.bindValue(":a_one", a_one)
        query.bindValue(":b_one", b_one)
        query.bindValue(":x_one", x_one)
        query.bindValue(":x_two", x_two)
        query.bindValue(":xm", xm)
        query.bindValue(":c_zero_one", c_zero_one)
        query.bindValue(":ex_one", ex_one)
        query.bindValue(":c_zero_two", c_zero_two)
        query.bindValue(":ex_two", ex_two)
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
                      "Type, "
                      "a_one, "
                      "b_one, "
                      "x_one, "
                      "x_two, "
                      "xm, "
                      "c_zero_one, "
                      "ex_one, "
                      "c_zero_two, "
                      "ex_two "
                      "FROM LeadingEdge "
                      "WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()
        return query.value
