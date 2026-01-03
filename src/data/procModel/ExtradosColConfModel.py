"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class ExtradosColConfModel(SqlTableModel, metaclass=Singleton):
    """
    :class: provides a SqlTableModel holding all data related to the Extrados colors configuration
    """
    __config_type = 0
    ''' :attr: Stores the current configuration type '''
    usageUpd = pyqtSignal()
    ''' :signal: emitted as soon the usage flag is changed '''
    OrderNumCol = 0
    ''':attr: num of column for 1..3: ordering the individual lines of a config'''
    FirstRibCol = 1
    ''':attr: number of the column holding the first rib of the config'''
    ConfigNumCol = 2
    ''':attr: number of the column holding the config number'''

    @staticmethod
    def create_table():
        """
        :method: Creates initially the empty table.
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists ExtradColsConf;")
        query.exec("create table if not exists ExtradColsConf ("
                   "OrderNum INTEGER,"
                   "FirstRib INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.__config_type = 0
        self.create_table()
        self.setTable("ExtradColsConf")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(self.FirstRibCol, Qt.Orientation.Horizontal, _("Rib num"))

    def update_row(self, config_num, first_rib):
        query = QSqlQuery()
        query.prepare("UPDATE ExtradColsConf SET FirstRib= :first_rib WHERE (ConfigNum = :config);")
        query.bindValue(":first_rib", first_rib)
        query.bindValue(":config", config_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    @staticmethod
    def get_row(config_num):
        """
        :method: reads values back from the internal database for a specific config and order number
        :param config_num: Configuration number. Starting with 1
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "FirstRib "
                      "FROM ExtradColsConf WHERE (ConfigNum = :config)")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        return query.value

    def set_type(self, config_type):
        """
        :method: Set and remember the configuration type currently in use
        :param config_type: Configuration type 0: not used, 1: old style, 2: new style
        :return: na
        """
        self.__config_type = config_type
        self.usageUpd.emit()

    def type(self):
        """
        :method: Return the configuration type currently used in use
        :return: 0: not used, 1: old style, 2: new style
        """
        return self.__config_type
