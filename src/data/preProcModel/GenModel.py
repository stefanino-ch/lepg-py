"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from Singleton.Singleton import Singleton
from data.SqlTableModel import SqlTableModel


class GenModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the general data
    """
    OrderNumCol = 0
    WingNameCol = 1
    ConfigNumCol = 2

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("PreProcGen")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Wing name"))

        self.set_num_rows_for_config(1, 1)

    def create_table(self):
        """
        :method: Creates initially the table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists PreProcGen;")
        query.exec("create table if not exists PreProcGen ("
                   "OrderNum INTEGER, "
                   "WingN TEXT, "
                   "ConfigNum INTEGER, "
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, wing_n):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE PreProcGen SET "
                      "WingN = :wing_n "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":wing_n", wing_n)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)

        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def get_row(self, config_num, order_num):
        """
        :method: Reads values back from the internal database for a config
                 and order number
        :param config_num: Starting with 1
        :param order_num: Starting with 1
        :return: values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "WingN "
                      "FROM PreProcGen "
                      "WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()
        return query.value
