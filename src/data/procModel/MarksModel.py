"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton


class MarksModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding the Marks parameters.
    """
    __className = 'MarksModel'
    ''' :attr: Does help to indicate the source of the log messages. '''

    MarksSpCol = 0
    ''':attr: Number of the col holding the marks spacing value'''
    PointRadCol = 1
    ''':attr: Number of the col holding the point radius value'''
    PointDisplCol = 2
    ''':attr: Number of the col holding the points displacement value'''

    def create_table(self):
        """
        :method: Creates initially the empty Marks table
        """
        query = QSqlQuery()

        query.exec("DROP TABLE if exists Marks;")
        query.exec("create table if not exists Marks ("
                   "MarksSp REAL,"
                   "PointRad REAL,"
                   "PointDispl REAL,"
                   "ID INTEGER PRIMARY KEY);")

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        self.create_table()
        self.setTable("Marks")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Marks Spacing [cm]"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Point Radius [cm]"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Point Displacement [cm]"))

        self.add_rows(-1, 1)

    def update_row(self, marks_sp, point_rad, point_displ):
        """
        :method: updates a specific row with the parameters passed.
        """
        query = QSqlQuery()
        query.prepare(
            "UPDATE Marks SET MarksSp= :marks_sp, PointRad= :point_rad, PointDispl= :point_displ WHERE (ID = :id);")
        query.bindValue(":marks_sp", marks_sp)
        query.bindValue(":point_rad", point_rad)
        query.bindValue(":point_displ", point_displ)
        query.bindValue(":id", 1)
        query.exec()
        self.select()  # to a select() to assure the model is updated properly

    def get_row(self):
        """
        :method: reads values back from the internal database
        :return: specific values read from internal database
        """
        query = QSqlQuery()
        query.prepare("Select "
                      "MarksSp, "
                      "PointRad, "
                      "PointDispl "
                      "FROM Marks")
        query.exec()
        query.next()
        return query.value
