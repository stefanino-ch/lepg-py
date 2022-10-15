"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
import os
import platform

from ConfigReader.ConfigReader import ConfigReader
from subprocess import Popen, PIPE


class ProcRunner:
    """
    :class: Does take care about the data handling for the executables
            for processing.
    """
    __className = 'ProcRunner'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self, proc_out_w):
        """
        :method: Class initialization
        :param proc_out_w: The instance of the window where the output of the
                           processor shall be written to
        """
        logging.debug(self.__className+'.__init__')

        self.userInfo = proc_out_w
        self.config_reader = ConfigReader()

    def run_pre_proc(self):
        """
        :method: Does all the needed setups to run the pre-processor.
        """
        logging.debug(self.__className+'.run_pre_proc')

        pre_proc = self.config_reader.get_pre_proc_path_name()

        # For Linux make sure x flag is set
        if platform.system() == 'Linux'\
                or platform.system() == 'Darwin':
            os.chmod(pre_proc, 0o744)

        set_path_cmd = 'cd ' + self.config_reader.get_pre_proc_directory()

        args = [set_path_cmd, pre_proc]
        self.run_command(args)

    def pre_proc_configured(self):
        """
        :method: Checks if
                 The configured pre proc path name string is >0 chars
                 The file the configured proc path name points really to a file
        :returns: True if both checks above are valid, False else
        """
        logging.debug(self.__className+'.pre_proc_configured')

        path_name = self.config_reader.get_pre_proc_path_name()

        if len(path_name) > 0:
            if os.path.isfile(path_name) is True:
                return True
            else:
                return False
        else:
            return False

    def run_proc(self):
        """
        :method: Does all the needed setups to run the processor.
        """
        logging.debug(self.__className+'.run_proc')

        proc = self.config_reader.get_proc_path_name()

        # For Linux make sure x flag is set
        if platform.system() == 'Linux'\
                or platform.system() == 'Darwin':
            os.chmod(proc, 0o744)

        set_path_cmd = 'cd ' + self.config_reader.get_proc_directory()

        args = [set_path_cmd, proc]
        self.run_command(args)

    def proc_configured(self):
        """
        :method: Checks if
                 The configured proc path name string is >0 chars
                 The file the configured proc path name points really to a file
        :returns: True if both checks above are valid, False else
        """
        logging.debug(self.__className+'.proc_configured')

        path_name = self.config_reader.get_proc_path_name()

        if len(path_name) > 0:
            if os.path.isfile(path_name) is True:
                return True
            else:
                return False
        else:
            return False

    def run_command(self, cmds):
        """
        :method: Does finally execute all the commands to run the processor
        :param cmds: A list of commands to be executed
        """

        for cmd in cmds:
            logging.debug(self.__className+'.run_command ' + cmd)

        if platform.system() == "Windows":
            process = Popen('cmd.exe', stdin=PIPE, stdout=PIPE, stderr=PIPE,
                            shell=False, encoding='utf8')
        elif platform.system() == "Linux":
            process = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE,
                            shell=False, encoding='utf8')
        elif platform.system() == "Darwin":
            process = Popen('/bin/zsh', stdin=PIPE, stdout=PIPE, stderr=PIPE,
                            shell=False, encoding='utf8')
        else:
            logging.error("Sorry, your operating system is not supported yet")
            return

        for cmd in cmds:
            process.stdin.write(cmd + "\n")
        process.stdin.close()

        while True:
            output = process.stdout.readline() + process.stderr.readline()

            if output == '' and process.poll() is not None:
                # TODO: Linux does not display path where files are saved
                self.userInfo.append_text(_('proc_terminating_msg'))
                break

            if output:
                logging.debug(self.__className+'.run_command '
                              + output.strip())
                self.userInfo.append_text(output.strip())

        return