"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from Singleton.Singleton import Singleton
from data.SqlTableModel import SqlTableModel


class TrailingEdgeModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data for trailing
            edge definition
    """
    __className = 'TrailingEdgeModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    OrderNumCol = 0
    TypeCol = 1
    aOneCol = 2
    bOneCol = 3
    xOneCol = 4
    xmCol = 5
    cZeroCol = 6
    yZeroCol = 7
    expCol = 8
    ConfigNumCol = 9

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("TrailingEdge")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Type"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("a1 [cm]"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("b1 [cm]"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("x1 [cm]"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("xm [cm]"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("c0 [cm]"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("y0 [cm]"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("exp [coef]"))

        self.set_num_rows_for_config(1, 1)

    def create_table(self):
        """
        :method: Creates initially the table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists TrailingEdge;")
        query.exec("create table if not exists TrailingEdge ("
                   "OrderNum INTEGER, "
                   "Type INTEGER, "
                   "a_one REAL, "
                   "b_one REAL, "
                   "x_one INTEGER, "
                   "xm INTEGER, "
                   "cZero REAL, "
                   "yZero REAL, "
                   "exp REAL, "
                   "ConfigNum INTEGER, "
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, type_num,
                   a_one, b_one,
                   x_one, xm, c_zero, y_zero, exp):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE TrailingEdge SET "
                      "Type= :typeN, "
                      "a_one= :a_one, "
                      "b_one= :b_one, "
                      "x_one= :x_one, "
                      "xm= :xm, "
                      "cZero= :cZero, "
                      "yZero= :yZero, "
                      "exp= :exp "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":typeN", type_num)
        query.bindValue(":a_one", a_one)
        query.bindValue(":b_one", b_one)
        query.bindValue(":x_one", x_one)
        query.bindValue(":xm", xm)
        query.bindValue(":cZero", c_zero)
        query.bindValue(":yZero", y_zero)
        query.bindValue(":exp", exp)
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
                      "xm, "
                      "cZero, "
                      "yZero, "
                      "exp "
                      "FROM TrailingEdge "
                      "WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()
        return query.value
