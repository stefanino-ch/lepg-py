'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QSizePolicy, QHeaderView,\
                            QSpinBox, QLabel, QTabWidget, QHBoxLayout,\
                            QVBoxLayout, QPushButton, QDataWidgetMapper
from gui.elements.LineEdit import LineEdit
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.ProcModel import ProcModel


class Lines(QMdiSubWindow):
    '''
    :class: Window to display and edit lines data
    '''

    __className = 'Lines'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()

        self.wing_M = ProcModel.WingModel()
        self.wing_M.dataChanged.connect(self.wingModelDataChange)

        self.lines_M = ProcModel.LinesModel()
        self.lines_M.numRowsForConfigChanged.connect(self.modelSizeChanged)

        self.proxyModel = []
        self.numLines_S = []

        self.buildWindow()

    def closeEvent(self, event):  # @UnusedVariable
        '''
        :method: Called at the time the user closes the window.
        '''
        logging.debug(self.__className+'.closeEvent')

    def buildWindow(self):
        '''
        :method: Creates the window including all GUI elements.

        Structure::

            window
                window_ly
                    config edit
                    numConfSpin
                    Tabs
                        numLinesSpin
                        LinesTable
                    -------------------------
                        OrderBtn | help_bar  | btn_bar

        Naming:

            conf equals plans
            details equals line paths
        '''
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(1100, 400)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Edit Lines"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.wing_M)

        contr_L = QLabel(_('Lines control parameter'))
        contr_L.setAlignment(Qt.AlignRight)
        self.contr_E = LineEdit()
        self.contr_E.setFixedWidth(40)
        self.wrapper.addMapping(self.contr_E,
                                ProcModel.WingModel.LinesConcTypeCol)
        self.contr_E.enableIntValidator(0, 3)
        self.contr_E.setHelpText(_('Lines-LinesControlParamDesc'))
        self.contr_E.setHelpBar(self.helpBar)

        contrLayout = QHBoxLayout()
        contrLayout.addWidget(contr_L)
        contrLayout.addWidget(self.contr_E)
        contrLayout.addStretch()

        self.windowLayout.addLayout(contrLayout)

        numConf_L = QLabel(_('Number of Line plans'))
        numConf_L.setAlignment(Qt.AlignRight)
        numConf_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                            QSizePolicy.Fixed))

        self.numConf_S = QSpinBox()
        self.numConf_S.setRange(0, 999)
        self.numConf_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                                 QSizePolicy.Fixed))
        self.numConf_S.setValue(self.lines_M.numConfigs())

        edit = self.numConf_S.lineEdit()
        edit.setReadOnly(True)
        self.numConf_S.valueChanged.connect(self.confSpinChange)

        numConfLayout = QHBoxLayout()
        numConfLayout.addWidget(numConf_L)
        numConfLayout.addWidget(self.numConf_S)
        numConfLayout.addStretch()
        self.windowLayout.addLayout(numConfLayout)

        self.tabs = QTabWidget()
        self.windowLayout.addWidget(self.tabs)

        # check if there's already data
        if self.lines_M.numConfigs() > 0:
            self.modelSizeChanged()

        sortBtn = QPushButton(_('Sort by order_num'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                          QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)

        self.wrapper.toFirst()
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/lines.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(sortBtn)
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)

        self.win.setLayout(self.windowLayout)

    def confSpinChange(self):
        '''
        :method: Called upon manual changes of the config spin. Does assure
                 all elements will follow the user configuration.
        '''
        logging.debug(self.__className+'.confSpinChange')
        currNumConfigs = self.lines_M.numConfigs()
        mustNumConfigs = self.numConf_S.value()

        if currNumConfigs > mustNumConfigs:
            # more tabs than we should have -> remove last
            self.lines_M.setNumRowsForConfig(currNumConfigs, 0)

        if currNumConfigs < mustNumConfigs:
            # missing configs -> add one
            self.lines_M.setNumRowsForConfig(mustNumConfigs, 1)

    def modelSizeChanged(self):
        '''
        :method: Called after the model has been changed it's size.
                 Herein we assure the GUI follows the model.
        '''
        logging.debug(self.__className+'.modelSizeChanged')

        currNumConfigs = self.lines_M.numConfigs()

        # config (num plans) spinbox
        if self.numConf_S.value() != currNumConfigs:
            self.numConf_S.blockSignals(True)
            self.numConf_S.setValue(currNumConfigs)
            self.numConf_S.blockSignals(False)

        # number of tabs
        diff = abs(currNumConfigs - self.tabs.count())
        if diff != 0:
            # we have to update the tabs
            i = 0
            if currNumConfigs > self.tabs.count():
                # add tabs
                while i < diff:
                    self.addTab()
                    i += 1
            else:
                # remove tabs
                while i < diff:
                    self.removeTab()
                    i += 1

        # update lines (pahts) spin
        i = 0
        while i < self.tabs.count():
            if self.numLines_S[i].value != self.lines_M.numRowsForConfig(i+1):
                self.numLines_S[i].blockSignals(True)
                self.numLines_S[i].setValue(self.lines_M.numRowsForConfig(i+1))
                self.numLines_S[i].blockSignals(False)
            i += 1

    def addTab(self):
        '''
        :method: Creates a new tab inculding all its widgets.
        '''
        logging.debug(self.__className+'.addTab')

        currNumTabs = self.tabs.count()

        tabWidget = QWidget()
        tabLayout = QVBoxLayout()

        # Data lines
        numLinesLayout = QHBoxLayout()

        numLines_L = QLabel(_('Number of Line paths'))
        numLines_L.setAlignment(Qt.AlignRight)
        numLines_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                             QSizePolicy.Fixed))
        self.numLines_S.append(QSpinBox())
        self.numLines_S[currNumTabs].setRange(1, 999)
        self.numLines_S[currNumTabs].setSizePolicy(QSizePolicy(
                                                    QSizePolicy.Fixed,
                                                    QSizePolicy.Fixed))
        self.numLines_S[currNumTabs].valueChanged.connect(self.numLinesChange)
        pathEdit = self.numLines_S[currNumTabs].lineEdit()
        pathEdit.setReadOnly(True)
        numLinesLayout.addWidget(numLines_L)
        numLinesLayout.addWidget(self.numLines_S[currNumTabs])
        numLinesLayout.addStretch()
        tabLayout.addLayout(numLinesLayout)

        self.proxyModel.append(QSortFilterProxyModel())
        self.proxyModel[currNumTabs].setSourceModel(self.lines_M)
        self.proxyModel[currNumTabs].setFilterKeyColumn(
                                        ProcModel.LinesModel.ConfigNumCol)

        self.proxyModel[currNumTabs].setFilterRegExp(
                                        QRegExp(str(currNumTabs+1)))

        branchTable = TableView()
        branchTable.setModel(self.proxyModel[currNumTabs])
        branchTable.verticalHeader().setVisible(False)
        branchTable.horizontalHeader().setSectionResizeMode(
                                            QHeaderView.Stretch)
        branchTable.hideColumn(self.lines_M.columnCount()-1)
        branchTable.hideColumn(self.lines_M.columnCount()-2)
        tabLayout.addWidget(branchTable)

        branchTable.enableIntValidator(
                        ProcModel.LinesModel.OrderNumCol,
                        ProcModel.LinesModel.OrderNumCol,
                        1,
                        999)
        branchTable.enableIntValidator(
                        ProcModel.LinesModel.NumBranchesCol,
                        ProcModel.LinesModel.NumBranchesCol,
                        1,
                        4)
        branchTable.enableIntValidator(
                        ProcModel.LinesModel.BranchLvlOneCol,
                        ProcModel.LinesModel.OrderLvlFourCol,
                        1,
                        99)
        branchTable.enableIntValidator(
                        ProcModel.LinesModel.AnchorLineCol,
                        ProcModel.LinesModel.AnchorLineCol,
                        1,
                        6)
        branchTable.enableIntValidator(
                        ProcModel.LinesModel.AnchorRibNumCol,
                        ProcModel.LinesModel.AnchorRibNumCol,
                        1,
                        999)

        branchTable.setHelpBar(self.helpBar)
        branchTable.setHelpText(
                        ProcModel.LinesModel.OrderNumCol,
                        _('OrderNumDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.NumBranchesCol,
                        _('Lines-NumBranchesDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.BranchLvlOneCol,
                        _('Lines-BranchLvlOneDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.OrderLvlOneCol,
                        _('Lines-OrderLvlOneDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.LevelOfRamTwoCol,
                        _('Lines-LevelOfRamTwoDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.OrderLvlTwoCol,
                        _('Lines-OrderLvlTwoDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.LevelOfRamThreeCol,
                        _('Lines-LevelOfRamThreeDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.OrderLvlThreeCol,
                        _('Lines-OrderLvlThreeDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.BranchLvlFourCol,
                        _('Lines-BranchLvlFourDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.OrderLvlFourCol,
                        _('Lines-OrderLvlFourDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.AnchorLineCol,
                        _('Lines-AnchorLineDesc'))
        branchTable.setHelpText(
                        ProcModel.LinesModel.AnchorRibNumCol,
                        _('Lines-AnchorRibNumDesc'))

        tabWidget.setLayout(tabLayout)

        i = self.tabs.addTab(tabWidget, str(currNumTabs+1))
        self.tabs.setCurrentIndex(i)

    def removeTab(self):
        '''
        :method: Removes the last tab from the GUI. Does take care at the same
                 time of the class internal elements and the data model.
        '''
        logging.debug(self.__className+'.removeTab')
        numTabs = self.tabs.count()
        self.tabs.removeTab(numTabs-1)
        # cleanup arrays
        self.proxyModel.pop(numTabs-1)
        self.numLines_S.pop(numTabs-1)

    def numLinesChange(self):
        '''
        :method: Called upon manual changes of the lines spin. Does assure
                 all elements will follow the user configuration.
        '''
        logging.debug(self.__className+'.num_lines_change')
        self.lines_M.setNumRowsForConfig(
                        self.tabs.currentIndex()+1,
                        self.numLines_S[self.tabs.currentIndex()].value())

    def wingModelDataChange(self):
        '''
        :method: Called if data in wing model changes. As mappings are lost
                 upon the use of select we have potentially to re establish
                 the mapping again.
        '''
        self.wrapper.addMapping(self.contr_E,
                                ProcModel.WingModel.LinesConcTypeCol)

    def sortBtnPress(self):
        '''
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        '''
        logging.debug(self.__className+'.sortBtnPress')

        if self.tabs.count() > 0:
            currTab = self.tabs.currentIndex()
            self.proxyModel[currTab].sort(
                                    ProcModel.LinesModel.OrderNumCol,
                                    Qt.AscendingOrder)
            self.proxyModel[currTab].setDynamicSortFilter(False)

    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className+'.btn_press')
        if q == 'Apply':
            pass

        elif q == 'Ok':
            self.close()

        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className +
                          '.btn_press unrecognized button press '+q)
