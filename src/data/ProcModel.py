"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0

Many thanks to the authors of:

https://doc.qt.io/qtforpython/overviews/sql-model.html

https://www.datacamp.com/community/tutorials/inner-classes-python
"""
import logging
import math

from PyQt5.QtCore import Qt, QFile, QTextStream, QObject, pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Singleton.Singleton import Singleton
from data.Database import Database
from data.PreProcOutfileReader import PreProcOutfileReader
from data.SqlTableModel import SqlTableModel


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
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')

        self.__fileSaved = True

        self.db = Database()
        self.db.openConnection()

        super().__init__()

        self.wing_m = ProcModel.WingModel()
        self.wing_m.dataChanged.connect(self.data_edit)
        self.rib_m = ProcModel.RibModel()
        self.rib_m.dataChanged.connect(self.data_edit)

        self.addRibPoints_m = ProcModel.AddRibPointsModel()
        self.addRibPoints_m.dataChanged.connect(self.data_edit)
        self.airf_m = ProcModel.AirfoilsModel()
        self.airf_m.dataChanged.connect(self.data_edit)
        self.airfThick_m = ProcModel.AirfoilThicknessModel()
        self.airfThick_m.dataChanged.connect(self.data_edit)
        self.anchPoints_m = ProcModel.AnchorPointsModel()
        self.anchPoints_m.dataChanged.connect(self.data_edit)
        self.brakes_m = ProcModel.BrakesModel()
        self.brakes_m.dataChanged.connect(self.data_edit)
        self.brakeLength_m = ProcModel.BrakeLengthModel()
        self.brakeLength_m.dataChanged.connect(self.data_edit)
        self.calageVar_m = ProcModel.CalageVarModel()
        self.calageVar_m.dataChanged.connect(self.data_edit)
        self.dxfLayerNames_m = ProcModel.DxfLayerNamesModel()
        self.dxfLayerNames_m.dataChanged.connect(self.data_edit)
        self.elLinesCorr_m = ProcModel.ElLinesCorrModel()
        self.elLinesCorr_m.dataChanged.connect(self.data_edit)
        self.elLinesDef_m = ProcModel.ElLinesDefModel()
        self.elLinesDef_m.dataChanged.connect(self.data_edit)
        self.extradosColConf_m = ProcModel.ExtradosColConfModel()
        self.extradosColConf_m.dataChanged.connect(self.data_edit)
        self.extradosColDet_m = ProcModel.ExtradosColDetModel()
        self.extradosColDet_m.dataChanged.connect(self.data_edit)
        self.globAoA_m = ProcModel.GlobAoAModel()
        self.globAoA_m.dataChanged.connect(self.data_edit)
        self.glueVent_m = ProcModel.GlueVentModel()
        self.glueVent_m.dataChanged.connect(self.data_edit)
        self.hvvhRibs_m = ProcModel.HvVhRibsModel()
        self.hvvhRibs_m.dataChanged.connect(self.data_edit)
        self.intradosColConf_m = ProcModel.IntradosColsConfModel()
        self.intradosColConf_m.dataChanged.connect(self.data_edit)
        self.intradosColDet_m = ProcModel.IntradosColsDetModel()
        self.intradosColDet_m.dataChanged.connect(self.data_edit)
        self.joncsDef_m = ProcModel.JoncsDefModel()
        self.joncsDef_m.dataChanged.connect(self.data_edit)
        self.ligthConf_m = ProcModel.LightConfModel()
        self.ligthConf_m.dataChanged.connect(self.data_edit)
        self.ligthDet_m = ProcModel.LightDetModel()
        self.ligthDet_m.dataChanged.connect(self.data_edit)
        self.lines_m = ProcModel.LinesModel()
        self.lines_m.dataChanged.connect(self.data_edit)
        self.marks_m = ProcModel.MarksModel()
        self.marks_m.dataChanged.connect(self.data_edit)
        self.marksTypes_m = ProcModel.MarksTypesModel()
        self.marksTypes_m.dataChanged.connect(self.data_edit)
        self.newSkinTensConf_m = ProcModel.NewSkinTensConfModel()
        self.newSkinTensConf_m.dataChanged.connect(self.data_edit)
        self.newSkinTensDet_m = ProcModel.NewSkinTensDetModel()
        self.newSkinTensDet_m.dataChanged.connect(self.data_edit)
        self.noseMylars_m = ProcModel.NoseMylarsModel()
        self.noseMylars_m.dataChanged.connect(self.data_edit)
        self.partsSep_m = ProcModel.PartsSeparationModel()
        self.partsSep_m.dataChanged.connect(self.data_edit)
        self.ramif_m = ProcModel.RamificationModel()
        self.ramif_m.dataChanged.connect(self.data_edit)
        self.skinTens_m = ProcModel.SkinTensionModel()
        self.skinTens_m.dataChanged.connect(self.data_edit)
        self.skinTensParams_m = ProcModel.SkinTensionParamsModel()
        self.skinTensParams_m.dataChanged.connect(self.data_edit)
        self.seewinAllowances_m = ProcModel.SewingAllowancesModel()
        self.seewinAllowances_m.dataChanged.connect(self.data_edit)
        self.specWingTyp_m = ProcModel.SpecWingTipModel()
        self.specWingTyp_m.dataChanged.connect(self.data_edit)
        self.thrDDxf_m = ProcModel.ThreeDDxfModel()
        self.thrDDxf_m.dataChanged.connect(self.data_edit)
        self.thrDShConf_m = ProcModel.ThreeDShConfModel()
        self.thrDShConf_m.dataChanged.connect(self.data_edit)
        self.thrDShUpDet_m = ProcModel.ThreeDShUpDetModel()
        self.thrDShUpDet_m.dataChanged.connect(self.data_edit)
        self.thrDShLoDet_m = ProcModel.ThreeDShLoDetModel()
        self.thrDShLoDet_m.dataChanged.connect(self.data_edit)
        self.thrDShPrint_m = ProcModel.ThreeDShPrintModel()
        self.thrDShPrint_m.dataChanged.connect(self.data_edit)
        self.twoDDxf_m = ProcModel.TwoDDxfModel()
        self.twoDDxf_m.dataChanged.connect(self.data_edit)

        self.fileReader = ProcFileReader()
        self.fileWriter = ProcFileWriter()

    def set_file_name(self, file_name):
        """
        :method: Does set the file name the data store shall work with.
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
                 and known version number.
        :param file_name: the name of the file to be checked
        """
        logging.debug(self.__className + '.is_valid_pre_proc_file')
        try:
            in_file = QFile(file_name)
            if in_file.open(QFile.ReadOnly | QFile.Text):
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
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

        return version_ok and title_ok

    def valid_file(self, file_name):
        """
        :method: Checks if a file can be opened and contains a valid title and
                 known version number.
        :param file_name: the name of the file to be checked
        """
        logging.debug(self.__className + '.valid_file')

        in_file = QFile(file_name)
        if in_file.open(QFile.ReadOnly | QFile.Text):
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
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

            self.set_file_name('')
            self.set_file_version('')

        return version_ok and title_ok

    def import_pre_proc_file(self):
        """
        :method: Checks for un applied/ unsaved data, and appropriate handling.
                 Does the File Open dialog handling.
        """
        logging.debug(self.__className + '.import_pre_proc_file')

        if not self.__fileSaved:
            # There is unsaved data, show a warning
            msg_box = QMessageBox()
            msg_box.setWindowTitle(_("Unsaved data"))
            msg_box.setText(_("You have unsaved data. \n\n"
                              "Press OK to open the new file and overwrite "
                              "the current changes.\nPress Cancel to abort. "))
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            answer = msg_box.exec()

            if answer == QMessageBox.Cancel:
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
        logging.debug(self.__className + '.open_read_file')

        if not self.__fileSaved:
            # There is unsaved data, show a warning
            msg_box = QMessageBox()
            msg_box.setWindowTitle(_("Unsaved data"))
            msg_box.setText(_("You have unsaved data. \n\n"
                              "Press OK to open the new file and overwrite "
                              "the current changes.\nPress Cancel to abort. "))
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            answer = msg_box.exec()

            if answer == QMessageBox.Cancel:
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
        logging.debug(self.__className + '.save_file')

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
        logging.debug(self.__className + '.save_file_as')

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

    class AddRibPointsModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding the parameters for the additional rib points.
        """
        __className = 'AddRibPointsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column used for ordering the individual lines of a config'''
        XCoordCol = 1
        ''':attr: Number of the col holding the X-Coordinate'''
        YCoordCol = 2
        ''':attr: Number of the col holding the Y-Coordinate'''
        ConfigNumCol = 3
        ''':attr: num of column for config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists AddRibPoints;")
            query.exec("create table if not exists AddRibPoints ("
                       "OrderNum INTEGER,"
                       "XCoord REAL,"
                       "YCoord REAL,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("AddRibPoints")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("X-Coordinate"))
            self.setHeaderData(2, Qt.Horizontal, _("Y-Coordinate"))

        def updateRow(self, configNum, orderNum, xCoord, yCoord):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE AddRibPoints SET "
                          "XCoord= :xCoord, "
                          "YCoord= :yCoord "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":xCoord", xCoord)
            query.bindValue(":yCoord", yCoord)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "XCoord, "
                          "YCoord "
                          "FROM AddRibPoints WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class AirfoilsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to the individual ribs. 
        '''
        __className = 'AirfoilsModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        RibNumCol = 0
        ''':attr: number of the rib number column'''
        AirfNameCol = 1
        ''':attr: number of the rib name column'''
        IntakeStartCol = 2
        ''':attr: number of the intake start column'''
        IntakeEndCol = 3
        ''':attr: number of the intake end column'''
        OpenCloseCol = 4
        ''':attr: number of the column for the open/ close config'''
        DisplacCol = 5
        ''':attr: number of the column for the displacement'''
        RelWeightCol = 6
        ''':attr: number of the column for the relative weight '''
        rrwCol = 7
        ''':attr: number of the column for the rrw config'''

        def createTable(self):
            '''
            :method: Creates initially the empty anchor points table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists Airfoils;")
            query.exec("create table if not exists Airfoils ("
                       "RibNum INTEGER,"
                       "AirfName TEXT,"
                       "IntakeStart REAL,"
                       "IntakeEnd REAL,"
                       "OpenClose INTEGER,"
                       "Displac REAL,"
                       "RelWeight REAL,"
                       "rrw REAL,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Airfoils")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Rib Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Name"))
            self.setHeaderData(2, Qt.Horizontal, _("Intake Start"))
            self.setHeaderData(3, Qt.Horizontal, _("Intake End"))
            self.setHeaderData(4, Qt.Horizontal, _("Open-close"))
            self.setHeaderData(5, Qt.Horizontal, _("Displac"))
            self.setHeaderData(6, Qt.Horizontal, _("Rel weight"))
            self.setHeaderData(7, Qt.Horizontal, _("rrw"))

        def getRow(self, ribNum):
            '''
            :method: reads values back from the internal database for a specific rib number
            :param ribNum: Rib number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "AirfName, "
                          "IntakeStart, "
                          "IntakeEnd, "
                          "OpenClose, "
                          "Displac, "
                          "RelWeight, "
                          "rrw "
                          "FROM Airfoils WHERE (RibNum = :rib)")
            query.bindValue(":rib", ribNum)
            query.exec()
            query.next()
            return query.value

    class AirfoilThicknessModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'AirfoilThicknessModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''

        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''

        OrderNumCol = 0
        ''':attr: num of column for ordering the individual lines of a config'''
        CoeffCol = 1
        ''':attr: Number of the col holding thickness parameter'''
        ConfigNumCol = 2
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("AirfoilThickness")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Rib num"))
            self.setHeaderData(1, Qt.Horizontal, _("Coef"))

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists AirfoilThickness;")
            query.exec("create table if not exists AirfoilThickness ("
                       "OrderNum INTEGER, "
                       "Coeff REAL, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, coeff):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE AirfoilThickness SET "
                          "Coeff= :coeff "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":coeff", coeff)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className + '.set_is_used')
            self.__isUsed = isUsed
            self.usageUpd.emit()

        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className + '.is_used')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Coeff "
                          "FROM AirfoilThickness WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class AnchorPointsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to the Anchor points. 
        '''
        __className = 'AnchorPointsModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        RibNumCol = 0
        ''':attr: Number of the rib number column'''
        NumAnchCol = 1
        ''':attr: Number of the column holding the number of anchors'''
        PosACol = 2
        ''':attr: Number the column holding Pos A'''
        PosBCol = 3
        ''':attr: Number the column holding Pos B'''
        PosCCol = 4
        ''':attr: Number the column holding Pos C'''
        PosDCol = 5
        ''':attr: Number the column holding Pos D'''
        PosECol = 6
        ''':attr: Number the column holding Pos E'''
        PosFCol = 7
        ''':attr: Number the column holding Pos F'''

        def createAnchorPointsTable(self):
            '''
            :method: Creates initially the empty anchor points table
            '''
            logging.debug(self.__className + '.createAnchorPointsTable')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists AnchorPoints;")
            query.exec("create table if not exists AnchorPoints ("
                       "RibNum INTEGER,"
                       "NumAnchors INTEGER,"
                       "PosA REAL,"
                       "PosB REAL,"
                       "PosC REAL,"
                       "PosD REAL,"
                       "PosE REAL,"
                       "PosF REAL,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createAnchorPointsTable()
            self.setTable("AnchorPoints")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Rib Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Num Anchors"))
            self.setHeaderData(2, Qt.Horizontal, _("Pos A"))
            self.setHeaderData(3, Qt.Horizontal, _("Pos B"))
            self.setHeaderData(4, Qt.Horizontal, _("Pos C"))
            self.setHeaderData(5, Qt.Horizontal, _("Pos D"))
            self.setHeaderData(6, Qt.Horizontal, _("Pos E"))
            self.setHeaderData(7, Qt.Horizontal, _("Pos F"))

        def getRow(self, ribNum):
            '''
            :method: reads values back from the internal database for a specific rib number
            :param ribNum: Rib number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "NumAnchors, "
                          "PosA, "
                          "PosB, "
                          "PosC, "
                          "PosD, "
                          "PosE, "
                          "PosF "
                          "FROM AnchorPoints WHERE (RibNum = :rib)")
            query.bindValue(":rib", ribNum)
            query.exec()
            query.next()
            return query.value

    class BrakesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the lines parameters. 
        '''
        __className = 'BrakesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        NumBranchesCol = 1
        ''':attr: Number of the col holding the number of branches'''
        BranchLvlOneCol = 2
        ''':attr: Number of the col holding the branching level 1 value'''
        OrderLvlOneCol = 3
        ''':attr: Number of the col holding order at level 1 value'''
        LevelOfRamTwoCol = 4
        ''':attr: Number of the col holding level of ramification 2 value'''
        OrderLvlTwoCol = 5
        ''':attr: Number of the col holding order at level 2 value'''
        LevelOfRamThreeCol = 6
        ''':attr: Number of the col holding level of ramification 3 value'''
        OrderLvlThreeCol = 7
        ''':attr: Number of the col holding order at level 3 value'''
        BranchLvlFourCol = 8
        ''':attr: Number of the col holding branching level 4 value'''
        OrderLvlFourCol = 9
        ''':attr: Number of the col holding order at level 4 value'''
        AnchorLineCol = 10
        ''':attr: Number of the col holding the  anchor line (1 = A, 2 = B, 3 = C, 4 = c 5 = D, 6 = brake) value'''
        AnchorRibNumCol = 11
        ''':attr: Number of the col holding the anchor rib number value'''
        ConfigNumCol = 12
        ''':attr: num of column for config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty Lines table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists Brakes;")
            query.exec("create table if not exists Brakes ("
                       "OrderNum INTEGER,"
                       "NumBranches INTEGER,"
                       "BranchLvlOne INTEGER,"
                       "OrderLvlOne INTEGER,"
                       "LevelOfRamTwo INTEGER,"
                       "OrderLvlTwo INTEGER,"
                       "LevelOfRamThree INTEGER,"
                       "OrderLvlThree INTEGER,"
                       "BranchLvlFour INTEGER,"
                       "OrderLvlFour INTEGER,"
                       "AnchorLine INTEGER,"
                       "AnchorRibNum INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into Brakes (OrderNum, ConfigNum, ID) Values( '1', '1', '1' );")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Brakes")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))
            self.setHeaderData(1, Qt.Horizontal, _("num Branches"))
            self.setHeaderData(2, Qt.Horizontal, _("Branch lvl 1"))
            self.setHeaderData(3, Qt.Horizontal, _("Order lvl 1"))
            self.setHeaderData(4, Qt.Horizontal, _("Ramif lvl2"))
            self.setHeaderData(5, Qt.Horizontal, _("Order lvl 2"))
            self.setHeaderData(6, Qt.Horizontal, _("Ramif lvl3"))
            self.setHeaderData(7, Qt.Horizontal, _("Order lvl 3"))
            self.setHeaderData(8, Qt.Horizontal, _("Branch lvl 4"))
            self.setHeaderData(9, Qt.Horizontal, _("Order lvl 4"))
            self.setHeaderData(10, Qt.Horizontal, _("Anchor"))
            self.setHeaderData(11, Qt.Horizontal, _("An. Rib num"))

        def updateRow(self, configNum, orderNum, i1, i2, i3, i4, i5, i6,
                      i7, i8, i9, i10, i11):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE Brakes SET "
                          "NumBranches= :i1, "
                          "BranchLvlOne= :i2, "
                          "OrderLvlOne= :i3, "
                          "LevelOfRamTwo= :i4, "
                          "OrderLvlTwo= :i5, "
                          "LevelOfRamThree= :i6, "
                          "OrderLvlThree= :i7, "
                          "BranchLvlFour= :i8, "
                          "OrderLvlFour= :i9, "
                          "AnchorLine= :i10, "
                          "AnchorRibNum= :i11 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":i1", i1)
            query.bindValue(":i2", i2)
            query.bindValue(":i3", i3)
            query.bindValue(":i4", i4)
            query.bindValue(":i5", i5)
            query.bindValue(":i6", i6)
            query.bindValue(":i7", i7)
            query.bindValue(":i8", i8)
            query.bindValue(":i9", i9)
            query.bindValue(":i10", i10)
            query.bindValue(":i11", i11)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "NumBranches, "
                          "BranchLvlOne, "
                          "OrderLvlOne, "
                          "LevelOfRamTwo, "
                          "OrderLvlTwo, "
                          "LevelOfRamThree, "
                          "OrderLvlThree, "
                          "BranchLvlFour, "
                          "OrderLvlFour, "
                          "AnchorLine, "
                          "AnchorRibNum "
                          "FROM Brakes WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class BrakeLengthModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Marks parameters. 
        '''
        __className = 'BrakeLengthModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        s1Col = 0
        ''':attr: Number of the col holding the s1 value'''
        s2Col = 1
        ''':attr: Number of the col holding the s2 value'''
        s3Col = 2
        ''':attr: Number of the col holding the s3 value'''
        s4Col = 3
        ''':attr: Number of the col holding the s4 value'''
        s5Col = 4
        ''':attr: Number of the col holding the s5 value'''
        d1Col = 5
        ''':attr: Number of the col holding the d1 value'''
        d2Col = 6
        ''':attr: Number of the col holding the d2 value'''
        d3Col = 7
        ''':attr: Number of the col holding the d3 value'''
        d4Col = 8
        ''':attr: Number of the col holding the d4 value'''
        d5Col = 9
        ''':attr: Number of the col holding the d5 value'''

        def createTable(self):
            '''
            :method: Creates initially the empty Brake length table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists BrakeLenght;")
            query.exec("create table if not exists BrakeLenght ("
                       "s1 INTEGER,"
                       "s2 INTEGER,"
                       "s3 INTEGER,"
                       "s4 INTEGER,"
                       "s5 INTEGER,"
                       "d1 INTEGER,"
                       "d2 INTEGER,"
                       "d3 INTEGER,"
                       "d4 INTEGER,"
                       "d5 INTEGER,"
                       "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into BrakeLenght (ID) Values( '1' );")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("BrakeLenght")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("s1 [\u0025]"))
            self.setHeaderData(1, Qt.Horizontal, _("s2 [\u0025]"))
            self.setHeaderData(2, Qt.Horizontal, _("s3 [\u0025]"))
            self.setHeaderData(3, Qt.Horizontal, _("s4 [\u0025]"))
            self.setHeaderData(4, Qt.Horizontal, _("s5 [\u0025]"))
            self.setHeaderData(5, Qt.Horizontal, _("d1 [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("d2 [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("d3 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("d4 [cm]"))
            self.setHeaderData(9, Qt.Horizontal, _("d5 [cm]"))

        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "s1, "
                          "s2, "
                          "s3, "
                          "s4, "
                          "s5, "
                          "d1, "
                          "d2, "
                          "d3, "
                          "d4, "
                          "d5 "
                          "FROM BrakeLenght")
            query.exec()
            query.next()

            return query.value

    class CalageVarModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
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
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("CalageVar")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.set_num_rows_for_config(1, 1)

            self.setHeaderData(1, Qt.Horizontal, _("Num risers"))
            self.setHeaderData(2, Qt.Horizontal, _("Pos r A"))
            self.setHeaderData(3, Qt.Horizontal, _("Pos r B"))
            self.setHeaderData(4, Qt.Horizontal, _("Pos r C"))
            self.setHeaderData(5, Qt.Horizontal, _("Pos r D"))
            self.setHeaderData(6, Qt.Horizontal, _("Pos r E"))
            self.setHeaderData(7, Qt.Horizontal, _("Pos r F"))
            self.setHeaderData(8, Qt.Horizontal, _("Max neg ang [deg]"))
            self.setHeaderData(9, Qt.Horizontal, _("Num neg steps"))
            self.setHeaderData(10, Qt.Horizontal, _("Max pos ang [deg]"))
            self.setHeaderData(11, Qt.Horizontal, _("Num pos steps"))

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
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

        def updateRow(self, configNum, orderNum, numRisers, posA, posB, posC, posD, posE, posF, maxNegAng, numNegSteps,
                      maxPosAng, numPosSteps):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

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
            query.bindValue(":numRisers", numRisers)
            query.bindValue(":posA", posA)
            query.bindValue(":posB", posB)
            query.bindValue(":posC", posC)
            query.bindValue(":posD", posD)
            query.bindValue(":posE", posE)
            query.bindValue(":posF", posF)
            query.bindValue(":maxNegAng", maxNegAng)
            query.bindValue(":numNegSteps", numNegSteps)
            query.bindValue(":maxPosAng", maxPosAng)
            query.bindValue(":numPosSteps", numPosSteps)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise 
            '''
            logging.debug(self.__className + '.set_is_used')
            self.__isUsed = isUsed
            self.usageUpd.emit()

        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise 
            '''
            logging.debug(self.__className + '.is_used')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

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

    class DxfLayerNamesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'DxfLayerNamesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for ordering the individual lines of a config'''
        LayerCol = 1
        ''':attr: Number of the col holding the lepg name of a layer'''
        DescriptionCol = 2
        ''':attr: Number of the col holding the user defined name of a layer'''
        ConfigNumCol = 3
        ''':attr: num of column for config number (always 1)'''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists DxfLayerNames;")
            query.exec("create table if not exists DxfLayerNames ("
                       "OrderNum INTEGER,"
                       "Layer text,"
                       "Description text,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("DxfLayerNames")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Layer name"))
            self.setHeaderData(2, Qt.Horizontal, _("Description"))

        def updateRow(self, configNum, orderNum, layer, desc):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE DxfLayerNames SET "
                          "Layer= :layer, "
                          "Description= :desc "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":layer", layer)
            query.bindValue(":desc", desc)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Layer, "
                          "Description "
                          "FROM DxfLayerNames WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class ElLinesCorrModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the parameters for the elastic lines correction. 
        '''
        __className = 'ElLinesCorrModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        LoadCol = 0
        ''':attr: Num of column for flight load'''
        TwoLineDistACol = 1
        ''':attr: Num of column for 1st two line load dist'''
        TwoLineDistBCol = 2
        ''':attr: Num of column for 2nd two line load dist'''
        ThreeLineDistACol = 3
        ''':attr: Num of column for 1st tree line load dist'''
        ThreeLineDistBCol = 4
        ''':attr: Num of column for 2nd tree line load dist'''
        ThreeLineDistCCol = 5
        ''':attr: Num of column for 3rd tree line load dist'''
        FourLineDistACol = 6
        ''':attr: Num of column for 1st four line load distr'''
        FourLineDistBCol = 7
        ''':attr: Num of column for 2nd four line load distr'''
        FourLineDistCCol = 8
        ''':attr: Num of column for 3rd four line load distr'''
        FourLineDistDCol = 9
        ''':attr: Num of column for 4th four line load distr'''
        FiveLineDistACol = 10
        ''':attr: Num of column for 1st five line load distr'''
        FiveLineDistBCol = 11
        ''':attr: Num of column for 2nd five line load distr'''
        FiveLineDistCCol = 12
        ''':attr: Num of column for 3rd five line load distr'''
        FiveLineDistDCol = 13
        ''':attr: Num of column for 4th five line load distr'''
        FiveLineDistECol = 14
        ''':attr: Num of column for 5th five line load distr'''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ElaslticLinesCorr;")
            query.exec("create table if not exists ElaslticLinesCorr ("
                       "Load REAL,"
                       "TwoLineDistA REAL, "
                       "TwoLineDistB REAL, "
                       "ThreeLineDistA REAL, "
                       "ThreeLineDistB REAL, "
                       "ThreeLineDistC REAL, "
                       "FourLineDistA REAL, "
                       "FourLineDistB REAL, "
                       "FourLineDistC REAL, "
                       "FourLineDistD REAL, "
                       "FiveLineDistA REAL, "
                       "FiveLineDistB REAL, "
                       "FiveLineDistC REAL, "
                       "FiveLineDistD REAL, "
                       "FiveLineDistE REAL, "
                       "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into ElaslticLinesCorr (ID) Values( '1' );")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ElaslticLinesCorr")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Load, "
                          "TwoLineDistA, "
                          "TwoLineDistB, "
                          "ThreeLineDistA, "
                          "ThreeLineDistB, "
                          "ThreeLineDistC, "
                          "FourLineDistA, "
                          "FourLineDistB, "
                          "FourLineDistC, "
                          "FourLineDistD, "
                          "FiveLineDistA, "
                          "FiveLineDistB, "
                          "FiveLineDistC, "
                          "FiveLineDistD, "
                          "FiveLineDistE "
                          "FROM ElaslticLinesCorr")
            query.exec()
            query.next()
            return query.value

    class ElLinesDefModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Elastic lines deformation parameters. (2nd part of elastic lines correction)
        '''
        __className = 'ElLinesDefModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: used here for the number of lines'''
        DefLowCol = 1
        ''':attr: Number of the col holding the deformation in the lower level'''
        DefMidCol = 2
        ''':attr: Number of the col holding the deformation in the medium level'''
        DefHighCol = 3
        ''':attr: Number of the col holding the deformation in the higher level'''
        ConfigNumCol = 4
        ''':attr: num of column for config number (always 1)'''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ElaslticLinesDef;")
            query.exec("create table if not exists ElaslticLinesDef ("
                       "OrderNum INTEGER,"
                       "DefLow REAL,"
                       "DefMid REAL,"
                       "DefHigh REAL,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ElaslticLinesDef")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Num lines per rib"))
            self.setHeaderData(1, Qt.Horizontal, _("Def in lower level"))
            self.setHeaderData(2, Qt.Horizontal, _("Def in mid level"))
            self.setHeaderData(3, Qt.Horizontal, _("Def in higher level"))

            self.set_num_rows_for_config(1, 5)

        def updateRow(self, configNum, orderNum, defLow, defMid, defHigh):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE ElaslticLinesDef SET "
                          "DefLow= :defLow, "
                          "DefMid= :defMid, "
                          "DefHigh= :defHigh "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":defLow", defLow)
            query.bindValue(":defMid", defMid)
            query.bindValue(":defHigh", defHigh)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "OrderNum, "
                          "DefLow, "
                          "DefMid, "
                          "DefHigh "
                          "FROM ElaslticLinesDef WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class ExtradosColConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the Extrados colors configuration 
        '''
        __className = 'ExtradosColConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table.
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ExtradColsConf;")
            query.exec("create table if not exists ExtradColsConf ("
                       "OrderNum INTEGER,"
                       "FirstRib INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ExtradColsConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(self.FirstRibCol, Qt.Horizontal, _("Rib num"))

        def updateRow(self, configNum, firstRib):
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE ExtradColsConf SET FirstRib= :firstRib WHERE (ConfigNum = :config);")
            query.bindValue(":firstRib", firstRib)
            query.bindValue(":config", configNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param order_num: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "FirstRib "
                          "FROM ExtradColsConf WHERE (ConfigNum = :config)")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            return query.value

    class ExtradosColDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all detail data related to the Extrados colors 
        '''
        __className = 'ExtradosColDetModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        DistTeCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table.
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ExtradColsDet;")
            query.exec("create table if not exists ExtradColsDet ("
                       "OrderNum INTEGER,"
                       "DistTe INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ExtradColsDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Dist TE"))

        def updateRow(self, configNum, orderNum, distTe):
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare(
                "UPDATE ExtradColsDet SET DistTe= :distTe WHERE (ConfigNum = :config  AND OrderNum = :order);")
            query.bindValue(":distTe", distTe)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "DistTe "
                          "FROM ExtradColsDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class GlobAoAModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the global AoA parameters. 
        '''
        __className = 'GlobAoAModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        FinesseCol = 0
        ''':attr: Number of the col holding the finesse value'''
        CentOfPressCol = 1
        ''':attr: Number of the col holding the center of pressure value'''
        CalageCol = 2
        ''':attr: Number of the col holding the calage value'''
        RisersCol = 3
        ''':attr: Number of the col holding the risers length value'''
        LinesCol = 4
        ''':attr: Number of the col holding the lines length value'''
        KarabinersCol = 5
        ''':attr: Number of the col holding the karabiners length value'''

        def createTable(self):
            '''
            :method: Creates initially the empty GlobalAoA table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists GlobalAoA;")
            query.exec("create table if not exists GlobalAoA ("
                       "Finesse REAL,"
                       "CentOfPress INTEGER,"
                       "Calage INTEGER,"
                       "Risers INTEGER,"
                       "Lines INTEGER,"
                       "Karabiners INTEGER,"
                       "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into GlobalAoA (ID) Values( '1' );")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("GlobalAoA")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Finesse [deg]"))
            self.setHeaderData(1, Qt.Horizontal, _("Center of Pressure"))
            self.setHeaderData(2, Qt.Horizontal, _("Calage"))
            self.setHeaderData(3, Qt.Horizontal, _("Risers [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("Lines [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("Karabiners [cm]"))

        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Finesse, "
                          "CentOfPress, "
                          "Calage, "
                          "Risers, "
                          "Lines, "
                          "Karabiners "
                          "FROM GlobalAoA")
            query.exec()
            query.next()
            return query.value

    class GlueVentModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding the glue vent parameters.
        """
        __className = 'GlueVentModel'
        '''
        :attr: Does help to indicate the source of the log messages.
        '''
        __isUsed = False
        '''
        :attr: Helps to remember if the section is in use or not
        '''

        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''

        OrderNumCol = 0
        '''
        :attr: Num of column for ordering the individual lines of a config
        '''
        VentParamCol = 1
        '''
        :attr: Number of the col holding the vent parameter
        '''
        ParamACol = 2
        '''
        :attr: Number of the col holding the additional parameter A (1)
        '''
        ParamBCol = 3
        '''
        :attr: Number of the col holding the additional parameter B (2)
        '''
        ParamCCol = 4
        '''
        :attr: Number of the col holding the additional parameter C (3)
        '''
        ConfigNumCol = 5
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None):
            """
            :method: Constructor
            """
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.create_table()
            self.setTable("GlueVent")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(self.OrderNumCol,
                               Qt.Horizontal,
                               _("Airfoil num"))
            self.setHeaderData(self.VentParamCol,
                               Qt.Horizontal,
                               _("Vent param"))
            self.setHeaderData(self.ParamACol,
                               Qt.Horizontal,
                               _("Opt param 1"))
            self.setHeaderData(self.ParamCCol,
                               Qt.Horizontal,
                               _("Opt param 2"))
            self.setHeaderData(self.ParamBCol,
                               Qt.Horizontal,
                               _("Opt param 3"))

        def create_table(self):
            """
            :method: Creates initially the empty table
            """
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists GlueVent;")
            query.exec("create table if not exists GlueVent ("
                       "OrderNum INTEGER, "
                       "VentParam REAL, "
                       "ParamA INTEGER, "
                       "ParamB INTEGER, "
                       "ParamC INTEGER, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def update_row(self, config_num, order_num,
                       vent_param, param_a, param_b, param_c):
            """
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitly explained here
                     as they should be well known.
            """
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE GlueVent SET "
                          "VentParam= :vent_param, "
                          "ParamA= :param_a, "
                          "ParamB= :param_b, "
                          "ParamC= :param_c "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.bindValue(":vent_param", vent_param)
            query.bindValue(":param_a", param_a)
            query.bindValue(":param_b", param_b)
            query.bindValue(":param_c", param_c)
            query.exec()
            self.select()  # assure the model is updated properly

        def set_is_used(self, is_used):
            """
            :method: Set the usage flag of the section
            :param is_used: True if section is in use, False otherwise
            """
            logging.debug(self.__className + '.set_is_used')
            self.__isUsed = is_used
            self.usageUpd.emit()

        def is_used(self):
            """
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise
            """
            logging.debug(self.__className + '.is_used')
            return self.__isUsed

        def get_row(self, config_num, order_num):
            """
            :method: Reads values back from the internal database for a
                     specific config and order number
            :param config_num: Configuration number. Starting with 1.
            :param order_num: Order number. Starting with 1.

            :return: Values read from internal database
            :rtype: QRecord
            """
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "OrderNum, "
                          "VentParam, "
                          "ParamA, "
                          "ParamB, "
                          "ParamC "
                          "FROM GlueVent WHERE (ConfigNum = :config) "
                          "ORDER BY OrderNum")
            query.bindValue(":config", config_num)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < order_num:
                query.next()
                i += 1
            return query.record()

    class HvVhRibsModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding the lines parameters.
        """
        __className = 'HvVhRibsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        TypeCol = 1
        ''':attr: Number of the col holding the rib type info'''
        IniRibCol = 2
        ''':attr: Number of the col holding initial rib of the configuration'''
        ParamACol = 3
        ''':attr: Number of the col holding param A'''
        ParamBCol = 4
        ''':attr: Number of the col holding param B'''
        ParamCCol = 5
        ''':attr: Number of the col holding param C'''
        ParamDCol = 6
        ''':attr: Number of the col holding param D'''
        ParamECol = 7
        ''':attr: Number of the col holding param E'''
        ParamFCol = 8
        ''':attr: Number of the col holding param F'''
        ParamGCol = 9
        ''':attr: Number of the col holding param G'''
        ParamHCol = 10
        ''':attr: Number of the col holding param H'''
        ParamICol = 11
        ''':attr: Number of the col holding param I'''
        ConfigNumCol = 12
        ''':attr: num of column for config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty Lines table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists HvVhRibs;")
            query.exec("create table if not exists HvVhRibs ("
                       "OrderNum INTEGER,"
                       "Type INTEGER,"
                       "IniRib INTEGER,"
                       "ParamA INTEGER,"
                       "ParamB INTEGER,"
                       "ParamC INTEGER,"
                       "ParamD REAL,"
                       "ParamE REAL,"
                       "ParamF REAL,"
                       "ParamG REAL,"
                       "ParamH REAL,"
                       "ParamI REAL,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("HvVhRibs")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(self.OrderNumCol, Qt.Horizontal, _("Order num"))
            self.setHeaderData(self.TypeCol, Qt.Horizontal, _("Type"))
            self.setHeaderData(self.IniRibCol, Qt.Horizontal, _("Ini Rib"))
            self.setHeaderData(self.ParamACol, Qt.Horizontal, _("Param A"))
            self.setHeaderData(self.ParamBCol, Qt.Horizontal, _("Param B"))
            self.setHeaderData(self.ParamCCol, Qt.Horizontal, _("Param C"))
            self.setHeaderData(self.ParamDCol, Qt.Horizontal, _("Param D"))
            self.setHeaderData(self.ParamECol, Qt.Horizontal, _("Param E"))
            self.setHeaderData(self.ParamFCol, Qt.Horizontal, _("Param F"))
            self.setHeaderData(self.ParamGCol, Qt.Horizontal, _("Param G"))
            self.setHeaderData(self.ParamHCol, Qt.Horizontal, _("Param H"))
            self.setHeaderData(self.ParamICol, Qt.Horizontal, _("Param I"))

        def updateDataRow(self, configNum, orderNum, typ, iniRib, paramA, paramB, paramC, paramD, paramE, paramF,
                          paramG, paramH=0, paramI=0):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.updateLineRow')

            query = QSqlQuery()
            query.prepare("UPDATE HvVhRibs SET "
                          "Type= :typ, "
                          "IniRib= :iniRib, "
                          "ParamA= :paramA, "
                          "ParamB= :paramB, "
                          "ParamC= :paramC, "
                          "ParamD= :paramD, "
                          "ParamE= :paramE, "
                          "ParamF= :paramF, "
                          "ParamG= :paramG, "
                          "ParamH= :paramH, "
                          "ParamI= :paramI "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typ", typ)
            query.bindValue(":iniRib", iniRib)
            query.bindValue(":paramA", paramA)
            query.bindValue(":paramB", paramB)
            query.bindValue(":paramC", paramC)
            query.bindValue(":paramD", paramD)
            query.bindValue(":paramE", paramE)
            query.bindValue(":paramF", paramF)
            query.bindValue(":paramG", paramG)
            query.bindValue(":paramH", paramH)
            query.bindValue(":paramI", paramI)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Type, "
                          "IniRib, "
                          "ParamA, "
                          "ParamB, "
                          "ParamC, "
                          "ParamD, "
                          "ParamE, "
                          "ParamF, "
                          "ParamG, "
                          "ParamH, "
                          "ParamI "
                          "FROM HvVhRibs WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class IntradosColsConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the Intrados colors configuration 
        '''
        __className = 'IntradosColsConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table.
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists IntradColsConf;")
            query.exec("create table if not exists IntradColsConf ("
                       "OrderNum INTEGER,"
                       "FirstRib INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("IntradColsConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(self.FirstRibCol, Qt.Horizontal, _("Rib num"))

        def updateRow(self, configNum, firstRib):
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE IntradColsConf SET FirstRib= :firstRib WHERE (ConfigNum = :config);")
            query.bindValue(":firstRib", firstRib)
            query.bindValue(":config", configNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param order_num: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "FirstRib "
                          "FROM IntradColsConf WHERE (ConfigNum = :config)")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            return query.value

    class IntradosColsDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all detail data related to the Intrados colors 
        '''
        __className = 'IntradosColsDetModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        DistTeCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        ConfigNumCol = 2
        ''':attr: number of the column holding the config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table.
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists IntradColsDet;")
            query.exec("create table if not exists IntradColsDet ("
                       "OrderNum INTEGER,"
                       "DistTe INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("IntradColsDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Dist TE"))

        def updateRow(self, configNum, orderNum, distTe):
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare(
                "UPDATE IntradColsDet SET DistTe= :distTe WHERE (ConfigNum = :config  AND OrderNum = :order);")
            query.bindValue(":distTe", distTe)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "DistTe "
                          "FROM IntradColsDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class JoncsDefModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Joncs definition data
        '''
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

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists JoncsDef;")
            query.exec("create table if not exists JoncsDef ("
                       "OrderNum INTEGER, "
                       "FirstRib INTEGER, "
                       "LastRib INTEGER, "
                       "pBA REAL, "
                       "pBB REAL, "
                       "pBC REAL, "
                       "PBD REAL, "
                       "pBE REAL, "
                       "pCA REAL, "
                       "pCB REAL, "
                       "pCC REAL, "
                       "PCD REAL, "
                       "pDA REAL, "
                       "pDB REAL, "
                       "pDC REAL, "
                       "PDD REAL, "
                       "Type INTEGER, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("JoncsDef")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))
            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
            self.setHeaderData(3, Qt.Horizontal, _("Row 2 A"))
            self.setHeaderData(4, Qt.Horizontal, _("Row 2 B"))
            self.setHeaderData(5, Qt.Horizontal, _("Row 2 C"))
            self.setHeaderData(6, Qt.Horizontal, _("Row 2 D"))
            self.setHeaderData(7, Qt.Horizontal, _("Row 2 E"))
            self.setHeaderData(8, Qt.Horizontal, _("Row 3 A"))
            self.setHeaderData(9, Qt.Horizontal, _("Row 3 B"))
            self.setHeaderData(10, Qt.Horizontal, _("Row 3 C"))
            self.setHeaderData(11, Qt.Horizontal, _("Row 3 D"))
            self.setHeaderData(12, Qt.Horizontal, _("Row 4 A"))
            self.setHeaderData(13, Qt.Horizontal, _("Row 4 B"))
            self.setHeaderData(14, Qt.Horizontal, _("Row 4 C"))
            self.setHeaderData(15, Qt.Horizontal, _("Row 4 D"))

        def updateTypeOneRow(self, configNum, orderNum, firstRib, lastRib, pBA, pBB, pBC, pBD, pCA, pCB, pCC, pCD, pDA,
                             pDB, pDC, pDD):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.updateTypeOneRow')

            query = QSqlQuery()
            query.prepare("UPDATE JoncsDef SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib, "
                          "pBA= :pBA, "
                          "pBB= :pBB, "
                          "pBC= :pBC, "
                          "pBD= :pBD, "
                          "pCA= :pCA, "
                          "pCB= :pCB, "
                          "pCC= :pCC, "
                          "pCD= :pCD, "
                          "pDA= :pDA, "
                          "pDB= :pDB, "
                          "pDC= :pDC, "
                          "pDD= :pDD, "
                          "Type= :t "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib)
            query.bindValue(":lastRib", lastRib)
            query.bindValue(":pBA", pBA)
            query.bindValue(":pBB", pBB)
            query.bindValue(":pBC", pBC)
            query.bindValue(":pBD", pBD)
            query.bindValue(":pCA", pCA)
            query.bindValue(":pCB", pCB)
            query.bindValue(":pCC", pCC)
            query.bindValue(":pCD", pCD)
            query.bindValue(":pDA", pDA)
            query.bindValue(":pDB", pDB)
            query.bindValue(":pDC", pDC)
            query.bindValue(":pDD", pDD)
            query.bindValue(":t", 1)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def updateTypeTwoRow(self, configNum, orderNum, firstRib, lastRib, pBA, pBB, pBC, pBD, pBE, pDA, pDB, pDC, pDD):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.updateTypeTwoRow')

            query = QSqlQuery()
            query.prepare("UPDATE JoncsDef SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib, "
                          "pBA= :pBA, "
                          "pBB= :pBB, "
                          "pBC= :pBC, "
                          "pBD= :pBD, "
                          "pBE= :pBE, "
                          "pDA= :pDA, "
                          "pDB= :pDB, "
                          "pDC= :pDC, "
                          "pDD= :pDD, "
                          "Type= 2 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib)
            query.bindValue(":lastRib", lastRib)
            query.bindValue(":pBA", pBA)
            query.bindValue(":pBB", pBB)
            query.bindValue(":pBC", pBC)
            query.bindValue(":pBD", pBD)
            query.bindValue(":pBE", pBE)
            query.bindValue(":pDA", pDA)
            query.bindValue(":pDB", pDB)
            query.bindValue(":pDC", pDC)
            query.bindValue(":pDD", pDD)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def setType(self, configNum, typeNum):
            '''
            :method: Sets for all rows of a specific config the type num 
            :param typeNum: 1: type== 1; 2: type== 2
            '''
            logging.debug(self.__className + '.setType')

            query = QSqlQuery()
            query.prepare("UPDATE JoncsDef SET "
                          "type= :type_num "
                          "WHERE (ConfigNum = :config);")
            query.bindValue(":type_num", typeNum)
            query.bindValue(":config", configNum)
            query.exec()

        def getType(self, configNum):
            '''
            :method: Detects for a defined config if the type is set. 
            :return: 0: type is empty; 1: type== 1; 2: type== 2
            '''
            logging.debug(self.__className + '.get_type')

            query = QSqlQuery()
            query.prepare("Select Type FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum ASC;")
            query.bindValue(":config", configNum)
            query.exec()
            typeNum = 0
            if query.next():
                typeNum = query.value(0)
                if typeNum == "":
                    typeNum = 0

            return typeNum

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "OrderNum, "
                          "FirstRib, "
                          "LastRib, "
                          "pBA, "
                          "pBB, "
                          "pBC, "
                          "PBD, "
                          "pBE, "
                          "pCA, "
                          "pCB, "
                          "pCC, "
                          "PCD, "
                          "pDA, "
                          "pDB, "
                          "pDC, "
                          "PDD, "
                          "Type "
                          "FROM JoncsDef WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class LightConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the global lightening config parameters 
        '''

        __className = 'LightConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        __numConfigs = 0

        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        InitialRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        FinalRibCol = 2
        ''':attr: number of the column holding the final rib'''
        ConfigNumCol = 3
        ''':attr: number of the column holding the config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty LightConf table.
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists LightConf;")
            query.exec("create table if not exists LightConf ("
                       "OrderNum INTEGER,"
                       "InitialRib INTEGER,"
                       "FinalRib INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("LightConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Initial Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Final Rib"))

        def updateRow(self, config, initialRib, finalRib):
            logging.debug(self.__className + '.setConfigRow')

            query = QSqlQuery()
            query.prepare("UPDATE LightConf SET InitialRib= :initial , FinalRib= :final WHERE (ConfigNum = :config);")
            query.bindValue(":initial", initialRib)
            query.bindValue(":final", finalRib)
            query.bindValue(":config", config)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config number
            :param configNum: Configuration number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "InitialRib, "
                          "FinalRib "
                          "FROM LightConf WHERE (ConfigNum = :config)")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            return query.value

    class LightDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to the indivudual lightening config parameters.
        '''
        # numDetailsChanged = pyqtSignal(int, int)
        '''
        :Signal: Emitted at the moment the number of data lines in the model is changed. \
        Param 1: the configuration number which has changed \
        Param2: new number of data lines
        '''

        __className = 'LightDetModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a confit'''
        LightTypCol = 1
        ''':attr: num of column for 1..3: hole type info'''
        DistLECol = 2
        ''':attr: num of column for 1..3: distance from LE to hole center in % chord '''
        DisChordCol = 3
        ''':attr: num of column for 1..3: distance from the center of hole to the chord line in % of chord'''
        HorAxisCol = 4
        ''':attr: num of column for 1..2: horizontal axis of the ellipse as % of chord; 3: traingle base as % of chord'''
        VertAxisCol = 5
        ''':attr: num of column for 1..2: ellipse vertical axis as % of chord; 3: triangle heigth as % of chord'''
        RotAngleCol = 6
        ''':attr: num of column 1..3:  for rotation angle of the ellipse'''
        Opt1Col = 7
        ''':attr: num of column 1: na; 2:  central strip width; 3: Radius of the smoothed corners'''
        ConfigNumCol = 8
        ''':attr: num of column for 1..3: config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty lightening details table.
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists LightDet;")
            query.exec("create table if not exists LightDet ("
                       "OrderNum INTEGER,"
                       "LightTyp INTEGER,"
                       "DistLE REAL,"
                       "DisChord REAL,"
                       "HorAxis REAL,"
                       "VertAxis REAL,"
                       "RotAngle REAL,"
                       "Opt1 REAL,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")
            query.exec("INSERT into LightDet (ConfigNum, OrderNum) Values( '1', '1' );")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("LightDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order Num"))
            self.setHeaderData(1, Qt.Horizontal, _("Light Typ"))
            self.setHeaderData(2, Qt.Horizontal, _("Dist LE"))
            self.setHeaderData(3, Qt.Horizontal, _("Dist chord"))
            self.setHeaderData(4, Qt.Horizontal, _("Hor axis"))
            self.setHeaderData(5, Qt.Horizontal, _("Vert axis"))
            self.setHeaderData(6, Qt.Horizontal, _("Rot angle"))
            self.setHeaderData(7, Qt.Horizontal, _("Opt "))

        def updateRow(self, configNum, orderNum, LightTyp, DistLE, DisChord, HorAxis, VertAxis, RotAngle, Opt1):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            # query.prepare("UPDATE LightDet SET LightTyp= :light, DistLE= :dist, DisChord= :dis, HorAxis= :hor, VertAxis= :vert, RotAngle: rot, Opt= :opt WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.prepare("UPDATE LightDet SET LightTyp= :light, "
                          "DistLE= :dist, DisChord= :dis, HorAxis= :hor, "
                          "VertAxis= :vert, RotAngle= :rot, Opt1= :opt1 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":light", LightTyp)
            query.bindValue(":dist", DistLE)
            query.bindValue(":dis", DisChord)
            query.bindValue(":hor", HorAxis)
            query.bindValue(":vert", VertAxis)
            query.bindValue(":rot", RotAngle)
            query.bindValue(":opt1", Opt1)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "LightTyp, "
                          "DistLE, "
                          "DisChord, "
                          "HorAxis, "
                          "VertAxis, "
                          "RotAngle, "
                          "Opt1 "
                          "FROM LightDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class LinesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the lines parameters.
        '''
        __className = 'LinesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        '''
        :attr: num of column for 1..3: ordering the individual lines
               of a config
        '''
        NumBranchesCol = 1
        ''':attr: Number of the col holding the number of branches'''
        BranchLvlOneCol = 2
        ''':attr: Number of the col holding the branching level 1 value'''
        OrderLvlOneCol = 3
        ''':attr: Number of the col holding order at level 1 value'''
        LevelOfRamTwoCol = 4
        ''':attr: Number of the col holding level of ramification 2 value'''
        OrderLvlTwoCol = 5
        ''':attr: Number of the col holding order at level 2 value'''
        LevelOfRamThreeCol = 6
        ''':attr: Number of the col holding level of ramification 3 value'''
        OrderLvlThreeCol = 7
        ''':attr: Number of the col holding order at level 3 value'''
        BranchLvlFourCol = 8
        ''':attr: Number of the col holding branching level 4 value'''
        OrderLvlFourCol = 9
        ''':attr: Number of the col holding order at level 4 value'''
        AnchorLineCol = 10
        '''
        :attr: Number of the col holding the  anchor line (
               1 = A, 2 = B, 3 = C, 4 = D, 5 = E, 6 = brake) value
        '''

        AnchorRibNumCol = 11
        ''':attr: Number of the col holding the anchor rib number value'''
        ConfigNumCol = 12
        ''':attr: num of column for config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty Lines table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists Lines;")
            query.exec("create table if not exists Lines ("
                       "OrderNum INTEGER,"
                       "NumBranches INTEGER,"
                       "BranchLvlOne INTEGER,"
                       "OrderLvlOne INTEGER,"
                       "LevelOfRamTwo INTEGER,"
                       "OrderLvlTwo INTEGER,"
                       "LevelOfRamThree INTEGER,"
                       "OrderLvlThree INTEGER,"
                       "BranchLvlFour INTEGER,"
                       "OrderLvlFour INTEGER,"
                       "AnchorLine INTEGER,"
                       "AnchorRibNum INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Lines")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))
            self.setHeaderData(1, Qt.Horizontal, _("Num branches"))
            self.setHeaderData(2, Qt.Horizontal, _("Ramif 1"))
            self.setHeaderData(3, Qt.Horizontal, _("Node 1"))
            self.setHeaderData(4, Qt.Horizontal, _("Ramif 2"))
            self.setHeaderData(5, Qt.Horizontal, _("Node 2"))
            self.setHeaderData(6, Qt.Horizontal, _("Ramif 3"))
            self.setHeaderData(7, Qt.Horizontal, _("Node 3"))
            self.setHeaderData(8, Qt.Horizontal, _("Ramif 4"))
            self.setHeaderData(9, Qt.Horizontal, _("Node 4"))
            self.setHeaderData(10, Qt.Horizontal, _("Anchor"))
            self.setHeaderData(11, Qt.Horizontal, _("Rib num"))

        def updateLineRow(self, configNum, orderNum, i1, i2, i3, i4, i5, i6,
                          i7, i8, i9, i10, i11):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here
                     as they should be well known.
            '''
            logging.debug(self.__className + '.updateLineRow')

            query = QSqlQuery()
            query.prepare("UPDATE Lines SET "
                          "NumBranches= :i1, "
                          "BranchLvlOne= :i2, "
                          "OrderLvlOne= :i3, "
                          "LevelOfRamTwo= :i4, "
                          "OrderLvlTwo= :i5, "
                          "LevelOfRamThree= :i6, "
                          "OrderLvlThree= :i7, "
                          "BranchLvlFour= :i8, "
                          "OrderLvlFour= :i9, "
                          "AnchorLine= :i10, "
                          "AnchorRibNum= :i11 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":i1", i1)
            query.bindValue(":i2", i2)
            query.bindValue(":i3", i3)
            query.bindValue(":i4", i4)
            query.bindValue(":i5", i5)
            query.bindValue(":i6", i6)
            query.bindValue(":i7", i7)
            query.bindValue(":i8", i8)
            query.bindValue(":i9", i9)
            query.bindValue(":i10", i10)
            query.bindValue(":i11", i11)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated

        def set_num_configs(self, must_num_configs):
            '''
            :method: Assures the model will be setup to hold the correct
                     number of configs based on parameters passed.
            :param must_num_configs: Number of configs the model must provide.
            '''
            logging.debug(self.__className + '.set_num_configs')
            currNumConfigs = self.num_configs()

            diff = abs(must_num_configs - currNumConfigs)
            if diff != 0:
                # do it only if really the number has changed
                i = 0
                if must_num_configs > currNumConfigs:
                    # add config lines
                    while i < diff:
                        self.add_row_for_config(currNumConfigs + 1 + i)
                        i += 1
                else:
                    # remove config lines
                    while i < diff:
                        self.remove_row_for_config(currNumConfigs - i)
                        i += 1

                # emit the change signal
                self.numConfigsChanged.emit(self.num_configs())

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a
                     specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "NumBranches, "
                          "BranchLvlOne, "
                          "OrderLvlOne, "
                          "LevelOfRamTwo, "
                          "OrderLvlTwo, "
                          "LevelOfRamThree, "
                          "OrderLvlThree, "
                          "BranchLvlFour, "
                          "OrderLvlFour, "
                          "AnchorLine, "
                          "AnchorRibNum "
                          "FROM Lines WHERE (ConfigNum = :config) "
                          "ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class MarksModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Marks parameters.
        '''
        __className = 'MarksModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        MarksSpCol = 0
        ''':attr: Number of the col holding the marks spacing value'''
        PointRadCol = 1
        ''':attr: Number of the col holding the point radius value'''
        PointDisplCol = 2
        ''':attr: Number of the col holding the points displacement value'''

        def createTable(self):
            '''
            :method: Creates initially the empty Marks table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists Marks;")
            query.exec("create table if not exists Marks ("
                       "MarksSp REAL,"
                       "PointRad REAL,"
                       "PointDispl REAL,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Marks")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Marks Spacing [cm]"))
            self.setHeaderData(1, Qt.Horizontal, _("Point Radius [cm]"))
            self.setHeaderData(2, Qt.Horizontal, _("Point Displacement [cm]"))

            self.add_rows(-1, 1)

        def updateRow(self, marksSp, pointRad, pointDispl):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare(
                "UPDATE Marks SET MarksSp= :marksSp, PointRad= :pointRad, PointDispl= :pointDispl WHERE (ID = :id);")
            query.bindValue(":marksSp", marksSp)
            query.bindValue(":pointRad", pointRad)
            query.bindValue(":pointDispl", pointDispl)
            query.bindValue(":id", 1)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "MarksSp, "
                          "PointRad, "
                          "PointDispl "
                          "FROM Marks")
            query.exec()
            query.next()
            return query.value

    class MarksTypesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
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
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
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
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("MarksTypes")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Marks type"))
            self.setHeaderData(2, Qt.Horizontal, _("Form 1"))
            self.setHeaderData(3, Qt.Horizontal, _("Form 1 1st param"))
            self.setHeaderData(4, Qt.Horizontal, _("Form 1 2nd param"))
            self.setHeaderData(5, Qt.Horizontal, _("Form 2"))
            self.setHeaderData(6, Qt.Horizontal, _("Form 2 1st param"))
            self.setHeaderData(7, Qt.Horizontal, _("Form 2 2nd param"))

        def updateRow(self, configNum, orderNum, pType, formOne, formOnePOne, formOnePTwo, formTwo, formTwoPOne,
                      formTwoPTwo):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

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
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

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

    class NewSkinTensConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: provides a SqlTableModel holding all data related to the group wide parameters for New Skin Tension 
        '''

        __className = 'NewSkinTensConfModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        __numConfigs = 0

        OrderNumCol = 0
        ''':attr: num of column for ordering the individual lines of a config'''
        InitialRibCol = 1
        ''':attr: number of the column holding the first rib of the config'''
        FinalRibCol = 2
        ''':attr: number of the column holding the final rib'''
        TypeCol = 3
        ''':attr: number of the column holding type information'''
        ConfigNumCol = 4
        ''':attr: number of the column holding the config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table.
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists NewSkinTensConf;")
            query.exec("create table if not exists NewSkinTensConf ("
                       "OrderNum INTEGER,"
                       "InitialRib INTEGER,"
                       "FinalRib INTEGER,"
                       "Type INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("NewSkinTensConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
            self.setHeaderData(3, Qt.Horizontal, _("Type"))

        def updateRow(self, config, initialRib, finalRib, calcT):
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare(
                "UPDATE NewSkinTensConf SET InitialRib= :initial , FinalRib= :final, Type= :calcT WHERE (ConfigNum = :config);")
            query.bindValue(":initial", initialRib)
            query.bindValue(":final", finalRib)
            query.bindValue(":calcT", calcT)
            query.bindValue(":config", config)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "OrderNum, "
                          "InitialRib, "
                          "FinalRib, "
                          "Type "
                          "FROM NewSkinTensConf WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class NewSkinTensDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all detail data related to New skin tension. 
        '''
        __className = 'NewSkinTensionDetModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for ordering the individual lines of a config'''
        TopDistLECol = 1
        ''':attr: Distance in % of chord on the leading edge of extrados'''
        TopWideCol = 2
        ''':attr: Extrados over-wide corresponding in % of chord'''
        BottDistTECol = 3
        ''':attr: Distance in % of chord on trailing edge'''
        BottWideCol = 4
        ''':attr: Intrados over-wide corresponding in % of chord'''
        ConfigNumCol = 5
        ''':attr: number of the column holding the config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty Skin tension table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists NewSkinTensDet;")
            query.exec("create table if not exists NewSkinTensDet ("
                       "OrderNum INTEGER, "
                       "TopDistLE REAL, "
                       "TopWide REAL, "
                       "BotDistTE REAL, "
                       "BotWide REAL, "
                       "ConfigNum INTEGER, "
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("NewSkinTensDet")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))
            self.setHeaderData(1, Qt.Horizontal, _("Top dist LE"))
            self.setHeaderData(2, Qt.Horizontal, _("Top widening"))
            self.setHeaderData(3, Qt.Horizontal, _("Bott dist TE"))
            self.setHeaderData(4, Qt.Horizontal, _("Bott widening"))

        def updateRow(self, configNum, orderNum, topDistLE, topWide, botDistTE, botWide):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE NewSkinTensDet SET "
                          "TopDistLE= :topDis, "
                          "TopWide= :topWide, "
                          "BotDistTE= :botDis, "
                          "BotWide= :botWide  "
                          "WHERE (ConfigNum = :config AND OrderNum= :order);")
            query.bindValue(":topDis", topDistLE)
            query.bindValue(":topWide", topWide)
            query.bindValue(":botDis", botDistTE)
            query.bindValue(":botWide", botWide)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "TopDistLE, "
                          "TopWide, "
                          "BotDistTE, "
                          "BotWide "
                          "FROM NewSkinTensDet WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class NoseMylarsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'NoseMylarsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: Number of the col holding the first rib'''
        LastRibCol = 2
        ''':attr: Number of the col holding the last rib'''
        xOneCol = 3
        ''':attr: Number of the col holding the 1st param of 2nd row'''
        uOneCol = 4
        ''':attr: Number of the col holding the 2nd param of 2nd row'''
        uTwoCol = 5
        ''':attr: Number of the col holding the 3rd param of 2nd row'''
        xTwoCol = 6
        ''':attr: Number of the col holding the 4th param of 2nd row'''
        vOneCol = 7
        ''':attr: Number of the col holding the 5th param of 2nd row'''
        vTwoCol = 8
        ''':attr: Number of the col holding the 1st param of 3rd row'''
        ConfigNumCol = 9
        ''':attr: num of column for config number (always 1)'''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists NoseMylars;")
            query.exec("create table if not exists NoseMylars ("
                       "OrderNum INTEGER, "
                       "FirstRib INTEGER, "
                       "LastRib INTEGER, "
                       "x_one REAL, "
                       "uOne REAL, "
                       "uTwo REAL, "
                       "x_two REAL, "
                       "vOne REAL, "
                       "vTwo REAL, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("NoseMylars")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Order num"))
            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))
            self.setHeaderData(3, Qt.Horizontal, _("X1"))
            self.setHeaderData(4, Qt.Horizontal, _("U1"))
            self.setHeaderData(5, Qt.Horizontal, _("U2"))
            self.setHeaderData(6, Qt.Horizontal, _("X2"))
            self.setHeaderData(7, Qt.Horizontal, _("V1"))
            self.setHeaderData(8, Qt.Horizontal, _("V2"))

        def updateRow(self, configNum, orderNum, firstRib, lastRib, xOne, uOne, uTwo, xTwo, vOne, vTwo):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE NoseMylars SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib, "
                          "x_one= :x_one, "
                          "uOne= :uOne, "
                          "uTwo= :uTwo, "
                          "x_two= :x_two, "
                          "vOne= :vOne, "
                          "vTwo= :vTwo "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib)
            query.bindValue(":lastRib", lastRib)
            query.bindValue(":x_one", xOne)
            query.bindValue(":uOne", uOne)
            query.bindValue(":uTwo", uTwo)
            query.bindValue(":x_two", xTwo)
            query.bindValue(":vOne", vOne)
            query.bindValue(":vTwo", vTwo)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "OrderNum, "
                          "FirstRib, "
                          "LastRib, "
                          "x_one, "
                          "uOne, "
                          "uTwo, "
                          "x_two, "
                          "vOne, "
                          "vTwo "
                          "FROM NoseMylars WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class PartsSeparationModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding the parts' separation
                settings.
        """
        __className = 'PartsSeparationModel'
        '''
        :attr: Does help to indicate the source of the log messages.
        '''
        __isUsed = False
        '''
        :attr: Helps to remember if the section is in use or not
        '''
        usageUpd = pyqtSignal()
        '''
        :signal: Emitted as soon the usage flag is changed
        '''
        OrderNumCol = 0
        '''
        :attr: Num of column for ordering the individual lines of a config
        '''
        Panel_x_col = 1
        '''
        :attr: Multiplication factor for x-direction panels separation
        '''
        Panel_x_min_col = 2
        '''
        :attr: Multiplication factor for x-direction panels minimum separation
        '''
        Panel_y_col = 3
        '''
        :attr: Multiplication factor for y-direction panels separation 
        '''
        Rib_x_col = 4
        '''
        :attr: Multiplication factor for x-direction ribs separation
        '''
        Rib_y_col = 5
        '''
        :attr: Multiplication factor for y-direction ribs separation
        '''
        Param6_col = 6
        '''
        :attr: Parameter still not used
        '''
        Param7_col = 7
        '''
        :attr: Parameter still not used
        '''
        Param8_col = 8
        '''
        :attr: Parameter still not used
        '''
        Param9_col = 9
        '''
        :attr: Parameter still not used
        '''
        Param10_col = 10
        '''
        :attr: Parameter still not used
        '''
        ConfigNumCol = 11
        '''
        :attr: Num of column for config number (always 1)
        '''

        def __init__(self, parent=None):
            """
            :method: Constructor
            """
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.create_table()
            self.setTable("PartsSeparation")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.set_num_rows_for_config(1, 1)

            self.setHeaderData(self.OrderNumCol,
                               Qt.Horizontal,
                               _("Order num"))
            self.setHeaderData(self.Panel_x_col,
                               Qt.Horizontal,
                               _("panel_x"))
            self.setHeaderData(self.Panel_x_min_col,
                               Qt.Horizontal,
                               _("panel_x_min"))
            self.setHeaderData(self.Panel_x_col,
                               Qt.Horizontal,
                               _("panel_y"))
            self.setHeaderData(self.Rib_x_col,
                               Qt.Horizontal,
                               _("rib_x"))
            self.setHeaderData(self.Rib_y_col,
                               Qt.Horizontal,
                               _("rib_y"))
            self.setHeaderData(self.Param6_col,
                               Qt.Horizontal,
                               _("parameter6"))
            self.setHeaderData(self.Param7_col,
                               Qt.Horizontal,
                               _("parameter7"))
            self.setHeaderData(self.Param8_col,
                               Qt.Horizontal,
                               _("parameter8"))
            self.setHeaderData(self.Param9_col,
                               Qt.Horizontal,
                               _("parameter9"))
            self.setHeaderData(self.Param10_col,
                               Qt.Horizontal,
                               _("parameter10"))

        def create_table(self):
            """
            :method: Creates initially the empty table
            """
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists PartsSeparation;")
            query.exec("create table if not exists PartsSeparation ("
                       "OrderNum INTEGER, "
                       "panel_x REAL, "
                       "panel_x_min REAL, "
                       "panel_y REAL, "
                       "rib_x REAL, "
                       "rib_y REAL, "
                       "param6 REAL, "
                       "param7 REAL, "
                       "param8 REAL, "
                       "param9 REAL, "
                       "param10 REAL, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def update_row(self, config_num, order_num,
                       panel_x, panel_x_min, panel_y,
                       rib_x, rib_y,
                       param6, param7, param8, param9, param10):
            """
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitly explained here
                     as they should be well known.
            """
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE PartsSeparation SET "
                          "panel_x= :panel_x, "
                          "panel_x_min= :panel_x_min, "
                          "panel_y= :panel_y, "
                          "rib_x= :rib_x, "
                          "rib_y= :rib_y, "
                          "param6= :param6, "
                          "param7= :param7, "
                          "param8= :param8, "
                          "param9= :param9, "
                          "param10= :param10 "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":panel_x", panel_x)
            query.bindValue(":panel_x_min", panel_x_min)
            query.bindValue(":panel_y", panel_y)
            query.bindValue(":rib_x", rib_x)
            query.bindValue(":rib_y", rib_y)
            query.bindValue(":param6", param6)
            query.bindValue(":param7", param7)
            query.bindValue(":param8", param8)
            query.bindValue(":param9", param9)
            query.bindValue(":param10", param10)
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            self.select()  # assure the model is updated properly

        def set_is_used(self, is_used):
            """
            :method: Set the usage flag of the section
            :param is_used: True if section is in use, False otherwise
            :type is_used: bool
            """
            logging.debug(self.__className + '.set_is_used')
            self.__isUsed = is_used
            self.usageUpd.emit()

        def is_used(self):
            """
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise
            :rtype: bool
            """
            logging.debug(self.__className + '.is_used')
            return self.__isUsed

        def get_row(self, config_num, order_num):
            """
            :method: Reads values back from the internal database for a
                     specific config and order number
            :param config_num: Configuration number. Starting with 1.
            :param order_num: Order number. Starting with 1.

            :return: Values read from internal database
            :rtype: QRecord
            """
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "panel_x, "
                          "panel_x_min, "
                          "panel_y, "
                          "rib_x, "
                          "rib_y, "
                          "param6, "
                          "param7, "
                          "param8, "
                          "param9, "
                          "param10 "
                          "FROM PartsSeparation WHERE (ConfigNum = :config) "
                          "ORDER BY OrderNum")
            query.bindValue(":config", config_num)
            query.exec()
            query.next()
            return query.record()

    class RamificationModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding the ramification parameters.
        """
        __className = 'RamificationModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for 1..3: ordering the individual lines of a config'''
        RowsCol = 1
        ''':attr: Number of the col holding the number of rows'''
        ThirdToSailCol = 2
        ''':attr: Number of the col holding the distance branching third to sail (l3)'''
        FourthToSailCol = 3
        ''':attr: Number of the col holding the distance beginning of fourth branching to sail (l2)'''
        ConfigNumCol = 4
        ''':attr: num of column for config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty Ramification table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists Ramification;")
            query.exec("create table if not exists Ramification ("
                       "OrderNum INTEGER,"
                       "Rows INTEGER,"
                       "ThirdToSail INTEGER,"
                       "FourthToSail INTEGER,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Ramification")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Rows"))
            self.setHeaderData(2, Qt.Horizontal, _("Third to sail [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("Fourth to sail [cm]"))

            self.set_num_rows_for_config(1, 4)

        def updateDataRow(self, configNum, orderNum, rows, thirdToSail, fourthToSail):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.updateDataRow')

            query = QSqlQuery()
            query.prepare("UPDATE Ramification SET "
                          "Rows= :rows, "
                          "ThirdToSail= :thirdToSail, "
                          "FourthToSail= :fourthToSail "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":rows", rows)
            query.bindValue(":thirdToSail", thirdToSail)
            query.bindValue(":fourthToSail", fourthToSail)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Rows, "
                          "ThirdToSail,"
                          "FourthToSail "
                          "FROM Ramification WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            query.next()
            return query.value

    class RibModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to the
                individual ribs.
        '''
        __className = 'RibModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        RibNumCol = 0
        ''':attr: number of the rib number column'''
        xribCol = 1
        ''':attr: number of the column providing rib X coordinate'''
        yLECol = 2
        '''
        :attr: number of the column providing Y coordinate of the
               leading edge
        '''
        yTECol = 3
        '''
        :attr: number of the column providing Y coordinate of the
               trailing edge
        '''
        xpCol = 4
        '''
        :attr: number of the column providing X' coordinate of the rib
               in its final position in space
        '''
        zCol = 5
        '''
        :attr: number of the column providing Z coordinate of the rib in
               its final position in space
        '''
        betaCol = 6
        '''
        :attr: number of the column providing the angle "beta" of the
               rib to the vertical (degres)
        '''
        RPCol = 7
        '''
        :attr: number of the column providing RP percentage of chord to
                  be held on the relative torsion of the airfoils
        '''
        WashinCol = 8
        '''
        :attr: number of the column providing washin in degrees defined
               manually (if parameter is set to "0")
        '''
        RotZCol = 9
        '''
        :attr: number of the column providing the rotation angle in z
               axis.
        '''
        PosZCol = 10
        '''
        :attr: number of the column holding the position of the z-axis
               rotation point
        '''

        def createRibTable(self):
            '''
            :method: Creates initially the empty rib table.
            '''
            logging.debug(self.__className + '.createRibTable')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists Rib;")
            query.exec("create table if not exists Rib ("
                       "RibNum INTEGER,"
                       "xrib REAL,"
                       "yLE REAL,"
                       "yTE REAL,"
                       "xp REAL,"
                       "z REAL,"
                       "beta REAL,"
                       "RP REAL,"
                       "Washin REAL,"
                       "Rot_Z REAL,"
                       "Pos_Z REAL,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createRibTable()
            self.setTable("Rib")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(self.RibNumCol, Qt.Horizontal, _("Rib Num"))
            self.setHeaderData(self.RPCol, Qt.Horizontal, _("RP"))
            self.setHeaderData(self.WashinCol, Qt.Horizontal, _("Washin"))
            self.setHeaderData(self.RotZCol, Qt.Horizontal, _("Z Rotation"))
            self.setHeaderData(self.PosZCol, Qt.Horizontal, _("Z Position"))

        def updateRow(self, ribNum, xrib, yLE, yTE, xp, z, beta, RP, Washin,
                      rotZ, posZ):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE Rib SET "
                          "xrib = :xrib, "
                          "yLE = :yLE, "
                          "yTE = :yTE, "
                          "xp = :xp, "
                          "z = :z, "
                          "beta = :beta, "
                          "RP = :RP, "
                          "Washin = :Washin, "
                          "Rot_Z = :rotZ, "
                          "Pos_Z = :posZ "
                          "WHERE (RibNum = :ribNum);")
            query.bindValue(":xrib", xrib)
            query.bindValue(":yLE", yLE)
            query.bindValue(":yTE", yTE)
            query.bindValue(":xp", xp)
            query.bindValue(":z", z)
            query.bindValue(":beta", beta)
            query.bindValue(":RP", RP)
            query.bindValue(":Washin", Washin)
            query.bindValue(":ribNum", ribNum)
            query.bindValue(":rotZ", rotZ)
            query.bindValue(":posZ", posZ)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def getRow(self, ribNum):
            '''
            :method: reads values back from the internal database for a
                     specific rib number
            :param ribNum: Rib number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "xrib, "
                          "yLE, "
                          "yTE, "
                          "xp, "
                          "z, "
                          "beta, "
                          "RP, "
                          "Washin, "
                          "Rot_Z, "
                          "Pos_Z "
                          "FROM Rib WHERE (RibNum = :rib)")
            query.bindValue(":rib", ribNum)
            query.exec()
            query.next()
            return query.value

    class SkinTensionModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data related to Skin tension. 
        '''
        __className = 'SkinTensionModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        TopDistLECol = 0
        ''':attr: Distance in % of chord on the leading edge of extrados'''
        TopWideCol = 1
        ''':attr: Extrados over-wide corresponding in % of chord'''
        BottDistTECol = 2
        ''':attr: Distance in % of chord on trailing edge'''
        BottWideCol = 3
        ''':attr: Intrados over-wide corresponding in % of chord'''

        def createTable(self):
            '''
            :method: Creates initially the empty Skin tension table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists SkinTension;")
            query.exec("create table if not exists SkinTension ("
                       "TopDistLE REAL,"
                       "TopWide REAL,"
                       "BottDistTE REAL,"
                       "BottWide REAL,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SkinTension")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)
            self.add_rows(-1, 6)

            self.setHeaderData(0, Qt.Horizontal, _("Top dist LE"))
            self.setHeaderData(1, Qt.Horizontal, _("Top widening"))
            self.setHeaderData(2, Qt.Horizontal, _("Bott dist TE"))
            self.setHeaderData(3, Qt.Horizontal, _("Bott widening"))

        def updateRow(self, row, topDistLE, topWide, bottDistTE, bottWide):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare(
                "UPDATE SkinTension SET TopDistLE= :topDis, TopWide= :topWide, BottDistTE= :bottDis, BottWide= :bottWide  WHERE (ID = :id);")
            query.bindValue(":topDis", topDistLE)
            query.bindValue(":topWide", topWide)
            query.bindValue(":bottDis", bottDistTE)
            query.bindValue(":bottWide", bottWide)
            query.bindValue(":id", row)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific config number
            :param configNum: Configuration number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "TopDistLE, "
                          "TopWide, "
                          "BottDistTE, "
                          "BottWide "
                          "FROM SkinTension WHERE (ID = :config)")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            return query.value

    class SkinTensionParamsModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the three individual params of the Skin tension setup. 
        '''
        __className = 'SkinTensionParamsModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        StrainMiniRibsCol = 0
        ''':attr: Parameter to control the mini ribs'''
        NumPointsCol = 1
        ''':attr: Number of points'''
        CoeffCol = 2
        ''':attr: The coefficient'''

        def createTable(self):
            '''
            :method: Creates initially the empty Skin tension params table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists SkinTensionParams;")
            query.exec("create table if not exists SkinTensionParams ("
                       "StrainMiniRibs REAL,"
                       "NumPoints Integer,"
                       "Coeff REAL,"
                       "ID INTEGER PRIMARY KEY);")
            query.exec(
                "INSERT into SkinTensionParams (StrainMiniRibs, NumPoints, Coeff,  ID) Values( '0.0114', '1000', '1.0', 1 );")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SkinTensionParams")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Strain mini ribs"))
            self.setHeaderData(1, Qt.Horizontal, _("Num points"))
            self.setHeaderData(2, Qt.Horizontal, _("Coeff"))

        def getRow(self):
            '''
            :method: reads values back from the internal database
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "StrainMiniRibs, "
                          "NumPoints, "
                          "Coeff "
                          "FROM SkinTensionParams")
            query.exec()
            query.next()
            return query.value

    class SewingAllowancesModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Sewing allowances parameters. 
        '''
        __className = 'SewingAllowancesModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        EdgeSeamCol = 0
        ''':attr: Number of the col holding the Edge seem values'''
        LeSeemCol = 1
        ''':attr: Number of the col holding the LE seem values'''
        TeSeemCol = 2
        ''':attr: Number of the col holding the TE seem values'''

        def createTable(self):
            '''
            :method: Creates initially the empty Sewing allowances table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists SewingAllowances;")
            query.exec("create table if not exists SewingAllowances ("
                       "EdgeSeam Integer,"
                       "LESeem Integer,"
                       "TESeem Integer,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SewingAllowances")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Edge seem [mm]"))
            self.setHeaderData(1, Qt.Horizontal, _("LE seem [mm]"))
            self.setHeaderData(2, Qt.Horizontal, _("TE seem [mm]"))

            self.add_rows(-1, 4)

        def updateRow(self, row, edgeSeam, leSeem=0, teSeem=0):
            '''
            :method: updates a specific row with the parameters passed.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare(
                "UPDATE SewingAllowances SET EdgeSeam= :edgeSeam, LESeem= :lESeem, TESeem= :tESeem WHERE (ID = :id);")
            query.bindValue(":edgeSeam", edgeSeam)
            query.bindValue(":lESeem", leSeem)
            query.bindValue(":tESeem", teSeem)
            query.bindValue(":id", row)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum):
            '''
            :method: reads values back from the internal database for a specific rib number
            :param ribNum: Rib number. Starting with 1. 
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "EdgeSeam, "
                          "LESeem, "
                          "TESeem "
                          "FROM SewingAllowances WHERE (ID = :config)")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            return query.value

    class SpecWingTipModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'SpecWingTipModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''

        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        OrderNumCol = 0
        '''
        :attr: num of column for ordering the individual lines
               of a config
        '''
        AngleLECol = 1
        ''':attr: Number of the col holding the LE angle'''
        AngleTECol = 2
        ''':attr: Number of the col holding the TE angle'''
        ConfigNumCol = 3
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("SpecWingTip")

            self.setHeaderData(1, Qt.Horizontal, _("LE Angle [deg]"))
            self.setHeaderData(2, Qt.Horizontal, _("TE Angle [deg]"))

            self.set_num_rows_for_config(1, 1)
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists SpecWingTip;")
            query.exec("create table if not exists SpecWingTip ("
                       "OrderNum INTEGER,"
                       "AngleLE REAL,"
                       "AngleTE REAL,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, angleLE, angleTE):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE SpecWingTip SET "
                          "AngleLE= :angleLE, "
                          "AngleTE= :angleTE "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":angleLE", angleLE)
            query.bindValue(":angleTE", angleTE)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise
            '''
            logging.debug(self.__className + '.set_is_used')
            self.__isUsed = isUsed
            self.usageUpd.emit()

        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise
            '''
            logging.debug(self.__className + '.is_used')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a
                     specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "OrderNum, "
                          "AngleLE, "
                          "AngleTE "
                          "FROM SpecWingTip WHERE (ConfigNum = :config) "
                          "ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class ThreeDDxfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'ThreeDDxfModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''

        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''

        OrderNumCol = 0
        '''
        :attr: num of column for ordering the individual lines
               of a config
        '''
        LineNameCol = 1
        ''':attr: Number of the col holding the fixed line name '''
        UnifilarCol = 2
        ''':attr: Number of the col holding the unifilar flag'''
        ColorCodeCol = 3
        ''':attr: Number of the col holding the color code'''
        ColorNameCol = 4
        ''':attr: Number of the col holding the optional color name'''
        ConfigNumCol = 5
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDDxf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.set_num_rows_for_config(1, 9)

            self.setHeaderData(1, Qt.Horizontal, _("Line Name"))
            self.setHeaderData(2, Qt.Horizontal, _("Unifilar"))
            self.setHeaderData(3, Qt.Horizontal, _("Color code"))
            self.setHeaderData(4, Qt.Horizontal, _("Color name (opt)"))

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ThreeDDxf;")
            query.exec("create table if not exists ThreeDDxf ("
                       "OrderNum INTEGER,"
                       "LineName TEXT,"
                       "Unifilar INTEGER, "
                       "ColorCode INTEGER,"
                       "ColorName TEXT,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def updateRow(self,
                      configNum,
                      orderNum,
                      lineName,
                      colorCode,
                      colorName,
                      unifilar=0):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here
                     as they should be well known.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE ThreeDDxf SET "
                          "LineName= :lineName, "
                          "Unifilar= :unifilar, "
                          "ColorCode= :colorCode, "
                          "ColorName= :colorName "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":lineName", lineName)
            query.bindValue(":unifilar", unifilar)
            query.bindValue(":colorCode", colorCode)
            query.bindValue(":colorName", colorName)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise
            '''
            logging.debug(self.__className + '.set_is_used')
            self.__isUsed = isUsed
            self.usageUpd.emit()

        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise
            '''
            logging.debug(self.__className + '.is_used')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a
                     specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "LineName, "
                          "Unifilar, "
                          "ColorCode, "
                          "ColorName "
                          "FROM ThreeDDxf WHERE (ConfigNum = :config) "
                          "ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class ThreeDShConfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the 3d Shaping configuration
        '''
        __className = 'ThreeDShConfModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for ordering the individual lines of a config'''
        FirstRibCol = 1
        ''':attr: Number of the col holding the first rib'''
        LastRibCol = 2
        ''':attr: Number of the col holding the last rib'''
        ConfigNumCol = 3
        ''':attr: num of column for config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ThreeDShapingConf;")
            query.exec("create table if not exists ThreeDShapingConf ("
                       "OrderNum INTEGER, "
                       "FirstRib INTEGER, "
                       "LastRib INTEGER, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingConf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("First Rib"))
            self.setHeaderData(2, Qt.Horizontal, _("Last Rib"))

        def updateRow(self, configNum, orderNum, firstRib, lastRib):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingConf SET "
                          "FirstRib= :firstRib, "
                          "LastRib= :lastRib "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":firstRib", firstRib)
            query.bindValue(":lastRib", lastRib)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "OrderNum, "
                          "FirstRib, "
                          "LastRib "
                          "FROM ThreeDShapingConf WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class ThreeDShUpDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the 3d Shaping data for the upper panels
        '''
        __className = 'ThreeDShUpDetModel'
        ''' :attr: Does help to indicate the source of the log messages. '''

        OrderNumCol = 0
        ''':attr: num of column for ordering the individual lines of a config'''
        IniPointCol = 1
        ''':attr: Number of the col holding initial point of the zone of influence'''
        CutPointCol = 2
        ''':attr: Number of the col holding position of the point where the cut is set'''
        DepthCol = 3
        ''':attr: Number of the col holding the shaping depth'''
        ConfigNumCol = 4
        ''':attr: num of column for config number'''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ThreeDShapingUpDetail;")
            query.exec("create table if not exists ThreeDShapingUpDetail ("
                       "OrderNum INTEGER, "
                       "IniPoint INTEGER, "
                       "CutPoint INTEGER, "
                       "Depth REAL, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingUpDetail")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Ini P"))
            self.setHeaderData(2, Qt.Horizontal, _("Cut P"))
            self.setHeaderData(3, Qt.Horizontal, _("Depth"))

        def updateRow(self, configNum, orderNum, iniPoint, cutPoint, depth):
            '''
            :method: Updates a specific row in the database with the values passed. Parameters are not explicitely explained here as they should be well known. 
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingUpDetail SET "
                          "IniPoint= :iniPoint, "
                          "CutPoint= :cutPoint, "
                          "Depth= :depth "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":iniPoint", iniPoint)
            query.bindValue(":cutPoint", cutPoint)
            query.bindValue(":depth", depth)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            self.select()  # to a select() to assure the model is updated properly

        def getRow(self, configNum, orderNum):
            '''
            :method: reads values back from the internal database for a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.  
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "IniPoint, "
                          "CutPoint, "
                          "Depth "
                          "FROM ThreeDShapingUpDetail WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class ThreeDShLoDetModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the 3d Shaping data for
                the lower panels
        '''
        __className = 'ThreeDShLoDetModel'
        '''
        :attr: Does help to indicate the source of the log messages.
        '''

        OrderNumCol = 0
        '''
        :attr: Num of column for ordering the individual lines
               of a config
        '''

        IniPointCol = 1
        '''
        :attr: Number of the col holding initial point of the zone
               of influence
        '''

        CutPointCol = 2
        '''
        :attr: Number of the col holding position of the point where the
               cut is set
        '''

        DepthCol = 3
        '''
        :attr: Number of the col holding the shaping depth
        '''

        ConfigNumCol = 4
        '''
        :attr: num of column for config number
        '''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ThreeDShapingLoDetail;")
            query.exec("create table if not exists ThreeDShapingLoDetail ("
                       "OrderNum INTEGER, "
                       "IniPoint INTEGER, "
                       "CutPoint INTEGER, "
                       "Depth REAL, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingLoDetail")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Ini P"))
            self.setHeaderData(2, Qt.Horizontal, _("Cut P"))
            self.setHeaderData(3, Qt.Horizontal, _("Depth"))

        def updateRow(self, configNum, orderNum, iniPoint, cutPoint, depth):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here
                     as they should be well known.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingLoDetail SET "
                          "IniPoint= :iniPoint, "
                          "CutPoint= :cutPoint, "
                          "Depth= :depth "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":iniPoint", iniPoint)
            query.bindValue(":cutPoint", cutPoint)
            query.bindValue(":depth", depth)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def getRow(self, configNum, orderNum):
            '''
            :method: Reads values back from the internal database for a
                     specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "IniPoint, "
                          "CutPoint, "
                          "Depth "
                          "FROM ThreeDShapingLoDetail WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class ThreeDShPrintModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the Print data for 3d Shaping
        '''
        __className = 'ThreeDShPrintModel'
        '''
        :attr: Does help to indicate the source of the log messages.
        '''

        OrderNumCol = 0
        '''
        :attr: Num of column for ordering the individual lines
               of a config
        '''
        NameCol = 1
        '''
        :attr: Number of the col holding the layer name
        '''
        DrawCol = 2
        '''
        :attr: Number of the col holding the info if the layer shall
               be drawn
        '''
        FirstPanelCol = 3
        '''
        :attr: Number of the col holding the number of the first panel
               to print
        '''
        LastPanelCol = 4
        '''
        :attr: Number of the col holding the number of the last panel
               to print
        '''
        SymmetricCol = 5
        '''
        :attr: Number of the col holding the symmetric information
        '''
        ConfigNumCol = 6
        '''
        :attr: num of column for config number
        '''

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists ThreeDShapingPrint;")
            query.exec("create table if not exists ThreeDShapingPrint ("
                       "OrderNum INTEGER, "
                       "Name TEXT, "
                       "Draw INTEGER, "
                       "FirstPanel INTEGER, "
                       "LastPanel INTEGER, "
                       "Symmetric INTEGER, "
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("ThreeDShapingPrint")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.set_num_configs(1)
            self.set_num_rows_for_config(1, 5)

            self.setHeaderData(1, Qt.Horizontal, _("Name"))
            self.setHeaderData(2, Qt.Horizontal, _("Draw"))
            self.setHeaderData(3, Qt.Horizontal, _("First panel"))
            self.setHeaderData(4, Qt.Horizontal, _("Last panel"))
            self.setHeaderData(5, Qt.Horizontal, _("Symmetric"))

        def updateRow(self, configNum, orderNum, name, draw,
                      firstPanel, lastPanel, symmetric):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here
                     as they should be well known.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE ThreeDShapingPrint SET "
                          "Name= :name, "
                          "Draw= :draw, "
                          "FirstPanel= :firstPanel, "
                          "LastPanel= :lastPanel, "
                          "Symmetric= :symmetric "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":name", name)
            query.bindValue(":draw", draw)
            query.bindValue(":firstPanel", firstPanel)
            query.bindValue(":lastPanel", lastPanel)
            query.bindValue(":symmetric", symmetric)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def getRow(self, configNum, orderNum):
            '''
            :method: Reads values back from the internal database for a
                     specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Name, "
                          "Draw, "
                          "FirstPanel, "
                          "LastPanel, "
                          "Symmetric "
                          "FROM ThreeDShapingPrint WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

    class TwoDDxfModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding the DXF layer names
        '''
        __className = 'TwoDDxfModel'
        ''' :attr: Does help to indicate the source of the log messages. '''
        __isUsed = False
        ''' :attr: Helps to remember if the section is in use or not'''

        usageUpd = pyqtSignal()
        '''
        :signal: emitted as soon the usage flag is changed
        '''
        OrderNumCol = 0
        '''
        :attr: Num of column for ordering the individual
               lines of a config
        '''
        LineNameCol = 1
        ''':attr: Number of the col holding the fixed line name '''
        ColorCodeCol = 2
        ''':attr: Number of the col holding the color code'''
        ColorNameCol = 3
        ''':attr: Number of the col holding the optional color name'''
        ConfigNumCol = 4
        ''':attr: num of column for config number (always 1)'''

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.createTable()
            self.setTable("TwoDDxf")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.set_num_rows_for_config(1, 6)

            self.setHeaderData(1, Qt.Horizontal, _("Line name"))
            self.setHeaderData(2, Qt.Horizontal, _("Color code"))
            self.setHeaderData(3, Qt.Horizontal, _("Color name"))

            # TODO Color name is optional, reader does not take this
            #      into account currently
            # TODO prefill table with correct names.

        def createTable(self):
            '''
            :method: Creates initially the empty table
            '''
            logging.debug(self.__className + '.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists TwoDDxf;")
            query.exec("create table if not exists TwoDDxf ("
                       "OrderNum INTEGER,"
                       "LineName TEXT,"
                       "ColorCode INTEGER,"
                       "ColorName TEXT,"
                       "ConfigNum INTEGER,"
                       "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, lineName,
                      colorCode, colorName):
            '''
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            '''
            logging.debug(self.__className + '.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE TwoDDxf SET "
                          "LineName= :lineName, "
                          "ColorCode= :colorCode, "
                          "ColorName= :colorName "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":lineName", lineName)
            query.bindValue(":colorCode", colorCode)
            query.bindValue(":colorName", colorName)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def setIsUsed(self, isUsed):
            '''
            :method: Set the usage flag of the section
            :param isUse: True if section is in use, False otherwise.
            '''
            logging.debug(self.__className + '.set_is_used')
            self.__isUsed = isUsed
            self.usageUpd.emit()

        def isUsed(self):
            '''
            :method: Returns the information if the section is in use or not
            :returns: True if section is in use, false otherwise
            '''
            logging.debug(self.__className + '.is_used')
            return self.__isUsed

        def getRow(self, configNum, orderNum):
            '''
            :method: Reads values back from the internal database for
                     a specific config and order number
            :param configNum: Configuration number. Starting with 1.
            :param orderNum: Order number. Starting with 1.
            :return: specific values read from internal database
            '''
            logging.debug(self.__className + '.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "LineName, "
                          "ColorCode, "
                          "ColorName "
                          "FROM TwoDDxf WHERE (ConfigNum = :config) ORDER BY OrderNum")
            query.bindValue(":config", configNum)
            query.exec()
            query.next()
            # now we are at the first row
            i = 1
            while i < orderNum:
                query.next()
                i += 1
            return query.value

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

        def create_wing_table(self):
            """
            :method: Creates initially the empty wing table
            """
            logging.debug(self.__className + '.create_wing_table')

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

        def __init__(self, parent=None):  # @UnusedVariable
            """
            :method: Constructor
            """
            logging.debug(self.__className + '.__init__')
            super().__init__()
            self.create_wing_table()
            self.setTable("Wing")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.set_num_rows_for_config(1, 1)

            self.rib_M = ProcModel.RibModel()
            self.anchPoints_M = ProcModel.AnchorPointsModel()
            self.airf_M = ProcModel.AirfoilsModel()
            self.lightC_M = ProcModel.LightConfModel()
            self.glueVent_M = ProcModel.GlueVentModel()
            self.airfThick_M = ProcModel.AirfoilThicknessModel()

            # self.data_changed.connect(self.sync_rib_num_data)
            self.dataChanged.connect(self.man_data_change)

            self.setHeaderData(0, Qt.Horizontal, _("Brand name"))
            self.setHeaderData(1, Qt.Horizontal, _("Wing name"))
            self.setHeaderData(2, Qt.Horizontal, _("Draw scale"))
            self.setHeaderData(3, Qt.Horizontal, _("Wing scale"))
            self.setHeaderData(4, Qt.Horizontal, _("Num cells"))
            self.setHeaderData(5, Qt.Horizontal, _("Num ribs"))
            self.setHeaderData(6, Qt.Horizontal, _("Alpha max tip"))
            self.setHeaderData(7, Qt.Horizontal, _("Alpha mode"))
            self.setHeaderData(8, Qt.Horizontal, _("Alpha max cent"))
            self.setHeaderData(9, Qt.Horizontal, _("Para type"))
            self.setHeaderData(10, Qt.Horizontal, _("Para param"))
            self.setHeaderData(11, Qt.Horizontal, _("Lines Conc Type"))
            self.setHeaderData(12, Qt.Horizontal, _("Brake length"))
            self.setHeaderData(13, Qt.Horizontal, _("x-Spacing"))
            self.setHeaderData(14, Qt.Horizontal, _("y-Spacing"))

        def man_data_change(self, q):
            """
            :method: If NumRibs is changed manually we must keep half_num_ribs
                     and Ribs table in sync.
            """
            logging.debug(self.__className + '.man_data_change')

            if q.column() == self.NumRibsCol:
                self.sync_rib_num_data()

        def sync_rib_num_data(self):
            """
            :method: If NumRibs is changed we must keep half_num_ribs and Ribs
                     table in sync. This method will calculate the current
                     number of half ribs and calls the method to set up the
                     model accordingly.
            """
            logging.debug(self.__className + '.sync_rib_num_data')

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
            logging.debug(self.__className + '.update_num_cells')

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
            logging.debug(self.__className + '.update_num_ribs')

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
            logging.debug(self.__className + '.get_row')

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


from data.ProcFileReader import ProcFileReader
from data.ProcFileWriter import ProcFileWriter
