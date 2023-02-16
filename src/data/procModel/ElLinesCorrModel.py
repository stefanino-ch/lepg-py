"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class ElLinesCorrModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the parameters for the elastic lines correction.
    """
    __className = 'ElLinesCorrModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    LoadCol = 0
    ''':attr: Num of column for flight load'''
    TwoLineDistACol = 1
    ''':attr: Num of column for 1st two line load dist'''
    TwoLineDistBCol = 2
    ''':attr: Num of column for 2nd two line load dist'''
    ThreeLineDistACol = 3
    ''':attr: Num of column for 1st tree line load dist'''
    ThreeLineDistBCol = 4
    ''':attr: Num of column for 2nd tree line load dist'''
    ThreeLineDistCCol = 5
    ''':attr: Num of column for 3rd tree line load dist'''
    FourLineDistACol = 6
    ''':attr: Num of column for 1st four line load distr'''
    FourLineDistBCol = 7
    ''':attr: Num of column for 2nd four line load distr'''
    FourLineDistCCol = 8
    ''':attr: Num of column for 3rd four line load distr'''
    FourLineDistDCol = 9
    ''':attr: Num of column for 4th four line load distr'''
    FiveLineDistACol = 10
    ''':attr: Num of column for 1st five line load distr'''
    FiveLineDistBCol = 11
    ''':attr: Num of column for 2nd five line load distr'''
    FiveLineDistCCol = 12
    ''':attr: Num of column for 3rd five line load distr'''
    FiveLineDistDCol = 13
    ''':attr: Num of column for 4th five line load distr'''
    FiveLineDistECol = 14
    ''':attr: Num of column for 5th five line load distr'''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists ElasticLinesCorr;")
        query.exec("create table if not exists ElasticLinesCorr ("
                   "Load REAL,"
                   "TwoLineDistA REAL, "
                   "TwoLineDistB REAL, "
                   "ThreeLineDistA REAL, "
                   "ThreeLineDistB REAL, "
                   "ThreeLineDistC REAL, "
                   "FourLineDistA REAL, "
                   "FourLineDistB REAL, "
                   "FourLineDistC REAL, "
                   "FourLineDistD REAL, "
                   "FiveLineDistA REAL, "
                   "FiveLineDistB REAL, "
                   "FiveLineDistC REAL, "
                   "FiveLineDistD REAL, "
                   "FiveLineDistE REAL, "
                   "ID INTEGER PRIMARY KEY);")
        query.exec("INSERT into ElasticLinesCorr (ID) Values( '1' );")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("ElasticLinesCorr")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

    def get_row(self):
        """
        :method: reads values back from the internal database
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "Load, "
                      "TwoLineDistA, "
                      "TwoLineDistB, "
                      "ThreeLineDistA, "
                      "ThreeLineDistB, "
                      "ThreeLineDistC, "
                      "FourLineDistA, "
                      "FourLineDistB, "
                      "FourLineDistC, "
                      "FourLineDistD, "
                      "FiveLineDistA, "
                      "FiveLineDistB, "
                      "FiveLineDistC, "
                      "FiveLineDistD, "
                      "FiveLineDistE "
                      "FROM ElasticLinesCorr")
        query.exec()
        query.next()
        return query.value
