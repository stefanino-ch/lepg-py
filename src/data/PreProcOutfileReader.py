"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
import os

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from ConfigReader.ConfigReader import ConfigReader
from data.FileHelpers import split_line


class PreProcOutfileReader:
    """
    :class: Supports the reading of the output file *geometry-out.txt* created
            by the pre-processor.
    """

    __className = 'PreProcOutfileReader'
    '''
    :attr: Does help to indicate the source of the log messages
    '''
    __file_path_name = ''
    '''
    :attr: Full path and name of the data file currently in use
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')

        self.config_reader = ConfigReader()

    def __valid_file(self, file_path_name):
        """
        :method: Checks if a file can be opened and contains a valid title
                 and known version number
        :param file_path_name: the name of the file to be checked
        """
        logging.debug(self.__className + '.valid_file')

        in_file = QFile(file_path_name)
        if in_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(in_file)
        else:
            logging.error(self.__className
                          + 'File cannot be opened '
                          + file_path_name)
            return False

        title_ok = False
        version_ok = False
        line_counter = 0

        while ((stream.atEnd() is not True)
               and not (title_ok and version_ok)
               and line_counter < 5):
            line = stream.readLine()

            if line.find('1.6') >= 0:
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

            self.__file_path_name = ''

        return version_ok and title_ok

    def __read_file(self):
        """
        :method: Reads the data file created by the pre-processor saves the
                 data in a double list.

        :returns: Data read from the file.
        :rtype:  List of rows, each row is described as a list of columns
        :returns: numCells
        :rtype: int
        """
        logging.debug(self.__className + '.__read_file')

        in_file = QFile(self.__file_path_name)
        in_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(in_file)

        ##############################
        # Over read file header
        # This is done by counting the number of *** lines
        counter = 0
        while counter < 5:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1

        # over read title
        stream.readLine()

        # There's no indication about the number of lines
        # We first read all into the memory
        line_array = []
        valid_data = True

        while valid_data:
            line = stream.readLine()

            if line.find('***************') >= 0:
                valid_data = False
            else:
                line_array.append(split_line(line))

        for i in range(2):
            stream.readLine()

        values = split_line(stream.readLine())
        num_cells = values[1]

        ##############################
        # Cleanup
        in_file.close()

        return line_array, num_cells

    def open_read_file(self, read_from_pre_proc_dir=False):
        """
        :method: File Open dialog handling.
                 Checks if the file header specifies a valid file
        :param read_from_pre_proc_dir: Set this to True if the file in the
                 configured pre-proc dir shall be read.

        :returns: Data read from the file.
        :rtype:  List of rows, each row is described as a list of columns
        :returns: numCells
        :rtype: int
        """
        logging.debug(self.__className + '.open_read_file')

        if read_from_pre_proc_dir is True:
            self.__file_path_name = \
                os.path.join(self.config_reader.get_pre_proc_directory(),
                             'geometry-out.txt')
            if not os.path.isfile(self.__file_path_name):
                msg_box = QMessageBox()
                msg_box.setWindowTitle(_('Ups!'))
                msg_box.setText(_('Either the file does not exist,\n'
                                  'or the pre-processor location\n'
                                  'is not setup.\n'
                                  '(Setup->Both Processors)'))
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()
                return [], 0

        else:
            file_name = QFileDialog.getOpenFileName(
                            None,
                            _('Open Pre-Proc file'),
                            "",
                            "Pre-Proc Files (*.txt);;All Files (*)")

            if file_name != ('', ''):
                # User has really selected a file, if it had aborted
                # the dialog an empty tuple is returned
                if self.__valid_file(file_name[0]):
                    self.__file_path_name = file_name[0]

        if self.__file_path_name != '':
            file_data, num_cells = self.__read_file()
        else:
            file_data = []
            num_cells = 0

        return file_data, num_cells
