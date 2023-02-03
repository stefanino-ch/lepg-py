"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from Singleton.Singleton import Singleton
from data.SqlTableModel import SqlTableModel


class VaultModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data for the vault
            definition.
    """
    OrderNumCol = 0
    TypeCol = 1
    aOneCol = 2
    bOneCol = 3
    xOneCol = 4
    cOneCol = 5
    rOneRACol = 6
    rTwoRACol = 7
    rThrRACol = 8
    rFouRACol = 9
    aOneRACol = 10
    aTwoRACol = 11
    aThrRACol = 12
    aFouRACol = 13
    ConfigNumCol = 14

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("Vault")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(2, Qt.Orientation.Horizontal, _("a1 [cm]"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("b1 [cm]"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("x1 [cm]"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("c1 [cm]"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("r1 [cm]"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("r2 [cm]"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("r3 [cm]"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("r4 [cm]"))
        self.setHeaderData(10, Qt.Orientation.Horizontal, _("a1 [deg]"))
        self.setHeaderData(11, Qt.Orientation.Horizontal, _("a2 [deg]"))
        self.setHeaderData(12, Qt.Orientation.Horizontal, _("a3 [deg]"))
        self.setHeaderData(13, Qt.Orientation.Horizontal, _("a4 [deg]"))

        self.set_num_rows_for_config(1, 1)

    def create_table(self):
        """
        :method: Creates initially the table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists Vault;")
        query.exec("create table if not exists Vault ("
                   "OrderNum INTEGER, "
                   "Type INTEGER, "
                   "a_one REAL, "
                   "b_one REAL, "
                   "x_one REAL, "
                   "cOne REAL, "
                   "rOneRA REAL, "
                   "rTwoRA REAL, "
                   "rThrRA REAL, "
                   "rFouRA REAL, "
                   "aOneRA REAL, "
                   "aTwoRA REAL, "
                   "aThrRA REAL, "
                   "aFouRA REAL, "
                   "ConfigNum INTEGER, "
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, type_num,
                   a_one, b_one,
                   x_one, c_one,
                   r_one_ra, r_two_ra, r_thr_ra, r_fou_ra,
                   a_one_ra, a_two_ra, a_thr_ra, a_fou_ra):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE Vault SET "
                      "Type= :typeN, "
                      "a_one= :a_one, "
                      "b_one= :b_one, "
                      "x_one= :x_one, "
                      "cOne= :cOne, "
                      "rOneRA= :rOneRA, "
                      "rTwoRA= :rTwoRA, "
                      "rThrRA= :rThrRA, "
                      "rFouRA= :rFouRA, "
                      "aOneRA= :aOneRA, "
                      "aTwoRA= :aTwoRA, "
                      "aThrRA= :aThreRA, "
                      "aFouRA= :aFouRA  "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":typeN", type_num)
        query.bindValue(":a_one", a_one)
        query.bindValue(":b_one", b_one)
        query.bindValue(":x_one", x_one)
        query.bindValue(":cOne", c_one)

        query.bindValue(":rOneRA", r_one_ra)
        query.bindValue(":rTwoRA", r_two_ra)
        query.bindValue(":rThrRA", r_thr_ra)
        query.bindValue(":rFouRA", r_fou_ra)

        query.bindValue(":aOneRA", a_one_ra)
        query.bindValue(":aTwoRA", a_two_ra)
        query.bindValue(":aThreRA", a_thr_ra)
        query.bindValue(":aFouRA", a_fou_ra)

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
                      "cOne, "
                      "rOneRA, "
                      "rTwoRA, "
                      "rThrRA, "
                      "rFouRA, "
                      "aOneRA, "
                      "aTwoRA, "
                      "aThrRA, "
                      "aFouRA "
                      "FROM Vault "
                      "WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()
        return query.value

    def update_type(self, config_num, order_num, type_num):
        query = QSqlQuery()
        query.prepare("UPDATE Vault SET "
                      "Type= :typeN "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":typeN", type_num)

        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        # to a select() to assure the model is updated properly
        self.select()

    def get_type(self, config_num, order_num):
        """
        :method: Reads type value back from the internal database for a
                 config and order number
        :param config_num: Starting with 1
        :param order_num: Starting with 1
        :return: type value
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "Type "
                      "FROM Vault "
                      "WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()
        return query.value(0)
