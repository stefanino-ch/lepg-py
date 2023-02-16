"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class IntradosColsConfModel(SqlTableModel, metaclass=Singleton):
    """
    :class: provides a SqlTableModel holding all data related to the Intrados colors configuration
    """
    __className = 'IntradosColsConfModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a config'''
    FirstRibCol = 1
    ''':attr: number of the column holding the first rib of the config'''
    ConfigNumCol = 2
    ''':attr: number of the column holding the config number'''

    def createTable(self):
        """
        :method: Creates initially the empty table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists IntradColsConf;")
        query.exec("create table if not exists IntradColsConf ("
                   "OrderNum INTEGER,"
                   "FirstRib INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("IntradColsConf")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(self.FirstRibCol, Qt.Orientation.Horizontal, _("Rib num"))

    def updateRow(self, configNum, firstRib):
        query = QSqlQuery()
        query.prepare("UPDATE IntradColsConf SET FirstRib= :first_rib WHERE (ConfigNum = :config);")
        query.bindValue(":first_rib", firstRib)
        query.bindValue(":config", configNum)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def getRow(self, configNum):
        """
        :method: reads values back from the internal database for a specific config and order number
        :param configNum: Configuration number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "FirstRib "
                      "FROM IntradColsConf WHERE (ConfigNum = :config)")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        return query.value
