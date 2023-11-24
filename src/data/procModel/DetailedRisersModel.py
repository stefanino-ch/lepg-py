"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class DetailedRisersModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel for the detailed raisers data
    """
    __isUsed = False
    ''' :attr: Helps to remember if the section is in use or not'''

    usageUpd = pyqtSignal()
    '''
    :signal: emitted as soon the usage flag is changed
    '''
    OrderNumCol = 0
    '''
    :attr: num of column for ordering the individual lines
           of a config
    '''
    ''':attr: Number of the col holding the riser A length'''
    LengthACol = 1
    ''':attr: Number of the col holding the riser B length'''
    LengthBCol = 2
    ''':attr: Number of the col holding the riser C length'''
    LengthCCol = 3
    ''':attr: Number of the col holding the riser D length'''
    LengthDCol = 4
    ''':attr: Number of the col holding the riser E length'''
    LengthECol = 5
    ''':attr: num of column for config number'''
    ConfigNumCol = 6

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("DetailedRisers")

        self.setHeaderData(self.LengthACol, Qt.Orientation.Horizontal, _("Riser A"))
        self.setHeaderData(self.LengthBCol, Qt.Orientation.Horizontal, _("Riser B"))
        self.setHeaderData(self.LengthCCol, Qt.Orientation.Horizontal, _("Riser C"))
        self.setHeaderData(self.LengthDCol, Qt.Orientation.Horizontal, _("Riser D"))
        self.setHeaderData(self.LengthECol, Qt.Orientation.Horizontal, _("Riser E"))

        self.set_num_rows_for_config(1, 1)
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists DetailedRisers;")
        query.exec("create table if not exists DetailedRisers ("
                   "OrderNum INTEGER,"
                   "LengthA REAL,"
                   "LengthB REAL,"
                   "LengthC REAL,"
                   "LengthD REAL,"
                   "LengthE REAL,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, length_a, length_b, length_c, length_d, length_e):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here as
                 they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE DetailedRisers SET "
                      "LengthA= :length_a, "
                      "LengthB= :length_b, "
                      "LengthC= :length_c, "
                      "LengthD= :length_d, "
                      "LengthE= :length_e "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":length_a", length_a)
        query.bindValue(":length_b", length_b)
        query.bindValue(":length_c", length_c)
        query.bindValue(":length_d", length_d)
        query.bindValue(":length_e", length_e)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated

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
        :method: reads values back from the internal database for a
                 specific config and order number
        :param config_num: Configuration number. Starting with 1
        :param order_num: Order number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "OrderNum, "
                      "LengthA, "
                      "LengthB, "
                      "LengthC, "
                      "LengthD, "
                      "LengthE "
                      "FROM DetailedRisers WHERE (ConfigNum = :config) "
                      "ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
