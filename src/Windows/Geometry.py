'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget,\
                            QSizePolicy, QHeaderView, QPushButton
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel


class Geometry(QMdiSubWindow):
    '''
    :class: Window to display and edit geometry data
    '''

    __className = 'Geometry'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()

        self.rib_M = ProcessorModel.RibModel()
        self.buildWindow()

    def closeEvent(self, event):  # @UnusedVariable
        '''
        :method: Called at the time the user closes the window.
        '''
        logging.debug(self.__className+'.closeEvent')

    def buildWindow(self):
        '''
        :method: Creates the window including all GUI elements.

        Layout::

            Data
            Buttons

        Structure::

            win
                windowLayout
                     Table
                    --------------------------
                    SortBtn | helpBar | btnBar

        '''
        logging.debug(self.__className + '.buildWindow')

        self.setWindowIcon(QIcon('Windows\\appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(900, 300)

        self.windowLayout = QVBoxLayout()

        self.helpBar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Geometry"))

        self.table = TableView()
        self.table.setModel(self.rib_M)
        # hide the ID column which is always at the end of the model
        self.table.hideColumn(self.rib_M.columnCount() - 1)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHelpBar(self.helpBar)

        self.table.setHelpText(ProcessorModel.RibModel.RibNumCol,
                               _('Proc-RibNumDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.xribCol,
                               _('Proc-xribDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.yLECol,
                               _('Proc-yLEDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.yTECol,
                               _('Proc-yTEDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.xpCol,
                               _('Proc-xpDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.zCol,
                               _('Proc-zDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.betaCol,
                               _('Proc-betaDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.RPCol,
                               _('Proc-RPDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.WashinCol,
                               _('Proc-WashinDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.RotZCol,
                               _('Proc-RotZDesc'))
        self.table.setHelpText(ProcessorModel.RibModel.PosZCol,
                               _('Proc-PosZDesc'))

        self.table.enableIntValidator(ProcessorModel.RibModel.RibNumCol,
                                      ProcessorModel.RibModel.RibNumCol,
                                      1, 999)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.xribCol,
                                         ProcessorModel.RibModel.xribCol,
                                         -500, 3000, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.yLECol,
                                         ProcessorModel.RibModel.yTECol,
                                         -500, 1000, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.xpCol,
                                         ProcessorModel.RibModel.xpCol,
                                         -500, 3000, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.zCol,
                                         ProcessorModel.RibModel.zCol,
                                         -500, 3000, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.betaCol,
                                         ProcessorModel.RibModel.betaCol,
                                         0, 105, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.RPCol,
                                         ProcessorModel.RibModel.RPCol,
                                         0, 100, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.WashinCol,
                                         ProcessorModel.RibModel.WashinCol,
                                         -45, 45, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.RotZCol,
                                         ProcessorModel.RibModel.RotZCol,
                                         -45, 45, 3)
        self.table.enableDoubleValidator(ProcessorModel.RibModel.PosZCol,
                                         ProcessorModel.RibModel.PosZCol,
                                         0, 100, 3)

        self.windowLayout.addWidget(self.table)

        self.sortBtn = QPushButton(_('Sort by Rib Number'))
        self.sortBtn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                               QSizePolicy.Fixed))
        self.sortBtn.clicked.connect(self.sortBtnPress)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/geometry.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.sortBtn)
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)

        self.windowLayout.addLayout(bottomLayout)

        self.win.setLayout(self.windowLayout)

    def sortBtnPress(self):
        '''
        : method : handles the sort of the table by rib number
        '''
        logging.debug(self.__className+'.sortBtnPress')
        self.rib_M.sortTable(ProcessorModel.RibModel.RibNumCol,
                             Qt.AscendingOrder)

    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className+'.btnPress')
        if q == 'Apply':
            pass

        elif q == 'Ok':
            self.close()

        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className +
                          '.btnPress unrecognized button press ' +
                          q)
