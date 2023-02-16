"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class LightConfModel(SqlTableModel, metaclass=Singleton):
    """
    :class: provides a SqlTableModel holding all data related to the global lightening config parameters
    """

    __className = 'LightConfModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    __numConfigs = 0

    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a config'''
    InitialRibCol = 1
    ''':attr: number of the column holding the first rib of the config'''
    FinalRibCol = 2
    ''':attr: number of the column holding the final rib'''
    ConfigNumCol = 3
    ''':attr: number of the column holding the config number'''

    def createTable(self):
        """
        :method: Creates initially the empty LightConf table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists LightConf;")
        query.exec("create table if not exists LightConf ("
                   "OrderNum INTEGER,"
                   "InitialRib INTEGER,"
                   "FinalRib INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("LightConf")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Initial Rib"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Final Rib"))

    def updateRow(self, config, initialRib, finalRib):
        query = QSqlQuery()
        query.prepare("UPDATE LightConf SET InitialRib= :initial , FinalRib= :final WHERE (ConfigNum = :config);")
        query.bindValue(":initial", initialRib)
        query.bindValue(":final", finalRib)
        query.bindValue(":config", config)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def getRow(self, configNum):
        """
        :method: reads values back from the internal database for a specific config number
        :param configNum: Configuration number. Starting with 1.
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "InitialRib, "
                      "FinalRib "
                      "FROM LightConf WHERE (ConfigNum = :config)")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        return query.value
