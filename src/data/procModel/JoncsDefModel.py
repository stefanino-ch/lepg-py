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

    paramLength = {
        1: 15,
        2: 12
    }
    ''':attr: defines the length (number of values) for the individual parameter lines'''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists JoncsDef;")
        query.exec("create table if not exists JoncsDef ("
                   "OrderNum INTEGER, "
                   "FirstRib INTEGER, "
                   "LastRib INTEGER, "
                   "p_ba REAL, "
                   "p_bb REAL, "
                   "p_bc REAL, "
                   "PBD REAL, "
                   "p_be REAL, "
                   "p_ca REAL, "
                   "p_cb REAL, "
                   "p_cc REAL, "
                   "PCD REAL, "
                   "p_da REAL, "
                   "p_db REAL, "
                   "p_dc REAL, "
                   "PDD REAL, "
                   "Type INTEGER, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
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

    def update_type_one_row(self, config_num, order_num, first_rib, last_rib, p_ba, p_bb, p_bc, p_bd,
                            p_ca, p_cb, p_cc, p_cd,
                            p_da, p_db, p_dc, p_dd):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE JoncsDef SET "
                      "FirstRib= :first_rib, "
                      "LastRib= :last_rib, "
                      "p_ba= :p_ba, "
                      "p_bb= :p_bb, "
                      "p_bc= :p_bc, "
                      "p_bd= :p_bd, "
                      "p_ca= :p_ca, "
                      "p_cb= :p_cb, "
                      "p_cc= :p_cc, "
                      "p_cd= :p_cd, "
                      "p_da= :p_da, "
                      "p_db= :p_db, "
                      "p_dc= :p_dc, "
                      "p_dd= :p_dd, "
                      "Type= :t "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":first_rib", first_rib)
        query.bindValue(":last_rib", last_rib)
        query.bindValue(":p_ba", p_ba)
        query.bindValue(":p_bb", p_bb)
        query.bindValue(":p_bc", p_bc)
        query.bindValue(":p_bd", p_bd)
        query.bindValue(":p_ca", p_ca)
        query.bindValue(":p_cb", p_cb)
        query.bindValue(":p_cc", p_cc)
        query.bindValue(":p_cd", p_cd)
        query.bindValue(":p_da", p_da)
        query.bindValue(":p_db", p_db)
        query.bindValue(":p_dc", p_dc)
        query.bindValue(":p_dd", p_dd)
        query.bindValue(":t", 1)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def update_type_two_row(self, config_num, order_num, first_rib, last_rib,
                            p_ba, p_bb, p_bc, p_bd, p_be,
                            p_da, p_db, p_dc, p_dd):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE JoncsDef SET "
                      "FirstRib= :first_rib, "
                      "LastRib= :last_rib, "
                      "p_ba= :p_ba, "
                      "p_bb= :p_bb, "
                      "p_bc= :p_bc, "
                      "p_bd= :p_bd, "
                      "p_be= :p_be, "
                      "p_da= :p_da, "
                      "p_db= :p_db, "
                      "p_dc= :p_dc, "
                      "p_dd= :p_dd, "
                      "Type= 2 "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":first_rib", first_rib)
        query.bindValue(":last_rib", last_rib)
        query.bindValue(":p_ba", p_ba)
        query.bindValue(":p_bb", p_bb)
        query.bindValue(":p_bc", p_bc)
        query.bindValue(":p_bd", p_bd)
        query.bindValue(":p_be", p_be)
        query.bindValue(":p_da", p_da)
        query.bindValue(":p_db", p_db)
        query.bindValue(":p_dc", p_dc)
        query.bindValue(":p_dd", p_dd)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def set_type(self, config_num, type_num):
        """
        :method: Sets for all rows of a specific config the type num
        :param config_num: Number of the configuration to read from
        :param type_num: 1: type== 1; 2: type== 2
        """
        query = QSqlQuery()
        query.prepare("UPDATE JoncsDef SET "
                      "type= :type_num "
                      "WHERE (ConfigNum = :config);")
        query.bindValue(":type_num", type_num)
        query.bindValue(":config", config_num)
        query.exec()

    def get_type(self, config_num):
        """
        :method: Detects for a defined config if the type is set.
        :return: 0: type is empty; 1: type== 1; 2: type== 2
        """
        query = QSqlQuery()
        query.prepare("Select Type FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum ASC;")
        query.bindValue(":config", config_num)
        query.exec()
        type_num = 0
        if query.next():
            type_num = query.value(0)
            if type_num == "":
                type_num = 0

        return type_num

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
                      "FirstRib, "
                      "LastRib, "
                      "p_ba, "
                      "p_bb, "
                      "p_bc, "
                      "PBD, "
                      "p_be, "
                      "p_ca, "
                      "p_cb, "
                      "p_cc, "
                      "PCD, "
                      "p_da, "
                      "p_db, "
                      "p_dc, "
                      "PDD, "
                      "Type "
                      "FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
