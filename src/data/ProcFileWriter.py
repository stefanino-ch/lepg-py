""""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'"""

from datetime import date
import logging
import os

from PyQt6.QtCore import QFile, QTextStream, QStringConverter
from PyQt6.QtWidgets import QMessageBox

from ConfigReader.ConfigReader import ConfigReader
from data.FileHelpers import chk_num, chk_str

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
from data.procModel.DetailedRisersModel import DetailedRisersModel
from data.procModel.XflrModel import XflrModel


class ProcFileWriter:
    """
    :class: Covers the operations to write a processor file.
    """

    __className = 'ProcFileWriter'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    __fileNamePath = ''
    '''
    :attr: Fully qualified path and name of the file to write
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        self.rib_m = RibModel()
        self.wing_m = WingModel()
        self.airfoils_m = AirfoilsModel()
        self.anchor_points_m = AnchorPointsModel()
        self.light_conf_m = LightConfModel()
        self.light_det_m = LightDetModel()
        self.skin_tens_m = SkinTensionModel()
        self.skin_tens_params_m = SkinTensionParamsModel()
        self.solve_equ_equ_m = SolveEquEquModel()
        self.special_parameters_m = SpecialParametersModel()
        self.sewing_allow_m = SewingAllowancesModel()
        self.marks_m = MarksModel()
        self.glob_aoa_m = GlobalAoAModel()
        self.lines_m = LinesModel()
        self.lines_char_m = LinesCharacteristicsModel()
        self.brakes_m = BrakeModel()
        self.brake_length_m = BrakeLengthModel()
        self.ramific_m = RamificationModel()
        self.hv_vh_ribs_m = HvVhRibsModel()
        self.extrados_col_conf_m = ExtradosColConfModel()
        self.extrados_col_det_m = ExtradosColDetModel()
        self.intrados_col_conf_m = IntradosColsConfModel()
        self.intrados_col_det_m = IntradosColsDetModel()
        self.add_rib_pts_m = AddRibPointsModel()
        self.el_lines_corr_m = ElLinesCorrModel()
        self.el_lines_def_m = ElLinesDefModel()
        self.dxf_lay_names_m = DxfLayerNamesModel()
        self.marks_t_m = MarksTypesModel()
        self.joncs_def_m = JoncsDefModel()
        self.nose_mylars_m = NoseMylarsModel()
        self.two_d_dxf_m = TwoDDxfModel()
        self.three_d_dxf_m = ThreeDDxfModel()
        self.glue_vent_m = GlueVentModel()
        self.spec_wing_tip_m = SpecWingTipModel()
        self.calage_var_m = CalageVarModel()
        self.three_d_sh_conf_m = ThreeDShConfModel()
        self.three_d_sh_up_det_M = ThreeDShUpDetModel()
        self.three_d_sh_lo_det_m = ThreeDShLoDetModel()
        self.three_d_sh_print_m = ThreeDShPrintModel()
        self.airf_thick_m = AirfoilThicknessModel()
        self.new_skin_tens_conf_m = NewSkinTensConfModel()
        self.new_skin_tens_det_m = NewSkinTensDetModel()
        self.parts_sep_m = PartsSeparationModel()
        self.detRisers_M = DetailedRisersModel()
        self.xflr_m = XflrModel()

    def set_file_path_name(self, file_path_name):
        """
        :method: Used to set the full path and filename to be written
        """
        self.__fileNamePath = file_path_name

    def write_file(self, for_proc=False):
        """
        :method: Writes all the values into a data file
        :warning: Filename must have been set already before, unless the file
                  shall be written for the PreProcessor
        :param for_proc: Set this to True if the file must be saved in the
                        directory where the PreProcessor resides

        :returns: True if file was written successfully, False else
        :rtype: bool
        """
        separator = '***************************************************\n'

        if for_proc is True:
            # Special file write into the directory where the
            # PreProcessor resides
            config_reader = ConfigReader()
            file_path_name = os.path.join(config_reader
                                          .get_proc_directory(),
                                          'leparagliding.txt')
        else:
            file_path_name = self.__fileNamePath

        # check if the file already exists
        if os.path.isfile(file_path_name):
            # file exists -> delete it
            os.remove(file_path_name)

        out_file = QFile(file_path_name)

        if not out_file.open(QFile.OpenModeFlag.ReadWrite | QFile.OpenModeFlag.Text):
            logging.error(self.__className
                          + '.write_file '
                          + out_file.errorString())

            msg_box = QMessageBox()
            msg_box.setWindowTitle("File save error")
            msg_box.setText('File can not be saved: '
                            + out_file.errorString())
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.Icon.Ok)
            msg_box.exec()
            return False

        # File is open, start writing
        stream = QTextStream(out_file)
        stream.setEncoding(QStringConverter.Encoding.Utf8)

        stream << separator
        stream << '* LABORATORI D\'ENVOL PARAGLIDING DESIGN\n'
        stream << '* Input data file version 3.21\n'
        stream << separator
        today = date.today()
        stream << '* Version %s\n' % today.strftime("%Y-%m-%d")
        stream << separator

        values = self.wing_m.get_row()
        stream << '*             1. GEOMETRY\n'
        stream << separator
        stream << '* Brand name\n'
        stream << '\"%s\"\n' % values.value(WingModel.BrandNameCol)
        stream << '* Wing name\n'
        stream << '\"%s\"\n' % values.value(WingModel.WingNameCol)
        stream << '* Drawing scale\n'
        stream << '%s\n' % chk_num(
            values.value(WingModel.DrawScaleCol), 1)
        stream << '* Wing scale\n'
        stream << '%s\n' % chk_num(
            values.value(WingModel.WingScaleCol), 1)
        stream << '* Number of cells\n'
        stream << '\t%s\n' % chk_num(
            values.value(WingModel.NumCellsCol))
        stream << '* Number of ribs\n'
        stream << '\t%s\n' % chk_num(
            values.value(WingModel.NumRibsCol))
        stream << '* Alpha max and parameter\n'
        stream << '\t%s' % chk_num(
            values.value(WingModel.AlphaMaxTipCol))
        stream << '\t%s' % chk_num(
            values.value(WingModel.AlphaModeCol), 1)
        if values.value(WingModel.AlphaModeCol) == '2':
            stream << '\t%s\n' \
                % values.value(WingModel.AlphaMaxCentCol)
        else:
            stream << '\n'

        stream << '* Paraglider type and parameter.\n'

        stream << '\t\"%s\"' % chk_str(
            values.value(WingModel.ParaTypeCol),
            'ds')
        stream << '\t%s\n' % chk_num(
            values.value(WingModel.ParaParamCol),
            1)
        stream << ('* Rib geometric parameters. '
                   'Extended data with two additional columns '
                   'for "Z" versions (!)\n')
        stream << ('* Rib    x-rib    y-LE    y-TE    xp    z    beta    '
                   'RP    Washin    Rot_z    Pos_z\n')
        for i in range(0, self.wing_m.halfNumRibs):
            values = self.rib_m.getRow(i + 1)
            stream << '%s' % (i + 1)

            for p in range(0, 10):
                stream << '\t%s' % chk_num(values(p))
                if p == 9:
                    stream << '\n'

        stream << separator
        stream << '*             2. AIRFOILS\n'
        stream << separator
        stream << '* Airfoil name, intake in, intake out, open , disp. rrw\n'
        for line_it in range(0, self.wing_m.halfNumRibs):
            values = self.airfoils_m.get_row(line_it + 1)
            stream << '%s' % (line_it + 1)

            for p in range(0, 7):
                if p == 0:
                    stream << '\t%s' % chk_str(values(p))
                else:
                    stream << '\t%s' % chk_num(values(p))
                if p == 6:
                    stream << '\n'

        stream << separator
        stream << '*            3. ANCHOR POINTS\n'
        stream << separator
        stream << '* Airf    Anch    A    B    C    D    E    F\n'
        for line_it in range(0, self.wing_m.halfNumRibs):
            values = self.anchor_points_m.getRow(line_it + 1)
            stream << '%s' % (line_it + 1)

            for p in range(0, 7):
                stream << '\t%s' % chk_num(values(p))
                if p == 6:
                    stream << '\n'

        stream << separator
        stream << '*          4. AIRFOIL HOLES\n'
        stream << separator
        num_configs = int(self.light_conf_m.num_configs())
        stream << '%s\n' % num_configs

        for g in range(0, num_configs):
            values = self.light_conf_m.getRow(g + 1)
            stream << '%s\n' % chk_num(values(0))
            stream << '%s\n' % chk_num(values(1))

            num_lines = self.light_det_m.num_rows_for_config(g + 1)
            stream << '%s\n' % num_lines
            for line_it in range(0, num_lines):
                values = self.light_det_m.get_row(g + 1, line_it + 1)
                for p in range(0, 7):
                    if p > 0:
                        stream << '\t'
                    stream << '%s' % chk_num(values(p))
                    if p == 6:
                        stream << '\t0.\t0.\n'

        stream << separator
        stream << '*           5. SKIN TENSION\n'
        stream << separator
        stream << 'Extrados\n'

        for line_it in range(0, 6):
            values = self.skin_tens_m.getRow(line_it + 1)

            for p in range(0, 4):
                if p > 0:
                    stream << '\t'
                stream << '%s' % chk_num(values(p))
                if p == 3:
                    stream << '\n'

        values = self.skin_tens_params_m.getRow()
        stream << '%s\n' % chk_num(values(0))
        stream << '%s' % chk_num(values(1))
        stream << '\t%s\n' % chk_num(values(2))

        stream << separator
        stream << '*           6. SEWING ALLOWANCES\n'
        stream << separator

        values = self.sewing_allow_m.get_row(1)
        for p in range(0, 3):
            if p > 0:
                stream << '\t'
            stream << '%s' % chk_num(values(p))
            if p == 2:
                stream << '\tupper panels (mm)\n'

        values = self.sewing_allow_m.get_row(2)
        for p in range(0, 3):
            if p > 0:
                stream << '\t'
            stream << '%s' % chk_num(values(p))
            if p == 2:
                stream << '\tlower panels (mm)\n'

        values = self.sewing_allow_m.get_row(3)
        stream << '%s' % chk_num(values(0))
        stream << '\tribs (mm)\n'

        values = self.sewing_allow_m.get_row(4)
        stream << '%s' % chk_num(values(0))
        stream << '\tvribs (mm)\n'

        stream << separator
        stream << '*           7. MARKS\n'
        stream << separator

        values = self.marks_m.get_row()
        stream << '%s' % chk_num(values(0))
        stream << '\t%s' % chk_num(values(1))
        stream << '\t%s\n' % chk_num(values(2))

        stream << separator
        stream << '*           8. Global angle of attack estimation\n'
        stream << separator
        values = self.glob_aoa_m.getRow()
        stream << '* Finesse GR\n'
        stream << '\t%s\n' % chk_num(values(0))
        stream << '* Plumb point estimation %\n'
        stream << '\t%s\n' % chk_num(values(1))
        stream << '* Calage %\n'
        stream << '\t%s\n' % chk_num(values(2))
        stream << '* Risers length cm\n'
        stream << '\t%s\n' % chk_num(values(3))
        stream << '* Line length cm\n'
        stream << '\t%s\n' % chk_num(values(4))
        stream << '* Karabiners cm\n'
        stream << '\t%s\n' % chk_num(values(5))

        stream << separator
        stream << '*          9. SUSPENSION LINES DESCRIPTION\n'
        stream << separator
        values = self.wing_m.get_row()
        stream << '%s\n' % chk_num(values.value(WingModel.LinesConcTypeCol))

        num_configs = self.lines_m.num_configs()
        stream << '%s\n' % num_configs

        for g in range(0, num_configs):
            num_lines = self.lines_m.num_rows_for_config(g + 1)
            stream << '%s\n' % num_lines

            for line_it in range(0, num_lines):
                values = self.lines_m.get_row(g + 1, line_it + 1)

                for p in range(0, 11):
                    if p > 0:
                        stream << '\t'
                    stream << '%s' % chk_num(values(p))
                    if p == 10:
                        stream << '\n'

        stream << separator
        stream << '*       10. BRAKES\n'
        stream << separator

        values = self.wing_m.get_row()
        stream << '%s\n' % chk_num(values.value(WingModel.BrakeLengthCol))

        num_lines = self.brakes_m.num_rows_for_config(1)
        stream << '%s\n' % num_lines
        for line_it in range(0, num_lines):
            values = self.brakes_m.get_row(1, line_it + 1)

            for p in range(0, 11):
                if p > 0:
                    stream << '\t'
                stream << '%s' % chk_num(values(p))
                if p == 10:
                    stream << '\n'

        stream << '* Brake distribution\n'
        values = self.brake_length_m.get_row()

        for p in range(0, 5):
            if p > 0:
                stream << '\t'
            stream << '%s' % chk_num(values(p))
            if p == 4:
                stream << '\n'
        for p in range(5, 10):
            if p > 5:
                stream << '\t'
            stream << '%s' % chk_num(values(p))
            if p == 9:
                stream << '\n'

        stream << separator
        stream << '*       11. Ramification lengths\n'
        stream << separator

        values = self.ramific_m.get_row(1, 1)
        stream << '3'
        stream << '\t%s\n' % chk_num(values(1))

        values = self.ramific_m.get_row(1, 2)
        stream << '4'
        stream << '\t%s' % chk_num(values(1))
        stream << '\t%s\n' % chk_num(values(2))

        values = self.ramific_m.get_row(1, 3)
        stream << '3'
        stream << '\t%s\n' % chk_num(values(1))

        values = self.ramific_m.get_row(1, 4)
        stream << '4'
        stream << '\t%s' % chk_num(values(1))
        stream << '\t%s\n' % chk_num(values(2))

        stream << separator
        stream << '*    12. H V and VH ribs\n'
        stream << separator
        num_lines = self.hv_vh_ribs_m.num_rows_for_config(1)
        stream << '%s\n' % num_lines
        values = self.wing_m.get_row()
        stream << '%s' % chk_num(values.value(WingModel.xSpacingCol))
        stream << '\t%s\n' % chk_num(values.value(WingModel.ySpacingCol))

        for line_it in range(0, num_lines):
            values = self.hv_vh_ribs_m.get_row(1, line_it + 1)

            for p in range(0, 9):
                if p == 0:
                    stream << '%s\t' % (line_it + 1)
                if p > 0:
                    stream << '\t'
                stream << '%s' % chk_num(values(p))

            if values(0) == 6 or values(0) == 16:
                stream << '\t%s' % chk_num(values(9))
                stream << '\t%s\n' % chk_num(values(10))
            else:
                stream << '\n'

        stream << separator
        stream << '*    15. Extrados colors\n'
        stream << separator
        num_groups = self.extrados_col_conf_m.num_configs()
        stream << '%s\n' % num_groups

        for g in range(0, num_groups):
            num_lines = self.extrados_col_det_m.num_rows_for_config(g + 1)

            values = self.extrados_col_conf_m.get_row(g + 1)
            stream << '%s' % values(0)
            stream << '\t%s\n' % num_lines

            for line_it in range(0, num_lines):
                values = self.extrados_col_det_m.getRow(g + 1, line_it + 1)
                stream << '%s' % (line_it + 1)
                stream << '\t%s\t0.\n' % chk_num(values(0))

        stream << separator
        stream << '*    16. Intrados colors\n'
        stream << separator
        num_groups = self.intrados_col_conf_m.num_configs()
        stream << '%s\n' % num_groups

        for g in range(0, num_groups):
            num_lines = self.intrados_col_det_m.num_rows_for_config(g + 1)

            values = self.intrados_col_conf_m.getRow(g + 1)
            stream << '%s' % values(0)
            stream << '\t%s\n' % num_lines

            for line_it in range(0, num_lines):
                values = self.intrados_col_det_m.getRow(g + 1, line_it + 1)
                stream << '%s' % (line_it + 1)
                stream << '\t%s\t0.\n' % chk_num(values(0))

        stream << separator
        stream << '*       17. Additional rib points\n'
        stream << separator
        num_lines = self.add_rib_pts_m.num_rows_for_config(1)
        stream << '%s\n' % num_lines

        for line_it in range(0, num_lines):
            values = self.add_rib_pts_m.get_row(1, line_it + 1)
            stream << '%s' % chk_num(values(0))
            stream << '\t%s\n' % chk_num(values(1))

        stream << separator
        stream << '*       18. Elastic lines corrections\n'
        stream << separator
        values = self.el_lines_corr_m.get_row()
        stream << '%s\n' % chk_num(values(0))

        stream << '%s' % chk_num(values(1))
        stream << '\t%s\n' % chk_num(values(2))

        stream << '%s' % chk_num(values(3))
        stream << '\t%s' % chk_num(values(4))
        stream << '\t%s\n' % chk_num(values(5))

        stream << '%s' % chk_num(values(6))
        stream << '\t%s' % chk_num(values(7))
        stream << '\t%s' % chk_num(values(8))
        stream << '\t%s\n' % chk_num(values(9))

        stream << '%s' % chk_num(values(10))
        stream << '\t%s' % chk_num(values(11))
        stream << '\t%s' % chk_num(values(12))
        stream << '\t%s' % chk_num(values(13))
        stream << '\t%s\n' % chk_num(values(14))

        num_lines = self.el_lines_def_m.num_rows_for_config(1)
        for line_it in range(0, num_lines):
            values = self.el_lines_def_m.getRow(1, line_it + 1)

            for p in range(0, 4):
                if p > 0:
                    stream << '\t'
                stream << '%s' % chk_num(values(p))
                if p == 3:
                    stream << '\n'

        stream << separator
        stream << '*       19. DXF layer names\n'
        stream << separator
        num_lines = self.dxf_lay_names_m.num_rows_for_config(1)
        stream << '%s\n' % num_lines

        for line_it in range(0, num_lines):
            values = self.dxf_lay_names_m.get_row(1, line_it + 1)

            for p in range(0, 2):
                if p > 0:
                    stream << '\t'
                stream << '%s' % chk_str(values(p))
                if p == 1:
                    stream << '\n'

        stream << separator
        stream << '*       20. Marks types\n'
        stream << separator
        num_lines = self.marks_t_m.num_rows_for_config(1)
        stream << '%s\n' % num_lines

        for line_it in range(0, num_lines):
            values = self.marks_t_m.get_row(1, line_it + 1)

            for p in range(0, 7):
                if p > 0:
                    stream << '\t'
                if p == 0:
                    stream << '%s' % chk_str(values(p))
                else:
                    stream << '%s' % chk_num(values(p))
                if p == 6:
                    stream << '\n'

        stream << separator
        stream << '*       21. JONCS DEFINITION (NYLON RODS)\n'
        stream << separator
        num_groups = self.joncs_def_m.num_configs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '2\n'  # we always use scheme 2!
            stream << '%s\n' % num_groups

            for g in range(0, num_groups):
                num_lines = self.joncs_def_m.num_rows_for_config(g + 1)
                values = self.joncs_def_m.get_row(g + 1, 1)
                scheme = values(JoncsDefModel.TypeCol)

                stream << '%s' % (g + 1)
                stream << '\t%s\n' % scheme
                stream << '%s\n' % num_lines

                for line_it in range(0, num_lines):
                    values = self.joncs_def_m.get_row(g + 1, line_it + 1)

                    stream << '%s' % (line_it + 1)
                    stream << '\t%s' % chk_num(values(JoncsDefModel.FirstRibCol))
                    stream << '\t%s\n' % chk_num(values(JoncsDefModel.LastRibCol))

                    # Line 1
                    stream << '%s' % chk_num(values(JoncsDefModel.pBACol))
                    stream << '\t%s' % chk_num(values(JoncsDefModel.pBBCol))
                    stream << '\t%s' % chk_num(values(JoncsDefModel.pBCCol))
                    if scheme == 1:
                        stream << '\t%s\n' % chk_num(values(JoncsDefModel.pBDCol))
                    else:
                        stream << '\t%s' % chk_num(values(JoncsDefModel.pBDCol))
                        stream << '\t%s\n' % chk_num(values(JoncsDefModel.pBECol))

                    if scheme == 1:
                        # Line 2
                        stream << '%s' % chk_num(values(JoncsDefModel.pCACol))
                        stream << '\t%s' % chk_num(values(JoncsDefModel.pCBCol))
                        stream << '\t%s' % chk_num(values(JoncsDefModel.pCCCol))
                        stream << '\t%s\n' % chk_num(values(JoncsDefModel.pCDCol))

                    # s values
                    stream << '%s' % chk_num(values(JoncsDefModel.pDACol))
                    stream << '\t%s' % chk_num(values(JoncsDefModel.pDBCol))
                    stream << '\t%s' % chk_num(values(JoncsDefModel.pDCCol))
                    stream << '\t%s\n' % chk_num(values(JoncsDefModel.pDDCol))

        stream << separator
        stream << '*       22. NOSE MYLARS DEFINITION\n'
        stream << separator
        num_groups = self.nose_mylars_m.num_configs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '1\n'
            stream << '%s\n' % num_groups

            for g in range(0, num_groups):
                num_lines = self.nose_mylars_m.num_rows_for_config(g + 1)

                for line_it in range(0, num_lines):
                    values = self.nose_mylars_m.get_row(g + 1, line_it + 1)

                    stream << '%s' % (line_it + 1)
                    stream << '\t%s' % chk_num(values(NoseMylarsModel.FirstRibCol))
                    stream << '\t%s\n' % chk_num(values(NoseMylarsModel.LastRibCol))

                    for p in range(0, 6):
                        if p > 0:
                            stream << '\t'

                        stream << '%s' % chk_num(values(NoseMylarsModel.xOneCol + p))

                        if p == 5:
                            stream << '\n'

        stream << separator
        stream << '*       23. TAB REINFORCEMENTS\n'
        stream << separator
        stream << '0\n'  # not yet operational

        stream << separator
        stream << '*       24. GENERAL 2D DXF OPTIONS\n'
        stream << separator
        if self.two_d_dxf_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'
            num_lines = self.two_d_dxf_m.num_rows_for_config(1)

            for line_it in range(0, num_lines):
                values = self.two_d_dxf_m.get_row(1, line_it + 1)

                for p in range(0, 3):
                    if p > 0:
                        stream << '\t'
                    if p == 1:
                        stream << '%s' % chk_num(values(p))
                    else:
                        stream << '%s' % chk_str(values(p))
                    if p == 2:
                        stream << '\n'

        stream << separator
        stream << '*       25. GENERAL 3D DXF OPTIONS\n'
        stream << separator
        if self.three_d_dxf_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'
            for line_it in range(0, 6):
                values = self.three_d_dxf_m.get_row(1, line_it + 1)

                stream << '%s' % chk_str(values(0))
                stream << '\t%s' % chk_num(values(2))
                stream << '\t%s\n' % chk_str(values(3))

            for line_it in range(6, 9):
                values = self.three_d_dxf_m.get_row(1, line_it + 1)
                for p in range(0, 4):
                    if p > 0:
                        stream << '\t'
                    if p == 1 or p == 2:
                        stream << '%s' % chk_num(values(p))
                    else:
                        stream << '%s' % chk_str(values(p))
                    if p == 3:
                        stream << '\n'

        stream << separator
        stream << '*       26. GLUE VENTS\n'
        stream << separator
        if self.glue_vent_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'
            num_lines = self.glue_vent_m.num_rows_for_config(1)

            # Since 3.17 we have a changing number of values
            # Vents 0, 1 -1, -2. -3 no additional values
            # Vents 4, -4, 6, -6    2  additional values
            # Vents 5, -5           3  additional values
            two_val_vents = [4, -4, 6, -6]
            thr_val_vents = [5, -5]

            for line_it in range(0, num_lines):
                values = self.glue_vent_m.get_row(1, line_it + 1)

                vent_type = chk_num(values.value(1))

                if vent_type in two_val_vents:
                    num_params = 4
                elif vent_type in thr_val_vents:
                    num_params = 5
                else:
                    num_params = 2

                for p in range(0, num_params):
                    if p > 0:
                        stream << '\t'
                    stream << '%s' % chk_num(values.value(p))
                    if p == num_params - 1:
                        stream << '\n'

        stream << separator
        stream << '*       27. SPECIAL WING TIP\n'
        stream << separator
        if self.spec_wing_tip_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            values = self.spec_wing_tip_m.get_row(1, 1)
            stream << 'AngleLE\t%s\n' % chk_num(values(SpecWingTipModel.AngleLECol))
            stream << 'AngleTE\t%s\n' % chk_num(values(SpecWingTipModel.AngleTECol))

        stream << separator
        stream << '*       28. PARAMETERS FOR CALAGE VARIATION\n'
        stream << separator
        if self.calage_var_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            values = self.calage_var_m.get_row(1, 1)
            stream << '%s\n' % chk_num(values(CalageVarModel.NumRisersCol))

            stream << '%s' % chk_num(values(CalageVarModel.PosACol))
            stream << '\t%s' % chk_num(values(CalageVarModel.PosBCol))
            stream << '\t%s' % chk_num(values(CalageVarModel.PosCCol))
            stream << '\t%s' % chk_num(values(CalageVarModel.PosDCol))
            stream << '\t%s' % chk_num(values(CalageVarModel.PosECol))
            stream << '\t%s\n' % chk_num(values(CalageVarModel.PosFCol))

            stream << '%s' % chk_num(values(CalageVarModel.MaxNegAngCol))
            stream << '\t%s' % chk_num(values(CalageVarModel.NumNegStepsCol))
            stream << '\t%s' % chk_num(values(CalageVarModel.MaxPosAngCol))
            stream << '\t%s\n' % chk_num(values(CalageVarModel.NumPosStepsCol))

        stream << separator
        stream << '*       29. 3D SHAPING\n'
        stream << separator
        num_groups = self.three_d_sh_conf_m.num_configs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '1\n'

            stream << '1\n'
            stream << 'groups\t%s\n' % num_groups

            for g in range(0, num_groups):
                values = self.three_d_sh_conf_m.get_row(g + 1, 1)
                stream << 'group\t%s' % (g + 1)
                stream << '\t%s' % chk_num(values(ThreeDShConfModel.FirstRibCol))
                stream << '\t%s\n' % chk_num(values(ThreeDShConfModel.LastRibCol))

                num_lines = self.three_d_sh_up_det_M.num_rows_for_config(g + 1)
                stream << 'upper\t%s\t1\n' % num_lines

                for line_it in range(0, num_lines):
                    values = self.three_d_sh_up_det_M.get_row(g + 1, line_it + 1)
                    stream << '%s' % (line_it + 1)

                    for p in range(0, 3):
                        stream << '\t%s' % chk_num(values(p))
                        if p == 2:
                            stream << '\n'

                num_lines = self.three_d_sh_lo_det_m.num_rows_for_config(g + 1)
                stream << 'lower\t%s\t1\n' % num_lines

                for line_it in range(0, num_lines):
                    values = self.three_d_sh_lo_det_m.get_row(g + 1, line_it + 1)
                    stream << '%s' % (line_it + 1)

                    for p in range(0, 3):
                        stream << '\t%s' % chk_num(values(p))
                        if p == 2:
                            stream << '\n'

            stream << '* Print parameters\n'
            num_lines = self.three_d_sh_print_m.num_rows_for_config(1)
            for line_it in range(0, num_lines):
                values = self.three_d_sh_print_m.get_row(1, line_it + 1)

                for p in range(0, 5):
                    if p > 0:
                        stream << '\t'
                    if p == 0:
                        stream << '%s' % chk_str(values(p))
                    else:
                        stream << '%s' % chk_num(values(p))
                    if p == 4:
                        stream << '\n'

        stream << separator
        stream << '*       30. AIRFOIL THICKNESS MODIFICATION\n'
        stream << separator
        if self.airf_thick_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            num_lines = self.airf_thick_m.num_rows_for_config(1)
            for line_it in range(0, num_lines):
                values = self.airf_thick_m.get_row(1, line_it + 1)

                stream << '%s' % (line_it + 1)
                stream << '\t%s\n' % chk_num(values(0))

        stream << separator
        stream << '*       31. NEW SKIN TENSION MODULE\n'
        stream << separator
        num_groups = self.new_skin_tens_conf_m.num_configs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '1\n'
            stream << '%s\n' % num_groups

            for g in range(0, num_groups):
                stream << '* Skin tension group\n'
                values = self.new_skin_tens_conf_m.get_row(g + 1, 1)
                num_lines = self.new_skin_tens_det_m.num_rows_for_config(g + 1)

                stream << '%s' % (g + 1)
                stream << '\t%s' % chk_num(values(NewSkinTensConfModel.InitialRibCol))
                stream << '\t%s' % chk_num(values(NewSkinTensConfModel.FinalRibCol))
                stream << '\t%s' % num_lines
                stream << '\t1\n'

                for line_it in range(0, num_lines):
                    values = self.new_skin_tens_det_m.get_row(g + 1,
                                                              line_it + 1)

                    stream << '%s' % (line_it + 1)
                    for p in range(0, 4):
                        stream << '\t%s' % chk_num(values(p))
                        if p == 3:
                            stream << '\n'

        stream << separator
        stream << '*       32. PARAMETERS FOR PARTS SEPARATION\n'
        stream << separator

        if self.parts_sep_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            values = self.parts_sep_m.get_row(1, 1)
            stream << 'panel_x\t%s\n' % values.value(0)
            stream << 'panel_x_min\t%s\n' % values.value(1)
            stream << 'panel_y\t%s\n' % values.value(2)
            stream << 'rib_x\t%s\n' % values.value(3)
            stream << 'rib_y\t%s\n' % values.value(4)
            stream << 'rib_1y\t%s\n' % values.value(5)
            # following parameters are not used, therefore hardcoded here
            stream << 'parameter7\t1.0\n'
            stream << 'parameter8\t1.0\n'
            stream << 'parameter9\t1.0\n'
            stream << 'parameter10\t1.0\n'

        stream << separator
        stream << '*       33. Detailed Risers\n'
        stream << separator

        if self.detRisers_M.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            # Write type (hardcoded as there is only type 1)
            stream << '1\n'

            values = self.detRisers_M.get_row(1, 1)
            riser_names = ['A', 'B', 'C', 'D', 'E']

            for val_it in range(0, 5):
                if values(val_it) != '':
                    stream << '%s\t%s\tcm\n' %(riser_names[val_it], values(val_it))

        stream << separator
        stream << '*       34. LINES CHARACTERISTICS TABLE\n'
        stream << separator

        if self.lines_char_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            num_lines = self.lines_char_m.num_rows_for_config(1)
            stream << '%i\n' % num_lines

            for i in range(0, num_lines):
                values = self.lines_char_m.get_row(1, i+1)
                for j in range(1, 12):
                    stream << '%s\t' % values(j)
                    if j == 6:
                        stream << 'daN\t'
                    if j == 8:
                        stream << 'g\t'
                    if j == 10:
                        stream << 'cm\t'
                stream << '\n'

        stream << separator
        stream << '*       35. SOLVE EQUILIBRIUM EQUATIONS\n'
        stream << separator

        if self.solve_equ_equ_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            values = self.solve_equ_equ_m.get_row(1, 1)
            stream << 'g\t%s\tm/s2\tgravity of Earth\n' % values(1)
            stream << 'ro\t%s\tkg/m3\tair mass density\n' % values(2)
            stream << 'mu\t%s\tmuPa\tair dynamic viscosity(microPascal)\n' % values(3)
            stream << 'V\t%s\tm/s\testimated flow speed\n' % values(4)
            stream << 'Alpha\t%s\tdeg\testimated wing angle of attact at trim speed\n' % values(5)
            stream << 'Cl\t%s\twing lift coefficient\n' % values(6)
            stream << 'cle\t%s\tlift correction coefficient\n' % values(7)
            stream << 'Cd\t%s\twing drag coefficient\n' % values(8)
            stream << 'cde\t%s\tdrag correction coefficient\n' % values(9)
            stream << 'Cm\t%s\twing moment coefficient\n' % values(10)
            stream << 'Spilot\t%s\tm2\tpilot + harness frontal surface\n' % values(11)
            stream << 'Cdpilot\t%s\tpilot + harness drag coefficient\n' % values(12)
            stream << 'Mw\t%s\tkg\twing mass\n' % values(13)
            stream << 'Mp\t%s\tkg\tpilot mass included harness and instruments\n' % values(14)
            stream << 'Pmc\t%s\tm\tpilot mass center below main karabiners\n' % values(15)
            stream << 'Mql\t%s\tg\tone quick link mass(riser - lines)\n' % values(16)
            stream << 'Ycp\t%s\tm\ty - coordinate center of pressure\n' % values(17)
            stream << 'Zcp\t%s\tm\tz - coordinate center of pressure\n' % values(18)

        stream << separator
        stream << '*       36. CREATE FILES FOR XFLR5 ANALYSIS\n'
        stream << separator

        if self.xflr_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'
            stream << '* Panel parameters\n'

            values = self.xflr_m.get_row(1, 1)
            stream << '%s\tchord nr\n' % values(1)
            stream << '%s\tper cell\n' % values(2)
            stream << '%s\tcosine distribution along chord\n' % values(3)
            stream << '%s\tuniform along span\n' % values(4)

            stream << '* Include billowed airfoils (more accuracy)\n'
            stream << '%s\n' % values(5)

        stream << separator
        stream << '*       37. SOME SPECIAL PARAMETERS\n'
        stream << separator

        if self.special_parameters_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            num_lines = self.special_parameters_m.num_rows_for_config(1)
            stream << '%i\n' % num_lines

            for i in range(0, num_lines):
                values = self.special_parameters_m.get_row(1, i+1)
                stream << '%s\t%s\n' % (values(1), values(2))

        stream << '\n'
        stream.flush()
        out_file.close()

        return True
