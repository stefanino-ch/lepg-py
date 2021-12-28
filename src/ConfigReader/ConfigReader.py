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
    :class: Does all the necessary work to read and save global program configurations.
    """

    def __init__(self):
        """
        :method: Constructor
        """
        super().__init__()

        # Variables and instances used across the class
        self.__config_file_name_path = ""
        self.__language = ""
        self.__pre_proc_directory = ""
        self.__lep_directory = ""
        self.__pre_proc_path_name = ""

        # TODO: convert this to boolean
        self.__pre_proc_show_outline = ''
        self.__proc_path_name = ""

        # TODO: convert this to boolean
        self.__check_for_updates = ''
        self.__track_branch = ''
        self.__parser = configparser.ConfigParser()

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
            self.__parser.read_file(openFile)

            if not self.__parser.has_section('Defaults'):
                self.__parser.add_section('Defaults')

            try:
                self.__language = self.__parser.get('Defaults',
                                                    'Language')
            except configparser.Error:
                # Value does not exist
                self.__language = "en"

            try:
                self.__pre_proc_directory = \
                    self.__parser.get('Defaults',
                                      'PreProcDirectory')
            except configparser.Error:
                # Value does not exist
                self.__pre_proc_directory = ""

            try:
                self.__lep_directory = self.__parser.get('Defaults',
                                                         'ProcDirectory')
            except configparser.Error:
                # Value does not exist
                self.__lep_directory = ""

            try:
                self.__pre_proc_path_name = \
                    self.__parser.get('Defaults',
                                      'PreProcPathName')
            except configparser.Error:
                # Value does not exist
                self.__pre_proc_path_name = ""

            try:
                self.__pre_proc_show_outline = \
                    self.__parser.get('Defaults',
                                      'PreProcShowOutline')
            except configparser.Error:
                # Value does not exist
                self.__pre_proc_show_outline = "yes"

            try:
                self.__proc_path_name = \
                    self.__parser.get('Defaults',
                                      'ProcPathName')
            except configparser.Error:
                # Value does not exist
                self.__proc_path_name = ""

            try:
                self.__check_for_updates = \
                    self.__parser.get('Defaults',
                                      'CheckForUpdates')
            except configparser.Error:
                # Value does not exist
                self.__check_for_updates = 'yes'

            try:
                self.__track_branch = self.__parser.get('Defaults',
                                                        'TrackBranch')
            except configparser.Error:
                # Value does not exist
                self.__track_branch = 'stable'

            openFile.close()

    def write_config_file(self):
        """
        :method: Write all configuration options in the config file

        Options changed during program execution must be written back with
        set… methods prior to write the config file. Usually you won't need to
        call this method, as every set… method does trigger immediately a
        write operation as well.
        """
        config_file = open(self.__configFilePathName, 'w')
        self.__parser.set('Defaults',
                          'Language',
                          self.__language)
        self.__parser.set('Defaults',
                          'PreProcDirectory',
                          self.__pre_proc_directory)
        self.__parser.set('Defaults',
                          'PreProcShowOutline',
                          self.__pre_proc_show_outline)
        self.__parser.set('Defaults',
                          'ProcDirectory',
                          self.__lep_directory)
        self.__parser.set('Defaults',
                          'PreProcPathName',
                          self.__pre_proc_path_name)
        self.__parser.set('Defaults',
                          'ProcPathName',
                          self.__proc_path_name)
        self.__parser.set('Defaults',
                          'CheckForUpdates',
                          self.__check_for_updates)
        self.__parser.set('Defaults',
                          'TrackBranch',
                          self.__track_branch)

        self.__parser.write(config_file)
        config_file.close()

    def get_language(self):
        """
        :method: Returns language info e.g. en
        """
        return self.__language

    def set_language(self, lang):
        """
        :method: Set the language info
        :param lang: language string e.g. en, de
        """
        self.__language = lang
        self.write_config_file()

    def get_pre_proc_directory(self):
        """
        :method: Returns the directory where the Pre-Processor resides
        """
        return self.__pre_proc_directory

    def set_pre_proc_directory(self, directory):
        """
        :method: Set the PreProcessor directory
        :param directory: Directory string
        """
        self.__pre_proc_directory = directory
        self.write_config_file()

    def get_proc_directory(self):
        """
        :method: Returns the directory where the Processor resides
        """
        return self.__lep_directory

    def set_proc_directory(self, directory):
        """
        :method: Set the Processor directory
        :param directory: Directory string
        """
        self.__lep_directory = directory
        self.write_config_file()

    def get_pre_proc_path_name(self):
        """
        :method: Return the path/ and name string for the PreProcessor
        """
        return self.__pre_proc_path_name

    def set_pre_proc_path_name(self, path_name):
        """
        :method: Sets the path/ and name string for the pre-processor
        :param path_name: Full path and name of the pre-processor executable
        """
        self.__pre_proc_path_name = path_name

        # At the same time we set also the path only information        
        directory = os.path.dirname(os.path.abspath(path_name))
        self.set_pre_proc_directory(directory)
        self.write_config_file()

    def get_proc_path_name(self):
        """
        :method: Return the path/ and name string for the Processor
        """
        return self.__proc_path_name

    def set_pre_proc_show_outline(self, show):
        """
        :method: Sets the info if the wing outline shall be displayed/ updated
                 automatically after processing.
        :param show: yes or no
        """
        self.__pre_proc_show_outline = show

    def get_pre_proc_show_outline(self):
        """
        :method: Return the info if the outline shall be displayed/ updated
                 automatically after processing.
        """
        return self.__pre_proc_show_outline

    def set_proc_path_name(self, path_name):
        """
        :method: Set the path/ and name string for the lep processor
        :param path_name: Full path and name of the Processor executable
        """
        self.__proc_path_name = path_name

        # At the same time we set also the path only information        
        directory = os.path.dirname(os.path.abspath(path_name))
        self.set_proc_directory(directory)

    def get_check_for_updates(self):
        """
        :method: Returns the setting if we should check for updates
        """
        return self.__check_for_updates

    def set_check_for_updates(self, check_state):
        """
        :method: Set the check for updates flag
        :param check_state: yes/ no handled as string.
        """
        self.__check_for_updates = check_state
        self.write_config_file()

    def get_track_branch(self):
        """
        :method: Returns the name of the track branch. This could be stable or latest
        """
        return self.__track_branch

    def set_track_branch(self, branch):
        """
        :method: Set the name of the branch to check for updates.
        :param branch: Branch name. Valid names are stable and latest.
        """
        self.__track_branch = branch
        self.write_config_file()
