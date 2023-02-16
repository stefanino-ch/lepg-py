"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class MarksTypesModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the DXF layer names
    """
    __className = 'MarksTypesModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    OrderNumCol = 0
    ''':attr: num of column for ordering the individual lines of a config'''
    TypeCol = 1
    ''':attr: Number of the col holding the type description of the mark'''
    FormOneCol = 2
    ''':attr: Number of the col holding the first mark form'''
    FormOnePOneCol = 3
    ''':attr: Number of the col holding the first parameter for the 1st mark form'''
    FormOnePTwoCol = 4
    ''':attr: Number of the col holding the 2nd parameter for the 1st mark form'''
    FormTwoCol = 5
    ''':attr: Number of the col holding the 2nd mark form'''
    FormTwoPOneCol = 6
    ''':attr: Number of the col holding the first parameter for the 2nd mark form'''
    FormTwoPTwoCol = 7
    ''':attr: Number of the col holding the 2nd parameter for the 2nd mark form'''
    ConfigNumCol = 8
    ''':attr: num of column for config number (always 1)'''

    def createTable(self):
        """
        :method: Creates initially the empty table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists MarksTypes;")
        query.exec("create table if not exists MarksTypes ("
                   "OrderNum INTEGER,"
                   "Type text,"
                   "FormOne INTEGER,"
                   "FormOnePOne REAL,"
                   "FormOnePTwo REAL,"
                   "FormTwo INTEGER,"
                   "FormTwoPOne REAL,"
                   "FormTwoPTwo REAL,"
                   "ConfigNum INTEGER,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self, parent=None):  # @UnusedVariable
        """
        :method: Class initialization
        """
        super().__init__()
        self.createTable()
        self.setTable("MarksTypes")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Marks type"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Form 1"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Form 1 1st param"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Form 1 2nd param"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Form 2"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Form 2 1st param"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Form 2 2nd param"))

    def updateRow(self, configNum, orderNum, pType, formOne, formOnePOne, formOnePTwo, formTwo, formTwoPOne,
                  formTwoPTwo):
        """
        :method: Updates a specific row in the database with the values passed. Parameters are not explicitly
                 explained here as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE MarksTypes SET "
                      "Type= :pType, "
                      "FormOne= :formOne, "
                      "FormOnePOne= :formOnePOne, "
                      "FormOnePTwo= :formOnePTwo, "
                      "FormTwo= :formTwo, "
                      "FormTwoPOne= :formTwoPOne, "
                      "FormTwoPTwo= :formTwoPTwo "
                      "WHERE (ConfigNum = :config AND OrderNum = :order);")
        query.bindValue(":pType", pType)
        query.bindValue(":formOne", formOne)
        query.bindValue(":formOnePOne", formOnePOne)
        query.bindValue(":formOnePTwo", formOnePTwo)
        query.bindValue(":formTwo", formTwo)
        query.bindValue(":formTwoPOne", formTwoPOne)
        query.bindValue(":formTwoPTwo", formTwoPTwo)
        query.bindValue(":config", configNum)
        query.bindValue(":order", orderNum)
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
                      "Type, "
                      "FormOne, "
                      "FormOnePOne, "
                      "FormOnePTwo, "
                      "FormTwo, "
                      "FormTwoPOne, "
                      "FormTwoPTwo "
                      "FROM MarksTypes WHERE (ConfigNum = :config) ORDER BY OrderNum")
        query.bindValue(":config", configNum)
        query.exec()
        query.next()
        # now we are at the first row
        i = 1
        while i < orderNum:
            query.next()
            i += 1
        return query.value
