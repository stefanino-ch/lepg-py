"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
import logging

from PyQt6.QtCore import QFile, QTextStream, QObject, pyqtSignal, QStringConverter
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from Singleton.Singleton import Singleton

from ConfigReader.ConfigReader import ConfigReader
from data.Database import Database

from data.preProcModel.CellsDistrModel import CellsDistrModel
from data.preProcModel.GenModel import GenModel
from data.preProcModel.LeadingEdgeModel import LeadingEdgeModel
from data.preProcModel.TrailingEdgeModel import TrailingEdgeModel
from data.preProcModel.VaultModel import VaultModel

from data.FileHelpers import split_line, rem_tab_space_quot, \
                             chk_str, chk_num


class PreProcModel(QObject, metaclass=Singleton):
    """
    :class: Does take care about the data handling for the pre-processor.
            Reads and writes the data files
            Holds as a central point all temporary data during program
            execution

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
    __className = 'PreProcModel'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    __fileNamePath = ''
    '''
    :attr: Full path and name of the data file currently in use
    '''
    __fileVersion = ''
    '''
    :attr: version number of the file currently in use
    '''

    def __init__(self):
        """
        :method: Class initialization
        """
        self.__fileSaved = True

        self.db = Database()
        self.db.open_connection()

        super().__init__()

        self.leadingE_M = LeadingEdgeModel()
        self.leadingE_M.dataChanged.connect(self.data_edit)

        self.trailingE_M = TrailingEdgeModel()
        self.trailingE_M.dataChanged.connect(self.data_edit)

        self.vault_M = VaultModel()
        self.vault_M.dataChanged.connect(self.data_edit)

        self.gen_M = GenModel()
        self.gen_M.dataChanged.connect(self.data_edit)

        self.cellsDistr_M = CellsDistrModel()
        self.cellsDistr_M.dataChanged.connect(self.data_edit)

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
        :method: Called upon data edit activities within the PreProcModel.
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
        :method: Returns the current status of the pre-proc file
        :retval: File saved = True
                 Unsaved data = False
        :rtype: bool
        """
        return self.__fileSaved

    def file_saved_char(self):
        """
        :method: Returns the current status of the pre-proc file as character
        :retval: Y = File saved
                 N = Unsaved data
        :rtype: str
        """
        if self.__fileSaved is True:
            return 'Y'
        else:
            return 'N'

    def valid_file(self, file_name):
        """
        :method: Checks if a file can be opened and contains a valid title
                 and known version number
        :param file_name: the name of the file to be checked
        """
        in_file = QFile(file_name)
        if in_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(in_file)
        else:
            logging.error(self.__className
                          + 'File cannot be opened '
                          + file_name)
            return False

        title_ok = False
        version_ok = False
        line_counter = 0

        while ((stream.atEnd() is not True)
               and not (title_ok and version_ok)
               and line_counter < 4):
            line = stream.readLine()
            if line.find('1.5') >= 0:
                self.set_file_version('1.5')
                version_ok = True
            elif line.find('1.6') >= 0:
                self.set_file_version('1.6')
                version_ok = True

            if line.find('GEOMETRY PRE-PROCESSOR') >= 0:
                title_ok = True
            line_counter += 1

        in_file.close()

        if not (version_ok and title_ok):
            logging.error(self.__className
                          + ' Result of PreProc file version check %s',
                          version_ok)
            logging.error(self.__className
                          + ' Result of PreProc file title check %s',
                          title_ok)

            msg_box = QMessageBox()
            msg_box.setWindowTitle(_('File read error'))
            msg_box.setText(_('File seems not to be a valid PreProcessor File! '
                            '\nVersion detected: ')
                            + str(version_ok)
                            + _('\nTitle detected: ')
                            + str(title_ok))
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.Icon.Ok)
            msg_box.exec()

            self.set_file_name('')
            self.set_file_version('')

        return version_ok and title_ok

    def open_file(self):
        """
        :method: Checks for unsaved data, and appropriate handling.
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
                        _('Open Pre-Proc file'),
                        "",
                        "Pre-Proc Files (*.txt);;All Files (*)")

        if file_name != ('', ''):
            # User has really selected a file, if it had aborted
            # the dialog an empty tuple is returned
            if self.valid_file(file_name[0]):
                self.set_file_name(file_name[0])
                self.read_file()
                self.set_file_saved(True)

    def save_file(self):
        """
        :method: Checks if there is already a valid file name, if not it asks
                 for it. Starts afterwards the writing process.
        """
        file_name = self.get_file_name()
        if len(file_name) != 0:
            # We do have already a valid filename
            self.write_file()
            self.set_file_saved(True)
        else:
            # Ask first for the filename
            file_name = QFileDialog.getSaveFileName(
                        None,
                        _('Save Pre-Processor file'),
                        "",
                        "Pre-Proc Files (*.txt);;All Files (*)")

            if file_name != ('', ''):
                # User has really selected a file, if it had aborted
                # the dialog an empty tuple is returned
                self.set_file_name(file_name[0])
                self.write_file()
                self.set_file_saved(True)

    def save_file_as(self):
        """
        :method: Asks for a new filename. Starts afterwards the
                 writing process.
        """
        # Ask first for the filename
        file_name = QFileDialog.getSaveFileName(
                    None,
                    _('Save Pre-Processor file as'),
                    "",
                    "Pre-Proc Files (*.txt);;All Files (*)")

        if file_name != ('', ''):
            # User has really selected a file, if it had aborted
            # the dialog an empty tuple is returned
            self.set_file_name(file_name[0])
            self.write_file()
            self.set_file_saved(True)

    def read_file(self):
        """
        :method: Reads the data file and saves the data in the internal
                 variables.
        :warning: Filename and Path must be set first!
        """
        in_file = QFile(self.get_file_name())
        in_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stream = QTextStream(in_file)

        ##############################
        # 1. Geometry
        # Over-read file header
        counter = 0
        while counter < 2:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1

        # Wing Name
        self.gen_M.set_num_configs(0)

        self.gen_M.set_num_rows_for_config(1, 1)
        name = stream.readLine()
        self.gen_M.update_row(1, 1, name)

        # 1. Leading edge
        for i in range(3):
            stream.readLine()

        one = rem_tab_space_quot(stream.readLine())
        two = split_line(stream.readLine())
        thr = split_line(stream.readLine())
        fou = split_line(stream.readLine())
        fiv = split_line(stream.readLine())
        six = split_line(stream.readLine())
        sev = split_line(stream.readLine())
        eig = split_line(stream.readLine())
        nin = split_line(stream.readLine())
        ten = split_line(stream.readLine())

        self.leadingE_M.set_num_configs(0)
        self.leadingE_M.set_num_configs(1)
        self.leadingE_M.update_row(1, 1, one, two[1], thr[1], fou[1], fiv[1],
                                   six[1], sev[1], eig[1], nin[1], ten[1])

        # 2. Trailing edge
        for i in range(3):
            stream.readLine()

        one = rem_tab_space_quot(stream.readLine())
        two = split_line(stream.readLine())
        thr = split_line(stream.readLine())
        fou = split_line(stream.readLine())
        fiv = split_line(stream.readLine())
        six = split_line(stream.readLine())
        sev = split_line(stream.readLine())
        eig = split_line(stream.readLine())

        self.trailingE_M.set_num_configs(0)
        self.trailingE_M.set_num_configs(1)
        self.trailingE_M.update_row(1, 1, one, two[1], thr[1], fou[1], fiv[1],
                                    six[1], sev[1], eig[1])

        # 3. Vault
        for i in range(3):
            stream.readLine()

        self.vault_M.set_num_configs(0)
        self.vault_M.set_num_configs(1)
        vtype = int(rem_tab_space_quot(stream.readLine()))

        one = split_line(stream.readLine())
        two = split_line(stream.readLine())
        thr = split_line(stream.readLine())
        fou = split_line(stream.readLine())

        if vtype == 1:
            self.vault_M.update_row(1, 1, vtype, one[1], two[1], thr[1],
                                    fou[1], 0, 0, 0, 0, 0, 0, 0, 0)

        else:
            self.vault_M.update_row(1, 1, vtype, 0, 0, 0, 0, one[0], two[0],
                                    thr[0], fou[0], one[1], two[1],
                                    thr[1], fou[1])

        # 4. Cells distribution
        for i in range(3):
            stream.readLine()

        self.cellsDistr_M.set_num_configs(0)

        distr_type = int(rem_tab_space_quot(stream.readLine()))

        if distr_type == 1:
            self.cellsDistr_M.set_num_rows_for_config(1, 1)
            num_cells = rem_tab_space_quot(stream.readLine())
            self.cellsDistr_M.update_row(1, 1, distr_type, 0, 0, num_cells)

        elif (distr_type == 2) or (distr_type == 3):
            self.cellsDistr_M.set_num_rows_for_config(1, 1)
            coef = rem_tab_space_quot(stream.readLine())
            num_cells = rem_tab_space_quot(stream.readLine())
            self.cellsDistr_M.update_row(1, 1, distr_type, coef, 0, num_cells)

        elif distr_type == 4:
            num_cells = int(rem_tab_space_quot(stream.readLine()))
            self.cellsDistr_M.set_num_rows_for_config(1, num_cells)

            for it in range(0, num_cells):
                width = split_line(stream.readLine())
                self.cellsDistr_M.update_row(1, it + 1, distr_type, 0, width[1],
                                             num_cells)

        ##############################
        # Cleanup
        in_file.close()

    def write_file(self, for_proc=False):
        """
        :method: Writes all the values into a data file
        :warning: Filename must have been set already before, unless the
                  file shall be written for the PreProcessor
        :param for_proc: Set this to True if the file must be saved in the
                        directory where the PreProcessor resides
        """
        separator = '***************************************************\n'

        # TODO: check also processor code for wrong deletion ...

        if for_proc is True:
            # Special file write into the directory where the
            # PreProcessor resides
            config_reader = ConfigReader()
            file_path_name = os.path.join(config_reader
                                          .get_pre_proc_directory(),
                                          'pre-data.txt')
        else:
            file_path_name = self.get_file_name()

        if for_proc is True:
            # Special file write into the directory where the
            # PreProcessor resides
            config_reader = ConfigReader()
            file_path_name = os.path.join(config_reader
                                          .get_pre_proc_directory(),
                                          'pre-data.txt')
        else:
            file_path_name = self.get_file_name()

        # check if the file already exists
        if os.path.isfile(file_path_name):
            # file exists -> delete it
            os.remove(file_path_name)

        out_file = QFile(file_path_name)

        if not out_file.open(QFile.OpenModeFlag.ReadWrite | QFile.OpenModeFlag.Text):
            logging.error(self.__className+'.write_file '
                          + out_file.errorString())

            msg_box = QMessageBox()
            msg_box.setWindowTitle(_("File save error"))
            msg_box.setText(_('File can not be saved: ')
                            + out_file.errorString())
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStandardButtons(QMessageBox.Icon.Ok)
            msg_box.exec()
            return

        # File is open, start writing
        stream = QTextStream(out_file)
        stream.setEncoding(QStringConverter.Encoding.Utf8)

        stream << separator
        stream << 'LEPARAGLIDING\n'
        stream << 'GEOMETRY PRE-PROCESSOR         V1.6\n'
        stream << separator

        values = self.gen_M.get_row(1, 1)
        stream << '%s\n' % (chk_str(values(0), ''))

        stream << separator
        stream << '* 1. Leading edge parameters\n'
        stream << separator
        values = self.leadingE_M.get_row(1, 1)
        # Type is always 1
        # Column is hidden in the GUI, value will be hardcoded here
        # stream << '%s\n' % (self.fh.chk_num(values(0), 1))
        stream << '1\n'
        stream << 'a1= %s\n' % chk_num(values(1))
        stream << 'b1= %s\n' % chk_num(values(2))
        stream << 'x1= %s\n' % chk_num(values(3))
        stream << 'x2= %s\n' % chk_num(values(4))
        stream << 'xm= %s\n' % chk_num(values(5))
        stream << 'c0= %s\n' % chk_num(values(6))
        stream << 'ex1= %s\n' % chk_num(values(7))
        stream << 'c02= %s\n' % chk_num(values(8))
        stream << 'ex2= %s\n' % chk_num(values(9))

        stream << separator
        stream << '* 2. Trailing edge parameters\n'
        stream << separator
        values = self.trailingE_M.get_row(1, 1)
        # Type is always 1
        # Column is hidden in the GUI, value will be hardcoded here
        # stream << '%s\n'        %(self.fh.chk_num(values(0),1))
        stream << '1\n'
        stream << 'a1= %s\n' % chk_num(values(1))
        stream << 'b1= %s\n' % chk_num(values(2))
        stream << 'x1= %s\n' % chk_num(values(3))
        stream << 'xm= %s\n' % chk_num(values(4))
        stream << 'c0= %s\n' % chk_num(values(5))
        stream << 'y0= %s\n' % chk_num(values(6))
        stream << 'exp= %s\n' % chk_num(values(7))

        stream << separator
        stream << '* 3. Vault\n'
        stream << separator

        values = self.vault_M.get_row(1, 1)
        stream << '%s\n' % (chk_num(values(0), 1))

        try:
            if int(values(0)) == 1:
                stream << 'a1= %s\n' % values(1)
                stream << 'b1= %s\n' % values(2)
                stream << 'x1= %s\n' % values(3)
                stream << 'c1= %s\n' % values(4)
            else:
                stream << '%s\t%s\n' % (values(5), values(9))
                stream << '%s\t%s\n' % (values(6), values(10))
                stream << '%s\t%s\n' % (values(7), values(11))
                stream << '%s\t%s\n' % (values(8), values(12))
        except:  # noqa: E722
            stream << 'a1= 0\n'
            stream << 'b1= 0\n'
            stream << 'x1= 0\n'
            stream << 'c1= 0\n'

        stream << separator
        stream << '* 4. Cells distribution\n'
        stream << separator
        values = self.cellsDistr_M.get_row(1, 1)
        stream << '%s\n' % chk_num(values(0), 1)

        try:
            if int(values(0)) == 1:
                stream << '%s\n' % values(3)

            elif int(values(0)) == 2 or int(values(0)) == 3:
                stream << '%s\n' % values(1)
                stream << '%s\n' % values(3)

            elif int(values(0)) == 4:
                num_lines = self.cellsDistr_M.num_rows_for_config(1)

                stream << '%s\n' % num_lines

                for it in range(0, num_lines):
                    values = self.cellsDistr_M.get_row(1, it + 1)
                    stream << '%s\t%s\n' % (it + 1, values(2))
        except:  # noqa: E722
            stream << '0\n'

        stream.flush()
        out_file.close()

        if for_proc is False:
            # Then we need to set the right file version
            self.set_file_version('1.6')
