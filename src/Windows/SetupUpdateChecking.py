'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QLabel, QComboBox, QCheckBox
from Windows.WindowBtnBar import WindowBtnBar
from ConfigReader.ConfigReader import ConfigReader

class SetupUpdateChecking(QMdiSubWindow):
    '''
    :class: Window to display and edit the Basic Data  
    '''

    __className = 'SetupUpdateChecking'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.confRdr = ConfigReader()

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
        
            win
                window_Ly 
                     Labels    | Edit fields
                     ...       | ...
                    -------------------------
                                | helpBar
                                | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(300, 150)

        self.window_Ly = QGridLayout()
        __winGRowL = 0
        __winGRowR = 0
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Setup update checking"))
        
        update_L = QLabel(_('Perform update checks at start'))
        update_L.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.update_ChB = QCheckBox()
        self.update_ChB.toggled.connect(self.updateChBChange)
        self.window_Ly.addWidget(update_L, __winGRowL, 0)
        self.window_Ly.addWidget(self.update_ChB, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        branch_L = QLabel(_('Branch'))
        branch_L.setAlignment(Qt.AlignRight)
        self.branch_CB = QComboBox()
        self.branch_CB.addItem(_("stable"))
        self.branch_CB.addItem(_("latest"))
        if self.confRdr.getTrackBranch() == 'stable':
            self.branch_CB.setCurrentIndex(0)
        else:
            self.branch_CB.setCurrentIndex(1)
            
        self.branch_CB.currentIndexChanged.connect(self.branchCbChange)
        self.branch_CB.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.window_Ly.addWidget(branch_L, __winGRowL, 0)
        self.window_Ly.addWidget(self.branch_CB, __winGRowR, 1)
        __winGRowL += 1
        __winGRowR += 1
        
        if self.confRdr.getCheckForUpdates() == 'yes':
            self.update_ChB.setChecked(True)
            self.branch_CB.setEnabled(True)
        else:
            self.update_ChB.setChecked(False)
            self.branch_CB.setEnabled(False)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('setup/updateCheck.html')

        self.window_Ly.addWidget(self.btnBar, __winGRowR ,1, Qt.AlignRight)
        __winGRowR += 1
        
        self.win.setLayout(self.window_Ly)

    def updateChBChange(self):
        '''
        :method: Called at the time the user alters the update checkbox
        ''' 
        logging.debug(self.__className + '.updateChBChange')
        
        if self.update_ChB.isChecked():
            self.confRdr.setCheckForUpdates('yes')
            self.branch_CB.setEnabled(True)
        else:
            self.confRdr.setCheckForUpdates('no')
            self.branch_CB.setEnabled(False)
        
    def branchCbChange(self):
        '''
        :method: Called at the time the user alters the branch combo box. 
        ''' 
        logging.debug(self.__className + '.branchCbChange')
        
        if self.branch_CB.currentIndex() ==0:
            self.confRdr.setTrackBranch('stable')
        else:
            self.confRdr.setTrackBranch('latest')
    
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        logging.debug(self.__className + '.btnPress')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    