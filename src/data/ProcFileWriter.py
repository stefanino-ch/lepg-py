""""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'"""

from datetime import date
import logging
import os

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QMessageBox

from ConfigReader.ConfigReader import ConfigReader
from data.FileHelpers import FileHelpers
from data.ProcModel import ProcModel


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
        Constructor
        """
        self.rib_m = ProcModel.RibModel()
        self.wing_m = ProcModel.WingModel()
        self.airfoils_m = ProcModel.AirfoilsModel()
        self.anchor_points_m = ProcModel.AnchorPointsModel()
        self.light_conf_m = ProcModel.LightConfModel()
        self.light_det_m = ProcModel.LightDetModel()
        self.skin_tens_m = ProcModel.SkinTensionModel()
        self.skin_tens_params_m = ProcModel.SkinTensionParamsModel()
        self.sewing_allow_m = ProcModel.SewingAllowancesModel()
        self.marks_m = ProcModel.MarksModel()
        self.glob_aoa_m = ProcModel.GlobAoAModel()
        self.lines_m = ProcModel.LinesModel()
        self.brakes_m = ProcModel.BrakesModel()
        self.brake_length_m = ProcModel.BrakeLengthModel()
        self.ramific_m = ProcModel.RamificationModel()
        self.hv_vh_ribs_m = ProcModel.HvVhRibsModel()
        self.extrados_col_conf_m = ProcModel.ExtradosColConfModel()
        self.extrados_col_det_m = ProcModel.ExtradosColDetModel()
        self.intrados_col_conf_m = ProcModel.IntradosColsConfModel()
        self.intrados_col_det_m = ProcModel.IntradosColsDetModel()
        self.add_rib_pts_m = ProcModel.AddRibPointsModel()
        self.el_lines_corr_m = ProcModel.ElLinesCorrModel()
        self.el_lines_def_m = ProcModel.ElLinesDefModel()
        self.dxf_lay_names_m = ProcModel.DxfLayerNamesModel()
        self.marks_t_m = ProcModel.MarksTypesModel()
        self.joncs_def_m = ProcModel.JoncsDefModel()
        self.nose_mylars_m = ProcModel.NoseMylarsModel()
        self.two_d_dxf_m = ProcModel.TwoDDxfModel()
        self.three_d_dxf_m = ProcModel.ThreeDDxfModel()
        self.glue_vent_m = ProcModel.GlueVentModel()
        self.spec_wing_tip_m = ProcModel.SpecWingTipModel()
        self.calage_var_m = ProcModel.CalageVarModel()
        self.three_d_sh_conf_m = ProcModel.ThreeDShConfModel()
        self.three_d_sh_up_det_M = ProcModel.ThreeDShUpDetModel()
        self.three_d_sh_lo_det_m = ProcModel.ThreeDShLoDetModel()
        self.three_d_sh_print_m = ProcModel.ThreeDShPrintModel()
        self.airf_thickn_m = ProcModel.AirfoilThicknessModel()
        self.new_skin_tens_conf_m = ProcModel.NewSkinTensConfModel()
        self.new_skin_tens_det_m = ProcModel.NewSkinTensDetModel()

        self.fh = FileHelpers()

    def set_file_path_name(self, file_path_name):
        """
        :method: Used to set the full path and filename to be written
        """
        self.__fileNamePath = file_path_name

    def write_file(self, for_proc=False):
        """
        :method: Writes all the values into a data file.
        :warning: Filename must have been set already before, unless the file
                  shall be written for the PreProcessor.
        :param for_proc: Set this to True if the file must be saved in the
                        directory where the PreProcessor resides

        :returns: True if file was written successfully, False else
        :rtype: bool
        """
        separator = '***************************************************\n'

        logging.debug(self.__className + '.write_file')

        if for_proc is True:
            # Special file write into the directory where the
            # PreProcessor resides
            config_reader = ConfigReader()
            file_path_name = os.path.join(config_reader
                                          .get_pre_proc_directory(),
                                          'leparagliding.txt')
        else:
            file_path_name = self.__fileNamePath

        # check if the file already exists
        if os.path.isfile(file_path_name):
            # file exists -> delete it
            os.remove(file_path_name)

        out_file = QFile(file_path_name)

        if not out_file.open(QFile.ReadWrite | QFile.Text):
            logging.error(self.__className
                          + '.write_file '
                          + out_file.errorString())

            msg_box = QMessageBox()
            msg_box.setWindowTitle("File save error")
            msg_box.setText('File can not be saved: '
                            + out_file.errorString())
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            return False

        # File is open, start writing
        stream = QTextStream(out_file)
        stream.setCodec('UTF-8')

        stream << separator
        stream << '* LABORATORI D\'ENVOL PARAGLIDING DESIGN\n'
        stream << '* Input data file version 3.17\n'
        stream << separator
        today = date.today()
        stream << '* Version %s\n' % today.strftime("%Y-%m-%d")
        stream << separator

        values = self.wing_m.get_row()
        stream << '*             1. GEOMETRY\n'
        stream << separator
        stream << '* Brand name\n'
        stream << '\"%s\"\n' % values.value(ProcModel.WingModel.BrandNameCol)
        stream << '* Wing name\n'
        stream << '\"%s\"\n' % values.value(ProcModel.WingModel.WingNameCol)
        stream << '* Drawing scale\n'
        stream << '%s\n' % self.fh.chkNum(
            values.value(ProcModel.WingModel.DrawScaleCol), 1)
        stream << '* Wing scale\n'
        stream << '%s\n' % self.fh.chkNum(
            values.value(ProcModel.WingModel.WingScaleCol), 1)
        stream << '* Number of cells\n'
        stream << '\t%s\n' % self.fh.chkNum(
            values.value(ProcModel.WingModel.NumCellsCol))
        stream << '* Number of ribs\n'
        stream << '\t%s\n' % self.fh.chkNum(
            values.value(ProcModel.WingModel.NumRibsCol))
        stream << '* Alpha max and parameter\n'
        stream << '\t%s' % self.fh.chkNum(
            values.value(ProcModel.WingModel.AlphaMaxTipCol))
        stream << '\t%s' % self.fh.chkNum(
            values.value(ProcModel.WingModel.AlphaModeCol), 1)
        if values.value(ProcModel.WingModel.AlphaModeCol) == '2':
            stream << '\t%s\n' \
                % values.value(ProcModel.WingModel.AlphaMaxCentCol)
        else:
            stream << '\n'

        stream << '* Paraglider type and parameter.\n'

        stream << '\t\"%s\"' % self.fh.chkStr(
            values.value(ProcModel.WingModel.ParaTypeCol),
            'ds')
        stream << '\t%s\n' % self.fh.chkNum(
            values.value(ProcModel.WingModel.ParaParamCol),
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
                stream << '\t%s' % self.fh.chkNum(values(p))
                if p == 9:
                    stream << '\n'

        stream << separator
        stream << '*             2. AIRFOILS\n'
        stream << separator
        stream << '* Airfoil name, intake in, intake out, open , disp. rrw\n'
        for line_it in range(0, self.wing_m.halfNumRibs):
            values = self.airfoils_m.getRow(line_it + 1)
            stream << '%s' % (line_it + 1)

            for p in range(0, 7):
                if p == 0:
                    stream << '\t%s' % self.fh.chkStr(values(p))
                else:
                    stream << '\t%s' % self.fh.chkNum(values(p))
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
                stream << '\t%s' % self.fh.chkNum(values(p))
                if p == 6:
                    stream << '\n'

        stream << separator
        stream << '*          4. AIRFOIL HOLES\n'
        stream << separator
        num_configs = int(self.light_conf_m.numConfigs())
        stream << '%s\n' % num_configs

        for g in range(0, num_configs):
            values = self.light_conf_m.getRow(g + 1)
            stream << '%s\n' % self.fh.chkNum(values(0))
            stream << '%s\n' % self.fh.chkNum(values(1))

            num_lines = self.light_det_m.numRowsForConfig(g + 1)
            stream << '%s\n' % num_lines
            for line_it in range(0, num_lines):
                values = self.light_det_m.getRow(g + 1, line_it + 1)
                for p in range(0, 7):
                    if p > 0:
                        stream << '\t'
                    stream << '%s' % self.fh.chkNum(values(p))
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
                stream << '%s' % self.fh.chkNum(values(p))
                if p == 3:
                    stream << '\n'

        values = self.skin_tens_params_m.getRow()
        stream << '%s\n' % self.fh.chkNum(values(0))
        stream << '%s' % self.fh.chkNum(values(1))
        stream << '\t%s\n' % self.fh.chkNum(values(2))

        stream << separator
        stream << '*           6. SEWING ALLOWANCES\n'
        stream << separator

        values = self.sewing_allow_m.getRow(1)
        for p in range(0, 3):
            if p > 0:
                stream << '\t'
            stream << '%s' % self.fh.chkNum(values(p))
            if p == 2:
                stream << '\tupper panels (mm)\n'

        values = self.sewing_allow_m.getRow(2)
        for p in range(0, 3):
            if p > 0:
                stream << '\t'
            stream << '%s' % self.fh.chkNum(values(p))
            if p == 2:
                stream << '\tlower panels (mm)\n'

        values = self.sewing_allow_m.getRow(3)
        stream << '%s' % self.fh.chkNum(values(0))
        stream << '\tribs (mm)\n'

        values = self.sewing_allow_m.getRow(4)
        stream << '%s' % self.fh.chkNum(values(0))
        stream << '\tvribs (mm)\n'

        stream << separator
        stream << '*           7. MARKS\n'
        stream << separator

        values = self.marks_m.getRow()
        stream << '%s' % self.fh.chkNum(values(0))
        stream << '\t%s' % self.fh.chkNum(values(1))
        stream << '\t%s\n' % self.fh.chkNum(values(2))

        stream << separator
        stream << '*           8. Global angle of attack estimation\n'
        stream << separator
        values = self.glob_aoa_m.getRow()
        stream << '* Finesse GR\n'
        stream << '\t%s\n' % self.fh.chkNum(values(0))
        stream << '* Center of pressure % of chord\n'
        stream << '\t%s\n' % self.fh.chkNum(values(1))
        stream << '* Calage %\n'
        stream << '\t%s\n' % self.fh.chkNum(values(2))
        stream << '* Risers lenght cm\n'
        stream << '\t%s\n' % self.fh.chkNum(values(3))
        stream << '* Line lenght cm\n'
        stream << '\t%s\n' % self.fh.chkNum(values(4))
        stream << '* Karabiners cm\n'
        stream << '\t%s\n' % self.fh.chkNum(values(5))

        stream << separator
        stream << '*          9. SUSPENSION LINES DESCRIPTION\n'
        stream << separator
        values = self.wing_m.get_row()
        stream << '%s\n' % self.fh.chkNum(values.value(ProcModel.WingModel.LinesConcTypeCol))

        num_configs = self.lines_m.numConfigs()
        stream << '%s\n' % num_configs

        for g in range(0, num_configs):
            num_lines = self.lines_m.numRowsForConfig(g + 1)
            stream << '%s\n' % num_lines

            for line_it in range(0, num_lines):
                values = self.lines_m.getRow(g + 1, line_it + 1)

                for p in range(0, 11):
                    if p > 0:
                        stream << '\t'
                    stream << '%s' % self.fh.chkNum(values(p))
                    if p == 10:
                        stream << '\n'

        stream << separator
        stream << '*       10. BRAKES\n'
        stream << separator

        values = self.wing_m.get_row()
        stream << '%s\n' % self.fh.chkNum(values.value(ProcModel.WingModel.BrakeLengthCol))

        num_lines = self.brakes_m.numRowsForConfig(1)
        stream << '%s\n' % num_lines
        for line_it in range(0, num_lines):
            values = self.brakes_m.getRow(1, line_it + 1)

            for p in range(0, 11):
                if p > 0:
                    stream << '\t'
                stream << '%s' % self.fh.chkNum(values(p))
                if p == 10:
                    stream << '\n'

        stream << '* Brake distribution\n'
        values = self.brake_length_m.getRow()

        for p in range(0, 5):
            if p > 0:
                stream << '\t'
            stream << '%s' % self.fh.chkNum(values(p))
            if p == 4:
                stream << '\n'
        for p in range(5, 10):
            if p > 5:
                stream << '\t'
            stream << '%s' % self.fh.chkNum(values(p))
            if p == 9:
                stream << '\n'

        stream << separator
        stream << '*       11. Ramification lengths\n'
        stream << separator

        values = self.ramific_m.getRow(1, 1)
        stream << '3'
        stream << '\t%s\n' % self.fh.chkNum(values(1))

        values = self.ramific_m.getRow(1, 2)
        stream << '4'
        stream << '\t%s' % self.fh.chkNum(values(1))
        stream << '\t%s\n' % self.fh.chkNum(values(2))

        values = self.ramific_m.getRow(1, 3)
        stream << '3'
        stream << '\t%s\n' % self.fh.chkNum(values(1))

        values = self.ramific_m.getRow(1, 4)
        stream << '4'
        stream << '\t%s' % self.fh.chkNum(values(1))
        stream << '\t%s\n' % self.fh.chkNum(values(2))

        stream << separator
        stream << '*    12. H V and VH ribs\n'
        stream << separator
        num_lines = self.hv_vh_ribs_m.numRowsForConfig(1)
        stream << '%s\n' % num_lines
        values = self.wing_m.get_row()
        stream << '%s' % self.fh.chkNum(values.value(ProcModel.WingModel.xSpacingCol))
        stream << '\t%s\n' % self.fh.chkNum(values.value(ProcModel.WingModel.ySpacingCol))

        for line_it in range(0, num_lines):
            values = self.hv_vh_ribs_m.getRow(1, line_it + 1)

            for p in range(0, 9):
                if p == 0:
                    stream << '%s\t' % (line_it + 1)
                if p > 0:
                    stream << '\t'
                stream << '%s' % self.fh.chkNum(values(p))

            if values(0) == 6 or values(0) == 16:
                stream << '\t%s' % self.fh.chkNum(values(9))
                stream << '\t%s\n' % self.fh.chkNum(values(10))
            else:
                stream << '\n'

        stream << separator
        stream << '*    15. Extrados colors\n'
        stream << separator
        num_groups = self.extrados_col_conf_m.numConfigs()
        stream << '%s\n' % num_groups

        for g in range(0, num_groups):
            num_lines = self.extrados_col_det_m.numRowsForConfig(g + 1)

            values = self.extrados_col_conf_m.getRow(g + 1)
            stream << '%s' % values(0)
            stream << '\t%s\n' % num_lines

            for line_it in range(0, num_lines):
                values = self.extrados_col_det_m.getRow(g + 1, line_it + 1)
                stream << '%s' % (line_it + 1)
                stream << '\t%s\t0.\n' % self.fh.chkNum(values(0))

        stream << separator
        stream << '*    16. Intrados colors\n'
        stream << separator
        num_groups = self.intrados_col_conf_m.numConfigs()
        stream << '%s\n' % num_groups

        for g in range(0, num_groups):
            num_lines = self.intrados_col_det_m.numRowsForConfig(g + 1)

            values = self.intrados_col_conf_m.getRow(g + 1)
            stream << '%s' % values(0)
            stream << '\t%s\n' % num_lines

            for line_it in range(0, num_lines):
                values = self.intrados_col_det_m.getRow(g + 1, line_it + 1)
                stream << '%s' % (line_it + 1)
                stream << '\t%s\t0.\n' % self.fh.chkNum(values(0))

        stream << separator
        stream << '*       17. Aditional rib points\n'
        stream << separator
        num_lines = self.add_rib_pts_m.numRowsForConfig(1)
        stream << '%s\n' % num_lines

        for line_it in range(0, num_lines):
            values = self.add_rib_pts_m.getRow(1, line_it + 1)
            stream << '%s' % self.fh.chkNum(values(0))
            stream << '\t%s\n' % self.fh.chkNum(values(1))

        stream << separator
        stream << '*       18. Elastic lines corrections\n'
        stream << separator
        values = self.el_lines_corr_m.getRow()
        stream << '%s\n' % self.fh.chkNum(values(0))

        stream << '%s' % self.fh.chkNum(values(1))
        stream << '\t%s\n' % self.fh.chkNum(values(2))

        stream << '%s' % self.fh.chkNum(values(3))
        stream << '\t%s' % self.fh.chkNum(values(4))
        stream << '\t%s\n' % self.fh.chkNum(values(5))

        stream << '%s' % self.fh.chkNum(values(6))
        stream << '\t%s' % self.fh.chkNum(values(7))
        stream << '\t%s' % self.fh.chkNum(values(8))
        stream << '\t%s\n' % self.fh.chkNum(values(9))

        stream << '%s' % self.fh.chkNum(values(10))
        stream << '\t%s' % self.fh.chkNum(values(11))
        stream << '\t%s' % self.fh.chkNum(values(12))
        stream << '\t%s' % self.fh.chkNum(values(13))
        stream << '\t%s\n' % self.fh.chkNum(values(14))

        num_lines = self.el_lines_def_m.numRowsForConfig(1)
        for line_it in range(0, num_lines):
            values = self.el_lines_def_m.getRow(1, line_it + 1)

            for p in range(0, 4):
                if p > 0:
                    stream << '\t'
                stream << '%s' % self.fh.chkNum(values(p))
                if p == 3:
                    stream << '\n'

        stream << separator
        stream << '*       19. DXF layer names\n'
        stream << separator
        num_lines = self.dxf_lay_names_m.numRowsForConfig(1)
        stream << '%s\n' % num_lines

        for line_it in range(0, num_lines):
            values = self.dxf_lay_names_m.getRow(1, line_it + 1)

            for p in range(0, 2):
                if p > 0:
                    stream << '\t'
                stream << '%s' % self.fh.chkStr(values(p))
                if p == 1:
                    stream << '\n'

        stream << separator
        stream << '*       20. Marks types\n'
        stream << separator
        num_lines = self.marks_t_m.numRowsForConfig(1)
        stream << '%s\n' % num_lines

        for line_it in range(0, num_lines):
            values = self.marks_t_m.getRow(1, line_it + 1)

            for p in range(0, 7):
                if p > 0:
                    stream << '\t'
                if p == 0:
                    stream << '%s' % self.fh.chkStr(values(p))
                else:
                    stream << '%s' % self.fh.chkNum(values(p))
                if p == 6:
                    stream << '\n'

        stream << separator
        stream << '*       21. JONCS DEFINITION (NYLON RODS)\n'
        stream << separator
        num_groups = self.joncs_def_m.numConfigs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '2\n'  # we always use scheme 2!
            stream << '%s\n' % num_groups

            for g in range(0, num_groups):
                num_lines = self.joncs_def_m.numRowsForConfig(g + 1)
                values = self.joncs_def_m.getRow(g + 1, 1)
                scheme = values(ProcModel.JoncsDefModel.TypeCol)

                stream << '%s' % (g + 1)
                stream << '\t%s\n' % scheme
                stream << '%s\n' % num_lines

                for line_it in range(0, num_lines):
                    values = self.joncs_def_m.getRow(g + 1, line_it + 1)

                    stream << '%s' % (line_it + 1)
                    stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.FirstRibCol))
                    stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.JoncsDefModel.LastRibCol))

                    # Line 1
                    stream << '%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pBACol))
                    stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pBBCol))
                    stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pBCCol))
                    if scheme == 1:
                        stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pBDCol))
                    else:
                        stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pBDCol))
                        stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pBECol))

                    if scheme == 1:
                        # Line 2
                        stream << '%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pCACol))
                        stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pCBCol))
                        stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pCCCol))
                        stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pCDCol))

                    # s values
                    stream << '%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pDACol))
                    stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pDBCol))
                    stream << '\t%s' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pDCCol))
                    stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.JoncsDefModel.pDDCol))

        stream << separator
        stream << '*       22. NOSE MYLARS DEFINITION\n'
        stream << separator
        num_groups = self.nose_mylars_m.numConfigs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '1\n'
            stream << '%s\n' % num_groups

            for g in range(0, num_groups):
                num_lines = self.nose_mylars_m.numRowsForConfig(g + 1)

                for line_it in range(0, num_lines):
                    values = self.nose_mylars_m.getRow(g + 1, line_it + 1)

                    stream << '%s' % (line_it + 1)
                    stream << '\t%s' % self.fh.chkNum(values(ProcModel.NoseMylarsModel.FirstRibCol))
                    stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.NoseMylarsModel.LastRibCol))

                    for p in range(0, 6):
                        if p > 0:
                            stream << '\t'

                        stream << '%s' % self.fh.chkNum(values(ProcModel.NoseMylarsModel.xOneCol + p))

                        if p == 5:
                            stream << '\n'

        stream << separator
        stream << '*       23. TAB REINFORCEMENTS\n'
        stream << separator
        stream << '0\n'  # not yet operational

        stream << separator
        stream << '*       24. GENERAL 2D DXF OPTIONS\n'
        stream << separator
        if self.two_d_dxf_m.isUsed() is False:
            stream << '0\n'
        else:
            stream << '1\n'
            num_lines = self.two_d_dxf_m.numRowsForConfig(1)

            for line_it in range(0, num_lines):
                values = self.two_d_dxf_m.getRow(1, line_it + 1)

                for p in range(0, 3):
                    if p > 0:
                        stream << '\t'
                    if p == 1:
                        stream << '%s' % self.fh.chkNum(values(p))
                    else:
                        stream << '%s' % self.fh.chkStr(values(p))
                    if p == 2:
                        stream << '\n'

        stream << separator
        stream << '*       25. GENERAL 3D DXF OPTIONS\n'
        stream << separator
        if self.three_d_dxf_m.isUsed() is False:
            stream << '0\n'
        else:
            stream << '1\n'
            for line_it in range(0, 6):
                values = self.three_d_dxf_m.getRow(1, line_it + 1)

                stream << '%s' % self.fh.chkStr(values(0))
                stream << '\t%s' % self.fh.chkNum(values(2))
                stream << '\t%s\n' % self.fh.chkStr(values(3))

            for line_it in range(6, 9):
                values = self.three_d_dxf_m.getRow(1, line_it + 1)
                for p in range(0, 4):
                    if p > 0:
                        stream << '\t'
                    if p == 1 or p == 2:
                        stream << '%s' % self.fh.chkNum(values(p))
                    else:
                        stream << '%s' % self.fh.chkStr(values(p))
                    if p == 3:
                        stream << '\n'

        stream << separator
        stream << '*       26. GLUE VENTS\n'
        stream << separator
        if self.glue_vent_m.is_used() is False:
            stream << '0\n'
        else:
            stream << '1\n'
            num_lines = self.glue_vent_m.numRowsForConfig(1)

            for line_it in range(0, num_lines):
                values = self.glue_vent_m.get_row(1, line_it + 1)

                for p in range(0, 2):
                    if p > 0:
                        stream << '\t'
                    stream << '%s' % self.fh.chkNum(values(p))
                    if p == 1:
                        stream << '\n'

        stream << separator
        stream << '*       27. SPECIAL WING TIP\n'
        stream << separator
        if self.spec_wing_tip_m.isUsed() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            values = self.spec_wing_tip_m.getRow(1, 1)
            stream << 'AngleLE\t%s\n' % self.fh.chkNum(values(ProcModel.SpecWingTipModel.AngleLECol))
            stream << 'AngleTE\t%s\n' % self.fh.chkNum(values(ProcModel.SpecWingTipModel.AngleTECol))

        stream << separator
        stream << '*       28. PARAMETERS FOR CALAGE VARIATION\n'
        stream << separator
        if self.calage_var_m.isUsed() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            values = self.calage_var_m.getRow(1, 1)
            stream << '%s\n' % self.fh.chkNum(values(ProcModel.CalageVarModel.NumRisersCol))

            stream << '%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.PosACol))
            stream << '\t%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.PosBCol))
            stream << '\t%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.PosCCol))
            stream << '\t%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.PosDCol))
            stream << '\t%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.PosECol))
            stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.CalageVarModel.PosFCol))

            stream << '%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.MaxNegAngCol))
            stream << '\t%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.NumNegStepsCol))
            stream << '\t%s' % self.fh.chkNum(values(ProcModel.CalageVarModel.MaxPosAngCol))
            stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.CalageVarModel.NumPosStepsCol))

        stream << separator
        stream << '*       29. 3D SHAPING\n'
        stream << separator
        num_groups = self.three_d_sh_conf_m.numConfigs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '1\n'

            stream << '1\n'
            stream << 'groups\t%s\n' % num_groups

            for g in range(0, num_groups):
                values = self.three_d_sh_conf_m.getRow(g + 1, 1)
                stream << 'group\t%s' % (g + 1)
                stream << '\t%s' % self.fh.chkNum(values(ProcModel.ThreeDShConfModel.FirstRibCol))
                stream << '\t%s\n' % self.fh.chkNum(values(ProcModel.ThreeDShConfModel.LastRibCol))

                num_lines = self.three_d_sh_up_det_M.numRowsForConfig(g + 1)
                stream << 'upper\t%s\t1\n' % num_lines

                for line_it in range(0, num_lines):
                    values = self.three_d_sh_up_det_M.getRow(g + 1, line_it + 1)
                    stream << '%s' % (line_it + 1)

                    for p in range(0, 3):
                        stream << '\t%s' % self.fh.chkNum(values(p))
                        if p == 2:
                            stream << '\n'

                num_lines = self.three_d_sh_lo_det_m.numRowsForConfig(g + 1)
                stream << 'lower\t%s\t1\n' % num_lines

                for line_it in range(0, num_lines):
                    values = self.three_d_sh_lo_det_m.getRow(g + 1, line_it + 1)
                    stream << '%s' % (line_it + 1)

                    for p in range(0, 3):
                        stream << '\t%s' % self.fh.chkNum(values(p))
                        if p == 2:
                            stream << '\n'

            stream << '* Print parameters\n'
            num_lines = self.three_d_sh_print_m.numRowsForConfig(1)
            for line_it in range(0, num_lines):
                values = self.three_d_sh_print_m.getRow(1, line_it + 1)

                for p in range(0, 5):
                    if p > 0:
                        stream << '\t'
                    if p == 0:
                        stream << '%s' % self.fh.chkStr(values(p))
                    else:
                        stream << '%s' % self.fh.chkNum(values(p))
                    if p == 4:
                        stream << '\n'

        stream << separator
        stream << '*       30. AIRFOIL THICKNESS MODIFICATION\n'
        stream << separator
        if self.airf_thickn_m.isUsed() is False:
            stream << '0\n'
        else:
            stream << '1\n'

            num_lines = self.airf_thickn_m.numRowsForConfig(1)
            for line_it in range(0, num_lines):
                values = self.airf_thickn_m.getRow(1, line_it + 1)

                stream << '%s' % (line_it + 1)
                stream << '\t%s\n' % self.fh.chkNum(values(0))

        stream << separator
        stream << '*       31. NEW SKIN TENSION MODULE\n'
        stream << separator
        num_groups = self.new_skin_tens_conf_m.numConfigs()
        if num_groups == 0:
            stream << '0\n'
        else:
            stream << '1\n'
            stream << '%s\n' % num_groups

            for g in range(0, num_groups):
                stream << '* Skin tension group\n'
                values = self.new_skin_tens_conf_m.getRow(g + 1, 1)
                num_lines = self.new_skin_tens_det_m.numRowsForConfig(g + 1)

                stream << '%s' % (g + 1)
                stream << '\t%s' % self.fh.chkNum(values(ProcModel.NewSkinTensConfModel.InitialRibCol))
                stream << '\t%s' % self.fh.chkNum(values(ProcModel.NewSkinTensConfModel.FinalRibCol))
                stream << '\t%s' % num_lines
                stream << '\t1\n'

                for line_it in range(0, num_lines):
                    values = self.new_skin_tens_det_m.getRow(g + 1,
                                                             line_it + 1)

                    stream << '%s' % (line_it + 1)
                    for p in range(0, 4):
                        stream << '\t%s' % self.fh.chkNum(values(p))
                        if p == 3:
                            stream << '\n'

        stream.flush()
        out_file.close()

        return True