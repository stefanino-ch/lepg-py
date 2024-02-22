"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class LinesCharacteristicsModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the individual lines characteristics
    """
    __isUsed = False
    ''' :attr: Helps to remember if the section is in use or not'''

    usageUpd = pyqtSignal()
    '''
    :signal: emitted as soon the usage flag is changed
    '''

    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    LineTypeCol = 1
    ''':attr: Number of the col holding the line type'''
    LineFormCol = 2
    ''':attr: Number of the col holding the line form (rectangular or circular)'''
    LineDiamCol = 3
    ''':attr: Number of the col holding the line diameter'''
    BDimCol = 4
    ''':attr: Number of the col holding the b-dimension'''
    LineLabelCol = 5
    ''':attr: Number of the col holding the line label'''
    MinBreakStrCol = 6
    ''':attr: Number of the col holding the minimal breaking strength'''
    MatTypeCol = 7
    ''':attr: Number of the col holding the material type'''
    WeightPerMCol = 8
    ''':attr: Number of the col holding the weight per m line'''
    LoopTypeCol = 9
    ''':attr: Number of the col holding the loop type (sewed or spliced)'''
    LoopLengthCol = 10
    ''':attr: Number of the col holding the loop length'''
    LineCadColorCol = 11
    ''':attr: Number of the col holding CAD color'''
    ConfigNumCol = 12
    ''':attr: num of column for config number (always 1)'''

    def create_table(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists LinesCharacteristics;")
        query.exec("create table if not exists LinesCharacteristics ("
                   "OrderNum INTEGER, "
                   "LineType INTEGER, "
                   "LineForm TEXT, "
                   "LineDiam REAL, "
                   "BDim REAL, "
                   "LineLabel TEXT, "
                   "MinBreakStr INTEGER, "
                   "MatType TEXT, "
                   "WeightPerM REAL, "
                   "LoopType TEXT, "
                   "LoopLength REAL, "
                   "LineCADColor INTEGER, "
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("LinesCharacteristics")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Order num"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Line Type"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Line Form"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Line Diam"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("B-Diam"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Line Label"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Min break str [daN]"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Mat type"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("Weight per m"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("Loop type"))
        self.setHeaderData(10, Qt.Orientation.Horizontal, _("Loop length"))
        self.setHeaderData(11, Qt.Orientation.Horizontal, _("CAD Color"))

    def update_row(self, config_num, order_num, line_type, line_form, line_diam, b_diam, line_label, min_break_str,
                   mat_type, weight_per_m, loop_type, loop_length, cad_color):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE NoseMylars SET "
                      "LineType= :line_type, "
                      "LineForm= :line_form, "
                      "LineDiam= :line_diam, "
                      "BDim= : b_diam, "
                      "LineLabel= :line_label, "
                      "MinBreakStr= :min_break_str, "
                      "MatType= : mat_type, "
                      "WeightPerM= :weight_per_m, "
                      "LoopType= :loop_type, "
                      "LoopLength= :loop_length, "
                      "LineCADColor= :cad_color "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":line_type", line_type)
        query.bindValue(":line_form", line_form)
        query.bindValue(":line_diam", line_diam)
        query.bindValue(":line_label", line_label)
        query.bindValue(":b_diam", b_diam)
        query.bindValue(":line_label", line_label)
        query.bindValue(":min_break_str", min_break_str)
        query.bindValue(":mat_type", mat_type)
        query.bindValue(":weight_per_m", loop_type)
        query.bindValue(":loop_type", loop_type)
        query.bindValue(":loop_length", loop_length)
        query.bindValue(":cad_color", cad_color)
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
                      "LineType, "
                      "LineForm, "
                      "LineDiam, "
                      "BDim, "
                      "LineLabel, "
                      "MinBreakStr, "
                      "MatType, "
                      "WeightPerM, "
                      "LoopType, "
                      "LoopLength, "
                      "LineCADColor "
                      "FROM NoseMylars WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", config_num)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < order_num:
            query.next()
            i += 1
        return query.value
