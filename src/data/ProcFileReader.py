""""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'"""
import logging

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QObject, QFile, QTextStream
from PyQt6.QtWidgets import QTextEdit

from data.FileHelpers import split_line, rem_tab_space_quot, rem_tab_space

from data.procModel.AddRibPointsModel import AddRibPointsModel
from data.procModel.AirfoilsModel import AirfoilsModel
from data.procModel.AirfoilThicknessModel import AirfoilThicknessModel
from data.procModel.AnchorPointsModel import AnchorPointsModel
from data.procModel.BrakeLengthModel import BrakeLengthModel
from data.procModel.BrakeModel import BrakeModel
from data.procModel.CalageVarModel import CalageVarModel
from data.procModel.DxfLayerNamesModel import DxfLayerNamesModel
from data.procModel.ElLinesCorrModel import ElLinesCorrModel
from data.procModel.ElLinesDefModel import ElLinesDefModel
from data.procModel.ExtradosColConfModel import ExtradosColConfModel
from data.procModel.ExtradosColDetModel import ExtradosColDetModel
from data.procModel.GlobalAoAModel import GlobalAoAModel
from data.procModel.GlueVentModel import GlueVentModel
from data.procModel.HvVhRibsModel import HvVhRibsModel
from data.procModel.IntradosColsConfModel import IntradosColsConfModel
from data.procModel.IntradosColsDetModel import IntradosColsDetModel
from data.procModel.JoncsDefModel import JoncsDefModel
from data.procModel.LightConfModel import LightConfModel
from data.procModel.LightDetModel import LightDetModel
from data.procModel.LinesModel import LinesModel
from data.procModel.LinesCharacteristicsModel import LinesCharacteristicsModel
from data.procModel.MarksModel import MarksModel
from data.procModel.MarksTypesModel import MarksTypesModel
from data.procModel.NewSkinTensConfModel import NewSkinTensConfModel
from data.procModel.NewSkinTensDetModel import NewSkinTensDetModel
from data.procModel.NoseMylarsModel import NoseMylarsModel
from data.procModel.PartsSeparationModel import PartsSeparationModel
from data.procModel.RamificationModel import RamificationModel
from data.procModel.RibModel import RibModel
from data.procModel.SewingAllowancesModel import SewingAllowancesModel
from data.procModel.SkinTensionModel import SkinTensionModel
from data.procModel.SkinTensionParamsModel import SkinTensionParamsModel
from data.procModel.SolveEquEquModel import SolveEquEquModel
from data.procModel.SpecialParametersModel import SpecialParametersModel
from data.procModel.SpecWingTipModel import SpecWingTipModel
from data.procModel.ThreeDDxfModel import ThreeDDxfModel
from data.procModel.ThreeDShConfModel import ThreeDShConfModel
from data.procModel.ThreeDShLoDetModel import ThreeDShLoDetModel
from data.procModel.ThreeDShPrintModel import ThreeDShPrintModel
from data.procModel.ThreeDShUpDetModel import ThreeDShUpDetModel
from data.procModel.TwoDDxfModel import TwoDDxfModel
from data.procModel.WingModel import WingModel
from data.procModel.XflrModel import XflrModel
from data.procModel.DetailedRisersModel import DetailedRisersModel


class WaitWindow(QTextEdit):
    """
    :class: Builds a minimized window to inform the user that file reading
            does take some time.
            All information is shown in the window title due to this discussion:
            https://stackoverflow.com/questions/67934352/window-opened-from-a-
            class-is-not-displaying-correctly/67937507#67937507
    """

    def __init__(self):
        super(WaitWindow, self).__init__()
        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)
        self.setMaximumSize(450, 0)
        self.setMinimumSize(450, 25)
        self.setWindowTitle(_("Please wait.. reading might take some time"))


class ProcFileReader(QObject):
    """
    :class: Covers the operations to read a processor file and write the data
            into the according models.
    """

    __className = 'ProcFileReader'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    __fileNamePath = ''  # type: str
    __fileVersion = 0.0  # type: float

    def __init__(self):
        """
        :method: Class initialization
        """
        super().__init__()

        self.wait_info_w = None

        self.addRibPts_M = AddRibPointsModel()
        self.airf_M = AirfoilsModel()
        self.airfThick_M = AirfoilThicknessModel()
        self.anchorPoints_M = AnchorPointsModel()
        self.brakes_M = BrakeModel()
        self.brakeL_M = BrakeLengthModel()
        self.calageVar_M = CalageVarModel()
        self.dxfLayNames_M = DxfLayerNamesModel()
        self.elLinesCorr_M = ElLinesCorrModel()
        self.elLinesDef_M = ElLinesDefModel()
        self.extradosColConf_M = ExtradosColConfModel()
        self.extradosColDet_M = ExtradosColDetModel()
        self.globAoA_M = GlobalAoAModel()
        self.glueVent_M = GlueVentModel()
        self.hVvHRibs_M = HvVhRibsModel()
        self.intradosColConf_M = IntradosColsConfModel()
        self.intradosColDet_M = IntradosColsDetModel()
        self.joncsDef_M = JoncsDefModel()
        self.lines_M = LinesModel()
        self.linesChar_M = LinesCharacteristicsModel()
        self.lightC_M = LightConfModel()
        self.lightD_M = LightDetModel()
        self.marks_M = MarksModel()
        self.marksT_M = MarksTypesModel()
        self.newSkinTensConf_M = NewSkinTensConfModel()
        self.newSkinTensDet_M = NewSkinTensDetModel()
        self.noseMylars_M = NoseMylarsModel()
        self.ramific_M = RamificationModel()
        self.partsSep_M = PartsSeparationModel()
        self.rib_M = RibModel()
        self.skinTens_M = SkinTensionModel()
        self.skinTensParams_M = SkinTensionParamsModel()
        self.solveEquEqu_M = SolveEquEquModel()
        self.specialParameters_M = SpecialParametersModel()
        self.specWingTyp_M = SpecWingTipModel()
        self.sewAll_M = SewingAllowancesModel()
        self.threeDDxf_M = ThreeDDxfModel()
        self.threeDShConf_M = ThreeDShConfModel()
        self.threeDShUpDet_M = ThreeDShUpDetModel()
        self.threeDShLoDet_M = ThreeDShLoDetModel()
        self.threeDShPr_M = ThreeDShPrintModel()
        self.twoDDxf_M = TwoDDxfModel()
        self.wing_M = WingModel()
        self.xflr_M = XflrModel()
        self.detRisers_m = DetailedRisersModel()

    def read_file(self, file_path_name, file_version):
        """
        :method: Reads the data file and saves the data in the internal
                 database.
        :warning: Filename and Path must be set first!
        """
        self.__fileNamePath = file_path_name
        self.__fileVersion = float(file_version)

        self.wait_info_w = WaitWindow()
        self.wait_info_w.show()

        in_file = QFile(self.__fileNamePath)
        in_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stream = QTextStream(in_file)

        ##############################
        # 1. GEOMETRY
        # Over read file header
        logging.debug(self.__className + '.read_file: 1. GEOMETRY')

        counter = 0
        while counter < 4:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1

        # Brand name
        stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.BrandNameCol),
            rem_tab_space_quot(line))

        # Wing name
        stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.WingNameCol),
            rem_tab_space_quot(line))

        # Draw scale
        stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.DrawScaleCol),
            rem_tab_space(line))

        # Wing scale
        stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.WingScaleCol),
            rem_tab_space(line))

        # Number of cells
        stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.NumCellsCol),
            rem_tab_space(line))

        # Number of Ribs
        stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.NumRibsCol),
            rem_tab_space(line))

        # Alpha max and parameter
        stream.readLine()
        values = split_line(stream.readLine())
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.AlphaMaxTipCol),
            values[0])
        try:
            self.wing_M.setData(
                self.wing_M.index(0, WingModel.AlphaModeCol),
                values[1])
        except:
            # in case of an empty file values[1] is missing
            self.wing_M.setData(
                self.wing_M.index(0, WingModel.AlphaModeCol),
                '')
            logging.error(self.__className + '.read_file: AlphaMode missing')

        if len(values) > 2:
            self.wing_M.setData(
                self.wing_M.index(0, WingModel.AlphaMaxCentCol),
                values[2])
        else:
            self.wing_M.setData(
                self.wing_M.index(0, WingModel.AlphaMaxCentCol),
                '')

        # Paraglider type and parameter
        stream.readLine()
        values = split_line(stream.readLine())
        self.wing_M.setData(
            self.wing_M.index(0, WingModel.ParaTypeCol),
            rem_tab_space_quot(values[0]))
        try:
            self.wing_M.setData(
                self.wing_M.index(0, WingModel.ParaParamCol),
                values[1])
        except:
            # in case of an empty file values[1] is missing
            self.wing_M.setData(
                self.wing_M.index(0, WingModel.ParaParamCol),
                '')
            logging.error(self.__className + '.read_file: ParaParam missing')

        # Rib geometric parameters
        # Rib  x-rib  y-LE  y-TE  xp  z  beta  RP  Washin Rot_z  Pos_z
        stream.readLine()
        stream.readLine()

        for i in range(0, self.wing_M.halfNumRibs):
            values = split_line(stream.readLine())
            for y in range(0, 9):
                self.rib_M.setData(self.rib_M.index(i, y), values[y])
            # with 3.16 two additional params was added
            if len(values) <= 9:
                # old data file
                self.rib_M.setData(self.rib_M.index(i, 9), 0)
                self.rib_M.setData(self.rib_M.index(i, 10), 50)
            else:
                # new file
                self.rib_M.setData(self.rib_M.index(i, 9), values[9])
                self.rib_M.setData(self.rib_M.index(i, 10), values[10])

        ##############################
        # 2. AIRFOILS
        logging.debug(self.__className + '.read_file: 2. AIRFOILS')

        for i in range(4):
            stream.readLine()

        for i in range(0, self.wing_M.halfNumRibs):
            values = split_line(stream.readLine())
            for y in range(0, 8):
                self.airf_M.setData(self.airf_M.index(i, y), values[y])

        ##############################
        # 3. ANCHOR POINTS
        logging.debug(self.__className + '.read_file: 3. ANCHOR POINTS')

        # Just over-read the lines for temporary testing
        for i in range(4):
            stream.readLine()

        for i in range(0, self.wing_M.halfNumRibs):
            values = split_line(stream.readLine())
            for y in range(0, 8):
                self.anchorPoints_M.setData(self.anchorPoints_M.index(i, y),
                                            values[y])

        ##############################
        # 4. RIB HOLES
        logging.debug(self.__className + '.read_file: 4. RIB HOLES')

        for i in range(3):
            stream.readLine()

        num_configs = int(rem_tab_space(stream.readLine()))
        self.lightC_M.set_num_configs(num_configs)
        for i in range(0, num_configs):
            ini = int(rem_tab_space(stream.readLine()))
            fin = int(rem_tab_space(stream.readLine()))
            self.lightC_M.updateRow(i + 1, ini, fin)

            num_config_lines = int(rem_tab_space(stream.readLine()))
            self.lightD_M.set_num_rows_for_config(i + 1, 0)
            self.lightD_M.set_num_rows_for_config(i + 1, num_config_lines)

            # ConfigNum, order_num, light_typ, dist_le, dist_chord, hor_axis,
            # vert_axis, rot_angle, opt_1
            for line_it in range(0, num_config_lines):
                values = split_line(stream.readLine())
                self.lightD_M.update_row(i + 1, line_it + 1, values[0],
                                         values[1],
                                         values[2],
                                         values[3],
                                         values[4],
                                         values[5],
                                         values[6])

        ##############################
        # 5. SKIN TENSION
        logging.debug(self.__className + '.read_file: 5. SKIN TENSION')

        for i in range(4):
            stream.readLine()

        for line_it in range(0, 6):
            values = split_line(stream.readLine())
            try:
                self.skinTens_M.updateRow(line_it + 1, values[0], values[1],
                                          values[2], values[3])
            except:
                # in case of an empty file values[1...3] are missing
                self.skinTens_M.updateRow(line_it + 1, 0, 0, 0, 0)
                logging.error(self.__className + '.read_file: Skin tension params missing')

        val = rem_tab_space(stream.readLine())
        self.skinTensParams_M.setData(
            self.skinTensParams_M.index(
                0,
                SkinTensionParamsModel.StrainMiniRibsCol), val)

        values = split_line(stream.readLine())
        self.skinTensParams_M.setData(
            self.skinTensParams_M.index(
                0,
                SkinTensionParamsModel.NumPointsCol), values[0])
        self.skinTensParams_M.setData(
            self.skinTensParams_M.index(
                0,
                SkinTensionParamsModel.CoeffCol), values[1])

        ##############################
        # 6. SEWING ALLOWANCES
        logging.debug(self.__className + '.read_file: 6. SEWING ALLOWANCES')

        for i in range(3):
            stream.readLine()

        for line_it in range(0, 2):
            values = split_line(stream.readLine())
            if len(values) > 3:
                self.sewAll_M.update_row(line_it + 1, values[0],
                                         values[1], values[2])
            else:
                # in case of an empty file
                self.sewAll_M.update_row(line_it + 1, 15, 25, 25)
                logging.error(
                    self.__className
                    + '.read_file: Sewing allowances for panels missing')

        values = split_line(stream.readLine())
        if len(values) > 2:
            self.sewAll_M.update_row(3, values[0])
        else:
            self.sewAll_M.update_row(3, 15)
            logging.error(
                self.__className
                + '.read_file: Sewing allowances for ribs missing')

        values = split_line(stream.readLine())
        if len(values) > 2:
            self.sewAll_M.update_row(4, values[0])
        else:
            self.sewAll_M.update_row(4, 15)
            logging.error(
                self.__className
                + '.read_file: Sewing allowances for v-ribs missing')

        ##############################
        # 7. MARKS
        logging.debug(self.__className + '.read_file: 7. MARKS')

        for i in range(3):
            stream.readLine()

        values = split_line(stream.readLine())
        try:
            self.marks_M.update_row(values[0], values[1], values[2])
        except:
            # in case of an empty file values[1...2] are missing
            self.marks_M.update_row(25, 0.5, 0.15)
            logging.error(self.__className + '.read_file: Marks missing')

        ##############################
        # 8. GLOBAL ANGLE OF ATTACK ESTIMATION
        logging.debug(self.__className
                      + '.read_file: 8. GLOBAL ANGLE OF ATTACK ESTIMATION')

        for i in range(3):
            stream.readLine()

        stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 GlobalAoAModel.FinesseCol),
                                 rem_tab_space(stream.readLine()))

        stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 GlobalAoAModel.PlumbPointCol),
                                 rem_tab_space(stream.readLine()))

        stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 GlobalAoAModel.CalageCol),
            rem_tab_space(stream.readLine()))

        stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 GlobalAoAModel.RisersCol),
            rem_tab_space(stream.readLine()))

        stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 GlobalAoAModel.LinesCol),
            rem_tab_space(stream.readLine()))

        stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 GlobalAoAModel.KarabinersCol),
            rem_tab_space(stream.readLine()))

        ##############################
        # 9. SUSPENSION LINES DESCRIPTION
        logging.debug(self.__className
                      + '.read_file: 9. SUSPENSION LINES DESCRIPTION')

        for i in range(3):
            stream.readLine()

        self.wing_M.setData(
            self.wing_M.index(0,
                              WingModel.LinesConcTypeCol),
            rem_tab_space(stream.readLine()))

        num_configs = int(rem_tab_space(stream.readLine()))

        for i in range(0, num_configs):
            num_config_lines = int(rem_tab_space(stream.readLine()))
            self.lines_M.set_num_rows_for_config(i + 1, 0)
            self.lines_M.set_num_rows_for_config(i + 1, num_config_lines)

            for line_it in range(0, num_config_lines):
                values = split_line(stream.readLine())

                # Starting with 3.21 there could be additional parameters
                # Make sure we have all elements for the update in the list
                while len(values) < 16:
                    values.append('')

                self.lines_M.update_row(i + 1, line_it + 1,
                                        values[0],
                                        values[1],
                                        values[2],
                                        values[3],
                                        values[4],
                                        values[5],
                                        values[6],
                                        values[7],
                                        values[8],
                                        values[9],
                                        values[10],
                                        values[12],
                                        values[13],
                                        values[14],
                                        values[15])


        ##############################
        # 10. BRAKES
        logging.debug(self.__className + '.read_file: 10. BRAKES')

        for i in range(3):
            stream.readLine()

        self.wing_M.setData(
            self.wing_M.index(0,
                              WingModel.BrakeLengthCol),
            rem_tab_space(stream.readLine()))

        # delete existing data
        self.brakes_M.set_num_rows_for_config(1, 0)

        # read new data
        num_config_lines = int(rem_tab_space(stream.readLine()))
        self.brakes_M.set_num_rows_for_config(1, num_config_lines)

        for line_it in range(0, num_config_lines):
            values = split_line(stream.readLine())
            # Starting with 3.21 there could be additional parameters
            # Make sure we have all elements for the update in the list
            while len(values) < 16:
                values.append('')
            try:
                self.brakes_M.update_row(1, line_it + 1,
                                         values[0],
                                         values[1],
                                         values[2],
                                         values[3],
                                         values[4],
                                         values[5],
                                         values[6],
                                         values[7],
                                         values[8],
                                         values[9],
                                         values[10],
                                         values[12],
                                         values[13],
                                         values[14],
                                         values[15])
            except:
                self.brakes_M.update_row(1, line_it + 1,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,
                                         0,0,0,0                                         )
                logging.error(self.__className
                              + '.read_file: Brake lines data missing')

        stream.readLine()

        for c in range(0, 2):
            values = split_line(stream.readLine())

            for p in range(0, 5):
                try:
                    self.brakeL_M.setData(
                        self.brakeL_M.index(0, p + (c * 5)), values[p])
                except:
                    self.brakeL_M.setData(
                        self.brakeL_M.index(0, p + (c * 5)), 0)
                    logging.error(
                        self.__className
                        + '.read_file: Brake distribution data missing')

        ##############################
        # 11. RAMIFICATION LENGTH
        logging.debug(self.__className + '.read_file:11. RAMIFICATION LENGTH')

        for i in range(3):
            stream.readLine()

        values = split_line(stream.readLine())
        try:
            self.ramific_M.update_row(1, 1, values[0], values[1], 0)
        except:
            self.ramific_M.update_row(1, 1, 0, 0, 0)
            logging.error(self.__className
                          + '.read_file: Ramification data missing')

        values = split_line(stream.readLine())
        try:
            self.ramific_M.update_row(1, 2, values[0], values[1], values[2])
        except:
            self.ramific_M.update_row(1, 2, 0, 0, 0)
            logging.error(self.__className
                          + '.read_file: Ramification data missing')

        values = split_line(stream.readLine())
        try:
            self.ramific_M.update_row(1, 3, values[0], values[1], 0)
        except:
            self.ramific_M.update_row(1, 3, 0, 0, 0)
            logging.error(self.__className
                          + '.read_file: Ramification data missing')

        values = split_line(stream.readLine())
        try:
            self.ramific_M.update_row(1, 4, values[0], values[1], values[2])
        except:
            self.ramific_M.update_row(1, 4, 0, 0, 0)
            logging.error(self.__className
                          + '.read_file: Ramification data missing')

        ##############################
        # 12. H V AND VH RIBS (Mini Ribs)
        logging.debug(self.__className
                      + '.read_file: 12. H V AND VH RIBS (Mini Ribs)')

        for i in range(3):
            stream.readLine()

        num_config_lines = int(rem_tab_space(stream.readLine()))

        values = split_line(stream.readLine())
        self.wing_M.setData(
            self.wing_M.index(0,
                              WingModel.xSpacingCol),
            values[0])
        try:
            self.wing_M.setData(
                self.wing_M.index(0,
                                  WingModel.ySpacingCol),
                values[1])
        except:
            self.wing_M.setData(
                self.wing_M.index(0,
                                  WingModel.ySpacingCol), 0)
            logging.error(self.__className
                          + '.read_file: H V and VH ribs data missing')

        # delete existing data
        self.hVvHRibs_M.set_num_rows_for_config(1, 0)
        # read new data
        self.hVvHRibs_M.set_num_rows_for_config(1, num_config_lines)

        for line_it in range(0, num_config_lines):
            values = split_line(stream.readLine())
            if (values[1] == '6') or (values[1] == '16'):
                self.hVvHRibs_M.update_row(1, line_it + 1,
                                           values[1],
                                           values[2],
                                           values[3],
                                           values[4],
                                           values[5],
                                           values[6],
                                           values[7],
                                           values[8],
                                           values[9],
                                           values[10],
                                           values[11])
            else:
                self.hVvHRibs_M.update_row(1, line_it + 1,
                                           values[1],
                                           values[2],
                                           values[3],
                                           values[4],
                                           values[5],
                                           values[6],
                                           values[7],
                                           values[8],
                                           values[9])

        ##############################
        # 15. EXTRADOS COLORS
        logging.debug(self.__className + '.read_file: 15. EXTRADOS COLORS')

        for i in range(3):
            stream.readLine()

        num_configs = int(rem_tab_space(stream.readLine()))
        self.extradosColConf_M.set_num_configs(num_configs)

        for configCounter in range(0, num_configs):
            values = split_line(stream.readLine())

            self.extradosColConf_M.update_row(configCounter + 1, values[0])

            num_config_lines = int(values[1])
            self.extradosColDet_M.set_num_rows_for_config(configCounter + 1,
                                                          num_config_lines)

            for line_it in range(0, num_config_lines):
                values = split_line(stream.readLine())
                self.extradosColDet_M.updateRow(configCounter + 1,
                                                line_it + 1,
                                                values[1])

        ##############################
        # 16. INTRADOS COLORS
        logging.debug(self.__className + '.read_file: 16. INTRADOS COLORS')

        for i in range(3):
            stream.readLine()

        num_configs = int(rem_tab_space(stream.readLine()))
        self.intradosColConf_M.set_num_configs(num_configs)

        for configCounter in range(0, num_configs):
            values = split_line(stream.readLine())

            self.intradosColConf_M.updateRow(configCounter + 1, values[0])

            num_config_lines = int(values[1])
            self.intradosColDet_M.set_num_rows_for_config(configCounter + 1,
                                                          num_config_lines)

            for line_it in range(0, num_config_lines):
                values = split_line(stream.readLine())
                self.intradosColDet_M.updateRow(configCounter + 1,
                                                line_it + 1,
                                                values[1])

        ##############################
        # 17. ADDITIONAL RIB POINTS
        logging.debug(self.__className
                      + '.read_file: 17. ADDITIONAL RIB POINTS')

        for i in range(3):
            stream.readLine()

        num_configs = int(rem_tab_space(stream.readLine()))
        self.addRibPts_M.set_num_rows_for_config(1, 0)
        self.addRibPts_M.set_num_rows_for_config(1, num_configs)

        for line_it in range(0, num_configs):
            values = split_line(stream.readLine())

            self.addRibPts_M.update_row(1, line_it + 1, values[0], values[1])

        ##############################
        # 18. ELASTIC LINES CORRECTIONS
        logging.debug(self.__className
                      + '.read_file: 18. ELASTIC LINES CORRECTIONS')

        for i in range(3):
            stream.readLine()

        self.elLinesCorr_M.setData(
            self.elLinesCorr_M.index(0,
                                     ElLinesCorrModel.LoadCol),
            rem_tab_space(stream.readLine()))

        values = split_line(stream.readLine())
        self.elLinesCorr_M.setData(
            self.elLinesCorr_M.index(0,
                                     ElLinesCorrModel.TwoLineDistACol),
            values[0])
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.TwoLineDistBCol),
                values[1])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.TwoLineDistBCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')

        values = split_line(stream.readLine())
        self.elLinesCorr_M.setData(
            self.elLinesCorr_M.index(0,
                                     ElLinesCorrModel.ThreeLineDistACol),
            values[0])
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.ThreeLineDistBCol),
                values[1])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.ThreeLineDistBCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.ThreeLineDistCCol),
                values[2])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.ThreeLineDistCCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')

        values = split_line(stream.readLine())
        self.elLinesCorr_M.setData(
            self.elLinesCorr_M.index(0,
                                     ElLinesCorrModel.FourLineDistACol),
            values[0])
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FourLineDistBCol),
                values[1])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FourLineDistBCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FourLineDistCCol),
                values[2])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FourLineDistCCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FourLineDistDCol),
                values[3])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FourLineDistDCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')

        values = split_line(stream.readLine())
        self.elLinesCorr_M.setData(
            self.elLinesCorr_M.index(0,
                                     ElLinesCorrModel.FiveLineDistACol),
            values[0])
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistBCol),
                values[1])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistBCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistCCol),
                values[2])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistCCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistDCol),
                values[3])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistDCol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistECol),
                values[4])
        except:
            self.elLinesCorr_M.setData(
                self.elLinesCorr_M.index(0,
                                         ElLinesCorrModel.FiveLineDistECol),
                0)
            logging.error(self.__className
                          + '.read_file: Elastic lines corr data missing')

        for line_it in range(0, 5):
            values = split_line(stream.readLine())
            try:
                self.elLinesDef_M.update_row(1,
                                             line_it + 1,
                                             values[1],
                                             values[2],
                                             values[3])
            except:
                self.elLinesDef_M.update_row(1,
                                             line_it + 1,
                                             0,
                                             0,
                                             0)
                logging.error(self.__className
                              + '.read_file: Elastic lines corr data missing')

        ##############################
        # 19. DXF LAYER NAMES
        logging.debug(self.__className + '.read_file: 19. DXF LAYER NAMES')

        for i in range(3):
            stream.readLine()

        num_configs = int(rem_tab_space(stream.readLine()))
        self.dxfLayNames_M.set_num_rows_for_config(1, 0)
        self.dxfLayNames_M.set_num_rows_for_config(1, num_configs)

        for line_it in range(0, num_configs):
            values = split_line(stream.readLine())

            self.dxfLayNames_M.update_row(1, line_it + 1, values[0], values[1])

        ##############################
        # 20. MARKS TYPES
        logging.debug(self.__className + '.read_file: 20. MARKS TYPES')

        for i in range(3):
            stream.readLine()

        num_configs = int(rem_tab_space(stream.readLine()))
        self.marksT_M.set_num_rows_for_config(1, 0)
        self.marksT_M.set_num_rows_for_config(1, num_configs)

        for line_it in range(0, num_configs):
            values = split_line(stream.readLine())

            self.marksT_M.update_row(1, line_it + 1, values[0],
                                     values[1], values[2], values[3],
                                     values[4], values[5], values[6])

        ##############################
        # 21. JONCS DEFINITION (NYLON RODS)
        logging.debug(self.__className
                      + '.read_file: 21. JONCS DEFINITION (NYLON RODS)')

        for i in range(3):
            stream.readLine()

        # delete all what is there
        self.joncsDef_M.set_num_configs(0)

        scheme = int(rem_tab_space(stream.readLine()))

        if scheme == 1:
            # in scheme 1 config num is always 1
            config_num = 1

            num_groups = int(rem_tab_space(stream.readLine()))
            self.joncsDef_M.set_num_rows_for_config(config_num, num_groups)

            for g in range(0, num_groups):
                values_a = split_line(stream.readLine())
                values_b = split_line(stream.readLine())
                values_c = split_line(stream.readLine())
                values_d = split_line(stream.readLine())
                self.joncsDef_M.update_type_one_row(config_num, g + 1,
                                                    values_a[1], values_a[2],
                                                    values_b[0], values_b[1],
                                                    values_b[2], values_b[3],
                                                    values_c[0], values_c[1],
                                                    values_c[2], values_c[3],
                                                    values_d[0], values_d[1],
                                                    values_d[2], values_d[3])

        elif scheme == 2:
            num_blocs = int(rem_tab_space(stream.readLine()))

            for b in range(0, num_blocs):
                values = split_line(stream.readLine())

                bloc_type = int(values[1])
                if bloc_type == 1:
                    num_groups = int(rem_tab_space(stream.readLine()))
                    self.joncsDef_M.set_num_rows_for_config(b + 1, num_groups)

                    for g in range(0, num_groups):
                        values_a = split_line(stream.readLine())
                        values_b = split_line(stream.readLine())
                        values_c = split_line(stream.readLine())
                        values_d = split_line(stream.readLine())
                        self.joncsDef_M.update_type_one_row(
                            b + 1, g + 1,
                            values_a[1], values_a[2],
                            values_b[0], values_b[1], values_b[2], values_b[3],
                            values_c[0], values_c[1], values_c[2], values_c[3],
                            values_d[0], values_d[1], values_d[2], values_d[3])

                else:
                    num_groups = int(rem_tab_space(stream.readLine()))
                    self.joncsDef_M.set_num_rows_for_config(b + 1, num_groups)

                    for g in range(0, num_groups):
                        values_a = split_line(stream.readLine())
                        values_b = split_line(stream.readLine())
                        values_c = split_line(stream.readLine())
                        self.joncsDef_M.update_type_two_row(
                            b + 1, g + 1,
                            values_a[1], values_a[2],
                            values_b[0], values_b[1], values_b[2], values_b[3],
                            values_b[4],
                            values_c[0], values_c[1], values_c[2], values_c[3])
        # Little bad hack. Some GUI depends on data within the rows set above.
        # To get the GUI updated properly we fake here a model update to force
        # an update in the GUI.
        self.joncsDef_M.numRowsForConfigChanged.emit(0, 0)

        ##############################
        # 22. NOSE MYLARS DEFINITION
        logging.debug(self.__className
                      + '.read_file: 22. NOSE MYLARS DEFINITION')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))
        self.noseMylars_M.set_num_configs(0)

        if data != 0:
            # we have data to read

            num_configs = int(rem_tab_space(stream.readLine()))
            self.noseMylars_M.set_num_rows_for_config(1, num_configs)

            for c in range(0, num_configs):
                values_a = split_line(stream.readLine())
                values_b = split_line(stream.readLine())

                self.noseMylars_M.update_row(1, c + 1,
                                             values_a[1], values_a[2],
                                             values_b[0], values_b[1],
                                             values_b[2], values_b[3],
                                             values_b[4], values_b[5])

        ##############################
        # 23. TAB REINFORCEMENTS
        logging.debug(self.__className
                      + '.read_file: Jump over 23. TAB REINFORCEMENTS')

        counter = 0
        while counter < 4:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1

        ##############################
        # 24. GENERAL 2D DXF OPTIONS
        # be carefully: previous code has already read both **** lines of header
        logging.debug(self.__className
                      + '.read_file: 24. GENERAL 2D DXF OPTIONS')

        data = int(rem_tab_space(stream.readLine()))

        self.twoDDxf_M.set_is_used(False)

        if data != 0:
            self.twoDDxf_M.set_is_used(True)
            self.twoDDxf_M.set_num_rows_for_config(1, 6)
            # we have data to read
            for line_it in range(0, 6):
                values = split_line(stream.readLine())
                self.twoDDxf_M.update_row(1, line_it + 1,
                                          values[0], values[1], values[2])

        ##############################
        # 25. GENERAL 3D DXF OPTIONS
        logging.debug(self.__className
                      + '.read_file: 25. GENERAL 3D DXF OPTIONS')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))

        self.threeDDxf_M.set_is_used(False)

        if data != 0:
            self.threeDDxf_M.set_is_used(True)
            self.threeDDxf_M.set_num_rows_for_config(1, 9)
            # we have data to read
            for line_it in range(0, 6):
                values = split_line(stream.readLine())
                self.threeDDxf_M.update_row(1, line_it + 1,
                                            values[0], values[1], values[2])

            for line_it in range(0, 3):
                values = split_line(stream.readLine())
                self.threeDDxf_M.update_row(1, line_it + 1 + 6,
                                            values[0], values[2],
                                            values[3], values[1])

        ##############################
        # 26. GLUE VENTS
        logging.debug(self.__className + '.read_file: 26. GLUE VENTS')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))

        self.glueVent_M.set_is_used(False)

        if data != 0:
            self.glueVent_M.set_is_used(True)
            # we have data to read
            for line_it in range(0, self.wing_M.halfNumRibs):
                values = split_line(stream.readLine())
                # Since 3.17 we have a changing number of values
                # Vents 0, 1 -1, -2. -3 no additional values
                # Vents 4, -4, 6, -6    2  additional values
                # Vents 5, -5           3  additional values
                two_val_vents = ['4', '-4', '6', '-6']
                thr_val_vents = ['5', '-5']
                if values[1] in two_val_vents:
                    self.glueVent_M.update_row(1,
                                               line_it + 1,
                                               values[1],
                                               values[2],
                                               values[3],
                                               '')
                elif values[1] in thr_val_vents:
                    self.glueVent_M.update_row(1,
                                               line_it + 1,
                                               values[1],
                                               values[2],
                                               values[3],
                                               values[4])
                else:
                    self.glueVent_M.update_row(1,
                                               line_it + 1,
                                               values[1],
                                               '',
                                               '',
                                               '')

        ##############################
        # 26. SPECIAL WING TIP
        logging.debug(self.__className + '.read_file: 26. SPECIAL WING TIP')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))

        self.specWingTyp_M.set_is_used(False)

        if data == 0:
            self.specWingTyp_M.set_is_used(False)
        else:
            self.specWingTyp_M.set_is_used(True)

            values_a = split_line(stream.readLine())
            values_b = split_line(stream.readLine())

            self.specWingTyp_M.update_row(1, 1, values_a[1], values_b[1])

        ##############################
        # 28. PARAMETERS FOR CALAGE VARIATION
        logging.debug(self.__className
                      + '.read_file: 28. PARAMETERS FOR CALAGE VARIATION')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))

        self.calageVar_M.set_is_used(False)

        if data != 0:
            self.calageVar_M.set_is_used(True)

            values_a = split_line(stream.readLine())
            values_b = split_line(stream.readLine())
            values_c = split_line(stream.readLine())

            self.calageVar_M.update_row(
                1, 1,
                values_a[0],
                values_b[0], values_b[1], values_b[2], values_b[3], values_b[4], values_b[5],
                values_c[0], values_c[1], values_c[2], values_c[3])

        ##############################
        # 29. 3D SHAPING
        logging.debug(self.__className + '.read_file: 29. 3D SHAPING')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))

        self.threeDShConf_M.set_num_configs(0)
        self.threeDShUpDet_M.set_num_configs(0)
        self.threeDShLoDet_M.set_num_configs(0)

        if data != 0:
            # over-read type as it is always 1
            stream.readLine()

            values = split_line(stream.readLine())
            num_groups = int(values[1])
            self.threeDShConf_M.set_num_configs(num_groups)

            for g in range(0, num_groups):
                # ribs and so
                values = split_line(stream.readLine())

                self.threeDShConf_M.update_row(g + 1, 1, values[2], values[3])

                # upper config
                values = split_line(stream.readLine())
                num_up_cuts = int(values[1])
                if num_up_cuts == 1:
                    self.threeDShUpDet_M.set_num_rows_for_config(g + 1, num_up_cuts)

                    values = split_line(stream.readLine())
                    self.threeDShUpDet_M.update_row(g + 1, 1, values[1],
                                                    values[2], values[3])

                elif num_up_cuts == 2:
                    self.threeDShUpDet_M.set_num_rows_for_config(g + 1, num_up_cuts)

                    values = split_line(stream.readLine())
                    self.threeDShUpDet_M.update_row(g + 1, 1, values[1],
                                                    values[2], values[3])

                    values = split_line(stream.readLine())
                    self.threeDShUpDet_M.update_row(g + 1, 2, values[1],
                                                    values[2], values[3])

                # lower config
                values = split_line(stream.readLine())
                num_lo_cuts = int(values[1])
                if num_lo_cuts == 1:
                    self.threeDShLoDet_M.set_num_rows_for_config(g + 1, num_lo_cuts)

                    values = split_line(stream.readLine())
                    self.threeDShLoDet_M.update_row(g + 1, 1, values[1],
                                                    values[2], values[3])

            stream.readLine()

            self.threeDShPr_M.set_num_rows_for_config(1, 0)
            self.threeDShPr_M.set_num_rows_for_config(1, 5)

            for line_it in range(0, 5):
                values = split_line(stream.readLine())
                self.threeDShPr_M.update_row(1, line_it + 1, values[0],
                                             values[1], values[2], values[3],
                                             values[4])

        ##############################
        # 30. AIRFOIL THICKNESS
        logging.debug(self.__className + '.read_file: 30. AIRFOIL THICKNESS')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))

        self.airfThick_M.set_is_used(False)

        if data != 0:
            self.airfThick_M.set_is_used(True)
            # we have data to read
            for line_it in range(0, self.wing_M.halfNumRibs):
                values = split_line(stream.readLine())
                self.airfThick_M.update_row(1, line_it + 1, values[1])

        ##############################
        # 31. NEW SKIN TENSION
        logging.debug(self.__className + '.read_file: 31. NEW SKIN TENSION')

        for i in range(3):
            stream.readLine()

        data = int(rem_tab_space(stream.readLine()))

        self.newSkinTensConf_M.set_num_configs(0)
        self.newSkinTensDet_M.set_num_configs(0)

        if data != 0:
            num_groups = int(rem_tab_space(stream.readLine()))
            self.newSkinTensConf_M.set_num_configs(num_groups)

            for g in range(0, num_groups):
                # comment line
                stream.readLine()

                values = split_line(stream.readLine())
                self.newSkinTensConf_M.update_row(g + 1, values[1], values[2],
                                                  values[4])

                num_lines = int(values[3])
                self.newSkinTensDet_M.set_num_rows_for_config(g + 1, num_lines)
                for line_it in range(0, num_lines):
                    values = split_line(stream.readLine())
                    self.newSkinTensDet_M.update_row(g + 1, line_it + 1,
                                                     values[1], values[2],
                                                     values[3], values[4])
        ##############################
        # 32. PARTS SEPARATION
        # Parts separation was introduced with 3.17

        if self.__fileVersion - 3.17 > -1e-10:

            logging.debug(self.__className + '.read_file: 32. PARTS SEPARATION')

            for line_it in range(3):
                stream.readLine()

            data = int(rem_tab_space(stream.readLine()))

            self.partsSep_M.set_is_used(False)

            if data != 0:
                self.partsSep_M.set_is_used(True)
                panel_x = split_line(stream.readLine())[1]
                panel_x_min = split_line(stream.readLine())[1]
                panel_y = split_line(stream.readLine())[1]
                rib_x = split_line(stream.readLine())[1]
                rib_y = split_line(stream.readLine())[1]
                rib_1y = split_line(stream.readLine())[1]
                param7 = split_line(stream.readLine())[1]
                param8 = split_line(stream.readLine())[1]
                param9 = split_line(stream.readLine())[1]
                param10 = split_line(stream.readLine())[1]

                self.partsSep_M.update_row(1, 1,
                                           panel_x, panel_x_min, panel_y,
                                           rib_x, rib_y,
                                           rib_1y, param7,
                                           param8, param9,
                                           param10)

        else:
            self.partsSep_M.set_is_used(False)

        ##############################
        # 33. DETAILED RISERS
        # Detailed raisers was introduced with 3.21
        if self.__fileVersion - 3.21 > -1e-10:
            logging.debug(self.__className + '.read_file: 33. DETAILED RISERS')

            for line_it in range(3):
                stream.readLine()

            data = int(rem_tab_space(stream.readLine()))

            self.detRisers_m.set_is_used(False)

            if data != 0:
                self.detRisers_m.set_is_used(True)
                # Type line: only type 1 at the moment, we don't need to evaluate this line
                stream.readLine()
                length_a = ''
                length_b = ''
                length_c = ''
                length_d = ''
                length_e = ''
                more_data = True

                while more_data:
                    data = split_line(stream.readLine())

                    if '*' in data[0]:
                        # We are at the end of the se +
                        more_data = False
                    else:
                        if 'A' in data[0:]:
                            length_a = data[1]
                        elif 'B' in data[0:]:
                            length_b = data[1]
                        elif 'C' in data[0:]:
                            length_c = data[1]
                        elif 'D' in data[0:]:
                            length_d = data[1]
                        elif 'E' in data[0:]:
                            length_e = data[1]
            else:
                self.detRisers_m.set_is_used(False)

            self.detRisers_m.update_row(1, 1, length_a, length_b, length_c, length_d, length_e)

        else:
            self.detRisers_m.set_is_used(False)

        ##############################
        # 34. LINES CHARACTERISTICS
        # Introduced with 3.21
        if self.__fileVersion - 3.21 > -1e-10:
            logging.debug(self.__className + '.read_file: 34. LINES CHARACTERISTICS')

            in_header = True
            while in_header:
                data = stream.readLine()
                if '*' not in data[0]:
                    in_header = False

            data = int(data)

            self.linesChar_M.set_is_used(False)
            self.linesChar_M.set_num_configs(0)

            if data != 0:
                self.linesChar_M.set_is_used(True)
                self.linesChar_M.set_num_configs(1)

                num_lines = int(rem_tab_space(stream.readLine()))
                self.linesChar_M.set_num_rows_for_config(1, num_lines)

                for i in range(0, num_lines):
                    values = split_line(stream.readLine())

                    # There could be 13 or 14 values in each line
                    if len(values) == 13:
                        self.linesChar_M.update_row(1, i+1, values[0], values[1], values[2], '',
                                                    values[3],  values[4], values[6], values[7], values[9],
                                                    values[10], values[12])
                    else:
                        self.linesChar_M.update_row(1, i + 1, values[0], values[1], values[2], values[3],
                                                    values[4], values[5], values[7], values[8], values[10],
                                                    values[11], values[13])

        ##############################
        # 35: SOLVE EQUILIBRIUM EQUATIONS
        # Introduced with 3.21
        if self.__fileVersion - 3.21 > -1e-10:
            logging.debug(self.__className + '.read_file: 35: SOLVE EQUILIBRIUM EQUATIONS')

            in_header = True
            while in_header:
                data = stream.readLine()
                if '*' not in data[0]:
                    in_header = False

            data = int(data)

            self.solveEquEqu_M.set_is_used(False)

            if data != 0:
                self.solveEquEqu_M.set_is_used(True)

                g= split_line(stream.readLine())[1]
                ro= split_line(stream.readLine())[1]
                mu= split_line(stream.readLine())[1]
                v= split_line(stream.readLine())[1]
                alpha= split_line(stream.readLine())[1]
                cl= split_line(stream.readLine())[1]
                cle= split_line(stream.readLine())[1]
                cd= split_line(stream.readLine())[1]
                cde= split_line(stream.readLine())[1]
                cm= split_line(stream.readLine())[1]
                spilot= split_line(stream.readLine())[1]
                cdpilot= split_line(stream.readLine())[1]
                mw= split_line(stream.readLine())[1]
                mp= split_line(stream.readLine())[1]
                pmc= split_line(stream.readLine())[1]
                mql= split_line(stream.readLine())[1]
                ycp= split_line(stream.readLine())[1]
                zcp= split_line(stream.readLine())[1]

                self.solveEquEqu_M.update_row(1, 1, g, ro, mu, v, alpha, cl, cle, cd , cde, cm,
                                              spilot, cdpilot, mw, mp, pmc, mql, ycp, zcp)

        ##############################
        # 36: CREATE FILES FOR XFLR5 ANALYSIS
        # Introduced with 3.21
        if self.__fileVersion - 3.21 > -1e-10:
            logging.debug(self.__className + '.read_file: 36: CREATE FILES FOR XFLR5 ANALYSIS')

            in_header = True
            while in_header:
                data = stream.readLine()
                if '*' not in data[0]:
                    in_header = False

            data = int(data)

            self.xflr_M.set_is_used(False)
            self.xflr_M.set_num_configs(0)

            if data != 0:
                self.xflr_M.set_is_used(True)
                self.xflr_M.set_num_configs(1)

                # Read the comment located before the data
                stream.readLine()
                chord_nr= split_line(stream.readLine())[0]
                per_cell= split_line(stream.readLine())[0]
                cos_dist= split_line(stream.readLine())[0]
                uniform= split_line(stream.readLine())[0]

                stream.readLine()
                inc_bill= split_line(stream.readLine())[0]

                self.xflr_M.update_row(1, 1, chord_nr, per_cell,
                                       cos_dist, uniform, inc_bill)

        ##############################
        # 37: SOME SPECIAL PARAMETERS
        # Introduced with 3.21
        if self.__fileVersion - 3.21 > -1e-10:
            logging.debug(self.__className + '.read_file: 37: SOME SPECIAL PARAMETERS')

            in_header = True
            while in_header:
                data = stream.readLine()
                if '*' not in data[0]:
                    in_header = False

            data = int(data)

            self.specialParameters_M.set_is_used(False)
            self.specialParameters_M.set_num_configs(0)

            if data != 0:
                self.specialParameters_M.set_is_used(True)
                self.specialParameters_M.set_num_configs(1)

                num_lines = int(rem_tab_space(stream.readLine()))
                self.specialParameters_M.set_num_rows_for_config(1, num_lines)

                for i in range(0, num_lines):
                    values = split_line(stream.readLine())

                    self.specialParameters_M.update_row(1, i+1, values[0], values[1])


        ##############################
        # Cleanup
        in_file.close()
        self.wait_info_w.close()
