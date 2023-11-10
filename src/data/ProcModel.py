"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to the authors of:

https://doc.qt.io/qtforpython/overviews/sql-model.html

https://www.datacamp.com/community/tutorials/inner-classes-python
"""
import logging

from PyQt6.QtCore import QFile, QTextStream, QObject, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from Singleton.Singleton import Singleton
from data.Database import Database
from data.PreProcOutfileReader import PreProcOutfileReader

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
from data.procModel.SpecWingTipModel import SpecWingTipModel
from data.procModel.ThreeDDxfModel import ThreeDDxfModel
from data.procModel.ThreeDShConfModel import ThreeDShConfModel
from data.procModel.ThreeDShLoDetModel import ThreeDShLoDetModel
from data.procModel.ThreeDShPrintModel import ThreeDShPrintModel
from data.procModel.ThreeDShUpDetModel import ThreeDShUpDetModel
from data.procModel.TwoDDxfModel import TwoDDxfModel
from data.procModel.WingModel import WingModel


class ProcModel(QObject, metaclass=Singleton):
    """
    :class: Does take care about the data handling for the processor.
        - Reads and writes the data files
        - Holds as a central point all temporary data during program execution

    Is implemented as a **Singleton**. Even if it is instantiated multiple
    times all data will be the same for all instances.
    """
    dataStatusUpdate = pyqtSignal(str, str)
    '''
    :signal:  Sent out as soon a file was opened or saved
        The first string indicates the class name
        The second string indicates
        - Data status changes saved/ edited
        - Filename and path has been changed
        - File version has been changed
    '''

    __className = 'ProcModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    __fileNamePath = ''
    '''
    :attr: Full path and name of the data file currently in use
    '''
    __fileVersion = ''
    '''
    :attr: Version number of the file currently in use
    '''
    __latestFileVersion = '3.17'
    '''
    :attr: Version number of the currently supported processor
    '''

    def __init__(self, parent=None):
        """
        :method: Class initialization
        """
        self.__fileSaved = True

        self.db = Database()
        self.db.open_connection()

        super().__init__()

        self.wing_m = WingModel()
        self.wing_m.dataChanged.connect(self.data_edit)

        self.rib_m = RibModel()
        self.rib_m.dataChanged.connect(self.data_edit)

        self.addRibPoints_m = AddRibPointsModel()
        self.addRibPoints_m.dataChanged.connect(self.data_edit)
        self.airf_m = AirfoilsModel()
        self.airf_m.dataChanged.connect(self.data_edit)
        self.airfThick_m = AirfoilThicknessModel()
        self.airfThick_m.dataChanged.connect(self.data_edit)
        self.anchPoints_m = AnchorPointsModel()
        self.anchPoints_m.dataChanged.connect(self.data_edit)
        self.brakes_m = BrakeModel()
        self.brakes_m.dataChanged.connect(self.data_edit)
        self.brakeLength_m = BrakeLengthModel()
        self.brakeLength_m.dataChanged.connect(self.data_edit)
        self.calageVar_m = CalageVarModel()
        self.calageVar_m.dataChanged.connect(self.data_edit)
        self.dxfLayerNames_m = DxfLayerNamesModel()
        self.dxfLayerNames_m.dataChanged.connect(self.data_edit)
        self.elLinesCorr_m = ElLinesCorrModel()
        self.elLinesCorr_m.dataChanged.connect(self.data_edit)
        self.elLinesDef_m = ElLinesDefModel()
        self.elLinesDef_m.dataChanged.connect(self.data_edit)
        self.extradosColConf_m = ExtradosColConfModel()
        self.extradosColConf_m.dataChanged.connect(self.data_edit)
        self.extradosColDet_m = ExtradosColDetModel()
        self.extradosColDet_m.dataChanged.connect(self.data_edit)
        self.globAoA_m = GlobalAoAModel()
        self.globAoA_m.dataChanged.connect(self.data_edit)
        self.glueVent_m = GlueVentModel()
        self.glueVent_m.dataChanged.connect(self.data_edit)
        self.hvvhRibs_m = HvVhRibsModel()
        self.hvvhRibs_m.dataChanged.connect(self.data_edit)
        self.intradosColConf_m = IntradosColsConfModel()
        self.intradosColConf_m.dataChanged.connect(self.data_edit)
        self.intradosColDet_m = IntradosColsDetModel()
        self.intradosColDet_m.dataChanged.connect(self.data_edit)
        self.joncsDef_m = JoncsDefModel()
        self.joncsDef_m.dataChanged.connect(self.data_edit)
        self.lightConf_m = LightConfModel()
        self.lightConf_m.dataChanged.connect(self.data_edit)
        self.lightDet_m = LightDetModel()
        self.lightDet_m.dataChanged.connect(self.data_edit)
        self.lines_m = LinesModel()
        self.lines_m.dataChanged.connect(self.data_edit)
        self.marks_m = MarksModel()
        self.marks_m.dataChanged.connect(self.data_edit)
        self.marksTypes_m = MarksTypesModel()
        self.marksTypes_m.dataChanged.connect(self.data_edit)
        self.newSkinTensConf_m = NewSkinTensConfModel()
        self.newSkinTensConf_m.dataChanged.connect(self.data_edit)
        self.newSkinTensDet_m = NewSkinTensDetModel()
        self.newSkinTensDet_m.dataChanged.connect(self.data_edit)
        self.noseMylars_m = NoseMylarsModel()
        self.noseMylars_m.dataChanged.connect(self.data_edit)
        self.partsSep_m = PartsSeparationModel()
        self.partsSep_m.dataChanged.connect(self.data_edit)
        self.ramif_m = RamificationModel()
        self.ramif_m.dataChanged.connect(self.data_edit)
        self.skinTens_m = SkinTensionModel()
        self.skinTens_m.dataChanged.connect(self.data_edit)
        self.skinTensParams_m = SkinTensionParamsModel()
        self.skinTensParams_m.dataChanged.connect(self.data_edit)
        self.sewingAllowances_m = SewingAllowancesModel()
        self.sewingAllowances_m.dataChanged.connect(self.data_edit)
        self.specWingTyp_m = SpecWingTipModel()
        self.specWingTyp_m.dataChanged.connect(self.data_edit)
        self.thrDDxf_m = ThreeDDxfModel()
        self.thrDDxf_m.dataChanged.connect(self.data_edit)
        self.thrDShConf_m = ThreeDShConfModel()
        self.thrDShConf_m.dataChanged.connect(self.data_edit)
        self.thrDShUpDet_m = ThreeDShUpDetModel()
        self.thrDShUpDet_m.dataChanged.connect(self.data_edit)
        self.thrDShLoDet_m = ThreeDShLoDetModel()
        self.thrDShLoDet_m.dataChanged.connect(self.data_edit)
        self.thrDShPrint_m = ThreeDShPrintModel()
        self.thrDShPrint_m.dataChanged.connect(self.data_edit)
        self.twoDDxf_m = TwoDDxfModel()
        self.twoDDxf_m.dataChanged.connect(self.data_edit)

        self.fileReader = ProcFileReader()
        self.fileWriter = ProcFileWriter()

    def set_file_name(self, file_name):
        """
        :method: Does set the file name the data store shall work with
        :param file_name: String containing full path and filename
        """
        self.__fileNamePath = file_name
        self.dataStatusUpdate.emit(self.__className, 'FileNamePath')

    def get_file_name(self):
        """
        :method: Returns the name of the file name member.
        """
        return self.__fileNamePath

    def set_file_version(self, file_version):
        """
        :method: Does set the file version the data store shall work with
        :param file_version: String containing the version number
        """
        self.__fileVersion = file_version
        self.dataStatusUpdate.emit(self.__className, 'FileVersion')

    def get_file_version(self):
        """
        :method: Returns the version info of the data file currently in use
        """
        return self.__fileVersion

    def data_edit(self):
        """
        :method: Called upon data edit activities within the proc model.
                 Does set the internal flags to track the data status
        """
        self.set_file_saved(False)

    def set_file_saved(self, file_saved_status: bool):
        """
        :method: Changes the internal flag to
                 File saved = True
                 Unsaved data = False
                 Emits a signal after every change.
        """
        self.__fileSaved = file_saved_status
        self.dataStatusUpdate.emit(self.__className, 'SaveStatus')

    def file_saved(self):
        """
        :method: Returns the current status of the proc file
        :retval: File saved = True
                 Unsaved data = False
        :rtype: bool
        """
        return self.__fileSaved

    def file_saved_char(self):
        """
        :method: Returns the current status of the proc file as character
        :retval: Y = File saved
                 N = Unsaved data
        :rtype: str
        """
        if self.__fileSaved is True:
            return 'Y'
        else:
            return 'N'

    def is_valid_pre_proc_file(self, file_name):
        """
        :method: Checks if a file can be opened and contains a valid title
                 and known version number
        :param file_name: the name of the file to be checked
        """
        try:
            in_file = QFile(file_name)
            if in_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(in_file)
        except:
            logging.error(self.__className
                          + 'File cannot be opened '
                          + file_name)
            return False

        title_ok = False
        version_ok = False
        line_counter = 0

        # noinspection PyUnboundLocalVariable
        while (stream.atEnd() is not True) \
                and not (title_ok and version_ok) \
                and line_counter < 10:

            line = stream.readLine()
            if line.find('1.6') >= 0:
                version_ok = True

            if line.find('Auxiliar geometry data') >= 0:
                title_ok = True
            line_counter += 1

        in_file.close()

        if not (version_ok and title_ok):
            logging.error(self.__className
                          + ' Result of Pre-Proc out file version check %s',
                          version_ok)
            logging.error(self.__className
                          + ' Result of Pre-Proc out file title check %s',
                          title_ok)

            msg_box = QMessageBox()
            msg_box.setWindowTitle(_('File read error'))
            msg_box.setText(
                _('File seems not to be a valid Pre-Proc output File! '
                  '\nVersion detected: ')
                + str(version_ok) + _('\nTitle detected: ')
                + str(title_ok))
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.Icon.Ok)
            msg_box.exec()

        return version_ok and title_ok

    def valid_file(self, file_name):
        """
        :method: Checks if a file can be opened and contains a valid title and
                 known version number
        :param file_name: the name of the file to be checked
        """
        in_file = QFile(file_name)
        if in_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(in_file)
        else:
            logging.error(self.__className +
                          'File cannot be opened ' +
                          file_name)
            return False

        title_ok = False
        version_ok = False
        line_counter = 0

        while (stream.atEnd() is not True) and \
                not (title_ok and version_ok) and \
                line_counter < 4:

            line = stream.readLine()
            if line.find('3.10') >= 0:
                self.set_file_version('3.10')
                version_ok = True
            elif line.find('3.15') >= 0:
                self.set_file_version('3.15')
                version_ok = True
            elif line.find('3.16') >= 0:
                self.set_file_version('3.16')
                version_ok = True
            elif line.find('3.17') >= 0:
                self.set_file_version('3.17')
                version_ok = True
            elif line.find('3.18') >= 0:
                self.set_file_version('3.18')
                version_ok = True
            elif line.find('3.19') >= 0:
                self.set_file_version('3.19')
                version_ok = True
            elif line.find('3.20') >= 0:
                self.set_file_version('3.20')
                version_ok = True

            if line.find('Input data file') >= 0:
                title_ok = True
            line_counter += 1

        in_file.close()

        if not (version_ok and title_ok):
            logging.error(self.__className
                          + ' Result of Proc file version check %s',
                          version_ok)
            logging.error(self.__className
                          + ' Result of Proc file title check %s',
                          title_ok)

            msg_box = QMessageBox()
            msg_box.setWindowTitle(_('File read error'))
            msg_box.setText(_('File seems not to be a valid Processor File!\n'
                              'Version detected: ')
                            + str(version_ok)
                            + _('\nTitle detected: ')
                            + str(title_ok))
            # TODO check if translation works if line is changed to correct length.
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.Icon.Ok)
            msg_box.exec()

            self.set_file_name('')
            self.set_file_version('')

        return version_ok and title_ok

    def import_pre_proc_file(self):
        """
        :method: Checks for un applied/ unsaved data, and appropriate handling.
                 Does the File Open dialog handling.
        """
        if not self.__fileSaved:
            # There is unsaved data, show a warning
            msg_box = QMessageBox()
            msg_box.setWindowTitle(_("Unsaved data"))
            msg_box.setText(_("You have unsaved data. \n\n"
                              "Press OK to open the new file and overwrite "
                              "the current changes.\nPress Cancel to abort. "))
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.Icon.Ok | QMessageBox.Icon.Cancel)
            answer = msg_box.exec()

            if answer == QMessageBox.StandardButton.Cancel:
                # User wants to abort
                return

        pre_proc_reader = PreProcOutfileReader()
        data, num_cells = pre_proc_reader.open_read_file(False)

        if len(data) > 0 and num_cells != 0:
            num_data_lines = len(data)
            self.wing_m.update_num_ribs(num_data_lines * 2)

            for line_it in range(0, num_data_lines):
                self.rib_m.updateRow(line_it + 1,
                                     data[line_it][1],
                                     data[line_it][2],
                                     data[line_it][3],
                                     data[line_it][4],
                                     data[line_it][5],
                                     data[line_it][6],
                                     data[line_it][7],
                                     data[line_it][8],
                                     0,
                                     0)
            self.set_file_name('')
            self.set_file_version('')
            self.set_file_saved(True)

    def open_file(self):
        """
        :method: Checks for un applied/ unsaved data, and appropriate handling.
                 Does the File Open dialog handling.
        """
        if not self.__fileSaved:
            # There is unsaved data, show a warning
            msg_box = QMessageBox()
            msg_box.setWindowTitle(_("Unsaved data"))
            msg_box.setText(_("You have unsaved data. \n\n"
                              "Press OK to open the new file and overwrite "
                              "the current changes.\nPress Cancel to abort. "))
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            answer = msg_box.exec()

            if answer == QMessageBox.StandardButton.Cancel:
                # User wants to abort
                return

        file_name = QFileDialog.getOpenFileName(
            None,
            _('Open Proc file'),
            "",
            "Pre Proc Files (*.txt);;All Files (*)")

        if file_name != ('', ''):
            # User has really selected a file, if it had aborted the
            # dialog an empty tuple is returned
            if self.valid_file(file_name[0]):
                self.set_file_name(file_name[0])

                self.fileReader.read_file(self.get_file_name(),
                                          self.get_file_version())
                self.set_file_saved(True)

    def save_file(self):
        """
        :method: Checks if there is already a valid file name, if not it
                 asks for it. Starts afterwards the writing process.
        """
        file_name = self.get_file_name()
        if len(file_name) > 0:
            # We do have already a valid filename
            self.set_file_version(self.__latestFileVersion)
            self.fileWriter.set_file_path_name(file_name)
            self.fileWriter.write_file()
            self.set_file_saved(True)
        else:
            # Ask first for the filename
            file_name = QFileDialog.getSaveFileName(
                None,
                _('Save Processor file'),
                "",
                "Geometry Files (*.txt);;All Files (*)")

            if file_name != ('', ''):
                # User has really selected a file, if it had
                # aborted the dialog an empty tuple is returned
                self.set_file_version(self.__latestFileVersion)
                self.set_file_name(file_name[0])
                self.fileWriter.set_file_path_name(file_name[0])
                self.fileWriter.write_file()
                self.set_file_saved(True)

    def save_file_as(self):
        """
        :method: Asks for a new filename. Starts afterwards the
                 writing process.
        """
        # Ask first for the filename
        file_name = QFileDialog.getSaveFileName(
            None,
            _('Save Processor file as'),
            "",
            "Geometry Files (*.txt);;All Files (*)")

        if file_name != ('', ''):
            # User has really selected a file, if it had
            # aborted the dialog an empty tuple is returned
            self.set_file_version(self.__latestFileVersion)
            self.set_file_name(file_name[0])
            self.fileWriter.set_file_path_name(file_name[0])
            self.fileWriter.write_file()
            self.set_file_saved(True)

    def write_for_proc_file(self):
        """
        :class: Writes the file directly to the proc directory
        """
        self.fileWriter.write_file(True)

from data.ProcFileReader import ProcFileReader  # noqa E402
from data.ProcFileWriter import ProcFileWriter  # noqa E402
