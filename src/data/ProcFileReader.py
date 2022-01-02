""""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'"""
import logging

from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QFile, QTextStream
from PyQt5.QtWidgets import QTextEdit

from data.ProcModel import ProcModel
from data.FileHelpers import FileHelpers


class WaitWindow(QTextEdit):
    """
    :class: Builds a minimalized window to inform the user that file reading
            does take some time.
            All infomation is shown in the window title due to this discussion:
            https://stackoverflow.com/questions/67934352/window-opened-from-a-
            class-is-not-displaying-correctly/67937507#67937507
    """
    def __init__(self):
        super(WaitWindow, self).__init__()
        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setMaximumSize(450, 0)
        self.setMinimumSize(450, 25)
        self.setWindowTitle(_("Please wait.. reading might take some time"))


class ProcFileReader(QObject):
    """
    :class: Covers the operations to read a processor file and write the data
            into the according models.
    """

    __className = 'ProcFileReader'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    __fileNamePath = ''

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        self.wait_info_w = None

        self.fh = FileHelpers()

        self.rib_M = ProcModel.RibModel()
        self.wing_M = ProcModel.WingModel()
        self.airf_M = ProcModel.AirfoilsModel()
        self.anchPoints_M = ProcModel.AnchorPointsModel()
        self.lightC_M = ProcModel.LightConfModel()
        self.lightD_M = ProcModel.LightDetModel()
        self.skinTens_M = ProcModel.SkinTensionModel()
        self.skinTensParams_M = ProcModel.SkinTensionParamsModel()
        self.sewAll_M = ProcModel.SewingAllowancesModel()
        self.marks_M = ProcModel.MarksModel()
        self.globAoA_M = ProcModel.GlobAoAModel()
        self.lines_M = ProcModel.LinesModel()
        self.brakes_M = ProcModel.BrakesModel()
        self.brakeL_M = ProcModel.BrakeLengthModel()
        self.ramif_M = ProcModel.RamificationModel()
        self.hVvHRibs_M = ProcModel.HvVhRibsModel()
        self.extradColsConf_M = ProcModel.ExtradosColConfModel()
        self.extradColsDet_M = ProcModel.ExtradosColDetModel()
        self.intradColsConf_M = ProcModel.IntradosColsConfModel()
        self.intradColsDet_M = ProcModel.IntradosColsDetModel()
        self.addRibPts_M = ProcModel.AddRibPointsModel()
        self.elLinesCorr_M = ProcModel.ElLinesCorrModel()
        self.elLinesDef_M = ProcModel.ElLinesDefModel()
        self.dxfLayNames_M = ProcModel.DxfLayerNamesModel()
        self.marksT_M = ProcModel.MarksTypesModel()
        self.joncsDef_M = ProcModel.JoncsDefModel()
        self.noseMylars_M = ProcModel.NoseMylarsModel()
        self.twoDDxf_M = ProcModel.TwoDDxfModel()
        self.threeDDxf_M = ProcModel.ThreeDDxfModel()
        self.glueVent_M = ProcModel.GlueVentModel()
        self.specWingTyp_M = ProcModel.SpecWingTipModel()
        self.calageVar_M = ProcModel.CalageVarModel()
        self.threeDShConf_M = ProcModel.ThreeDShConfModel()
        self.threeDShUpDet_M = ProcModel.ThreeDShUpDetModel()
        self.threeDShLoDet_M = ProcModel.ThreeDShLoDetModel()
        self.threeDShPr_M = ProcModel.ThreeDShPrintModel()
        self.airfThick_M = ProcModel.AirfoilThicknessModel()
        self.newSkinTensConf_M = ProcModel.NewSkinTensConfModel()
        self.newSkinTensDet_M = ProcModel.NewSkinTensDetModel()

    def set_file_path_name(self, file_path_name):
        """
        :method: Used to set the full path and filename to be read
        """
        self.__fileNamePath = file_path_name

    def read_file(self):
        """
        :method: Reads the data file and saves the data in the internal
                 database.
        :warning: Filename and Path must be set first!
        """
        logging.debug(self.__className+'.read_file')

        self.wait_info_w = WaitWindow()
        self.wait_info_w.show()

        in_file = QFile(self.__fileNamePath)
        in_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(in_file)

        ##############################
        # 1. GEOMETRY
        # Over read file header
        logging.debug(self.__className+'.read_file: 1. GEOMETRY')

        counter = 0
        while counter < 4:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1

        # Brand name
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.BrandNameCol),
                self.fh.remTabSpaceQuot(line))

        # Wing name
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.WingNameCol),
                self.fh.remTabSpaceQuot(line))

        # Draw scale
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.DrawScaleCol),
                self.fh.remTabSpace(line))

        # Wing scale
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.WingScaleCol),
                self.fh.remTabSpace(line))

        # Number of cells
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.NumCellsCol),
                self.fh.remTabSpace(line))

        # Number of Ribs
        line = stream.readLine()
        line = stream.readLine()
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.NumRibsCol),
                self.fh.remTabSpace(line))

        # Alpha max and parameter
        line = stream.readLine()
        values = self.fh.splitLine(stream.readLine())
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.AlphaMaxTipCol),
                values[0])
        try:
            self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.AlphaModeCol),
                values[1])
        except:
            # in case of an empty file values[1] is missing
            self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.AlphaModeCol),
                '')
            logging.error(self.__className+'.read_file: AlphaMode missing')

        if len(values) > 2:
            self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.AlphaMaxCentCol),
                values[2])
        else:
            self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.AlphaMaxCentCol),
                '')

        # Paraglider type and parameter
        line = stream.readLine()
        values = self.fh.splitLine(stream.readLine())
        self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.ParaTypeCol),
                self.fh.remTabSpaceQuot(values[0]))
        try:
            self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.ParaParamCol),
                values[1])
        except:
            # in case of an empty file values[1] is missing
            self.wing_M.setData(
                self.wing_M.index(0, ProcModel.WingModel.ParaParamCol),
                '')
            logging.error(self.__className+'.read_file: ParaParam missing')

        # Rib geometric parameters
        # Rib  x-rib  y-LE  y-TE  xp  z  beta  RP  Washin Rot_z  Pos_z
        line = stream.readLine()
        line = stream.readLine()

        for i in range(0, self.wing_M.halfNumRibs):
            values = self.fh.splitLine(stream.readLine())
            for y in range(0, 9):
                self.rib_M.setData(self.rib_M.index(i, y), values[y])
            # with 3.16 two additional params was added
            if len(values) <= 9:
                # old data file
                self.rib_M.setData(self.rib_M.index(i, 9), 0)
                self.rib_M.setData(self.rib_M.index(i, 10), 50)
            else:
                # new file
                self.rib_M.setData(self.rib_M.index(i, 9), values[9])
                self.rib_M.setData(self.rib_M.index(i, 10), values[10])

        ##############################
        # 2. AIRFOILS
        logging.debug(self.__className+'.read_file: 2. AIRFOILS')

        for i in range(4):
            line = stream.readLine()

        for i in range(0, self.wing_M.halfNumRibs):
            values = self.fh.splitLine(stream.readLine())
            for y in range(0, 8):
                self.airf_M.setData(self.airf_M.index(i, y), values[y])

        ##############################
        # 3. ANCHOR POINTS
        logging.debug(self.__className+'.read_file: 3. ANCHOR POINTS')

        # Just overreading the lines for temporary testing
        for i in range(4):
            line = stream.readLine()

        for i in range(0, self.wing_M.halfNumRibs):
            values = self.fh.splitLine(stream.readLine())
            for y in range(0, 8):
                self.anchPoints_M.setData(self.anchPoints_M.index(i, y),
                                          values[y])

        ##############################
        # 4. RIB HOLES
        logging.debug(self.__className+'.read_file: 4. RIB HOLES')

        for i in range(3):
            line = stream.readLine()

        numConfigs = int(self.fh.remTabSpace(stream.readLine()))
        self.lightC_M.setNumConfigs(numConfigs)
        for i in range(0, numConfigs):
            ini = int(self.fh.remTabSpace(stream.readLine()))
            fin = int(self.fh.remTabSpace(stream.readLine()))
            self.lightC_M.updateRow(i+1, ini, fin)

            numConfigLines = int(self.fh.remTabSpace(stream.readLine()))
            self.lightD_M.setNumRowsForConfig(i+1, 0)
            self.lightD_M.setNumRowsForConfig(i+1, numConfigLines)

            # ConfigNum, order_num, LightTyp, DistLE, DisChord, HorAxis,
            # VertAxis, RotAngle, Opt1
            for l in range(0, numConfigLines):
                values = self.fh.splitLine(stream.readLine())
                self.lightD_M.updateRow(i+1, l+1, values[0],
                                        values[1],
                                        values[2],
                                        values[3],
                                        values[4],
                                        values[5],
                                        values[6])

        ##############################
        # 5. SKIN TENSION
        logging.debug(self.__className+'.read_file: 5. SKIN TENSION')

        for i in range(4):
            line = stream.readLine()

        for l in range(0, 6):
            values = self.fh.splitLine(stream.readLine())
            try:
                self.skinTens_M.updateRow(l+1, values[0], values[1],
                                          values[2], values[3])
            except:
                # in case of an empty file values[1...3] are missing
                self.skinTens_M.updateRow(l+1, 0, 0, 0, 0)
                logging.error(self.__className+'.read_file: Skin tension params missing')

        val = self.fh.remTabSpace(stream.readLine())
        self.skinTensParams_M.setData(
            self.skinTensParams_M.index(
                0,
                ProcModel.SkinTensionParamsModel.StrainMiniRibsCol), val)

        values = self.fh.splitLine(stream.readLine())
        self.skinTensParams_M.setData(
            self.skinTensParams_M.index(
                0,
                ProcModel.SkinTensionParamsModel.NumPointsCol), values[0])
        self.skinTensParams_M.setData(
            self.skinTensParams_M.index(
                0,
                ProcModel.SkinTensionParamsModel.CoeffCol), values[1])

        ##############################
        # 6. SEWING ALLOWANCES
        logging.debug(self.__className+'.read_file: 6. SEWING ALLOWANCES')

        for i in range(3):
            line = stream.readLine()

        for l in range(0, 2):
            values = self.fh.splitLine(stream.readLine())
            if len(values) > 3:
                self.sewAll_M.updateRow(l+1, values[0],
                                        values[1], values[2])
            else:
                # in case of an empty file
                self.sewAll_M.updateRow(l+1, 15, 25, 25)
                logging.error(self.__className+'.read_file: Seewing allowances for panels missing')

        values = self.fh.splitLine(stream.readLine())
        if len(values) > 2:
            self.sewAll_M.updateRow(3, values[0])
        else:
            self.sewAll_M.updateRow(3, 15)
            logging.error(self.__className+'.read_file: Seewing allowances for ribs missing')

        values = self.fh.splitLine(stream.readLine())
        if len(values) > 2:
            self.sewAll_M.updateRow(4, values[0])
        else:
            self.sewAll_M.updateRow(4, 15)
            logging.error(self.__className+'.read_file: Seewing allowances for v-ribs missing')

        ##############################
        # 7. MARKS
        logging.debug(self.__className+'.read_file: 7. MARKS')

        for i in range(3):
            line = stream.readLine()

        values = self.fh.splitLine(stream.readLine())
        try:
            self.marks_M.updateRow(values[0], values[1], values[2])
        except:
            # in case of an empty file values[1...2] are missing
            self.marks_M.updateRow(25, 0.5, 0.15)
            logging.error(self.__className+'.read_file: Marks missing')

        ##############################
        # 8. GLOBAL ANGLE OF ATTACK ESTIMATION
        logging.debug(self.__className+'.read_file: 8. GLOBAL ANGLE OF ATTACK ESTIMATION')

        for i in range(3):
            line = stream.readLine()

        line = stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 ProcModel.GlobAoAModel.FinesseCol),
            self.fh.remTabSpace(stream.readLine()))

        line = stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 ProcModel.GlobAoAModel.CentOfPressCol),
            self.fh.remTabSpace(stream.readLine()))

        line = stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 ProcModel.GlobAoAModel.CalageCol),
            self.fh.remTabSpace(stream.readLine()))

        line = stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 ProcModel.GlobAoAModel.RisersCol),
            self.fh.remTabSpace(stream.readLine()))

        line = stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 ProcModel.GlobAoAModel.LinesCol),
            self.fh.remTabSpace(stream.readLine()))

        line = stream.readLine()
        self.globAoA_M.setData(
            self.globAoA_M.index(0,
                                 ProcModel.GlobAoAModel.KarabinersCol),
            self.fh.remTabSpace(stream.readLine()))

        ##############################
        # 9. SUSPENSION LINES DESCRIPTION
        logging.debug(self.__className+'.read_file: 9. SUSPENSION LINES DESCRIPTION')

        for i in range(3):
            line = stream.readLine()

        self.wing_M.setData(
            self.wing_M.index(0,
                              ProcModel.WingModel.LinesConcTypeCol),
            self.fh.remTabSpace(stream.readLine()))

        numConfigs = int(self.fh.remTabSpace(stream.readLine()))

        for i in range(0, numConfigs):
            numConfigLines = int(self.fh.remTabSpace(stream.readLine()))
            self.lines_M.setNumRowsForConfig(i+1, 0)
            self.lines_M.setNumRowsForConfig(i+1, numConfigLines)

            for l in range(0, numConfigLines):
                values = self.fh.splitLine(stream.readLine())
                self.lines_M.updateLineRow(i+1, l+1,
                                           values[0],
                                           values[1],
                                           values[2],
                                           values[3],
                                           values[4],
                                           values[5],
                                           values[6],
                                           values[7],
                                           values[8],
                                           values[9],
                                           values[10])

        ##############################
        # 10. BRAKES
        logging.debug(self.__className+'.read_file: 10. BRAKES')

        for i in range(3):
            line = stream.readLine()

        self.wing_M.setData(
            self.wing_M.index(0,
                              ProcModel.WingModel.BrakeLengthCol),
            self.fh.remTabSpace(stream.readLine()))

        # delete existing data
        self.brakes_M.setNumRowsForConfig(1, 0)

        # read new data
        numConfigLines = int(self.fh.remTabSpace(stream.readLine()))
        self.brakes_M.setNumRowsForConfig(1, numConfigLines)

        for l in range(0, numConfigLines):
            values = self.fh.splitLine(stream.readLine())
            try:
                self.brakes_M.updateRow(1, l+1,
                                        values[0],
                                        values[1],
                                        values[2],
                                        values[3],
                                        values[4],
                                        values[5],
                                        values[6],
                                        values[7],
                                        values[8],
                                        values[9],
                                        values[10])
            except:
                self.brakes_M.updateRow(1, l+1,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0)
                logging.error(self.__className+'.read_file: Brake lines data missing')

        line = stream.readLine()

        for c in range(0, 2):
            values = self.fh.splitLine(stream.readLine())

            for p in range(0, 5):
                try:
                    self.brakeL_M.setData(self.brakeL_M.index(0, p + (c*5) ), values[p] )
                except:
                    self.brakeL_M.setData(self.brakeL_M.index(0, p + (c*5) ), 0 )
                    logging.error(self.__className+'.read_file: Brake distribution data missing')

        ##############################
        # 11. RAMIFICATION LENGTH
        logging.debug(self.__className+'.read_file:11. RAMIFICATION LENGTH')
        
        for i in range(3):
            line = stream.readLine()
        
        values =  self.fh.splitLine( stream.readLine() )
        try:
            self.ramif_M.updateDataRow(1, 1, values[0], values[1], 0)
        except:
            self.ramif_M.updateDataRow(1, 1, 0, 0, 0)
            logging.error(self.__className+'.read_file: Ramification data missing')
        
        values =  self.fh.splitLine( stream.readLine() )
        try:
            self.ramif_M.updateDataRow(1, 2, values[0], values[1], values[2])
        except:
            self.ramif_M.updateDataRow(1, 2, 0, 0, 0)
            logging.error(self.__className+'.read_file: Ramification data missing')
                    
        values =  self.fh.splitLine( stream.readLine() )
        try:
            self.ramif_M.updateDataRow(1,3, values[0], values[1], 0)
        except:
            self.ramif_M.updateDataRow(1,3, 0, 0, 0)
            logging.error(self.__className+'.read_file: Ramification data missing')
            
        values =  self.fh.splitLine( stream.readLine() )
        try:
            self.ramif_M.updateDataRow(1, 4, values[0], values[1], values[2])
        except:
            self.ramif_M.updateDataRow(1, 4, 0, 0, 0)
            logging.error(self.__className+'.read_file: Ramification data missing')

        ##############################
        # 12. H V AND VH RIBS (Mini Ribs)
        logging.debug(self.__className+'.read_file: 12. H V AND VH RIBS (Mini Ribs)')
        
        for i in range(3):
            line = stream.readLine()
        
        numConfigLines = int(self.fh.remTabSpace( stream.readLine() ) )
        
        values =  self.fh.splitLine( stream.readLine() )
        self.wing_M.setData(self.wing_M.index(0, ProcModel.WingModel.xSpacingCol), values[0])
        try:
            self.wing_M.setData(self.wing_M.index(0, ProcModel.WingModel.ySpacingCol), values[1])
        except:
            self.wing_M.setData(self.wing_M.index(0, ProcModel.WingModel.ySpacingCol), 0)
            logging.error(self.__className+'.read_file: H V and VH ribs data missing')
        
        # delete existing data
        self.hVvHRibs_M.setNumRowsForConfig(1, 0 )
        # read new data
        self.hVvHRibs_M.setNumRowsForConfig(1, numConfigLines )
        
        for l in range(0, numConfigLines):
            values =  self.fh.splitLine( stream.readLine() )
            if (values[1] == '6') or (values[1] == '16'):
                self.hVvHRibs_M.updateDataRow(1, l+1, \
                                        values[1], \
                                        values[2], \
                                        values[3], \
                                        values[4], \
                                        values[5], \
                                        values[6], \
                                        values[7], \
                                        values[8], \
                                        values[9], \
                                        values[10], \
                                        values[11])
            else:
                self.hVvHRibs_M.updateDataRow(1, l+1, \
                                        values[1], \
                                        values[2], \
                                        values[3], \
                                        values[4], \
                                        values[5], \
                                        values[6], \
                                        values[7], \
                                        values[8], \
                                        values[9])

        ##############################
        # 15. EXTRADOS COLORS
        logging.debug(self.__className+'.read_file: 15. EXTRADOS COLORS')
        
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int(self.fh.remTabSpace( stream.readLine() ) )
        self.extradColsConf_M.setNumConfigs(numConfigs)
        
        for configCounter in range(0, numConfigs):
            values =  self.fh.splitLine( stream.readLine() )
            
            self.extradColsConf_M.updateRow(configCounter+1, values[0])
            
            numConfigLines = int(values[1])
            self.extradColsDet_M.setNumRowsForConfig(configCounter+1, numConfigLines)
                   
            for l in range(0, numConfigLines):
                values =  self.fh.splitLine( stream.readLine() )
                self.extradColsDet_M.updateRow(configCounter+1, l+1, values[1] )
            
        ##############################
        # 16. INTRADOS COLORS
        logging.debug(self.__className+'.read_file: 16. INTRADOS COLORS')
        
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int(self.fh.remTabSpace( stream.readLine() ) )
        self.intradColsConf_M.setNumConfigs(numConfigs)
        
        for configCounter in range(0, numConfigs):
            values =  self.fh.splitLine( stream.readLine() )
            
            self.intradColsConf_M.updateRow(configCounter+1, values[0])
            
            numConfigLines = int(values[1])
            self.intradColsDet_M.setNumRowsForConfig(configCounter+1, numConfigLines)
                   
            for l in range(0, numConfigLines):
                values =  self.fh.splitLine( stream.readLine() )
                self.intradColsDet_M.updateRow(configCounter+1, l+1, values[1] )
        
        
        ##############################
        # 17. ADDITIONAL RIB POINTS
        logging.debug(self.__className+'.read_file: 17. ADDITIONAL RIB POINTS')
        
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int(self.fh.remTabSpace( stream.readLine() ) )
        self.addRibPts_M.setNumRowsForConfig(1, 0)
        self.addRibPts_M.setNumRowsForConfig(1, numConfigs)
        
        for l in range(0, numConfigs):
            values =  self.fh.splitLine( stream.readLine() )
            
            self.addRibPts_M.updateRow(1, l+1, values[0], values[1])

        ##############################
        # 18. ELASTIC LINES CORRECTIONS
        logging.debug(self.__className+'.read_file: 18. ELASTIC LINES CORRECTIONS')
        
        for i in range(3):
            line = stream.readLine()
        
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.LoadCol), self.fh.remTabSpace(stream.readLine()))
        
        values =  self.fh.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.TwoLineDistACol), values[0])
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.TwoLineDistBCol), values[1])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.TwoLineDistBCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        
        values =  self.fh.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.ThreeLineDistACol), values[0])
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.ThreeLineDistBCol), values[1])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.ThreeLineDistBCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.ThreeLineDistCCol), values[2])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.ThreeLineDistCCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')

        values =  self.fh.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FourLineDistACol), values[0])
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FourLineDistBCol), values[1])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FourLineDistBCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElasticLinesCorrModelFourLineDistCCol), values[2])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FourLineDistCCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FourLineDistDCol), values[3])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FourLineDistDCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        
        values =  self.fh.splitLine( stream.readLine() )
        self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistACol), values[0])
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistBCol), values[1])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistBCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistCCol), values[2])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistCCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistDCol), values[3])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistDCol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')
        try:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistECol), values[4])
        except:
            self.elLinesCorr_M.setData(self.elLinesCorr_M.index(0, ProcModel.ElLinesCorrModel.FiveLineDistECol), 0)
            logging.error(self.__className+'.read_file: Elastic lines corr data missing')

        for l in range (0,5):
            values =  self.fh.splitLine( stream.readLine() )
            try:
                self.elLinesDef_M.updateRow(1, l+1, values[1], values[2], values[3])
            except:
                self.elLinesDef_M.updateRow(1, l+1, 0, 0, 0)
                logging.error(self.__className+'.read_file: Elastic lines corr data missing')
            
        ##############################
        # 19. DXF LAYER NAMES
        logging.debug(self.__className+'.read_file: 19. DXF LAYER NAMES')
        
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int( self.fh.remTabSpace( stream.readLine() ) )
        self.dxfLayNames_M.setNumRowsForConfig(1,0)
        self.dxfLayNames_M.setNumRowsForConfig(1, numConfigs)
        
        for l in range(0, numConfigs):
            values =  self.fh.splitLine( stream.readLine() )
            
            self.dxfLayNames_M.updateRow(1, l+1, values[0], values[1])
            
        ##############################
        # 20. MARKS TYPES
        logging.debug(self.__className+'.read_file: 20. MARKS TYPES')
        
        for i in range(3):
            line = stream.readLine()
        
        numConfigs = int( self.fh.remTabSpace( stream.readLine() ) )
        self.marksT_M.setNumRowsForConfig(1,0)
        self.marksT_M.setNumRowsForConfig(1, numConfigs)
        
        for l in range(0, numConfigs):
            values =  self.fh.splitLine( stream.readLine() )
            
            self.marksT_M.updateRow(1, l+1, values[0], \
                                    values[1], values[2], values[3], \
                                    values[4], values[5], values[6])
            
        ##############################
        # 21. JONCS DEFINITION (NYLON RODS)
        logging.debug(self.__className+'.read_file: 21. JONCS DEFINITION (NYLON RODS)')
        
        for i in range(3):
            line = stream.readLine()
        
        # delete all what is there
        self.joncsDef_M.setNumConfigs(0)
            
        scheme = int( self.fh.remTabSpace( stream.readLine() ) )
            
        if scheme == 1:
            # in scheme 1 config num is always 1
            configNum = 1
            
            numGroups =  int( self.fh.remTabSpace( stream.readLine() ) )
            self.joncsDef_M.setNumRowsForConfig(configNum, numGroups)
            
            for g in range (0, numGroups):
                valuesA = self.fh.splitLine( stream.readLine() )
                valuesB = self.fh.splitLine( stream.readLine() )
                valuesC = self.fh.splitLine( stream.readLine() )
                valuesD = self.fh.splitLine( stream.readLine() )
                self.joncsDef_M.updateTypeOneRow(configNum, g+1, \
                                                 valuesA[1], valuesA[2], \
                                                 valuesB[0], valuesB[1], valuesB[2], valuesB[3], \
                                                 valuesC[0], valuesC[1], valuesC[2], valuesC[3], \
                                                 valuesD[0], valuesD[1], valuesD[2], valuesD[3] )
        
        elif scheme == 2:
            numBlocs =  int( self.fh.remTabSpace( stream.readLine() ) )
            
            for b in range (0,numBlocs):
                values = self.fh.splitLine( stream.readLine() )
                
                blocType = int(values[1])
                if blocType == 1:
                    numGroups =  int( self.fh.remTabSpace( stream.readLine() ) )
                    self.joncsDef_M.setNumRowsForConfig(b+1, numGroups)
                    
                    for g in range (0, numGroups):
                        valuesA = self.fh.splitLine( stream.readLine() )
                        valuesB = self.fh.splitLine( stream.readLine() )
                        valuesC = self.fh.splitLine( stream.readLine() )
                        valuesD = self.fh.splitLine( stream.readLine() )
                        self.joncsDef_M.updateTypeOneRow(b+1, g+1, \
                                                         valuesA[1], valuesA[2], \
                                                         valuesB[0], valuesB[1], valuesB[2], valuesB[3], \
                                                         valuesC[0], valuesC[1], valuesC[2], valuesC[3], \
                                                         valuesD[0], valuesD[1], valuesD[2], valuesD[3] )

                else:
                    numGroups =  int( self.fh.remTabSpace( stream.readLine() ) )
                    self.joncsDef_M.setNumRowsForConfig(b+1, numGroups)
                    
                    for g in range (0, numGroups):
                        valuesA = self.fh.splitLine( stream.readLine() )
                        valuesB = self.fh.splitLine( stream.readLine() )
                        valuesC = self.fh.splitLine( stream.readLine() )
                        self.joncsDef_M.updateTypeTwoRow(b+1, g+1, \
                                                         valuesA[1], valuesA[2], \
                                                         valuesB[0], valuesB[1], valuesB[2], valuesB[3], valuesB[4], \
                                                         valuesC[0], valuesC[1], valuesC[2], valuesC[3])
        # Little bad hack. Some of the GUI depends on data within the rows set above. 
        # To get teh GUI updated properly we fake here a model update to force an update in the GUI.  
        self.joncsDef_M.numRowsForConfigChanged.emit(0, 0)

        ##############################
        # 22. NOSE MYLARS DEFINITION
        logging.debug(self.__className+'.read_file: 22. NOSE MYLARS DEFINITION')
        
        for i in range(3):
            line = stream.readLine()
            
        data = int(self.fh.remTabSpace( stream.readLine() ) )
        self.noseMylars_M.setNumConfigs(0)
        
        if data != 0:
            # we have data to read
            
            numConfigs = int(self.fh.remTabSpace( stream.readLine() ) )
            self.noseMylars_M.setNumRowsForConfig(1, numConfigs)
        
            for c in range(0, numConfigs):
                valuesA = self.fh.splitLine( stream.readLine() )
                valuesB = self.fh.splitLine( stream.readLine() )
                
                self.noseMylars_M.updateRow(1, c+1, \
                                            valuesA[1], valuesA[2], \
                                            valuesB[0], valuesB[1], valuesB[2], valuesB[3], valuesB[4], valuesB[5])  
       
        ##############################
        # 23. TAB REINFORCEMENTS
        logging.debug(self.__className+'.read_file: Jump over 23. TAB REINFORCEMENTS')
        
        counter = 0
        while counter < 4:
            line = stream.readLine()
            if line.find('***************') >= 0:
                counter += 1
        
        ##############################
        # 24. GENERAL 2D DXF OPTIONS
        # be carefull: previous code has already read both **** lines of header        
        logging.debug(self.__className+'.read_file: 24. GENERAL 2D DXF OPTIONS')
        
        data = int( self.fh.remTabSpace( stream.readLine() ) )
        
        self.twoDDxf_M.setIsUsed(False)
        
        if data != 0:
            self.twoDDxf_M.setIsUsed(True)
            self.twoDDxf_M.setNumRowsForConfig(1, 6)
            # we have data to read
            for l in range(0, 6 ):
                values =  self.fh.splitLine( stream.readLine() )
                self.twoDDxf_M.updateRow(1, l+1, values[0], values[1], values[2])    
            
        ##############################
        # 25. GENERAL 3D DXF OPTIONS
        logging.debug(self.__className+'.read_file: 25. GENERAL 3D DXF OPTIONS')
        
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.fh.remTabSpace( stream.readLine() ) )
        
        self.threeDDxf_M.setIsUsed(False)
        
        if data != 0:
            self.threeDDxf_M.setIsUsed(True)
            self.threeDDxf_M.setNumRowsForConfig(1, 9)
            # we have data to read
            for l in range(0, 6 ):
                values =  self.fh.splitLine( stream.readLine() )
                self.threeDDxf_M.updateRow(1, l+1, values[0], values[1], values[2])
                
            for l in range(0, 3 ):
                values =  self.fh.splitLine( stream.readLine() )
                self.threeDDxf_M.updateRow(1, l+1+6, values[0], values[2], values[3], values[1])
        
        ##############################
        # 26. GLUE VENTS
        logging.debug(self.__className+'.read_file: 26. GLUE VENTS')
        
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.fh.remTabSpace( stream.readLine() ) )
        
        self.glueVent_M.setIsUsed(False)
        
        if data != 0:
            self.glueVent_M.setIsUsed(True)
            # we have data to read
            for l in range( 0, self.wing_M.halfNumRibs ):
                values =  self.fh.splitLine( stream.readLine() )
                self.glueVent_M.updateRow(1, l+1, values[1])
        
        ##############################
        # 26. SPECIAL WING TIP
        logging.debug(self.__className+'.read_file: 26. SPECIAL WING TIP')
        
        for i in range(3):
            line = stream.readLine()
        
        data = int( self.fh.remTabSpace( stream.readLine() ) )   
        
        self.specWingTyp_M.setIsUsed(False)
        self.specWingTyp_M.setNumRowsForConfig(1, 1)
        
        if data != 0:
            self.specWingTyp_M.setIsUsed(True)
            
            valuesA =  self.fh.splitLine( stream.readLine() )
            valuesB =  self.fh.splitLine( stream.readLine() )
            
            self.specWingTyp_M.updateRow(1, 1, valuesA[1], valuesB[1])
            
        ##############################
        # 28. PARAMETERS FOR CALAGE VARIATION
        logging.debug(self.__className+'.read_file: 28. PARAMETERS FOR CALAGE VARIATION')
        
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.fh.remTabSpace( stream.readLine() ) )   
        
        self.calageVar_M.setIsUsed(False)
        self.calageVar_M.setNumRowsForConfig(1, 1)
        
        if data != 0:
            self.calageVar_M.setIsUsed(True)
            
            valuesA =  self.fh.splitLine( stream.readLine() )
            valuesB =  self.fh.splitLine( stream.readLine() )
            valuesC =  self.fh.splitLine( stream.readLine() )
            
            self.calageVar_M.updateRow(1, 1, \
                                       valuesA[0], \
                                       valuesB[0], valuesB[1], valuesB[2], valuesB[3], valuesB[4], valuesB[5], \
                                       valuesC[0], valuesC[1], valuesC[2], valuesC[3])
        
        ##############################
        # 29. 3D SHAPING
        logging.debug(self.__className+'.read_file: 29. 3D SHAPING')
        
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.fh.remTabSpace( stream.readLine() ) )
        
        self.threeDShConf_M.setNumConfigs(0)
        self.threeDShUpDet_M.setNumConfigs(0)
        self.threeDShLoDet_M.setNumConfigs(0)
        
        if data != 0:
            # overread type as it is always 1
            line = stream.readLine()
            
            values =  self.fh.splitLine( stream.readLine() )
            numGroups = int (values[1])
            self.threeDShConf_M.setNumConfigs(numGroups)
            
            for g in range(0, numGroups):
                # ribs and so
                values = self.fh.splitLine( stream.readLine() )
                
                self.threeDShConf_M.updateRow(g+1, 1, values[2], values[3])
                
                # upper config
                values = self.fh.splitLine( stream.readLine() )
                numUpCuts = int (values[1] )
                if numUpCuts == 1:
                    self.threeDShUpDet_M.setNumRowsForConfig(g+1, numUpCuts)
                    
                    values = self.fh.splitLine( stream.readLine() )
                    self.threeDShUpDet_M.updateRow(g+1, 1, values[1], values[2], values[3])
                    
                elif numUpCuts == 2:
                    self.threeDShUpDet_M.setNumRowsForConfig(g+1, numUpCuts)
                    
                    values = self.fh.splitLine( stream.readLine() )
                    self.threeDShUpDet_M.updateRow(g+1, 1, values[1], values[2], values[3])
                    
                    values = self.fh.splitLine( stream.readLine() )
                    self.threeDShUpDet_M.updateRow(g+1, 2, values[1], values[2], values[3])
                    
                # lower config
                values = self.fh.splitLine( stream.readLine() )
                numLoCuts = int (values[1] )
                if numLoCuts == 1:
                    self.threeDShLoDet_M.setNumRowsForConfig(g+1, numUpCuts)
                    
                    values = self.fh.splitLine( stream.readLine() )
                    self.threeDShLoDet_M.updateRow(g+1, 1, values[1], values[2], values[3])
            
            line = stream.readLine()
            
            self.threeDShPr_M.setNumRowsForConfig(1, 0)
            self.threeDShPr_M.setNumRowsForConfig(1, 5)
            
            for l in range(0,5):
                values = self.fh.splitLine( stream.readLine() )
                self.threeDShPr_M.updateRow(1, l+1, values[0], values[1], values[2], values[3], values[4])
                
        ##############################
        # 30. AIRFOIL THICKNESS
        logging.debug(self.__className+'.read_file: 30. AIRFOIL THICKNESS')
        
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.fh.remTabSpace( stream.readLine() ) )
        
        self.airfThick_M.setIsUsed(False)
        
        if data != 0:
            self.airfThick_M.setIsUsed(True)
            # we have data to read
            for l in range( 0, self.wing_M.halfNumRibs ):
                values =  self.fh.splitLine( stream.readLine() )
                self.airfThick_M.updateRow(1, l+1, values[1])
        
        
        ##############################
        # 31. NEW SKIN TENSION
        logging.debug(self.__className+'.read_file: 31. NEW SKIN TENSION')
        
        for i in range(3):
            line = stream.readLine()
            
        data = int( self.fh.remTabSpace( stream.readLine() ) )
        
        self.newSkinTensConf_M.setNumConfigs(0)
        self.newSkinTensDet_M.setNumConfigs(0)
        
        if data != 0:
            numGroups = int( self.fh.remTabSpace( stream.readLine() ) )
            self.newSkinTensConf_M.setNumConfigs(numGroups)
            
            for g in range (0, numGroups):
                # comment line
                line = stream.readLine()
                
                values = self.fh.splitLine( stream.readLine() )
                self.newSkinTensConf_M.updateRow(g+1, values[1], values[2], values[4])
                
                numLines = int(values[3])
                self.newSkinTensDet_M.setNumRowsForConfig(g+1, numLines)
                for l in range (0, numLines):
                    values = self.fh.splitLine( stream.readLine() )
                    self.newSkinTensDet_M.updateRow(g+1, l+1, values[1], values[2], values[3], values[4])
            
        ##############################
        # Cleanup
        in_file.close()
        self.wait_info_w.close()
