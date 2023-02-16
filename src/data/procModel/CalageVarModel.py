"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class CalageVarModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the DXF layer names
    """
    __className = 'CalageVarModel'
    ''' :attr: Does help to indicate the source of the log messages. '''
    __isUsed = False
    ''' :attr: Helps to remember if the section is in use or not'''

    usageUpd = pyqtSignal()
    '''
    :signal: emitted as soon the usage flag is changed
    '''
    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    NumRisersCol = 1
    ''':attr: Number of the col holding the fixed line name '''
    PosACol = 2
    ''':attr: Number of the col holding the position for riser A'''
    PosBCol = 3
    ''':attr: Number of the col holding the position for riser B'''
    PosCCol = 4
    ''':attr: Number of the col holding the position for riser C'''
    PosDCol = 5
    ''':attr: Number of the col holding the position for riser D'''
    PosECol = 6
    ''':attr: Number of the col holding the position for riser E'''
    PosFCol = 7
    ''':attr: Number of the col holding the position for riser F'''
    MaxNegAngCol = 8
    ''':attr: Number of the col holding the max negative angle'''
    NumNegStepsCol = 9
    ''':attr: Number of the col holding the number of steps for the positive angle simulation'''
    MaxPosAngCol = 10
    ''':attr: Number of the col holding the max positive angle'''
    NumPosStepsCol = 11
    ''':attr: Number of the col holding the number of steps for the negative angle simulation'''
    ConfigNumCol = 12
    ''':attr: num of column for config number (always 1)'''

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("CalageVar")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.set_num_rows_for_config(1, 1)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Num risers"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Pos r A"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Pos r B"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Pos r C"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Pos r D"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Pos r E"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Pos r F"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("Max neg ang [deg]"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("Num neg steps"))
        self.setHeaderData(10, Qt.Orientation.Horizontal, _("Max pos ang [deg]"))
        self.setHeaderData(11, Qt.Orientation.Horizontal, _("Num pos steps"))

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists CalageVar;")
        query.exec("create table if not exists CalageVar ("
                   "OrderNum INTEGER, "
                   "NumRisers INTEGER, "
                   "PosA REAL, "
                   "PosB REAL, "
                   "PosC REAL, "
                   "PosD REAL, "
                   "PosE REAL, "
                   "PosF REAL, "
                   "MaxNegAng REAL, "
                   "NumNegSteps INTEGER, "
                   "MaxPosAng REAL, "
                   "NumPosSteps INTEGER, "
                   "ConfigNum INTEGER, "
                   "ID INTEGER PRIMARY KEY);")

    def update_row(self, config_num, order_num, num_risers, pos_a, pos_b,
                   pos_c, pos_d, pos_e, pos_f, max_neg_ang, num_neg_steps,
                   max_pos_ang, num_pos_steps):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE CalageVar SET "
                      "NumRisers= :numRisers, "
                      "PosA= :posA, "
                      "PosB= :posB, "
                      "PosC= :posC, "
                      "PosD= :posD, "
                      "PosE= :posE, "
                      "PosF= :posF, "
                      "MaxNegAng= :maxNegAng, "
                      "NumNegSteps= :numNegSteps, "
                      "MaxPosAng= :maxPosAng, "
                      "NumPosSteps= :numPosSteps "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":numRisers", num_risers)
        query.bindValue(":posA", pos_a)
        query.bindValue(":posB", pos_b)
        query.bindValue(":posC", pos_c)
        query.bindValue(":posD", pos_d)
        query.bindValue(":posE", pos_e)
        query.bindValue(":posF", pos_f)
        query.bindValue(":maxNegAng", max_neg_ang)
        query.bindValue(":numNegSteps", num_neg_steps)
        query.bindValue(":maxPosAng", max_pos_ang)
        query.bindValue(":numPosSteps", num_pos_steps)
        query.bindValue(":config", config_num)
        query.bindValue(":order", order_num)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def setIsUsed(self, isUsed):
        """
        :method: Set the usage flag of the section
        :param isUsed: True if section is in use, False otherwise
        """
        self.__isUsed = isUsed
        self.usageUpd.emit()

    def isUsed(self):
        """
        :method: Returns the information if the section is in use or not
        :returns: True if section is in use, false otherwise
        """
        return self.__isUsed

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
                      "NumRisers, "
                      "PosA, "
                      "PosB, "
                      "PosC, "
                      "PosD, "
                      "PosE, "
                      "PosF, "
                      "MaxNegAng, "
                      "NumNegSteps, "
                      "MaxPosAng, "
                      "NumPosSteps "
                      "FROM CalageVar WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
