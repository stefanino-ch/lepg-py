"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import math

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from data.SqlTableModel import SqlTableModel
from Singleton.Singleton import Singleton

from data.procModel.AirfoilsModel import AirfoilsModel
from data.procModel.AirfoilThicknessModel import AirfoilThicknessModel
from data.procModel.AnchorPointsModel import AnchorPointsModel
from data.procModel.GlueVentModel import GlueVentModel
from data.procModel.LightConfModel import LightConfModel
from data.procModel.RibModel import RibModel


def create_wing_table():
    """
    :method: Creates initially the empty wing table
    """
    query = QSqlQuery()
    query.exec("DROP TABLE if exists Wing;")
    query.exec("create table if not exists Wing ("
               "BrandName TEXT, "
               "WingName TEXT, "
               "DrawScale REAL, "
               "WingScale REAL, "
               "NumCells INTEGER, "
               "NumRibs INTEGER, "
               "AlphaMaxTip REAL, "
               "AlphaMode INTEGER, "
               "AlphaMaxCent REAL, "
               "ParaType TEXT, "
               "ParaParam INTEGER, "
               "LinesConcType INTEGER, "
               "Brakelength INTEGER, "
               "xSpacing REAL, "
               "ySpacing REAL, "
               "OrderNum INTEGER,"
               "ConfigNum INTEGER,"
               "ID INTEGER PRIMARY KEY);")


class WingModel(SqlTableModel, metaclass=Singleton):
    """
    :class: Provides a SqlTableModel holding all data related to the
            wing itself.
    """
    __className = 'WingModel'

    BrandNameCol = 0
    ''':attr: number of the brand name column'''
    WingNameCol = 1
    ''':attr: number of the wing name column'''
    DrawScaleCol = 2
    ''':attr: number of the draw scale column'''
    WingScaleCol = 3
    ''':attr: number of the wing scale column'''
    NumCellsCol = 4
    ''':attr: number of the number of cells column'''
    NumRibsCol = 5
    ''':attr: number of the number of ribs column'''
    AlphaMaxTipCol = 6
    ''':attr: number of the alpha max angle on wingtip column'''
    AlphaModeCol = 7
    ''':attr: number of the alpha type column'''
    AlphaMaxCentCol = 8
    ''':attr: number of the alpha max angle in center column'''
    ParaTypeCol = 9
    ''':attr: number of the paraglider type column'''
    ParaParamCol = 10
    '''
    :attr: number of the column holding the parameter attached to
           paraglider type
    '''
    LinesConcTypeCol = 11
    ''':attr: number of the column holding the lines concept type'''
    BrakeLengthCol = 12
    ''':attr: number of the column holding the length of the brake lines'''
    xSpacingCol = 13
    ''':attr: number of the column holding xSpacing for the HvVh Ribs'''
    ySpacingCol = 14
    ''':attr: number of the column holding ySpacing for the HvVh Ribs'''
    OrderNumCol = 15
    '''
    :attr: num of column for ordering the individual lines
           of a config
    '''
    ConfigNumCol = 16
    ''':attr: num of column for config number (always 1)'''
    halfNumRibs = 0
    '''
    :attr: the number of different ribs needed to build the wing.
           This is more or less the half number of total ribs.
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()
        create_wing_table()
        self.setTable("Wing")
        self.select()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.set_num_rows_for_config(1, 1)

        self.rib_M = RibModel()
        self.anchPoints_M = AnchorPointsModel()
        self.airf_M = AirfoilsModel()
        self.lightC_M = LightConfModel()
        self.glueVent_M = GlueVentModel()
        self.airfThick_M = AirfoilThicknessModel()

        # self.data_changed.connect(self.sync_rib_num_data)
        self.dataChanged.connect(self.man_data_change)

        self.setHeaderData(0, Qt.Orientation.Horizontal, _("Brand name"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, _("Wing name"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, _("Draw scale"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, _("Wing scale"))
        self.setHeaderData(4, Qt.Orientation.Horizontal, _("Num cells"))
        self.setHeaderData(5, Qt.Orientation.Horizontal, _("Num ribs"))
        self.setHeaderData(6, Qt.Orientation.Horizontal, _("Alpha max tip"))
        self.setHeaderData(7, Qt.Orientation.Horizontal, _("Alpha mode"))
        self.setHeaderData(8, Qt.Orientation.Horizontal, _("Alpha max cent"))
        self.setHeaderData(9, Qt.Orientation.Horizontal, _("Para type"))
        self.setHeaderData(10, Qt.Orientation.Horizontal, _("Para param"))
        self.setHeaderData(11, Qt.Orientation.Horizontal, _("Lines Conc Type"))
        self.setHeaderData(12, Qt.Orientation.Horizontal, _("Brake length"))
        self.setHeaderData(13, Qt.Orientation.Horizontal, _("x-Spacing"))
        self.setHeaderData(14, Qt.Orientation.Horizontal, _("y-Spacing"))

    def man_data_change(self, q):
        """
        :method: If NumRibs is changed manually we must keep half_num_ribs
                 and Ribs table in sync.
        """
        if q.column() == self.NumRibsCol:
            self.sync_rib_num_data()

    def sync_rib_num_data(self):
        """
        :method: If NumRibs is changed we must keep half_num_ribs and Ribs
                 table in sync. This method will calculate the current
                 number of half ribs and calls the method to set up the
                 model accordingly.
        """
        num_ribs = self.index(0, self.NumRibsCol).data()

        try:
            num_ribs = int(num_ribs)
            go_on = True
        except ValueError:
            return

        if go_on:
            self.halfNumRibs = math.ceil(float(num_ribs) / 2)

            self.rib_M.setup_rib_rows(self.halfNumRibs)
            self.airf_M.setup_rib_rows(self.halfNumRibs)
            self.anchPoints_M.setup_rib_rows(self.halfNumRibs)
            self.glueVent_M.set_num_rows_for_config(1, self.halfNumRibs)
            self.airfThick_M.set_num_rows_for_config(1, self.halfNumRibs)

    def update_num_cells(self, num_cells):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here
                 as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE Wing SET "
                      "NumCells= :num_cells ")
        query.bindValue(":num_cells", num_cells)
        query.exec()

        self.select()  # to a select() to assure the model is updated

    def update_num_ribs(self, num_ribs):
        """
        :method: Updates a specific row in the database with the values
                 passed. Parameters are not explicitly explained here
                 as they should be well known.
        """
        query = QSqlQuery()
        query.prepare("UPDATE Wing SET "
                      "NumRibs= :num_ribs; ")
        query.bindValue(":num_ribs", num_ribs)
        query.exec()
        self.select()  # to a select() to assure the model is updated
        self.sync_rib_num_data()

    def get_row(self):
        """
        :method: reads values back from the internal database

        :returns: Values read from internal database
        :rtype: QRecord
        """
        query = QSqlQuery()
        query.prepare("SELECT "
                      "BrandName, "
                      "WingName, "
                      "DrawScale, "
                      "WingScale, "
                      "NumCells, "
                      "NumRibs, "
                      "AlphaMaxTip, "
                      "AlphaMode, "
                      "AlphaMaxCent, "
                      "ParaType, "
                      "ParaParam, "
                      "LinesConcType, "
                      "Brakelength, "
                      "xSpacing, "
                      "ySpacing FROM Wing")
        query.exec()
        query.next()
        return query.record()
