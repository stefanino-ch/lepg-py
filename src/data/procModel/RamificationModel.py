"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class RamificationModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the ramification parameters.
    """
    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a config'''
    RowsCol = 1
    ''':attr: Number of the col holding the number of rows'''
    ThirdToSailCol = 2
    ''':attr: Number of the col holding the distance branching third to sail (l3)'''
    FourthToSailCol = 3
    ''':attr: Number of the col holding the distance beginning of fourth branching to sail (l2)'''
    ConfigNumCol = 4
    ''':attr: num of column for config number'''

    def createTable(self):
        """
        :method: Creates initially the empty Ramification table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists Ramification;")
        query.exec("create table if not exists Ramification ("
                   "OrderNum INTEGER,"
                   "Rows INTEGER,"
                   "ThirdToSail INTEGER,"
                   "FourthToSail INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("Ramification")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Rows"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Third to sail [cm]"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Fourth to sail [cm]"))

        self.set_num_rows_for_config(1, 4)

    def updateDataRow(self, configNum, orderNum, rows, thirdToSail, fourthToSail):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE Ramification SET "
                      "Rows= :rows, "
                      "ThirdToSail= :thirdToSail, "
                      "FourthToSail= :fourthToSail "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":rows", rows)
        query.bindValue(":thirdToSail", thirdToSail)
        query.bindValue(":fourthToSail", fourthToSail)
        query.bindValue(":config", configNum)
        query.bindValue(":order", orderNum)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def getRow(self, configNum, orderNum):
        """
        :method: reads values back from the internal database for a specific config and order number
        :param configNum: Configuration number. Starting with 1
        :param orderNum: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "Rows, "
                      "ThirdToSail,"
                      "FourthToSail "
                      "FROM Ramification WHERE (ConfigNum = :config AND OrderNum = :order)")
        query.bindValue(":config", configNum)
        query.bindValue(":order", orderNum)
        query.exec()
        query.next()
        return query.value
