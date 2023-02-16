"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class NewSkinTensConfModel(SqlTableModel, metaclass=Singleton):
    """
    :class: provides a SqlTableModel holding all data related to the group wide parameters for New Skin Tension
    """

    __className = 'NewSkinTensConfModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    __numConfigs = 0

    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    InitialRibCol = 1
    ''':attr: number of the column holding the first rib of the config'''
    FinalRibCol = 2
    ''':attr: number of the column holding the final rib'''
    TypeCol = 3
    ''':attr: number of the column holding type information'''
    ConfigNumCol = 4
    ''':attr: number of the column holding the config number'''

    def createTable(self):
        """
        :method: Creates initially the empty table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists NewSkinTensConf;")
        query.exec("create table if not exists NewSkinTensConf ("
                   "OrderNum INTEGER,"
                   "InitialRib INTEGER,"
                   "FinalRib INTEGER,"
                   "Type INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("NewSkinTensConf")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("First Rib"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Last Rib"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Type"))

    def updateRow(self, config, initialRib, finalRib, calcT):
        query = QSqlQuery()
        query.prepare(
            "UPDATE NewSkinTensConf SET InitialRib= :initial , FinalRib= :final, Type= :calcT WHERE (ConfigNum = :config);")
        query.bindValue(":initial", initialRib)
        query.bindValue(":final", finalRib)
        query.bindValue(":calcT", calcT)
        query.bindValue(":config", config)
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
                      "OrderNum, "
                      "InitialRib, "
                      "FinalRib, "
                      "Type "
                      "FROM NewSkinTensConf WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
