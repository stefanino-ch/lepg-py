"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
import logging

from PyQt5.QtCore import Qt, QFile, QTextStream, QObject, pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Singleton.Singleton import Singleton
from data.SqlTableModel import SqlTableModel

from ConfigReader.ConfigReader import ConfigReader
from data.Database import Database

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

    def __init__(self, parent=None):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')

        self.__fileSaved = True

        self.db = Database()
        self.db.openConnection()

        super().__init__()

        self.leadingE_M = self.LeadingEdgeModel()
        self.leadingE_M.dataChanged.connect(self.data_edit)

        self.trailingE_M = self.TrailingEdgeModel()
        self.trailingE_M.dataChanged.connect(self.data_edit)

        self.vault_M = self.VaultModel()
        self.vault_M.dataChanged.connect(self.data_edit)

        self.gen_M = self.GenModel()
        self.gen_M.dataChanged.connect(self.data_edit)

        self.cellsDistr_M = self.CellsDistrModel()
        self.cellsDistr_M.dataChanged.connect(self.data_edit)

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
        :method: Does set the file version the data store shall work with.
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
                 and known version number.
        :param file_name: the name of the file to be checked
        """
        logging.debug(self.__className + '.valid_file')

        in_file = QFile(file_name)
        if in_file.open(QFile.ReadOnly | QFile.Text):
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
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

            self.set_file_name('')
            self.set_file_version('')

        return version_ok and title_ok

    def open_file(self):
        """
        :method: Checks for unsaved data, and appropriate handling.
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
        logging.debug(self.__className + '.save_file')

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
                # User has really selected a file, if it would have aborted
                # the dialog an empty tuple is retured
                self.set_file_name(file_name[0])
                self.write_file()
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
        logging.debug(self.__className+'.read_file')

        in_file = QFile(self.get_file_name())
        in_file.open(QFile.ReadOnly | QFile.Text)
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

        logging.debug(self.__className+'.read_file: Wing name')
        self.gen_M.set_num_rows_for_config(1, 1)
        name = stream.readLine()
        self.gen_M.update_row(1, 1, name)

        # 1. Leading edge
        logging.debug(self.__className+'.read_file: Leading edge')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()

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
        logging.debug(self.__className+'.read_file: Trailing edge')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()

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
        self.trailingE_M.updateRow(1, 1, one, two[1], thr[1], fou[1], fiv[1],
                                   six[1], sev[1], eig[1])

        # 3. Vault
        logging.debug(self.__className+'.read_file: vault')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()

        self.vault_M.set_num_configs(0)
        self.vault_M.set_num_configs(1)
        vtype = int(rem_tab_space_quot(stream.readLine()))

        one = split_line(stream.readLine())
        two = split_line(stream.readLine())
        thr = split_line(stream.readLine())
        fou = split_line(stream.readLine())

        if vtype == 1:
            self.vault_M.updateRow(1, 1, vtype, one[1], two[1], thr[1],
                                   fou[1], 0, 0, 0, 0, 0, 0, 0, 0)

        else:
            self.vault_M.updateRow(1, 1, vtype, 0, 0, 0, 0, one[0], two[0],
                                   thr[0], fou[0], one[1], two[1],
                                   thr[1], fou[1])

        # 4. Cells distribution
        logging.debug(self.__className+'.read_file: Cells')
        for i in range(3):  # @UnusedVariable
            line = stream.readLine()

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
        :method: Writes all the values into a data file.
        :warning: Filename must have been set already before, unless the
                  file shall be written for the PreProcessor.
        :param for_proc: Set this to True if the file must be saved in the
                        directory where the PreProcessor resides.
        """
        separator = '***************************************************\n'

        logging.debug(self.__className+'.write_file')
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

        if not out_file.open(QFile.ReadWrite | QFile.Text):
            logging.error(self.__className+'.write_file '
                          + out_file.errorString())

            msg_box = QMessageBox()
            msg_box.setWindowTitle(_("File save error"))
            msg_box.setText(_('File can not be saved: ')
                            + out_file.errorString())
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            return

        # File is open, start writing
        stream = QTextStream(out_file)
        stream.setCodec('UTF-8')

        stream << separator
        stream << 'LEPARAGLIDING\n'
        stream << 'GEOMETRY PRE-PROCESSOR         V1.6\n'
        stream << separator

        values = self.gen_M.getRow(1, 1)
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
        values = self.trailingE_M.getRow(1, 1)
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
                stream << '%s\n' % values(3)

                for it in range(0, int(values(3))):
                    values = self.cellsDistr_M.get_row(1, it + 1)
                    stream << '%s\t%s\n' % (it + 1, values(2))
        except:  # noqa: E722
            stream << '0\n'

        stream.flush()
        out_file.close()

        if for_proc is False:
            # Then we need to set the right file version
            self.set_file_version('1.6')

    class CellsDistrModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding all for cells distribution.
        """
        __className = 'CellsDistrModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        DistrTypeCol = 1
        CoefCol = 2
        WidthCol = 3
        NumCellsCol = 4
        ConfigNumCol = 5

        def __init__(self, parent=None):  # @UnusedVariable
            """
            :method: Constructor
            """
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.create_table()
            self.setTable("PreProcCellsDistr")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(0, Qt.Horizontal, _("Cell Num"))
            self.setHeaderData(2, Qt.Horizontal, _("Coef"))
            self.setHeaderData(3, Qt.Horizontal, _("Width"))
            self.setHeaderData(4, Qt.Horizontal, _("Num cells"))

            self.set_num_rows_for_config(1, 1)

        def create_table(self):
            """
            :method: Creates initially the table
            """
            logging.debug(self.__className+'.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists PreProcCellsDistr;")
            query.exec("create table if not exists PreProcCellsDistr ("
                       "OrderNum INTEGER, "
                       "DistrType INTEGER, "
                       "Coef REAL, "
                       "Width REAL, "
                       "NumCells INTEGER, "
                       "ConfigNum INTEGER, "
                       "ID INTEGER PRIMARY KEY);")

        def update_row(self, config_num, order_num, distr_type, coef, width,
                       numCells):
            """
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            """
            logging.debug(self.__className+'.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE PreProcCellsDistr SET "
                          "DistrType = :distr_type, "
                          "Coef = :coef, "
                          "Width = :width, "
                          "NumCells = :num_cells "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":distr_type", distr_type)
            query.bindValue(":coef", coef)
            query.bindValue(":width", width)
            query.bindValue(":num_cells", numCells)
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)

            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def get_row(self, config_num, order_num):
            """
            :method: Reads values back from the internal database for a
                     config and order number
            :param config_num: Starting with 1.
            :param order_num: Starting with 1.
            :return: values read from internal database
            """
            logging.debug(self.__className+'.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "DistrType, "
                          "Coef, "
                          "Width, "
                          "NumCells "
                          "FROM PreProcCellsDistr "
                          "WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            query.next()
            return query.value

        def update_type(self, config_num, order_num, distr_type):
            logging.debug(self.__className+'.update_type')

            query = QSqlQuery()
            query.prepare("UPDATE PreProcCellsDistr SET "
                          "DistrType= :typeN "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", distr_type)

            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def get_type(self, config_num, order_num):
            """
            :method: Reads type value back from the internal database for
                     a config and order number
            :param config_num: Starting with 1.
            :param order_num: Starting with 1.
            :return: type value
            """
            logging.debug(self.__className+'.get_type')

            query = QSqlQuery()
            query.prepare("Select "
                          "DistrType "
                          "FROM PreProcCellsDistr "
                          "WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            query.next()

            if query.value(0) == '':
                return 1
            else:
                return query.value(0)

    class GenModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding the general data
        """
        __className = 'GenModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        WingNameCol = 1
        ConfigNumCol = 2

        def __init__(self, parent=None):  # @UnusedVariable
            """
            :method: Constructor
            """
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.create_table()
            self.setTable("PreProcGen")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Wing name"))

            self.set_num_rows_for_config(1, 1)

        def create_table(self):
            """
            :method: Creates initially the table
            """
            logging.debug(self.__className+'.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists PreProcGen;")
            query.exec("create table if not exists PreProcGen ("
                       "OrderNum INTEGER, "
                       "WingN TEXT, "
                       "ConfigNum INTEGER, "
                       "ID INTEGER PRIMARY KEY);")

        def update_row(self, config_num, order_num, wing_n):
            """
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitly explained here as
                     they should be well known.
            """
            logging.debug(self.__className+'.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE PreProcGen SET "
                          "WingN = :wing_n "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":wing_n", wing_n)
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)

            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def getRow(self, config_num, order_num):
            """
            :method: Reads values back from the internal database for a config
                     and order number
            :param config_num: Starting with 1.
            :param ordergNum: Starting with 1.
            :return: values read from internal database
            """
            logging.debug(self.__className+'.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "WingN "
                          "FROM PreProcGen "
                          "WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            query.next()
            return query.value

    class LeadingEdgeModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding all data for leading
                edge definition.
        """
        __className = 'LeadingEdgeModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        TypeCol = 1
        aOneCol = 2
        bOneCol = 3
        xOneCol = 4
        xTwoCol = 5
        xmCol = 6
        cZeroOneCol = 7
        exOneCol = 8
        cZeroTwoCol = 9
        exTwoCol = 10
        ConfigNumCol = 11

        def __init__(self, parent=None):  # @UnusedVariable
            """
            :method: Constructor
            """
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.create_table()
            self.setTable("LeadingEdge")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Type"))
            self.setHeaderData(2, Qt.Horizontal, _("a1 [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("b1 [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("x1 [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("x2 [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("xm [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("c01 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("ex1 [coef]"))
            self.setHeaderData(9, Qt.Horizontal, _("c02 [coef]"))
            self.setHeaderData(10, Qt.Horizontal, _("ex2 [coef]"))

            self.set_num_rows_for_config(1, 1)

        def create_table(self):
            """
            :method: Creates initially the table
            """
            logging.debug(self.__className+'.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists LeadingEdge;")
            query.exec("create table if not exists LeadingEdge ("
                       "OrderNum INTEGER, "
                       "Type INTEGER, "
                       "a_one REAL, "
                       "b_one REAL, "
                       "x_one INTEGER, "
                       "x_two INTEGER, "
                       "xm INTEGER, "
                       "c_zero_one INTEGER, "
                       "ex_one REAL, "
                       "c_zero_two INTEGER, "
                       "ex_two REAL, "
                       "ConfigNum INTEGER, "
                       "ID INTEGER PRIMARY KEY);")

        def update_row(self, config_num, order_num, type_num,
                       a_one, b_one,
                       x_one, x_two, xm, c_zero_one, ex_one,
                       c_zero_two, ex_two):
            """
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            """
            logging.debug(self.__className+'.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE LeadingEdge SET "
                          "Type= :typeN, "
                          "a_one= :a_one, "
                          "b_one= :b_one, "
                          "x_one= :x_one, "
                          "x_two= :x_two, "
                          "xm= :xm, "
                          "c_zero_one= :c_zero_one, "
                          "ex_one= :ex_one, "
                          "c_zero_two= :c_zero_two, "
                          "ex_two= :ex_two "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", type_num)
            query.bindValue(":a_one", a_one)
            query.bindValue(":b_one", b_one)
            query.bindValue(":x_one", x_one)
            query.bindValue(":x_two", x_two)
            query.bindValue(":xm", xm)
            query.bindValue(":c_zero_one", c_zero_one)
            query.bindValue(":ex_one", ex_one)
            query.bindValue(":c_zero_two", c_zero_two)
            query.bindValue(":ex_two", ex_two)
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def get_row(self, config_num, order_num):
            """
            :method: Reads values back from the internal database for a
                     config and order number
            :param config_num: Starting with 1.
            :param order_num: Starting with 1.
            :return: values read from internal database
            """
            logging.debug(self.__className+'.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Type, "
                          "a_one, "
                          "b_one, "
                          "x_one, "
                          "x_two, "
                          "xm, "
                          "c_zero_one, "
                          "ex_one, "
                          "c_zero_two, "
                          "ex_two "
                          "FROM LeadingEdge "
                          "WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            query.next()
            return query.value

    class TrailingEdgeModel(SqlTableModel, metaclass=Singleton):
        """
        :class: Provides a SqlTableModel holding all data for trailing
                edge definition
        """
        __className = 'TrailingEdgeModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        TypeCol = 1
        aOneCol = 2
        bOneCol = 3
        xOneCol = 4
        xmCol = 5
        cZeroCol = 6
        yZeroCol = 7
        expCol = 8
        ConfigNumCol = 9

        def __init__(self, parent=None):  # @UnusedVariable
            """
            :method: Constructor
            """
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.create_table()
            self.setTable("TrailingEdge")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(1, Qt.Horizontal, _("Type"))
            self.setHeaderData(2, Qt.Horizontal, _("a1 [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("b1 [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("x1 [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("xm [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("c0 [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("y0 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("exp [coef]"))

            self.set_num_rows_for_config(1, 1)

        def create_table(self):
            """
            :method: Creates initially the table
            """
            logging.debug(self.__className+'.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists TrailingEdge;")
            query.exec("create table if not exists TrailingEdge ("
                       "OrderNum INTEGER, "
                       "Type INTEGER, "
                       "a_one REAL, "
                       "b_one REAL, "
                       "x_one INTEGER, "
                       "xm INTEGER, "
                       "cZero REAL, "
                       "yZero REAL, "
                       "exp REAL, "
                       "ConfigNum INTEGER, "
                       "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, typeNum,
                      aOne, bOne,
                      xOne, xm, cZero, yZero, exp):
            """
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            """
            logging.debug(self.__className+'.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE TrailingEdge SET "
                          "Type= :typeN, "
                          "a_one= :a_one, "
                          "b_one= :b_one, "
                          "x_one= :x_one, "
                          "xm= :xm, "
                          "cZero= :cZero, "
                          "yZero= :yZero, "
                          "exp= :exp "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", typeNum)
            query.bindValue(":a_one", aOne)
            query.bindValue(":b_one", bOne)
            query.bindValue(":x_one", xOne)
            query.bindValue(":xm", xm)
            query.bindValue(":cZero", cZero)
            query.bindValue(":yZero", yZero)
            query.bindValue(":exp", exp)
            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def getRow(self, configNum, order_num):
            '''
            :method: Reads values back from the internal database for a
                     config and order number
            :param configNum: Starting with 1.
            :param order_num: Starting with 1.
            :return: values read from internal database
            '''
            logging.debug(self.__className+'.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Type, "
                          "a_one, "
                          "b_one, "
                          "x_one, "
                          "xm, "
                          "cZero, "
                          "yZero, "
                          "exp "
                          "FROM TrailingEdge "
                          "WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", configNum)
            query.bindValue(":order", order_num)
            query.exec()
            query.next()
            return query.value

    class VaultModel(SqlTableModel, metaclass=Singleton):
        '''
        :class: Provides a SqlTableModel holding all data for the vault
                definition.
        '''
        __className = 'VaultModel'
        '''
        :attr: Does help to indicate the source of the log messages
        '''
        OrderNumCol = 0
        TypeCol = 1
        aOneCol = 2
        bOneCol = 3
        xOneCol = 4
        cOneCol = 5
        rOneRACol = 6
        rTwoRACol = 7
        rThrRACol = 8
        rFouRACol = 9
        aOneRACol = 10
        aTwoRACol = 11
        aThrRACol = 12
        aFouRACol = 13
        ConfigNumCol = 14

        def __init__(self, parent=None):  # @UnusedVariable
            '''
            :method: Constructor
            '''
            logging.debug(self.__className+'.__init__')
            super().__init__()
            self.createTable()
            self.setTable("Vault")
            self.select()
            self.setEditStrategy(QSqlTableModel.OnFieldChange)

            self.setHeaderData(2, Qt.Horizontal, _("a1 [cm]"))
            self.setHeaderData(3, Qt.Horizontal, _("b1 [cm]"))
            self.setHeaderData(4, Qt.Horizontal, _("x1 [cm]"))
            self.setHeaderData(5, Qt.Horizontal, _("c1 [cm]"))
            self.setHeaderData(6, Qt.Horizontal, _("r1 [cm]"))
            self.setHeaderData(7, Qt.Horizontal, _("r2 [cm]"))
            self.setHeaderData(8, Qt.Horizontal, _("r3 [cm]"))
            self.setHeaderData(9, Qt.Horizontal, _("r4 [cm]"))
            self.setHeaderData(10, Qt.Horizontal, _("a1 [deg]"))
            self.setHeaderData(11, Qt.Horizontal, _("a2 [deg]"))
            self.setHeaderData(12, Qt.Horizontal, _("a3 [deg]"))
            self.setHeaderData(13, Qt.Horizontal, _("a4 [deg]"))

            self.set_num_rows_for_config(1, 1)

        def createTable(self):
            '''
            :method: Creates initially the table
            '''
            logging.debug(self.__className+'.create_table')
            query = QSqlQuery()

            query.exec("DROP TABLE if exists Vault;")
            query.exec("create table if not exists Vault ("
                       "OrderNum INTEGER, "
                       "Type INTEGER, "
                       "a_one REAL, "
                       "b_one REAL, "
                       "x_one REAL, "
                       "cOne REAL, "
                       "rOneRA REAL, "
                       "rTwoRA REAL, "
                       "rThrRA REAL, "
                       "rFouRA REAL, "
                       "aOneRA REAL, "
                       "aTwoRA REAL, "
                       "aThrRA REAL, "
                       "aFouRA REAL, "
                       "ConfigNum INTEGER, "
                       "ID INTEGER PRIMARY KEY);")

        def updateRow(self, configNum, orderNum, typeNum,
                      aOne, bOne,
                      xOne, cOne,
                      rOneRA, rTwoRA, rThrRA, rFouRA,
                      aOneRA, aTwoRA, aThreRA, aFouRA):
            """
            :method: Updates a specific row in the database with the values
                     passed. Parameters are not explicitely explained here as
                     they should be well known.
            """
            logging.debug(self.__className+'.update_row')

            query = QSqlQuery()
            query.prepare("UPDATE Vault SET "
                          "Type= :typeN, "
                          "a_one= :a_one, "
                          "b_one= :b_one, "
                          "x_one= :x_one, "
                          "cOne= :cOne, "
                          "rOneRA= :rOneRA, "
                          "rTwoRA= :rTwoRA, "
                          "rThrRA= :rThrRA, "
                          "rFouRA= :rFouRA, "
                          "aOneRA= :aOneRA, "
                          "aTwoRA= :aTwoRA, "
                          "aThrRA= :aThreRA, "
                          "aFouRA= :aFouRA  "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", typeNum)
            query.bindValue(":a_one", aOne)
            query.bindValue(":b_one", bOne)
            query.bindValue(":x_one", xOne)
            query.bindValue(":cOne", cOne)

            query.bindValue(":rOneRA", rOneRA)
            query.bindValue(":rTwoRA", rTwoRA)
            query.bindValue(":rThrRA", rThrRA)
            query.bindValue(":rFouRA", rFouRA)

            query.bindValue(":aOneRA", aOneRA)
            query.bindValue(":aTwoRA", aTwoRA)
            query.bindValue(":aThreRA", aThreRA)
            query.bindValue(":aFouRA", aFouRA)

            query.bindValue(":config", configNum)
            query.bindValue(":order", orderNum)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def get_row(self, config_num, order_num):
            """
            :method: Reads values back from the internal database for a
                     config and order number
            :param config_num: Starting with 1.
            :param order_num: Starting with 1.
            :return: values read from internal database
            """
            logging.debug(self.__className+'.get_row')

            query = QSqlQuery()
            query.prepare("Select "
                          "Type, "
                          "a_one, "
                          "b_one, "
                          "x_one, "
                          "cOne, "
                          "rOneRA, "
                          "rTwoRA, "
                          "rThrRA, "
                          "rFouRA, "
                          "aOneRA, "
                          "aTwoRA, "
                          "aThrRA, "
                          "aFouRA "
                          "FROM Vault "
                          "WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            query.next()
            return query.value

        def update_type(self, config_num, order_num, type_num):
            logging.debug(self.__className+'.update_type')

            query = QSqlQuery()
            query.prepare("UPDATE Vault SET "
                          "Type= :typeN "
                          "WHERE (ConfigNum = :config AND OrderNum = :order);")
            query.bindValue(":typeN", type_num)

            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            # to a select() to assure the model is updated properly
            self.select()

        def get_type(self, config_num, order_num):
            """
            :method: Reads type value back from the internal database for a
                     config and order number.
            :param config_num: Starting with 1.
            :param order_num: Starting with 1.
            :return: type value
            """
            logging.debug(self.__className+'.get_type')

            query = QSqlQuery()
            query.prepare("Select "
                          "Type "
                          "FROM Vault "
                          "WHERE (ConfigNum = :config AND OrderNum = :order)")
            query.bindValue(":config", config_num)
            query.bindValue(":order", order_num)
            query.exec()
            query.next()
            return query.value(0)
