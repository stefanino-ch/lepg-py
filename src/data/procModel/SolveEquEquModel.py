"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class SolveEquEquModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the Solve Equilibrum Equations
    """
    __isUsed = False
    ''' :attr: Helps to remember if the section is in use or not'''

    usageUpd = pyqtSignal()
    '''
    :signal: emitted as soon the usage flag is changed
    '''

    OrderNumCol = 0
    ''':attr: '''
    g_Col = 1
    ''':attr: '''
    ro_Col = 2
    ''':attr: '''
    mu_Col = 3
    ''':attr: '''
    V_Col = 4
    ''':attr: '''
    Alpha_Col = 5
    ''':attr: '''
    Cl_Col = 6
    ''':attr: '''
    cle_Col = 7
    ''':attr: '''
    Cd_Col = 8
    ''':attr: '''
    cde_Col = 9
    ''':attr: '''
    Cm_Col = 10
    ''':attr: '''
    Splilot_Col = 11
    ''':attr: '''
    Cdplilot_Col = 12
    ''':attr: '''
    Mw_Col = 13
    ''':attr: '''
    Mp_Col = 14
    ''':attr: '''
    Pmc_Col = 15
    ''':attr: '''
    Mql_Col = 16
    ''':attr: '''
    Ycp_Col = 17
    ''':attr: '''
    Zcp_Col = 18
    ''':attr: '''
    ConfigNumCol = 19
    ''':attr: num of column for config number (always 1)'''
    ID_Col = 20
    ''':attr: '''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists SolveEquEqu;")
        query.exec("create table if not exists SolveEquEqu ("
                   "OrderNum INTEGER, "
                   "g REAL, "
                   "ro REAL, "
                   "mu REAL, "
                   "V REAL, "
                   "Alpha REAL, "
                   "Cl REAL, "
                   "cle REAL, "
                   "Cd REAL, "
                   "cde REAL, "
                   "Cm REAL, "
                   "Spilot REAL, "
                   "Cdpilot REAL, "
                   "Mw REAL, "
                   "Mp REAL, "
                   "Pmc REAL, "
                   "Mql REAL, "
                   "Ycp REAL, "
                   "Zcp REAL, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("SolveEquEqu")

        self.set_num_rows_for_config(1,1)
        self.update_row(1,1,9.807,1.225,18.46,12.4,9.45,0.67913,1.0,
                        0.03790, 1.1, 0.0, 0.438, 0.6, 4.0, 70, 0.2,
                        8.0, 0.575, 0.395)

        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        # self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order num"))

    def update_row(self, config_num, order_num, g, ro, mu, v, alpha, cl, cle, cd, cde, cm, spilot, cdpilot,
                   mw, mp, pmc, mql, ycp, zcp):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE SolveEquEqu SET "
                      "g= :g, "
                      "ro= :ro, "
                      "mu= :mu, "
                      "V= :V, "
                      "Alpha= :Alpha, "
                      "Cl= :Cl, "
                      "cle= :cle, "
                      "Cd= :Cd, "
                      "cde= :cde, "
                      "Cm= :Cm, "
                      "Spilot= :Spilot, "
                      "Cdpilot= :Cdpilot, "
                      "Mw= :Mw, "
                      "Mp= :Mp, "
                      "Pmc= :Pmc, "
                      "Mql= :Mql, "
                      "Ycp= :Ycp, "
                      "Zcp= :Zcp "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":g", g)
        query.bindValue(":ro", ro)
        query.bindValue(":mu", mu)
        query.bindValue(":V", v)
        query.bindValue(":Alpha", alpha)
        query.bindValue(":Cl", cl)
        query.bindValue(":cle", cle)
        query.bindValue(":Cd", cd)
        query.bindValue(":cde", cde)
        query.bindValue(":Cm", cm)
        query.bindValue(":Spilot", spilot)
        query.bindValue(":Cdpilot", cdpilot)
        query.bindValue(":Mw", mw)
        query.bindValue(":Mp", mp)
        query.bindValue(":Pmc", pmc)
        query.bindValue(":Mql", mql)
        query.bindValue(":Ycp", ycp)
        query.bindValue(":Zcp", zcp)
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
                      "g, "
                      "ro, "
                      "mu, "
                      "V, "
                      "Alpha, "
                      "Cl, "
                      "cle, "
                      "Cd, "
                      "cde, "
                      "Cm, "
                      "Spilot, "
                      "Cdpilot, "
                      "Mw, "
                      "Mp, "
                      "Pmc, "
                      "Mql, "
                      "Ycp, "
                      "Zcp "
                      "FROM SolveEquEqu WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
