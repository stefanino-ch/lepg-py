"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class XflrModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the data for XFLR5
    """
    __isUsed = False
    ''' :attr: Helps to remember if the section is in use or not'''

    usageUpd = pyqtSignal()
    '''
    :signal: emitted as soon the usage flag is changed
    '''

    OrderNumCol = 0
    ''':attr: '''
    chord_nr_Col = 1
    ''':attr: '''
    per_cell_Col = 2
    ''':attr: '''
    cos_dist_Col = 3
    ''':attr: '''
    uniform_Col = 4
    ''':attr: '''
    inc_bill_Col = 5
    ''':attr: '''
    ConfigNumCol = 6
    ''':attr: num of column for config number (always 1)'''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists xflr;")
        query.exec("create table if not exists xflr ("
                   "OrderNum INTEGER, "
                   "chord_nr INTEGER, "
                   "per_cell INTEGER, "
                   "cos_dist REAL, "
                   "uniform INTEGER, "
                   "inc_bill Text, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("xflr")

        self.set_num_rows_for_config(1, 1)

        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("cord nr"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("per cell"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("cosine dist"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("uniform"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Include bill"))

    def update_row(self, config_num, order_num, chord_nr, per_cell, cos_dist, uniform, inc_bill):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE xflr SET "
                      "chord_nr= :chord_nr, "
                      "per_cell= :per_cell, "
                      "cos_dist= :cos_dist, "
                      "uniform= :uniform, "
                      "inc_bill= :inc_bill "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":chord_nr", chord_nr)
        query.bindValue(":per_cell", per_cell)
        query.bindValue(":cos_dist", cos_dist)
        query.bindValue(":uniform", uniform)
        query.bindValue(":inc_bill", inc_bill)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

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
        :method: reads values back from the internal database for a specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "OrderNum, "
                      "chord_nr, "
                      "per_cell, "
                      "cos_dist, "
                      "uniform, "
                      "inc_bill "
                      "FROM xflr WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
