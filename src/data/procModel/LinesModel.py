"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class LinesModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the lines parameters.
    """
    __className = 'LinesModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    OrderNumCol = 0
    '''
    :attr: num of column for 1..3: ordering the individual lines
           of a config
    '''
    NumBranchesCol = 1
    ''':attr: Number of the col holding the number of branches'''
    LevelOfRamOneCol = 2
    ''':attr: Number of the col holding the branching level 1 value'''
    OrderLvlOneCol = 3
    ''':attr: Number of the col holding order at level 1 value'''
    LevelOfRamTwoCol = 4
    ''':attr: Number of the col holding level of ramification 2 value'''
    OrderLvlTwoCol = 5
    ''':attr: Number of the col holding order at level 2 value'''
    LevelOfRamThreeCol = 6
    ''':attr: Number of the col holding level of ramification 3 value'''
    OrderLvlThreeCol = 7
    ''':attr: Number of the col holding order at level 3 value'''
    LevelOfRamFourCol = 8
    ''':attr: Number of the col holding branching level 4 value'''
    OrderLvlFourCol = 9
    ''':attr: Number of the col holding order at level 4 value'''
    AnchorLineCol = 10
    '''
    :attr: Number of the col holding the  anchor line (
           1 = A, 2 = B, 3 = C, 4 = D, 5 = E, 6 = brake) value
    '''

    AnchorRibNumCol = 11
    ''':attr: Number of the col holding the anchor rib number value'''
    ConfigNumCol = 12
    ''':attr: num of column for config number'''

    def create_table(self):
        """
        :method: Creates initially the empty Lines table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists Lines;")
        query.exec("create table if not exists Lines ("
                   "OrderNum INTEGER,"
                   "NumBranches INTEGER,"
                   "BranchLvlOne INTEGER,"
                   "OrderLvlOne INTEGER,"
                   "LevelOfRamTwo INTEGER,"
                   "OrderLvlTwo INTEGER,"
                   "LevelOfRamThree INTEGER,"
                   "OrderLvlThree INTEGER,"
                   "BranchLvlFour INTEGER,"
                   "OrderLvlFour INTEGER,"
                   "AnchorLine INTEGER,"
                   "AnchorRibNum INTEGER,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("Lines")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Num branches"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Ramif 1"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Node 1"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Ramif 2"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Node 2"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Ramif 3"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Node 3"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("Ramif 4"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("Node 4"))
        self.setHeaderData(10, Qt.Orientation.Horizontal, _("Anchor"))
        self.setHeaderData(11, Qt.Orientation.Horizontal, _("Rib num"))

    def update_row(self, config_num, order_num, i1, i2, i3, i4, i5, i6,
                   i7, i8, i9, i10, i11):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here
                 as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE Lines SET "
                      "NumBranches= :i1, "
                      "BranchLvlOne= :i2, "
                      "OrderLvlOne= :i3, "
                      "LevelOfRamTwo= :i4, "
                      "OrderLvlTwo= :i5, "
                      "LevelOfRamThree= :i6, "
                      "OrderLvlThree= :i7, "
                      "BranchLvlFour= :i8, "
                      "OrderLvlFour= :i9, "
                      "AnchorLine= :i10, "
                      "AnchorRibNum= :i11 "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":i1", i1)
        query.bindValue(":i2", i2)
        query.bindValue(":i3", i3)
        query.bindValue(":i4", i4)
        query.bindValue(":i5", i5)
        query.bindValue(":i6", i6)
        query.bindValue(":i7", i7)
        query.bindValue(":i8", i8)
        query.bindValue(":i9", i9)
        query.bindValue(":i10", i10)
        query.bindValue(":i11", i11)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated

    def set_num_configs(self, must_num_configs):
        """
        :method: Assures the model will be setup to hold the correct
                 number of configs based on parameters passed
        :param must_num_configs: Number of configs the model must provide
        """
        curr_num_configs = self.num_configs()

        diff = abs(must_num_configs - curr_num_configs)
        if diff != 0:
            # do it only if really the number has changed
            i = 0
            if must_num_configs > curr_num_configs:
                # add config lines
                while i < diff:
                    self.add_row_for_config(curr_num_configs + 1 + i)
                    i += 1
            else:
                # remove config lines
                while i < diff:
                    self.remove_row_for_config(curr_num_configs - i)
                    i += 1

            # emit the change signal
            self.numConfigsChanged.emit(self.num_configs())

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
                      "NumBranches, "
                      "BranchLvlOne, "
                      "OrderLvlOne, "
                      "LevelOfRamTwo, "
                      "OrderLvlTwo, "
                      "LevelOfRamThree, "
                      "OrderLvlThree, "
                      "BranchLvlFour, "
                      "OrderLvlFour, "
                      "AnchorLine, "
                      "AnchorRibNum "
                      "FROM Lines WHERE (ConfigNum = :config) "
                      "ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
