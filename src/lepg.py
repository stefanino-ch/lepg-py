"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import os
from os import path
import webbrowser

import gettext
import logging.config
import sys
from packaging import version

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, \
    QMessageBox, QMenu

from __init__ import __version__
from VersionCheck.VersionCheck import VersionCheck

from ConfigReader.ConfigReader import ConfigReader
from DataStores.PreProcModel import PreProcModel
from DataStores.ProcModel import ProcModel

from gui.DataStatusOverview import DataStatusOverview
from gui.PreProcData import PreProcData
from gui.PreProcWingOutline import PreProcWingOutline
from gui.BasicData import BasicData
from gui.Geometry import Geometry
from gui.Airfoils import Airfoils
from gui.RibHoles import RibHoles
from gui.HelpAbout import HelpAbout
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from Processors.ProcRunner import ProcRunner
from gui.ProcessorOutput import ProcessorOutput
from gui.AnchorPoints import AnchorPoints
from gui.SkinTension import SkinTension
from gui.SeewingAllowances import SeewingAllowances
from gui.Marks import Marks
from gui.GlobalAoA import GlobalAoA
from gui.Lines import Lines
from gui.Brakes import Brakes
from gui.Ramification import Ramification
from gui.HvVhRibs import HvVhRibs
from gui.ExtradColors import ExtradColors
from gui.IntradColors import IntradColors
from gui.AddRibPoints import AddRibPoints
from gui.ElasticLinesCorr import ElasticLinesCorr
from gui.DxfLayerNames import DxfLayerNames
from gui.MarksTypes import MarksTypes
from gui.JoncsDefinition import JoncsDefinition
from gui.NoseMylars import NoseMylars
from gui.TwoDDxf import TwoDDxfModel
from gui.ThreeDDxf import ThreeDDxfModel
from gui.GlueVent import GlueVent
from gui.SpecWingTip import SpecWingTip
from gui.CalageVar import CalageVar
from gui.ThreeDShaping import ThreeDShaping
from gui.AirfoilThickness import AirfoilThickness
from gui.NewSkinTension import NewSkinTension
from gui.PreProcCellsDistribution import PreProcCellsDistribution
from gui.SetupProcessors import SetupProcessors
from gui.SetupUpdateChecking import SetupUpdateChecking
from PyQt5.Qt import QStatusBar


# TODO: bring windows to front if they are called


class MainWindow(QMainWindow):
    """
    :class: Creates the main window of the application
    """

    __className = 'MainWindow'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self, parent=None):
        """
        :method: Constructor
        """
        # Delete old log file
        self.proc_out_w = None
        self.pre_proc_cells_distr_w = None
        self.pre_proc_wing_outline_w = None
        
        self.delete_logfile()

        # Set up the logger
        # Additional code needed due to pyinstaller. Check doc there.
        bundle_dir = getattr(sys,
                             '_MEIPASS',
                             path.abspath(path.dirname(__file__)))
        path_to_dat = path.abspath(path.join(bundle_dir, 'logger.conf'))

        logging.config.fileConfig(path_to_dat, disable_existing_loggers=False)
        self.logger = logging.getLogger('root')
        # DEBUG
        # INFO
        # WARNING
        # ERROR
        # CRITICAL
        logging.debug(self.__className + '.__init__')

        # Setup languages
        locale_path = 'translations'
        self.config_reader = ConfigReader()

        if self.config_reader.get_language() == "de":
            lang_de = gettext.translation('lepg',
                                          locale_path,
                                          languages=['de'])
            lang_de.install()
        elif self.config_reader.get_language() == "en":
            lang_en = gettext.translation('lepg',
                                          locale_path,
                                          languages=['en'])
            lang_en.install()
        else:
            lang_en = gettext.translation('lepg',
                                          locale_path,
                                          languages=['en'])
            lang_en.install()

        self.ppm = PreProcModel()

        self.pm = ProcModel()

        self.dws = DataWindowStatus()

        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("lepg-py %s" % __version__)
        self.mainMenu = self.menuBar()

        # Build the individual menus
        self.build_file_menu()
        self.build_pre_proc_menu()
        self.build_proc_menu()
        self.build_plan_menu()
        self.build_view_menu()
        self.build_setup_menu()
        self.build_help_menu()

        # Create the status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # VersionCheck
        if self.config_reader.get_check_for_updates() is True:
            version_check = VersionCheck()
            version_check.setBranch(self.config_reader.get_track_branch())

            if version_check.remoteVersionFound():
                remote_version = version_check.getRemoteVersion()
                logging.debug(self.__className
                              + ' Remote Version:   '
                              + remote_version + '\n')
                logging.debug(self.__className
                              + ' Current Version:  '
                              + __version__ + '\n')

                if version.parse(remote_version) > version.parse(__version__):
                    msg_box = QMessageBox()
                    msg_box.setTextFormat(Qt.RichText)
                    msg_box.setWindowTitle(_('Newer version found'))
                    msg_box.setText(_('Current Version: ')
                                    + str(__version__) + '<br>'
                                    + _('Version on remote: ')
                                    + str(remote_version) + '<br>'
                                    + _('Maybe you should consider an update '
                                        'from')
                                    + '<br>'
                                    + ('<a href="https://github.com/stefanino'
                                       '-ch/lepg-py/tree/stable/distribution">'
                                       'Github.com</a>')
                                    + '<br>' + '<br>'
                                    + _('More info about the different '
                                        'versions you will find in the <br>'
                                        'online help: Help-> Online Help')
                                    + '<br>' + '<br>'
                                    + _('Or in Settings-> Update checking'))
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec()
            else:
                logging.error(self.__className
                              + 'Unable to get the update information.\n')
                logging.error(self.__className
                              + 'Error information: '
                              + version_check.getErrorInfo()
                              + '\n')
        else:
            logging.debug(self.__className
                          + ' Update check disabled in config file.\n')

    def build_file_menu(self):
        """
        :method: Builds the complete file menu
        """
        # Define the actions
        file_data_status_act = QAction(_('Show Data Status'), self)
        file_data_status_act.setStatusTip(_('Provides an overview about what '
                                            'data has (not) been saved'))
        file_data_status_act.triggered.connect(self.file_data_status)

        file_restart_act = QAction(_('Restart'), self)
        file_restart_act.setStatusTip(_('Restart the app'))
        file_restart_act.triggered.connect(self.file_restart)

        file_exit_act = QAction(_('Exit'), self)
        file_exit_act.setStatusTip(_('Leave the app'))
        file_exit_act.triggered.connect(self.file_exit)

        # Build the menu
        file_menu = self.mainMenu.addMenu(_('File'))
        file_menu.addAction(file_data_status_act)
        file_menu.addSeparator()
        file_menu.addAction(file_restart_act)
        file_menu.addSeparator()
        file_menu.addAction(file_exit_act)

    def file_data_status(self):
        """
        :method: Opens the File Data Status overview window.
        """
        if self.dws.windowExists('DataStatusOverview') is False:
            self.file_data_status_w = DataStatusOverview()
            self.dws.registerWindow('DataStatusOverview')
            self.mdi.addSubWindow(self.file_data_status_w)
        self.file_data_status_w.show()

    def file_restart(self):
        """
        :method: Restarts the application.
            Thanks to: https://blog.petrzemek.net/2014/03/23/
            restarting-a-python-script-within-itself/
        """
        os.execv(sys.executable, ['python'] + sys.argv)

    def file_exit(self):
        """
        :method: Does all the work to close properly the application.
        """
        logging.debug(self.__className + '.file_exit')
        sys.exit()

    def build_pre_proc_menu(self):
        """
        :method: Builds the complete Pre-Processor menu
        """
        # Define the actions
        pre_proc_open_file_act = QAction(_('Open PreProc File'), self)
        pre_proc_open_file_act.setStatusTip(_('open_preProc_file_desc'))
        pre_proc_open_file_act.triggered.connect(self.pre_proc_open_file)

        pre_proc_save_act = QAction(_('Save PreProc File'), self)
        pre_proc_save_act.setStatusTip(_('save_preProc_file_desc'))
        pre_proc_save_act.triggered.connect(self.pre_proc_save_file)

        pre_proc_save_as_act = QAction(_('Save PreProc File As ..'), self)
        pre_proc_save_as_act.setStatusTip(_('save_preProc_file_as_desc'))
        pre_proc_save_as_act.triggered.connect(self.pre_proc_save_file_as)

        pre_proc_edit_act = QAction(_('Name, LE, TE, Vault'), self)
        pre_proc_edit_act.setStatusTip(_('edit_preProc_data_description'))
        pre_proc_edit_act.triggered.connect(self.pre_proc_edit)

        pre_proc_cells_distr_act = QAction(_('Cells distribution'), self)
        pre_proc_cells_distr_act.setStatusTip(
            _('edit_preProc_cellsDistr_description'))
        pre_proc_cells_distr_act.triggered.connect(self.pre_proc_cells_distr_edit)

        pre_proc_run_act = QAction(_('Run Pre-Processor'), self)
        pre_proc_run_act.setStatusTip(_('run_preProc_des'))
        pre_proc_run_act.triggered.connect(self.pre_proc_run)

        pre_proc_wing_outline = QAction(_('Show wing outline'), self)
        pre_proc_wing_outline.setStatusTip(_('show_WingOutline_des'))
        pre_proc_wing_outline.triggered.connect(self.pre_proc_wing_outline)

        # Build the menu
        pre_proc_menu = self.mainMenu.addMenu(_('Pre Processor'))
        pre_proc_menu.addAction(pre_proc_open_file_act)
        pre_proc_menu.addAction(pre_proc_save_act)
        pre_proc_menu.addAction(pre_proc_save_as_act)
        pre_proc_menu.addSeparator()
        pre_proc_menu.addAction(pre_proc_edit_act)
        pre_proc_menu.addAction(pre_proc_cells_distr_act)
        pre_proc_menu.addSeparator()
        pre_proc_menu.addAction(pre_proc_run_act)
        pre_proc_menu.addSeparator()
        pre_proc_menu.addAction(pre_proc_wing_outline)

    def pre_proc_open_file(self):
        """
        :method: Called if the user selects *Pre Processor*
                 -> *Open PreProc File*
        """
        self.ppm.open_file()

    def pre_proc_save_file(self):
        """
        :method: Called if the user selects *Pre Processor*
                 -> *Save PreProc File*
        """
        self.ppm.save_file()

    def pre_proc_save_file_as(self):
        """
        :method: Called if the user selects *Pre Processor*
                 -> *Save PreProc File As ...*
        """
        self.ppm.save_file_as()

    def pre_proc_edit(self):
        """
        :method: Called if the user selects *Pre Processor*
                 -> *Name, LE, TE, Vault*
        """
        if self.dws.windowExists('PreProcDataEdit') is False:
            self.preProcEditW = PreProcData()
            self.dws.registerWindow('PreProcDataEdit')
            self.mdi.addSubWindow(self.preProcEditW)
        self.preProcEditW.show()

    def pre_proc_cells_distr_edit(self):
        """
        :method: Called if the user selects *Pre Processor*
                 -> *Cells distribution*
        """
        if self.dws.windowExists('PreProcCellsDistribution') is False:
            self.pre_proc_cells_distr_w = PreProcCellsDistribution()
            self.dws.registerWindow('PreProcCellsDistribution')
            self.mdi.addSubWindow(self.pre_proc_cells_distr_w)
        self.pre_proc_cells_distr_w.show()

    def pre_proc_wing_outline(self):
        """
        :method: Called if the user selects *Pre Processor*
                 -> *Show wing outline*
        """
        if self.dws.windowExists('PreProcWingOutline') is False:
            self.pre_proc_wing_outline_w = PreProcWingOutline()
            self.dws.registerWindow('PreProcWingOutline')
            self.mdi.addSubWindow(self.pre_proc_wing_outline_w)
        self.pre_proc_wing_outline_w.open_pre_proc_file(False)
        self.pre_proc_wing_outline_w.show()

    def pre_proc_run(self):
        """
        :method: Called if the user selects *Pre Processor*
                 -> *Run Pre-Processor*
        """
        logging.debug(self.__className + '.pre_proc_run')

        # Save current file into processor directory
        self.ppm.write_file(True)

        # Open the window for the user info
        if self.dws.windowExists('ProcessorOutput') is False:
            self.proc_out_w = ProcessorOutput()
            self.dws.registerWindow('ProcessorOutput')
            self.mdi.addSubWindow(self.proc_out_w)
        self.proc_out_w.show()

        # Finally, run the processor
        proc_runner = ProcRunner(self.proc_out_w)

        if proc_runner.pre_proc_configured() is False:
            msg_box = QMessageBox()
            msg_box.setWindowTitle(_('Potentially missing configuration!'))
            msg_box.setText(_('For a successful pre-processor run you must '
                              'configure\nthe pre-processor in Setup '
                              '->Both Processors.'))
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        else:
            proc_runner.run_pre_proc()
            if self.config_reader.get_pre_proc_show_outline() is True:
                self.pre_proc_wing_outline()

    def build_proc_menu(self):
        """
        :method: Builds the complete Processor menu
        """
        # Define the actions
        pre_proc_import_a = QAction(_('Import Pre-Proc output file'), self)
        pre_proc_import_a.setStatusTip(_('import-pre-proc_file_desc'))
        pre_proc_import_a.triggered.connect(self.pre_proc_import)

        proc_open_file_a = QAction(_('Open Processor File'), self)
        proc_open_file_a.setStatusTip(_('open_Proc_file_desc'))
        proc_open_file_a.triggered.connect(self.proc_open_file)

        proc_save_a = QAction(_('Save Processor File'), self)
        proc_save_a.setStatusTip(_('save_proc_file_desc'))
        proc_save_a.triggered.connect(self.proc_save_file)

        proc_save_as_a = QAction(_('Save Processor File As ..'), self)
        proc_save_as_a.setStatusTip(_('save_proc_file_as_desc'))
        proc_save_as_a.triggered.connect(self.proc_save_file_as)

        proc_basic_data_a = QAction(_('Basic data'), self)
        proc_basic_data_a.setStatusTip(_('Editing the wing basics'))
        proc_basic_data_a.triggered.connect(self.proc_basic_data_edit)

        proc_geometry_a = QAction(_('Geometry'), self)
        proc_geometry_a.setStatusTip(_('Edit wing geometry'))
        proc_geometry_a.triggered.connect(self.proc_geometry_edit)

        proc_airfoils_a = QAction(_('Airfoils'), self)
        proc_airfoils_a.setStatusTip(_('Edit airfoils geometry'))
        proc_airfoils_a.triggered.connect(self.proc_airfoils_edit)

        proc_anchor_points_a = QAction(_('Anchor points'), self)
        proc_anchor_points_a.setStatusTip(_('Edit Anchor points data'))
        proc_anchor_points_a.triggered.connect(self.proc_anchor_points_edit)

        proc_rib_holes_a = QAction(_('Rib holes'), self)
        proc_rib_holes_a.setStatusTip(_('Edit rib holes (rib lightening) data'))
        proc_rib_holes_a.triggered.connect(self.proc_rib_holes_edit)

        proc_skin_tension_a = QAction(_('Skin tension'), self)
        proc_skin_tension_a.setStatusTip(_('Edit skin tension data'))
        proc_skin_tension_a.triggered.connect(self.proc_skin_tension_edit)

        proc_gen_ao_a_a = QAction(_('Estimated general AoA'), self)
        proc_gen_ao_a_a.setStatusTip(_('Edit global AoA data'))
        proc_gen_ao_a_a.triggered.connect(self.proc_global_aoa_edit)

        proc_lines_a = QAction(_('Lines'), self)
        proc_lines_a.setStatusTip(_('Edit Lines data'))
        proc_lines_a.triggered.connect(self.proc_lines_edit)

        proc_brakes_a = QAction(_('Brakes'), self)
        proc_brakes_a.setStatusTip(_('Edit Brake lines data'))
        proc_brakes_a.triggered.connect(self.proc_brakes_edit)

        proc_ram_a = QAction(_('Ramifications length'), self)
        proc_ram_a.setStatusTip(_('Edit Ramification data'))
        proc_ram_a.triggered.connect(self.proc_ramification_edit)

        proc_hv_vh_ribs_a = QAction(_('HV and VH ribs'), self)
        proc_hv_vh_ribs_a.setStatusTip(_('Edit HV/ VH ribs data'))
        proc_hv_vh_ribs_a.triggered.connect(self.proc_hv_vh_edit)

        proc_extrados_colors_a = QAction(_('Colors upper sail'), self)
        proc_extrados_colors_a.setStatusTip(_('Edit the color settings of the '
                                              'upper sail'))
        proc_extrados_colors_a.triggered.connect(self.proc_extrados_colors_edit)

        proc_intrados_colors_a = QAction(_('Colors lower sail'), self)
        proc_intrados_colors_a.setStatusTip(_('Edit the color settings of the '
                                              'lower sail'))
        proc_intrados_colors_a.triggered.connect(self.proc_intrados_colors_edit)

        proc_add_rib_pts_a = QAction(_('Additional rib points'), self)
        proc_add_rib_pts_a.setStatusTip(_('Edit additional rib points data'))
        proc_add_rib_pts_a.triggered.connect(self.proc_add_rib_pts_edit)

        proc_el_lines_corr_a = QAction(_('Elastic lines correction'), self)
        proc_el_lines_corr_a.setStatusTip(_('Edit elastic lines correction data'))
        proc_el_lines_corr_a.triggered.connect(self.proc_el_lines_corr_edit)

        proc_joncs_def_a = QAction(_('Joncs definitions'), self)
        proc_joncs_def_a.setStatusTip(_('Edit joncs (nylon rods) definition'))
        proc_joncs_def_a.triggered.connect(self.proc_joncs_def_edit)

        proc_nose_mylars_a = QAction(_('Nose mylars'), self)
        proc_nose_mylars_a.setStatusTip(_('Edit nose mylars definition'))
        proc_nose_mylars_a.triggered.connect(self.proc_nose_mylars_edit)

        proc_edit_tab_reinf_a = QAction(_('Tab reinforcements'), self)
        proc_edit_tab_reinf_a.setEnabled(False)

        proc_glue_vents_a = QAction(_('Glue vents'), self)
        proc_glue_vents_a.setStatusTip(_('Edit glue vent definitions'))
        proc_glue_vents_a.triggered.connect(self.proc_glue_vent_edit)

        proc_spec_wing_tip_a = QAction(_('Special wingtip'), self)
        proc_spec_wing_tip_a.setStatusTip(_('Edit Special wing tip definitions'))
        proc_spec_wing_tip_a.triggered.connect(self.proc_spec_wing_tip_edit)

        proc_calage_var_a = QAction(_('Calage variation'), self)
        proc_calage_var_a.setStatusTip(_('Edit parameters for calage '
                                       'variation study'))
        proc_calage_var_a.triggered.connect(self.proc_calage_var_edit)

        proc_three_d_shaping_a = QAction(_('3D shaping'), self)
        proc_three_d_shaping_a.setStatusTip(_('Enable and edit parameters for '
                                              '3D shaping'))
        proc_three_d_shaping_a.triggered.connect(self.proc_three_d_shaping_edit)

        proc_airfoil_thick_a = QAction(_('Airfoil thickness'), self)
        proc_airfoil_thick_a.setStatusTip(_('Edit parameters for airfoil '
                                          'thickness'))
        proc_airfoil_thick_a.triggered.connect(self.proc_airfoil_thick_edit)

        proc_new_skin_tens_a = QAction(_('New skin tension'), self)
        proc_new_skin_tens_a.setStatusTip(_('Edit parameters for new skin '
                                            'tension'))
        proc_new_skin_tens_a.triggered.connect(self.proc_new_skin_tension_edit)

        proc_run_act = QAction(_('Run Processor'), self)
        proc_run_act.setStatusTip(_('run_Processor_des'))
        proc_run_act.triggered.connect(self.proc_run)

        # Build the menu
        proc_menu = self.mainMenu.addMenu(_('Processor'))
        proc_menu.addAction(pre_proc_import_a)
        proc_menu.addSeparator()
        proc_menu.addAction(proc_open_file_a)
        proc_menu.addAction(proc_save_a)
        proc_menu.addAction(proc_save_as_a)
        proc_menu.addSeparator()
        proc_menu.addAction(proc_basic_data_a)
        proc_menu.addAction(proc_geometry_a)
        proc_menu.addAction(proc_airfoils_a)
        proc_menu.addAction(proc_anchor_points_a)
        proc_menu.addAction(proc_rib_holes_a)

        skin_tens_menu = QMenu(_('Skin tension'), self)
        skin_tens_menu.addAction(proc_skin_tension_a)
        skin_tens_menu.addAction(proc_new_skin_tens_a)
        proc_menu.addMenu(skin_tens_menu)

        proc_menu.addAction(proc_gen_ao_a_a)
        proc_menu.addAction(proc_lines_a)
        proc_menu.addAction(proc_brakes_a)
        proc_menu.addAction(proc_ram_a)
        proc_menu.addAction(proc_hv_vh_ribs_a)

        cols_menu = QMenu(_('Colors'), self)
        cols_menu.addAction(proc_extrados_colors_a)
        cols_menu.addAction(proc_intrados_colors_a)
        proc_menu.addMenu(cols_menu)

        proc_menu.addAction(proc_add_rib_pts_a)
        proc_menu.addAction(proc_el_lines_corr_a)
        proc_menu.addAction(proc_joncs_def_a)
        proc_menu.addAction(proc_nose_mylars_a)
        proc_menu.addAction(proc_edit_tab_reinf_a)
        proc_menu.addAction(proc_glue_vents_a)
        proc_menu.addAction(proc_spec_wing_tip_a)
        proc_menu.addAction(proc_calage_var_a)
        proc_menu.addAction(proc_three_d_shaping_a)
        proc_menu.addAction(proc_airfoil_thick_a)

        proc_menu.addSeparator()
        proc_menu.addAction(proc_run_act)

    def pre_proc_import(self):
        """
        :method: Called if the user selects *Processor* ->
                 *Import Pre-Proc File*
        """
        self.pm.import_pre_proc_file()

    def proc_open_file(self):
        """
        :method: Called if the user selects *Processor*
                 -> *Open Processor File*
        """
        self.pm.open_file()

    def proc_save_file(self):
        """
        :method: Called if the user selects *Processor*
                 -> *Save Processor File*
        """
        self.pm.save_file()

    def proc_save_file_as(self):
        """
        :method: Called if the user selects *Processor*
                 -> *Save Processor File As…*
        """
        self.pm.save_file_as()

    def proc_basic_data_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Basic data*
        """
        if self.dws.windowExists('ProcBasicData') is False:
            self.basic_data_w = BasicData()
            self.dws.registerWindow('ProcBasicData')
            self.mdi.addSubWindow(self.basic_data_w)
        self.basic_data_w.show()

    def proc_geometry_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Geometry*
        """
        if self.dws.windowExists('Geometry') is False:
            self.geometry_w = Geometry()
            self.dws.registerWindow('Geometry')
            self.mdi.addSubWindow(self.geometry_w)
        self.geometry_w.show()

    def proc_airfoils_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Airfoils*
        """
        if self.dws.windowExists('Airfoils') is False:
            self.airfoils_w = Airfoils()
            self.dws.registerWindow('Airfoils')
            self.mdi.addSubWindow(self.airfoils_w)
        self.airfoils_w.show()

    def proc_anchor_points_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Anchor Points*
        """
        if self.dws.windowExists('AnchorPoints') is False:
            self.anchor_points_w = AnchorPoints()
            self.dws.registerWindow('AnchorPoints')
            self.mdi.addSubWindow(self.anchor_points_w)
        self.anchor_points_w.show()

    def proc_rib_holes_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Airfoils*
        """
        if self.dws.windowExists('RibHoles') is False:
            self.rib_holes_w = RibHoles()
            self.dws.registerWindow('RibHoles')
            self.mdi.addSubWindow(self.rib_holes_w)
        self.rib_holes_w.show()

    def proc_skin_tension_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Skin tension*
        """
        if self.dws.windowExists('SkinTension') is False:
            self.skin_tension_w = SkinTension()
            self.dws.registerWindow('SkinTension')
            self.mdi.addSubWindow(self.skin_tension_w)
        self.skin_tension_w.show()

    def proc_global_aoa_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Global AoA*
        """
        if self.dws.windowExists('GlobalAoA') is False:
            self.global_aoa_w = GlobalAoA()
            self.dws.registerWindow('GlobalAoA')
            self.mdi.addSubWindow(self.global_aoa_w)
        self.global_aoa_w.show()

    def proc_lines_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Lines*
        """
        if self.dws.windowExists('Lines') is False:
            self.lines_w = Lines()
            self.dws.registerWindow('Lines')
            self.mdi.addSubWindow(self.lines_w)
        self.lines_w.show()

    def proc_brakes_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Brakes*
        """
        if self.dws.windowExists('Brakes') is False:
            self.brakes_w = Brakes()
            self.dws.registerWindow('Brakes')
            self.mdi.addSubWindow(self.brakes_w)
        self.brakes_w.show()

    def proc_ramification_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Ramification*
        """
        if self.dws.windowExists('Ramification') is False:
            self.ramification_W = Ramification()
            self.dws.registerWindow('Ramification')
            self.mdi.addSubWindow(self.ramification_W)
        self.ramification_W.show()

    def proc_hv_vh_edit(self):
        """
        :method: Called if the user selects *Processor* -> *HV VH Ribs*
        """
        if self.dws.windowExists('HvVhRibs') is False:
            self.hv_vh_w = HvVhRibs()
            self.dws.registerWindow('HvVhRibs')
            self.mdi.addSubWindow(self.hv_vh_w)
        self.hv_vh_w.show()

    def proc_extrados_colors_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Colors upper sail*
        """
        if self.dws.windowExists('ExtradosColors') is False:
            self.extrados_colors_w = ExtradColors()
            self.dws.registerWindow('ExtradosColors')
            self.mdi.addSubWindow(self.extrados_colors_w)
        self.extrados_colors_w.show()

    def proc_intrados_colors_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Colors lower sail*
        """
        if self.dws.windowExists('IntradosColors') is False:
            self.intrados_colors_w = IntradColors()
            self.dws.registerWindow('IntradosColors')
            self.mdi.addSubWindow(self.intrados_colors_w)
        self.intrados_colors_w.show()

    def proc_add_rib_pts_edit(self):
        """
        :method: Called if the user selects *Processor*
                 -> *Additional rib points*
        """
        if self.dws.windowExists('AddRibPoints') is False:
            self.add_rib_pts_w = AddRibPoints()
            self.dws.registerWindow('AddRibPoints')
            self.mdi.addSubWindow(self.add_rib_pts_w)
        self.add_rib_pts_w.show()

    def proc_el_lines_corr_edit(self):
        """
        :method: Called if the user selects *Processor*
                 -> *Elastic lines correction*
        """
        if self.dws.windowExists('ElasticLinesCorr') is False:
            self.el_lines_corr_w = ElasticLinesCorr()
            self.dws.registerWindow('ElasticLinesCorr')
            self.mdi.addSubWindow(self.el_lines_corr_w)
        self.el_lines_corr_w.show()

    def proc_joncs_def_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Joncs definition*
        """
        if self.dws.windowExists('JoncsDef') is False:
            self.joncs_def_w = JoncsDefinition()
            self.dws.registerWindow('JoncsDef')
            self.mdi.addSubWindow(self.joncs_def_w)
        self.joncs_def_w.show()

    def proc_nose_mylars_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Nose mylars*
        """
        if self.dws.windowExists('NoseMylars') is False:
            self.nose_mylars_w = NoseMylars()
            self.dws.registerWindow('NoseMylars')
            self.mdi.addSubWindow(self.nose_mylars_w)
        self.nose_mylars_w.show()

    def proc_glue_vent_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Glue vents*
        """
        if self.dws.windowExists('GlueVent') is False:
            self.glue_vent_w = GlueVent()
            self.dws.registerWindow('GlueVent')
            self.mdi.addSubWindow(self.glue_vent_w)
        self.glue_vent_w.show()

    def proc_spec_wing_tip_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Special wing tip*
        """
        if self.dws.windowExists('SpecWingTip') is False:
            self.spec_wing_tip_w = SpecWingTip()
            self.dws.registerWindow('SpecWingTip')
            self.mdi.addSubWindow(self.spec_wing_tip_w)
        self.spec_wing_tip_w.show()

    def proc_calage_var_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Calage variation*
        """
        if self.dws.windowExists('CalageVar') is False:
            self.calage_var_w = CalageVar()
            self.dws.registerWindow('CalageVar')
            self.mdi.addSubWindow(self.calage_var_w)
        self.calage_var_w.show()

    def proc_three_d_shaping_edit(self):
        """
        :method: Called if the user selects *Processor* -> *3D Shaping*
        """
        if self.dws.windowExists('ThreeDShaping') is False:
            self.three_d_sh_w = ThreeDShaping()
            self.dws.registerWindow('ThreeDShaping')
            self.mdi.addSubWindow(self.three_d_sh_w)
        self.three_d_sh_w.show()

    def proc_airfoil_thick_edit(self):
        """
        :method: Called if the user selects *Processor* -> *Airfoil thickness*
        """
        if self.dws.windowExists('AirfoilThickness') is False:
            self.airfoil_thick_w = AirfoilThickness()
            self.dws.registerWindow('AirfoilThickness')
            self.mdi.addSubWindow(self.airfoil_thick_w)
        self.airfoil_thick_w.show()

    def proc_new_skin_tension_edit(self):
        """
        :method: Called if the user selects *Processor* -> *New skin tension*
        """
        if self.dws.windowExists('NewSkinTension') is False:
            self.new_skin_tens_w = NewSkinTension()
            self.dws.registerWindow('NewSkinTension')
            self.mdi.addSubWindow(self.new_skin_tens_w)
        self.new_skin_tens_w.show()

    def proc_run(self):
        """
        :method: Called if the user selects *Processor* -> *Run Processor*
        """
        logging.debug(self.__className + '.proc_run')

        # Save current file into processor directory
        self.pm.write_file(True)

        # Open the window for the user info
        if self.dws.windowExists('ProcessorOutput') is False:
            self.proc_out_w = ProcessorOutput()
            self.dws.registerWindow('ProcessorOutput')
            self.mdi.addSubWindow(self.proc_out_w)
        self.proc_out_w.show()

        # Finally, run the processor
        proc_runner = ProcRunner(self.proc_out_w)

        if proc_runner.proc_configured() is False:
            msg_box = QMessageBox()
            msg_box.setWindowTitle(_('Potentially missing configuration!'))
            msg_box.setText(_('For a successful processor run you must '
                              'configure\nthe processor in Setup->'
                              'Both Processors.'))
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        else:
            proc_runner.run_proc()

    def build_plan_menu(self):
        """
        :method: Builds the complete Plan menu
        """
        # Define the actions

        plan_seewing_all_a = QAction(_('Seewing Allowance'), self)
        plan_seewing_all_a.setStatusTip(_('Edit Seewing allowances'))
        plan_seewing_all_a.triggered.connect(self.plan_seewing_all_edit)

        plan_marks_a = QAction(_('Marks'), self)
        plan_marks_a.setStatusTip(_('Edit the Marks parameters'))
        plan_marks_a.triggered.connect(self.plan_marks_edit)

        plan_dxf_layer_names_a = QAction(_('DXF Layer names'), self)
        plan_dxf_layer_names_a.setStatusTip(_('Edit the names of the individual '
                                              'DXF layers'))
        plan_dxf_layer_names_a.triggered.connect(self.plan_dxf_layer_names_edit)

        proc_marks_t_a = QAction(_('Marks types'), self)
        proc_marks_t_a.setStatusTip(_('Edit individual parameters for the marks '
                                    'on the plans'))
        proc_marks_t_a.triggered.connect(self.marks_types_edit)

        proc_two_d_dxf_a = QAction(_('2D DXF options'), self)
        proc_two_d_dxf_a.setStatusTip(_('Edit for the 2D dxf plans'))
        proc_two_d_dxf_a.triggered.connect(self.two_d_dxf_edit)

        proc_three_d_dxf_a = QAction(_('3D DXF options'), self)
        proc_three_d_dxf_a.setStatusTip(_('Edit for the 3D dxf plans'))
        proc_three_d_dxf_a.triggered.connect(self.three_d_dxf_edit)

        # Build the menu
        plan_menu = self.mainMenu.addMenu(_('Plan'))
        plan_menu.addAction(plan_seewing_all_a)
        plan_menu.addAction(plan_marks_a)
        plan_menu.addAction(plan_dxf_layer_names_a)
        plan_menu.addAction(proc_marks_t_a)
        plan_menu.addAction(proc_two_d_dxf_a)
        plan_menu.addAction(proc_three_d_dxf_a)

    def plan_seewing_all_edit(self):
        """
        :method: Called if the user selects *Plan* -> *Sewing allowances*
        """
        if self.dws.windowExists('SeewingAllowances') is False:
            self.seewing_all_w = SeewingAllowances()
            self.dws.registerWindow('SeewingAllowances')
            self.mdi.addSubWindow(self.seewing_all_w)
        self.seewing_all_w.show()

    def plan_marks_edit(self):
        """
        :method: Called if the user selects *Plan* -> *Marks*
        """
        if self.dws.windowExists('Marks') is False:
            self.marks_w = Marks()
            self.dws.registerWindow('Marks')
            self.mdi.addSubWindow(self.marks_w)
        self.marks_w.show()

    def plan_dxf_layer_names_edit(self):
        """
        :method: Called if the user selects *Plan* -> *DXF Layer names*
        """
        if self.dws.windowExists('DxfLayerNames') is False:
            self.dxf_layer_names_w = DxfLayerNames()
            self.dws.registerWindow('DxfLayerNames')
            self.mdi.addSubWindow(self.dxf_layer_names_w)
        self.dxf_layer_names_w.show()

    def marks_types_edit(self):
        """
        :method: Called if the user selects *Plan* -> Marks types*
        """
        if self.dws.windowExists('MarksTypes') is False:
            self.marks_types_w = MarksTypes()
            self.dws.registerWindow('MarksTypes')
            self.mdi.addSubWindow(self.marks_types_w)
        self.marks_types_w.show()

    def two_d_dxf_edit(self):
        """
        :method: Called if the user selects *Plan* -> 2D DFX *
        """
        if self.dws.windowExists('TwoDDxf') is False:
            self.two_d_dxf_w = TwoDDxfModel()
            self.dws.registerWindow('TwoDDxf')
            self.mdi.addSubWindow(self.two_d_dxf_w)
        self.two_d_dxf_w.show()

    def three_d_dxf_edit(self):
        """
        :method: Called if the user selects *Plan* -> 3D DFX*
        """
        if self.dws.windowExists('ThreeDDxf') is False:
            self.three_d_dxf_w = ThreeDDxfModel()
            self.dws.registerWindow('ThreeDDxf')
            self.mdi.addSubWindow(self.three_d_dxf_w)
        self.three_d_dxf_w.show()

    def build_view_menu(self):
        """
        :method: Builds the View menu
        """
        # Define the actions
        view_cascade_act = QAction(_('Cascade'), self)
        view_cascade_act.setStatusTip(_('Cascade all windows'))
        view_cascade_act.triggered.connect(self.view_cascade)
        #
        view_tile_act = QAction(_('Tile'), self)
        view_tile_act.setStatusTip(_('Tile all windows'))
        view_tile_act.triggered.connect(self.view_tile)
        # Build the menu
        view_menu = self.mainMenu.addMenu(_('View'))
        view_menu.addSeparator()
        view_menu.addAction(view_cascade_act)
        view_menu.addAction(view_tile_act)

    def view_cascade(self):
        """
        :method: Called if the user selects *View* -> *Cascade*
        """
        self.mdi.cascadeSubWindows()

    def view_tile(self):
        """
        :method: Called if the user selects *View* -> *Tile*
        """
        self.mdi.tileSubWindows()

    def build_setup_menu(self):
        """
        :method: Builds the Setup menu
        """
        # Define actions
        setup_lang_en_act = QAction("English", self)
        setup_lang_en_act.setStatusTip('Switches the display language '
                                       'to english')
        setup_lang_en_act.triggered.connect(self.setup_lang_en)

        setup_lang_de_act = QAction("Deutsch", self)
        setup_lang_de_act.setStatusTip('Wechselt zur deutschen Anzeige')
        setup_lang_de_act.triggered.connect(self.setup_lang_de)

        setup_proc_act = QAction(_('Both Processors'), self)
        setup_proc_act.setStatusTip(_('Setup locations for both processors'))
        setup_proc_act.triggered.connect(self.setup_processors)

        setup_upd_check_act = QAction(_('Update checking'), self)
        setup_upd_check_act.setStatusTip(_('Setup if and for which version '
                                           'to check for updates'))
        setup_upd_check_act.triggered.connect(self.setup_update_checking)

        # add actions
        setup_menu = self.mainMenu.addMenu(_('Setup'))
        setup_lang_menu = setup_menu.addMenu(_('Language'))
        setup_lang_menu.addAction(setup_lang_en_act)
        setup_lang_menu.addAction(setup_lang_de_act)
        setup_menu.addSeparator()
        setup_menu.addAction(setup_proc_act)
        setup_menu.addSeparator()
        setup_menu.addAction(setup_upd_check_act)

    def setup_lang_de(self):
        """
        :method: Called if the user selects *Setup* *Language* -> *German*
        """
        config = ConfigReader()
        config.set_language("de")
        self.display_restart_msg()

    def setup_lang_en(self):
        """
        :method: Called if the user selects *Setup* *Language* -> *English*
        """
        config = ConfigReader()
        config.set_language("en")
        self.display_restart_msg()

    def display_restart_msg(self):
        """
        :method: Displays a message to the user to restart the application
                after switching the language
        """
        msg = QMessageBox()

        msg.setWindowTitle(_("Switching language"))
        msg.setIcon(QMessageBox.Information)
        msg.setText(_("Please restart the application."))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setFixedWidth(300)
        msg.exec_()

    def setup_processors(self):
        """
        :method: Called if the user selects *Setup* -> *Both processors*
        """
        if self.dws.windowExists('SetupProcessors') is False:
            self.setup_proc_w = SetupProcessors()
            self.dws.registerWindow('SetupProcessors')
            self.mdi.addSubWindow(self.setup_proc_w)
        self.setup_proc_w.show()

    def setup_update_checking(self):
        """
        :method: Called if the user selects *Setup* -> *Update checking*
        """
        if self.dws.windowExists('SetupUpdateChecking') is False:
            self.setup_update_check_w = SetupUpdateChecking()
            self.dws.registerWindow('SetupUpdateChecking')
            self.mdi.addSubWindow(self.setup_update_check_w)
        self.setup_update_check_w.show()

    def build_help_menu(self):
        """
        :method: Builds the Help Menu
        """
        online_help_act = QAction(_('Online Help'), self)
        online_help_act.setStatusTip(_('Opens the online help in your browser'))
        online_help_act.triggered.connect(self.online_help)

        help_about_act = QAction(_('About'), self)
        help_about_act.setStatusTip(_('Short info about the program'))
        help_about_act.triggered.connect(self.help_about)

        # Build the menu
        file_menu = self.mainMenu.addMenu(_('Help'))
        file_menu.addAction(online_help_act)
        file_menu.addAction(help_about_act)

    def online_help(self):
        """
        :method: Opens the online help in the browser
        """

        config = ConfigReader()

        webbrowser.open('file://'
                        + os.path.join(os.getcwd(),
                                       'userHelp',
                                       config.get_language(),
                                       'introduction.html'))

    def help_about(self):
        """
        :method: Opens the Help About window.
        """
        if self.dws.windowExists('HelpAbout') is False:
            self.helpAboutW = HelpAbout()
            self.dws.registerWindow('HelpAbout')
            self.mdi.addSubWindow(self.helpAboutW)
        self.helpAboutW.show()

    def delete_logfile(self):
        """
        :method: Deletes the log file if there's one
        """
        directory_path = os.path.dirname(os.path.realpath(__file__))
        log_path_name = os.path.join(directory_path, 'logfile.txt')

        if os.path.isfile(log_path_name):
            os.remove(log_path_name)


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
