"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

import logging

from DataStores.ProcessorModel import ProcessorModel
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMdiSubWindow,
                             QWidget,
                             QSizePolicy,
                             QHeaderView,
                             QSpinBox,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton,
                             QDataWidgetMapper,
                             )
from gui.elements.TableView import TableView
from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar


class AddRibPoints(QMdiSubWindow):
    """
    :class: Window to display and edit Brake line details
    """

    __className = 'AddRibPoints'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        logging.debug(self.__className + '.__init__')
        super().__init__()

        self.addRibPts_M = ProcessorModel.AddRibPointsModel()
        self.addRibPts_M.numRowsForConfigChanged.connect(self.modelSizeChanged)
        self.buildWindow()

    def closeEvent(self, event):  # @UnusedVariable
        """
        :method: Called at the time the user closes the window.
        """
        logging.debug(self.__className + '.closeEvent')

    def buildWindow(self):
        """
        :method: Creates the window including all GUI elements.

        Structure::

            win
                windowLayout
                    numLinesSpin
                    Table
                    -------------------------
                        OrderBtn  helpBar  | btn_bar

        Naming:
            Conf is always one as there is only one configuration possible
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(550, 400)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Additional rib points"))

        self.wrapper = QDataWidgetMapper()
        self.wrapper.setModel(self.addRibPts_M)

        numLines_L = QLabel(_('Number of configs'))
        numLines_L.setAlignment(Qt.AlignRight)
        numLines_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                             QSizePolicy.Fixed))

        self.numLines_S = QSpinBox()
        self.numLines_S.setRange(0, 999)
        self.numLines_S.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                                  QSizePolicy.Fixed))
        self.numLines_S.valueChanged.connect(self.numLinesChange)
        numLinesEdit = self.numLines_S.lineEdit()
        numLinesEdit.setReadOnly(True)

        numLinesLayout = QHBoxLayout()
        numLinesLayout.addWidget(numLines_L)
        numLinesLayout.addWidget(self.numLines_S)
        numLinesLayout.addStretch()
        self.windowLayout.addLayout(numLinesLayout)
        ###############

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.addRibPts_M)

        ribs_T = TableView()
        ribs_T.setModel(self.proxyModel)
        ribs_T.verticalHeader().setVisible(False)
        ribs_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ribs_T.hideColumn(self.addRibPts_M.columnCount() - 1)
        ribs_T.hideColumn(self.addRibPts_M.columnCount() - 2)
        self.windowLayout.addWidget(ribs_T)

        ribs_T.enableIntValidator(ProcessorModel.AddRibPointsModel.OrderNumCol,
                                  ProcessorModel.AddRibPointsModel.OrderNumCol,
                                  1, 999)
        ribs_T.enableDoubleValidator(ProcessorModel.AddRibPointsModel.XCoordCol,
                                     ProcessorModel.AddRibPointsModel.YCoordCol,
                                     1, 100, 2)

        ribs_T.setHelpBar(self.helpBar)
        ribs_T.setHelpText(ProcessorModel.AddRibPointsModel.OrderNumCol,
                           _('OrderNumDesc'))
        ribs_T.setHelpText(ProcessorModel.AddRibPointsModel.XCoordCol,
                           _('AddRibPts-XCoordDesc'))
        ribs_T.setHelpText(ProcessorModel.AddRibPointsModel.YCoordCol,
                           _('AddRibPts-YCoordDesc'))

        sortBtn = QPushButton(_('Sort by orderNum'))
        sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                          QSizePolicy.Fixed))
        sortBtn.clicked.connect(self.sortBtnPress)

        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue(self.addRibPts_M.numRowsForConfig(1))
        self.numLines_S.blockSignals(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/addRibPoints.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(sortBtn)
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)

        self.win.setLayout(self.windowLayout)

    def modelSizeChanged(self):
        """
        :method: Called after the model has been changed it's size. Herein we
                 assure the GUI follows the model.
        """
        logging.debug(self.__className + '.modelSizeChanged')
        self.numLines_S.blockSignals(True)
        self.numLines_S.setValue(self.addRibPts_M.numRowsForConfig(1))
        self.numLines_S.blockSignals(False)

    def numLinesChange(self):
        """
        :method: Called upon manual changes of the lines spin. Does assure all
                 elements will follow the user configuration.
        """
        logging.debug(self.__className + '.numLinesChange')
        self.addRibPts_M.setNumRowsForConfig(1, self.numLines_S.value())

    def sortBtnPress(self):
        """
        :method: Executed if the sort button is pressed. Does a one time sort
                 based on the numbers in the OrderNum column.
        """
        logging.debug(self.__className + '.sortBtnPress')

        self.proxyModel.sort(ProcessorModel.AddRibPointsModel.OrderNumCol,
                             Qt.AscendingOrder)
        self.proxyModel.setDynamicSortFilter(False)

    def btnPress(self, q):
        """
        :method: Handling of all pressed buttons.
        """
        logging.debug(self.__className + '.btn_press')
        if q == 'Apply':
            pass

        elif q == 'Ok':
            self.close()

        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className
                          + '.btn_press unrecognized button press '
                          + q)
