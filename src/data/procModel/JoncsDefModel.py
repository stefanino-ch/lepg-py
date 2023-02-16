"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class JoncsDefModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the Joncs definition data
    """
    __className = 'JoncsDefModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    FirstRibCol = 1
    ''':attr: Number of the col holding the first rib'''
    LastRibCol = 2
    ''':attr: Number of the col holding the last rib'''
    pBACol = 3
    ''':attr: Number of the col holding the 1st param of 2nd row'''
    pBBCol = 4
    ''':attr: Number of the col holding the 2nd param of 2nd row'''
    pBCCol = 5
    ''':attr: Number of the col holding the 3rd param of 2nd row'''
    pBDCol = 6
    ''':attr: Number of the col holding the 4th param of 2nd row'''
    pBECol = 7
    ''':attr: Number of the col holding the 5th param of 2nd row'''
    pCACol = 8
    ''':attr: Number of the col holding the 1st param of 3rd row'''
    pCBCol = 9
    ''':attr: Number of the col holding the 2nd param of 3rd row'''
    pCCCol = 10
    ''':attr: Number of the col holding the 3rd param of 3rd row'''
    pCDCol = 11
    ''':attr: Number of the col holding the 4th param of 3rd row'''
    pDACol = 12
    ''':attr: Number of the col holding the 1st param of 4th row'''
    pDBCol = 13
    ''':attr: Number of the col holding the 2nd param of 4th row'''
    pDCCol = 14
    ''':attr: Number of the col holding the 3rd param of 4th row'''
    pDDCol = 15
    ''':attr: Number of the col holding the 4th param of 4th row'''
    TypeCol = 16
    ''':attr: Number of the col holding the type num'''
    ConfigNumCol = 17
    ''':attr: num of column for config number (always 1)'''

    def createTable(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists JoncsDef;")
        query.exec("create table if not exists JoncsDef ("
                   "OrderNum INTEGER, "
                   "FirstRib INTEGER, "
                   "LastRib INTEGER, "
                   "pBA REAL, "
                   "pBB REAL, "
                   "pBC REAL, "
                   "PBD REAL, "
                   "pBE REAL, "
                   "pCA REAL, "
                   "pCB REAL, "
                   "pCC REAL, "
                   "PCD REAL, "
                   "pDA REAL, "
                   "pDB REAL, "
                   "pDC REAL, "
                   "PDD REAL, "
                   "Type INTEGER, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("JoncsDef")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("First Rib"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Last Rib"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Row 2 A"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Row 2 B"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Row 2 C"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Row 2 D"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Row 2 E"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("Row 3 A"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("Row 3 B"))
        self.setHeaderData(10, Qt.Orientation.Horizontal, _("Row 3 C"))
        self.setHeaderData(11, Qt.Orientation.Horizontal, _("Row 3 D"))
        self.setHeaderData(12, Qt.Orientation.Horizontal, _("Row 4 A"))
        self.setHeaderData(13, Qt.Orientation.Horizontal, _("Row 4 B"))
        self.setHeaderData(14, Qt.Orientation.Horizontal, _("Row 4 C"))
        self.setHeaderData(15, Qt.Orientation.Horizontal, _("Row 4 D"))

    def updateTypeOneRow(self, configNum, orderNum, firstRib, lastRib, pBA, pBB, pBC, pBD, pCA, pCB, pCC, pCD, pDA,
                         pDB, pDC, pDD):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE JoncsDef SET "
                      "FirstRib= :first_rib, "
                      "LastRib= :last_rib, "
                      "pBA= :pBA, "
                      "pBB= :pBB, "
                      "pBC= :pBC, "
                      "pBD= :pBD, "
                      "pCA= :pCA, "
                      "pCB= :pCB, "
                      "pCC= :pCC, "
                      "pCD= :pCD, "
                      "pDA= :pDA, "
                      "pDB= :pDB, "
                      "pDC= :pDC, "
                      "pDD= :pDD, "
                      "Type= :t "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":first_rib", firstRib)
        query.bindValue(":last_rib", lastRib)
        query.bindValue(":pBA", pBA)
        query.bindValue(":pBB", pBB)
        query.bindValue(":pBC", pBC)
        query.bindValue(":pBD", pBD)
        query.bindValue(":pCA", pCA)
        query.bindValue(":pCB", pCB)
        query.bindValue(":pCC", pCC)
        query.bindValue(":pCD", pCD)
        query.bindValue(":pDA", pDA)
        query.bindValue(":pDB", pDB)
        query.bindValue(":pDC", pDC)
        query.bindValue(":pDD", pDD)
        query.bindValue(":t", 1)
        query.bindValue(":config", configNum)
        query.bindValue(":order", orderNum)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def updateTypeTwoRow(self, configNum, orderNum, firstRib, lastRib, pBA, pBB, pBC, pBD, pBE, pDA, pDB, pDC, pDD):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE JoncsDef SET "
                      "FirstRib= :first_rib, "
                      "LastRib= :last_rib, "
                      "pBA= :pBA, "
                      "pBB= :pBB, "
                      "pBC= :pBC, "
                      "pBD= :pBD, "
                      "pBE= :pBE, "
                      "pDA= :pDA, "
                      "pDB= :pDB, "
                      "pDC= :pDC, "
                      "pDD= :pDD, "
                      "Type= 2 "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":first_rib", firstRib)
        query.bindValue(":last_rib", lastRib)
        query.bindValue(":pBA", pBA)
        query.bindValue(":pBB", pBB)
        query.bindValue(":pBC", pBC)
        query.bindValue(":pBD", pBD)
        query.bindValue(":pBE", pBE)
        query.bindValue(":pDA", pDA)
        query.bindValue(":pDB", pDB)
        query.bindValue(":pDC", pDC)
        query.bindValue(":pDD", pDD)
        query.bindValue(":config", configNum)
        query.bindValue(":order", orderNum)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def setType(self, configNum, typeNum):
        """
        :method: Sets for all rows of a specific config the type num
        :param configNum: Number of the configuration to read from
        :param typeNum: 1: type== 1; 2: type== 2
        """
        query = QSqlQuery()
        query.prepare("UPDATE JoncsDef SET "
                      "type= :type_num "
                      "WHERE (ConfigNum = :config);")
        query.bindValue(":type_num", typeNum)
        query.bindValue(":config", configNum)
        query.exec()

    def getType(self, configNum):
        """
        :method: Detects for a defined config if the type is set.
        :return: 0: type is empty; 1: type== 1; 2: type== 2
        """
        query = QSqlQuery()
        query.prepare("Select Type FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum ASC;")
        query.bindValue(":config", configNum)
        query.exec()
        typeNum = 0
        if query.next():
            typeNum = query.value(0)
            if typeNum == "":
                typeNum = 0

        return typeNum

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
                      "FirstRib, "
                      "LastRib, "
                      "pBA, "
                      "pBB, "
                      "pBC, "
                      "PBD, "
                      "pBE, "
                      "pCA, "
                      "pCB, "
                      "pCC, "
                      "PCD, "
                      "pDA, "
                      "pDB, "
                      "pDC, "
                      "PDD, "
                      "Type "
                      "FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
