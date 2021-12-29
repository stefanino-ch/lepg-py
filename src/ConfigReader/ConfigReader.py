"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

from __future__ import annotations
import os
import configparser

from PyQt5.QtCore import QObject
from Singleton.Singleton import Singleton


class ConfigReader(QObject, metaclass=Singleton):
    """
    :class: Does all the necessary work to read and save global program
            configurations.
    """
    LANGUAGE = 'language'

    PRE_PROC_PATH_NAME = 'pre_proc_path_name'
    PRE_PROC_SHOW_OUTLINE = 'pre_proc_show_outline'

    PROC_PATH_NAME = 'proc_path_name'

    CHECK_FOR_UPDATES = 'check_for_updates'
    TRACKING_BRANCH = 'tracking_branch'

    def __init__(self):
        """
        :method: Constructor
        """
        super().__init__()

        # Variables and instances used across the class
        self.__config_file_path_name = ""
        self.__language = ""

        self.__pre_proc_path_name = ""
        self.__pre_proc_path = ""
        self.__pre_proc_show_outline = True  # type: bool

        self.__proc_path_name = ""
        self.__proc_path = ""

        self.__check_for_updates = True  # type: bool
        self.__track_branch = ''

        self.config_parser = configparser.ConfigParser()

        # Detect the current application path
        self.__configFilePathName = os.path.join(os.getcwd(), 'configFile.txt')

        if os.path.exists(self.__configFilePathName):
            self.read_config_file()
        elif IOError:
            # Just create an empty file
            config_file = open(self.__configFilePathName, 'w')
            config_file.close()
            self.read_config_file()

    def read_config_file(self):
        """
        :method: Reads all values from the config file. Does apply hardcoded
                 defaults if a key/ value pair does not exist in the file.
        """
        with open(self.__configFilePathName, 'r+') as openFile:
            self.config_parser.read_file(openFile)

            if not self.config_parser.has_section('Defaults'):
                self.config_parser.add_section('Defaults')

            try:
                self.__language = self.config_parser.get('Defaults',
                                                         self.LANGUAGE)
            except configparser.Error:
                # Value does not exist
                self.__language = "en"

            try:
                self.__pre_proc_path_name = \
                    self.config_parser.get('Defaults',
                                           self.PRE_PROC_PATH_NAME)
                # At the same time we set also the path only information
                directory = os.path.dirname(
                    os.path.abspath(self.__pre_proc_path_name))
                self.__pre_proc_path = directory

            except configparser.Error:
                # Value does not exist
                self.__pre_proc_path_name = ""
                self.__pre_proc_path = ""

            try:
                self.__pre_proc_show_outline = \
                    self.config_parser.getboolean('Defaults',
                                                  self.PRE_PROC_SHOW_OUTLINE)
            except configparser.Error:
                # Value does not exist
                self.__pre_proc_show_outline = True

            try:
                self.__proc_path_name = \
                    self.config_parser.get('Defaults',
                                           self.PROC_PATH_NAME)

                # At the same time we set also the path only information
                directory = os.path.dirname(
                    os.path.abspath(self.__proc_path_name))
                self.__proc_path = directory

            except configparser.Error:
                # Value does not exist
                self.__proc_path_name = ""

            try:
                self.__check_for_updates = \
                    self.config_parser.getboolean('Defaults',
                                                  self.CHECK_FOR_UPDATES)
            except configparser.Error:
                # Value does not exist
                self.__check_for_updates = True

            try:
                self.__track_branch = self.config_parser.get('Defaults',
                                                             self.TRACKING_BRANCH)
            except configparser.Error:
                # Value does not exist
                self.__track_branch = 'stable'

            openFile.close()

    def write_config_file(self):
        """
        :method: Write all configuration options in the config file.

        Options changed during program execution must be written back with
        set… methods prior to write the config file. Usually you won't need to
        call this method, as every set… method does trigger immediately a
        write operation as well.
        """
        config_file = open(self.__configFilePathName, 'w')
        self.config_parser.set('Defaults',
                               self.LANGUAGE,
                               self.__language)
        self.config_parser.set('Defaults',
                               self.PRE_PROC_PATH_NAME,
                               self.__pre_proc_path_name)
        self.config_parser.set('Defaults',
                               self.PRE_PROC_SHOW_OUTLINE,
                               str(self.__pre_proc_show_outline))
        self.config_parser.set('Defaults',
                               self.PROC_PATH_NAME,
                               self.__proc_path_name)
        self.config_parser.set('Defaults',
                               self.CHECK_FOR_UPDATES,
                               str(self.__check_for_updates))
        self.config_parser.set('Defaults',
                               self.TRACKING_BRANCH,
                               self.__track_branch)

        self.config_parser.write(config_file)
        config_file.close()

    def set_language(self, lang):
        """
        :method: Set the language info.
        :param lang: language string e.g. en, de
        """
        self.__language = lang
        self.write_config_file()

    def get_language(self):
        """
        :method: Returns language info e.g. en.
        """
        return self.__language

    def set_pre_proc_path_name(self, path_name):
        """
        :method: Sets the path/ and name string for the pre-processor.
        :param path_name: Full path and name of the pre-processor executable.
        """
        self.__pre_proc_path_name = path_name

        # At the same time we set also the path only information
        directory = os.path.dirname(os.path.abspath(path_name))
        self.__pre_proc_path = directory

        self.write_config_file()

    def get_pre_proc_path_name(self):
        """
        :method: Return the path/ and name string for the PreProcessor.
        """
        return self.__pre_proc_path_name

    def get_pre_proc_directory(self):
        """
        :method: Returns the directory where the Pre-Processor resides.
        """
        return self.__pre_proc_path

    def set_proc_path_name(self, path_name):
        """
        :method: Set the path/ and name string for the lep processor.
        :param path_name: Full path and name of the Processor executable.
        """
        self.__proc_path_name = path_name

        # At the same time we set also the path only information
        directory = os.path.dirname(os.path.abspath(path_name))
        self.__proc_path = directory

        self.write_config_file()

    def get_proc_path_name(self):
        """
        :method: Return the path/ and name string for the Processor.
        """
        return self.__proc_path_name

    def get_proc_directory(self):
        """
        :method: Returns the directory where the Processor resides.
        """
        return self.__proc_path

    def set_pre_proc_show_outline(self, show):
        """
        :method: Sets the info if the wing outline shall be displayed/ updated
                 automatically after processing.
        :param show: True or False
        """
        self.__pre_proc_show_outline = show
        self.write_config_file()

    def get_pre_proc_show_outline(self):
        """
        :method: Return the info if the outline shall be displayed/ updated
                 automatically after processing.
        """
        return self.__pre_proc_show_outline

    def set_check_for_updates(self, check_state):
        """
        :method: Set the check for updates flag.
        :param check_state: yes/ no handled as string.
        """
        self.__check_for_updates = check_state
        self.write_config_file()

    def get_check_for_updates(self):
        """
        :method: Returns the setting if we should check for updates.
        """
        return self.__check_for_updates

    def set_track_branch(self, branch):
        """
        :method: Set the name of the branch to check for updates.
        :param branch: Branch name. Valid names are stable and latest.
        """
        self.__track_branch = branch
        self.write_config_file()

    def get_track_branch(self):
        """
        :method: Returns the name of the track branch. This could be
                 stable or latest.
        """
        return self.__track_branch
