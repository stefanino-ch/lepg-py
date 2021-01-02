'''
:author: Stefan Feuz; http://www.laboratoridenvol.com
:license: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy, QMessageBox, QGroupBox, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QLabel
from Windows.LineEdit import LineEdit
from Windows.WindowBtnBar import WindowBtnBar
from Windows.WindowHelpBar import WindowHelpBar
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.PreProcessorStore import PreProcessorStore

class PreProcDataEdit(QMdiSubWindow):
    '''
    :class: Window to display and edit the PreProc data. 
    '''
    dataStatusUpdate = pyqtSignal(str,str)
    '''
    :signal: Sent out as soon the user has edited data or has clicked a button. The first string indicates the window name. The second string indicates if and which button has been pressed.
    '''
    __windowName = 'PreProcDataEdit'

    def __init__(self):
        '''
        :classmethod: Constructor
        '''
        logging.debug(self.__windowName+'.__init__')
        super().__init__()
        self.pps = PreProcessorStore()
        self.dws = DataWindowStatus()
        self.dws.registerSignal(self.dataStatusUpdate)
        self.buildWindow()
        self.pps.dataStatusUpdate.connect(self.updateInputs)   

    def closeEvent(self, event):  # @UnusedVariable
        '''
        :classmethod: called at the time the user closes the window. Does check for unsaved data and warns the user in case. 
        '''
        # Check for unapplied data
        if self.dws.getWindowDataStatus(self.__windowName) == 0:
            # there is unapplied data
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Changed data")
            msgBox.setText("Data changed in this window has not been applied.\n\nPress OK to close the window, data will be lost.\nPress Cancel to abort. ")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            answer = msgBox.exec()
            
            if answer == QMessageBox.Ok:
                # user wants to quit, dont save, close
                self.dataStatusUpdate.emit(self.__windowName,'Cancel')
                self.dws.unregisterSignal(self.dataStatusUpdate)
                self.dws.unregisterWindow(self.__windowName)
                self.pps.dataStatusUpdate.disconnect(self.updateInputs)
                logging.debug(self.__windowName+'.closeEvent')
                event.accept()
            else:
                # abort cancel 
                event.ignore()
   
    def buildWindow(self):
        '''
        :classmethod: Creates the window including all GUI elements. 
        
        Layout::
        
            Data
            Help window
            Buttons
            
        Structure:: 
        
            win
                windowGrid                        |
                    wing_F                        |
                        wing_G                    |
                    --------------------------------------------------------
                    edge_L                        |    vault_F
                        le_F            te_F      |        vault_G
                            le_G            te_G  |
                    ---------------------------------------------------------
                    cd_F                          |    helpBar
                        cd_G                      |                
                    --------------------------------------------------------
                                                  |    btnBar
        '''
        logging.debug(self.__windowName + '.buildWindow')
        __frameWidth = 350
        __col0width = 60
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)

        self.windowGrid = QGridLayout()
        __winGRowL = 0
        __winGRowR = 0
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Pre Processor data edit"))
        
        # Wing Frame
        self.wing_F = QGroupBox()    
        self.wing_F.setTitle(_("Wing"))
        self.wing_F.setFixedWidth(__frameWidth)
        self.windowGrid.addWidget(self.wing_F, __winGRowL, 0, Qt.AlignLeft)
        __winGRowL += 1
        
        self.wing_G = QGridLayout()
        self.wing_G.setColumnMinimumWidth(0, __col0width)
        self.wing_F.setLayout(self.wing_G)
        
        self.wingName_L = QLabel(_('Wing name'))
        self.wingName_L.setAlignment(Qt.AlignRight)
        self.wingName_E = LineEdit()
        self.wingName_E.enableRegExpValidator("(.|\s)*\S(.|\s)*")
        self.wingName_E.setText(self.pps.getSingleVal('WingName'))
        self.wingName_E.textEdited.connect(self.dataStatusChanged)
        self.wingName_E.setHelpText(_('PreProc-WingNameDesc'))
        self.wingName_E.setHelpBar(self.helpBar)
        self.wing_G.addWidget(self.wingName_L, 0, 0)
        self.wing_G.addWidget(self.wingName_E, 0, 1)

        # Edge layout
        self.edge_L = QHBoxLayout()
        self.windowGrid.addLayout(self.edge_L, __winGRowL, 0, Qt.AlignLeft)
        __winGRowL += 1
        
        # Leading Edge Frame
        self.le_F = QGroupBox()    
        self.le_F.setTitle(_("Leading Edge"))
        self.le_F.setFixedWidth(__frameWidth/2)
        self.edge_L.addWidget(self.le_F)
        
        self.le_G = QGridLayout()
        self.le_G.setColumnMinimumWidth(0, __col0width)
        self.le_F.setLayout(self.le_G)
        __leGRow = 0
        
        self.le_type_L = QLabel(_('Type'))
        self.le_type_L.setAlignment(Qt.AlignRight)
        self.le_type_E = LineEdit()
        self.le_type_E.setText(self.pps.getSingleVal('LE_type'))
        self.le_type_E.textEdited.connect(self.dataStatusChanged)
        self.le_type_E.setHelpText(_('PreProc-le_type_desc'))
        self.le_type_E.setHelpBar(self.helpBar)
        self.le_type_E.setEnabled(False)
        self.le_G.addWidget(self.le_type_L, __leGRow, 0)
        self.le_G.addWidget(self.le_type_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_a1_L = QLabel('a1 [cm]')
        self.le_a1_L.setAlignment(Qt.AlignRight)
        self.le_a1_E = LineEdit()
        self.le_a1_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_a1_E.setText(self.pps.getSingleVal('LE_a1'))
        self.le_a1_E.textEdited.connect(self.dataStatusChanged)
        self.le_a1_E.setHelpText(_('PreProc-le_a1_desc'))
        self.le_a1_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_a1_L, __leGRow, 0)
        self.le_G.addWidget(self.le_a1_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_b1_L = QLabel('b1 [cm]')
        self.le_b1_L.setAlignment(Qt.AlignRight)
        self.le_b1_E = LineEdit()
        self.le_b1_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_b1_E.setText(self.pps.getSingleVal('LE_b1'))
        self.le_b1_E.textEdited.connect(self.dataStatusChanged)
        self.le_b1_E.setHelpText(_('PreProc-le_b1_desc'))
        self.le_b1_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_b1_L, __leGRow, 0)
        self.le_G.addWidget(self.le_b1_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_x1_L = QLabel('x1 [cm]')
        self.le_x1_L.setAlignment(Qt.AlignRight)
        self.le_x1_E = LineEdit()
        self.le_x1_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_x1_E.setText(self.pps.getSingleVal('LE_x1'))
        self.le_x1_E.textEdited.connect(self.dataStatusChanged)
        self.le_x1_E.setHelpText(_('PreProc-le_x1_desc'))
        self.le_x1_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_x1_L, __leGRow, 0)
        self.le_G.addWidget(self.le_x1_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_x2_L = QLabel('x2 [cm]')
        self.le_x2_L.setAlignment(Qt.AlignRight)
        self.le_x2_E = LineEdit()
        self.le_x2_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_x2_E.setText(self.pps.getSingleVal('LE_x2'))
        self.le_x2_E.textEdited.connect(self.dataStatusChanged)
        self.le_x2_E.setHelpText(_('PreProc-le_x2_desc'))
        self.le_x2_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_x2_L, __leGRow, 0)
        self.le_G.addWidget(self.le_x2_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_xm_L = QLabel('xm [cm]')
        self.le_xm_L.setAlignment(Qt.AlignRight)
        self.le_xm_E = LineEdit()
        self.le_xm_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_xm_E.setText(self.pps.getSingleVal('LE_xm'))
        self.le_xm_E.textEdited.connect(self.dataStatusChanged)
        self.le_xm_E.setHelpText(_('PreProc-le_xm_desc'))
        self.le_xm_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_xm_L, __leGRow, 0)
        self.le_G.addWidget(self.le_xm_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_c01_L = QLabel('c01 [cm]')
        self.le_c01_L.setAlignment(Qt.AlignRight)
        self.le_c01_E = LineEdit()
        self.le_c01_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_c01_E.setText(self.pps.getSingleVal('LE_c01'))
        self.le_c01_E.textEdited.connect(self.dataStatusChanged)
        self.le_c01_E.setHelpText(_('PreProc-le_c0_desc'))
        self.le_c01_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_c01_L, __leGRow, 0)
        self.le_G.addWidget(self.le_c01_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_ex1_L = QLabel('ex1 [coef]')
        self.le_ex1_L.setAlignment(Qt.AlignRight)
        self.le_ex1_E = LineEdit()
        self.le_ex1_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_ex1_E.setText(self.pps.getSingleVal('LE_ex1'))
        self.le_ex1_E.textEdited.connect(self.dataStatusChanged)
        self.le_ex1_E.setHelpText(_('PreProc-te_ex1_desc'))
        self.le_ex1_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_ex1_L, __leGRow, 0)
        self.le_G.addWidget(self.le_ex1_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_c02_L = QLabel('c02 [cm]')
        self.le_c02_L.setAlignment(Qt.AlignRight)
        self.le_c02_E = LineEdit()
        self.le_c02_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_c02_E.setText(self.pps.getSingleVal('LE_c02'))
        self.le_c02_E.textEdited.connect(self.dataStatusChanged)
        self.le_c02_E.setHelpText(_('PreProc-le_c02_desc'))
        self.le_c02_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_c02_L, __leGRow, 0)
        self.le_G.addWidget(self.le_c02_E, __leGRow, 1)
        __leGRow += 1
        
        self.le_ex2_L = QLabel('ex2 [coef]')
        self.le_ex2_L.setAlignment(Qt.AlignRight)
        self.le_ex2_E = LineEdit()
        self.le_ex2_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.le_ex2_E.setText(self.pps.getSingleVal('LE_ex2'))
        self.le_ex2_E.textEdited.connect(self.dataStatusChanged)
        self.le_ex2_E.setHelpText(_('PreProc-le_ex2_desc'))
        self.le_ex2_E.setHelpBar(self.helpBar)
        self.le_G.addWidget(self.le_ex2_L, __leGRow, 0)
        self.le_G.addWidget(self.le_ex2_E, __leGRow, 1)
        __leGRow += 1
        
        # Trailing Edge Frame
        self.te_F = QGroupBox()    
        self.te_F.setTitle(_("Trailing Edge"))
        self.te_F.setFixedWidth(__frameWidth/2)
        self.edge_L.addWidget(self.te_F)

        self.te_G = QGridLayout()
        self.te_G.setColumnMinimumWidth(0, __col0width)
        self.te_F.setLayout(self.te_G)
        __teGRow = 0
        
        self.te_type_L = QLabel(_('Type'))
        self.te_type_L.setAlignment(Qt.AlignRight)
        self.te_type_E = LineEdit()
        self.te_type_E.setText(self.pps.getSingleVal('TE_type'))
        self.te_type_E.textEdited.connect(self.dataStatusChanged)
        self.te_type_E.setHelpText(_('PreProc-te_type_desc'))
        self.te_type_E.setHelpBar(self.helpBar)
        self.te_type_E.setEnabled(False)
        self.te_G.addWidget(self.te_type_L, __teGRow, 0)
        self.te_G.addWidget(self.te_type_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_a1_L = QLabel('a1 [cm]')
        self.te_a1_L.setAlignment(Qt.AlignRight)
        self.te_a1_E = LineEdit()
        self.te_a1_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.te_a1_E.setText(self.pps.getSingleVal('TE_a1'))
        self.te_a1_E.textEdited.connect(self.dataStatusChanged)
        self.te_a1_E.setHelpText(_('PreProc-te_a1_desc'))
        self.te_a1_E.setHelpBar(self.helpBar)
        self.te_G.addWidget(self.te_a1_L, __teGRow, 0)
        self.te_G.addWidget(self.te_a1_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_b1_L = QLabel('b1 [cm]')
        self.te_b1_L.setAlignment(Qt.AlignRight)
        self.te_b1_E = LineEdit()
        self.te_b1_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.te_b1_E.setText(self.pps.getSingleVal('TE_b1'))
        self.te_b1_E.textEdited.connect(self.dataStatusChanged)
        self.te_b1_E.setHelpText(_('PreProc-te_b1_desc'))
        self.te_b1_E.setHelpBar(self.helpBar)
        self.te_G.addWidget(self.te_b1_L, __teGRow, 0)
        self.te_G.addWidget(self.te_b1_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_x1_L = QLabel('x1 [cm]')
        self.te_x1_L.setAlignment(Qt.AlignRight)
        self.te_x1_E = LineEdit()
        self.te_x1_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.te_x1_E.setText(self.pps.getSingleVal('TE_x1'))
        self.te_x1_E.textEdited.connect(self.dataStatusChanged)
        self.te_x1_E.setHelpText(_('PreProc-te_x1_desc'))
        self.te_x1_E.setHelpBar(self.helpBar)
        self.te_G.addWidget(self.te_x1_L, __teGRow, 0)
        self.te_G.addWidget(self.te_x1_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_xm_L = QLabel('xm [cm]')
        self.te_xm_L.setAlignment(Qt.AlignRight)
        self.te_xm_E = LineEdit()
        self.te_xm_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.te_xm_E.setText(self.pps.getSingleVal('TE_xm'))
        self.te_xm_E.textEdited.connect(self.dataStatusChanged)
        self.te_xm_E.setHelpText(_('PreProc-te_xm_desc'))
        self.te_xm_E.setHelpBar(self.helpBar)
        self.te_G.addWidget(self.te_xm_L, __teGRow, 0)
        self.te_G.addWidget(self.te_xm_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_c0_L = QLabel('c0 [cm]')
        self.te_c0_L.setAlignment(Qt.AlignRight)
        self.te_c0_E = LineEdit()
        self.te_c0_E.enableDoubleValidator(-9999.99, 9999.99, 2)
        self.te_c0_E.setText(self.pps.getSingleVal('TE_c0'))
        self.te_c0_E.textEdited.connect(self.dataStatusChanged)
        self.te_c0_E.setHelpText(_('PreProc-te_c0_desc'))
        self.te_c0_E.setHelpBar(self.helpBar)
        self.te_G.addWidget(self.te_c0_L, __teGRow, 0)
        self.te_G.addWidget(self.te_c0_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_y0_L = QLabel('y0 [cm]')
        self.te_y0_L.setAlignment(Qt.AlignRight)
        self.te_y0_E = LineEdit()
        self.te_y0_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.te_y0_E.setText(self.pps.getSingleVal('TE_y0'))
        self.te_y0_E.textEdited.connect(self.dataStatusChanged)
        self.te_y0_E.setHelpText(_('PreProc-te_y0_desc'))
        self.te_y0_E.setHelpBar(self.helpBar)
        self.te_G.addWidget(self.te_y0_L, __teGRow, 0)
        self.te_G.addWidget(self.te_y0_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_exp_L = QLabel('exp [coef]')
        self.te_exp_L.setAlignment(Qt.AlignRight)
        self.te_exp_E = LineEdit()
        self.te_exp_E.enableDoubleValidator(0.00, 9999.99, 2)
        self.te_exp_E.setText(self.pps.getSingleVal('TE_exp'))
        self.te_exp_E.textEdited.connect(self.dataStatusChanged)
        self.te_exp_E.setHelpText(_('PreProc-te_exp_desc'))
        self.te_exp_E.setHelpBar(self.helpBar)
        self.te_G.addWidget(self.te_exp_L, __teGRow, 0)
        self.te_G.addWidget(self.te_exp_E, __teGRow, 1)
        __teGRow += 1
        
        self.te_sp1_L = QLabel('')
        self.te_G.addWidget(self.te_sp1_L, __teGRow, 0)
        __teGRow += 1
        self.te_sp2_L = QLabel('')
        self.te_G.addWidget(self.te_sp2_L, __teGRow, 0)
        
        # Switch to next column
        __winGRowR = 1
        
        # Vault
        self.vault_F = QGroupBox()    
        self.vault_F.setTitle(_("Vault"))
        self.vault_F.setFixedWidth(__frameWidth)
        self.windowGrid.addWidget(self.vault_F, __winGRowR, 1, Qt.AlignLeft)
        __winGRowR += 1
        
        self.vault_G = QGridLayout()
        self.vault_G.setColumnMinimumWidth(0, __col0width/2)
        self.vault_G.setColumnMinimumWidth(2, __col0width/2)
        self.vault_G.setColumnMinimumWidth(4, __col0width/2)
        self.vault_F.setLayout(self.vault_G)
        __vaultGRow = 0
        
        self.vault_cb_L = QLabel(_('Type'))
        self.vault_cb = QComboBox()
        self.vault_cb.addItem(_("Sin-Cos"))
        self.vault_cb.addItem(_("Radius-Angle"))
        self.vault_cb.setCurrentIndex( int(self.pps.getSingleVal('Vault_type')) -1 )
        self.vault_cb.currentIndexChanged.connect(self.vault_cb_change)
        self.vault_G.addWidget(self.vault_cb_L, __vaultGRow, 0, Qt.AlignRight )
        self.vault_G.addWidget(self.vault_cb, __vaultGRow, 1, Qt.AlignRight )
        __vaultGRow += 1
        
        # Vault Type 1
        self.vault1_a1_L = QLabel('a1 [cm]')
        self.vault1_a1_E = LineEdit()
        self.vault1_a1_E.enableDoubleValidator(0.0000, 9999.9999, 4)
        self.vault1_a1_E.setText(self.pps.getSingleVal('Vault_a1'))
        self.vault1_a1_E.textEdited.connect(self.dataStatusChanged)
        self.vault1_a1_E.setHelpText(_('PreProc-vault1_a1_desc'))
        self.vault1_a1_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault1_a1_L, __vaultGRow, 0, Qt.AlignRight )
        self.vault_G.addWidget(self.vault1_a1_E, __vaultGRow, 1, Qt.AlignRight )
        __vaultGRow += 1

        self.vault1_b1_L = QLabel('b1 [cm]')
        self.vault1_b1_E = LineEdit()
        self.vault1_b1_E.enableDoubleValidator(0.0000, 9999.9999, 4)
        self.vault1_b1_E.setText(self.pps.getSingleVal('Vault_b1'))
        self.vault1_b1_E.textEdited.connect(self.dataStatusChanged)
        self.vault1_b1_E.setHelpText(_('PreProc-vault1_b1_desc'))
        self.vault1_b1_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault1_b1_L, __vaultGRow, 0, Qt.AlignRight )
        self.vault_G.addWidget(self.vault1_b1_E, __vaultGRow, 1, Qt.AlignRight )
        __vaultGRow += 1

        self.vault1_x1_L = QLabel('x1 [cm]')
        self.vault1_x1_E = LineEdit()
        self.vault1_x1_E.enableDoubleValidator(0.0000, 9999.9999, 4)
        self.vault1_x1_E.setText(self.pps.getSingleVal('Vault_x1'))
        self.vault1_x1_E.textEdited.connect(self.dataStatusChanged)
        self.vault1_x1_E.setHelpText(_('PreProc-vault1_x1_desc'))
        self.vault1_x1_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault1_x1_L, __vaultGRow, 0, Qt.AlignRight )
        self.vault_G.addWidget(self.vault1_x1_E, __vaultGRow, 1, Qt.AlignRight )
        
        __vaultGRow += 1
        
        self.vault1_c1_L = QLabel('c1 [cm]')
        self.vault1_c1_E = LineEdit()
        self.vault1_c1_E.enableDoubleValidator(0.0000, 9999.9999, 4)
        self.vault1_c1_E.setText(self.pps.getSingleVal('Vault_c1'))
        self.vault1_c1_E.textEdited.connect(self.dataStatusChanged)
        self.vault1_c1_E.setHelpText(_('PreProc-vault1_c1_desc'))
        self.vault1_c1_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault1_c1_L, __vaultGRow, 0, Qt.AlignRight )
        self.vault_G.addWidget(self.vault1_c1_E, __vaultGRow, 1, Qt.AlignRight )
        __vaultGRow += 1
        
        # Vault Type 2 - Radius
        __vaultGRow = 1
        
        self.vault2_r1_L = QLabel('r1 [cm]')
        self.vault2_r1_E = LineEdit()
        self.vault2_r1_E.enableDoubleValidator(0.000, 9999.999, 3)
        self.vault2_r1_E.setText( str(self.pps.getVault_t2_dta(0,0)) )
        self.vault2_r1_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_r1_E.setHelpText(_('PreProc-vault2_r_desc'))
        self.vault2_r1_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_r1_L, __vaultGRow, 2, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_r1_E, __vaultGRow, 3, Qt.AlignRight )
        __vaultGRow += 1
        
        self.vault2_r2_L = QLabel('r2 [cm]')
        self.vault2_r2_E = LineEdit()
        self.vault2_r2_E.enableDoubleValidator(0.000, 9999.999, 3)
        self.vault2_r2_E.setText( str(self.pps.getVault_t2_dta(1,0)) )
        self.vault2_r2_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_r2_E.setHelpText(_('PreProc-vault2_r_desc'))
        self.vault2_r2_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_r2_L, __vaultGRow, 2, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_r2_E, __vaultGRow, 3, Qt.AlignRight )
        __vaultGRow += 1
        
        self.vault2_r3_L = QLabel('r3 [cm]')
        self.vault2_r3_E = LineEdit()
        self.vault2_r3_E.enableDoubleValidator(0.000, 9999.999, 3)
        self.vault2_r3_E.setText( str(self.pps.getVault_t2_dta(2,0)) )
        self.vault2_r3_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_r3_E.setHelpText(_('PreProc-vault2_r_desc'))
        self.vault2_r3_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_r3_L, __vaultGRow, 2, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_r3_E, __vaultGRow, 3, Qt.AlignRight )
        __vaultGRow += 1
        
        self.vault2_r4_L = QLabel('r4 [cm]')
        self.vault2_r4_E = LineEdit()
        self.vault2_r4_E.enableDoubleValidator(0.000, 9999.999, 3)
        self.vault2_r4_E.setText( str(self.pps.getVault_t2_dta(3,0)) )
        self.vault2_r4_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_r4_E.setHelpText(_('PreProc-vault2_r_desc'))
        self.vault2_r4_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_r4_L, __vaultGRow, 2, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_r4_E, __vaultGRow, 3, Qt.AlignRight )
        __vaultGRow += 1
        
        # Vault Type 2 - Angle
        __vaultGRow = 1
        self.vault2_a1_L = QLabel('a1 [deg]')
        self.vault2_a1_E = LineEdit()
        self.vault2_a1_E.enableDoubleValidator(-45.00, 45.00, 2)
        self.vault2_a1_E.setText( str(self.pps.getVault_t2_dta(0,1)) )
        self.vault2_a1_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_a1_E.setHelpText(_('PreProc-vault2_a_desc'))
        self.vault2_a1_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_a1_L, __vaultGRow, 4, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_a1_E, __vaultGRow, 5, Qt.AlignRight )
        __vaultGRow += 1
        
        self.vault2_a2_L = QLabel('a2 [deg]')
        self.vault2_a2_E = LineEdit()
        self.vault2_a2_E.enableDoubleValidator(-45.00, 45.00, 2)
        self.vault2_a2_E.setText( str(self.pps.getVault_t2_dta(1,1)) )
        self.vault2_a2_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_a2_E.setHelpText(_('PreProc-vault2_a_desc'))
        self.vault2_a2_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_a2_L, __vaultGRow, 4, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_a2_E, __vaultGRow, 5, Qt.AlignRight )
        __vaultGRow += 1
        
        self.vault2_a3_L = QLabel('a3 [deg]')
        self.vault2_a3_E = LineEdit()
        self.vault2_a3_E.enableDoubleValidator(-45.00, 45.00, 2)
        self.vault2_a3_E.setText( str(self.pps.getVault_t2_dta(2,1)) )
        self.vault2_a3_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_a3_E.setHelpText(_('PreProc-vault2_a_desc'))
        self.vault2_a3_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_a3_L, __vaultGRow, 4, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_a3_E, __vaultGRow, 5, Qt.AlignRight )
        __vaultGRow += 1
        
        self.vault2_a4_L = QLabel('a4 [deg]')
        self.vault2_a4_E = LineEdit()
        self.vault2_a4_E.enableDoubleValidator(-45.00, 45.00, 2)
        self.vault2_a4_E.setText( str(self.pps.getVault_t2_dta(3,1)) )
        self.vault2_a4_E.textEdited.connect(self.dataStatusChanged)
        self.vault2_a4_E.setHelpText(_('PreProc-vault2_a_desc'))
        self.vault2_a4_E.setHelpBar(self.helpBar)
        self.vault_G.addWidget(self.vault2_a4_L, __vaultGRow, 4, Qt.AlignRight )
        self.vault_G.addWidget(self.vault2_a4_E, __vaultGRow, 5, Qt.AlignRight )
        __vaultGRow += 1
        
        # make sure accessibility of input fields is correct
        self.enableDisableVault()
        
        # Cells distribution
        self.cd_F = QGroupBox()    
        self.cd_F.setTitle(_("Cells distribution"))
        self.cd_F.setFixedWidth(__frameWidth/2)
        self.windowGrid.addWidget(self.cd_F, __winGRowL, 0, Qt.AlignLeft)
        __winGRowL += 1

        self.cd_G = QGridLayout()
        self.cd_G.setColumnMinimumWidth(0, __col0width)
        self.cd_F.setLayout(self.cd_G)
        __cdGRow = 0
        
        self.cd_type_L = QLabel(_('Distr Type'))
        self.cd_type_L.setAlignment(Qt.AlignRight)
        self.cd_type_E = LineEdit()
        self.cd_type_E.enableIntValidator(2, 3)
        self.cd_type_E.setText(self.pps.getSingleVal('CellDistT'))
        self.cd_type_E.textEdited.connect(self.dataStatusChanged)
        self.cd_type_E.setHelpText(_('PreProc-cd_type_desc'))
        self.cd_type_E.setHelpBar(self.helpBar)
        self.cd_G.addWidget(self.cd_type_L, __cdGRow, 0)
        self.cd_G.addWidget(self.cd_type_E, __cdGRow, 1)
        
        __cdGRow += 1
        
        self.cd_coeff_L = QLabel(_('Distr Coeff'))
        self.cd_coeff_L.setAlignment(Qt.AlignRight)
        self.cd_coeff_E = LineEdit()
        self.cd_coeff_E.enableDoubleValidator(0.00, 1.00, 2)
        self.cd_coeff_E.setText(self.pps.getSingleVal('CellDistCoeff'))
        self.cd_coeff_E.textEdited.connect(self.dataStatusChanged)
        self.cd_coeff_E.setHelpText(_('PreProc-cd_coeff_desc'))
        self.cd_coeff_E.setHelpBar(self.helpBar)
        self.cd_G.addWidget(self.cd_coeff_L, __cdGRow, 0)
        self.cd_G.addWidget(self.cd_coeff_E, __cdGRow, 1)
        __cdGRow += 1
        
        self.cd_num_L = QLabel(_('Cell num'))
        self.cd_num_L.setAlignment(Qt.AlignRight)
        self.cd_num_E = LineEdit()
        self.cd_num_E.enableIntValidator(1, 99)
        self.cd_num_E.setText(self.pps.getSingleVal('CellNum'))
        self.cd_num_E.textEdited.connect(self.dataStatusChanged)
        self.cd_num_E.setHelpText(_('PreProc-cd_num_desc'))
        self.cd_num_E.setHelpBar(self.helpBar)
        self.cd_G.addWidget(self.cd_num_L, __cdGRow, 0)
        self.cd_G.addWidget(self.cd_num_E, __cdGRow, 1)
        __cdGRow += 1
  
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar()
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('preproc/preproc.html')
        
        self.windowGrid.addWidget(self.helpBar, __winGRowR ,1, Qt.AlignRight)
        __winGRowR += 1
        self.windowGrid.addWidget(self.btnBar, __winGRowR ,1, Qt.AlignRight)
        __winGRowR += 1
        
        self.win.setLayout(self.windowGrid)
    
    def vault_cb_change(self, q):
        '''
        :classmethod: Handles change of vault combo box selection.
        '''
        logging.debug(self.__windowName+'.vault_cb_change '+str(q))
        
        self.dataStatusUpdate.emit(self.__windowName,'edit')
        self.enableDisableVault()
    
    def enableDisableVault(self):
        '''
        :classmethod: Enables disables the vault input fields, depending on vault combo box settings
        '''
        if self.vault_cb.currentIndex() == 0:
            # Sin-Cos
            sinCos = True
            radAng = False
        else:
            # Radius-Angle
            sinCos = False
            radAng = True
        
        self.vault1_a1_E.setEnabled(sinCos)
        self.vault1_b1_E.setEnabled(sinCos)
        self.vault1_x1_E.setEnabled(sinCos)
        self.vault1_c1_E.setEnabled(sinCos)
        
        self.vault2_r1_E.setEnabled(radAng)
        self.vault2_r2_E.setEnabled(radAng)
        self.vault2_r3_E.setEnabled(radAng)
        self.vault2_r4_E.setEnabled(radAng)
        
        self.vault2_a1_E.setEnabled(radAng)
        self.vault2_a2_E.setEnabled(radAng)
        self.vault2_a3_E.setEnabled(radAng)
        self.vault2_a4_E.setEnabled(radAng)
        
    
    def btnPress(self, q):
        '''
        :classmethod: Does the handling of all pressed buttons.
        '''
        if q == 'Apply':
            self.writeDataToStore()
            self.dataStatusUpdate.emit(self.__windowName,'Apply')
        elif q == 'Ok':
            self.writeDataToStore()
            self.dataStatusUpdate.emit(self.__windowName,'Ok')
            self.close()
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__windowName + '.btnPress unrecognized button press '+q)

    def updateInputs(self, n, q):  # @UnusedVariable
        '''
        :classmethod: If data in central store changes, we will update in here the according input fields.
        '''
        if q == 'WingName':
            self.wingName_E.setText(self.pps.getSingleVal('WingName'))
        elif q == 'LE_type':
            self.le_type_E.setText(self.pps.getSingleVal('LE_type'))
        elif q == 'LE_a1':    
            self.le_a1_E.setText(self.pps.getSingleVal('LE_a1'))
        elif q == 'LE_b1':    
            self.le_b1_E.setText(self.pps.getSingleVal('LE_b1'))
        elif q == 'LE_x1':    
            self.le_x1_E.setText(self.pps.getSingleVal('LE_x1'))
        elif q == 'LE_x2':    
            self.le_x2_E.setText(self.pps.getSingleVal('LE_x2'))   
        elif q == 'LE_xm':    
            self.le_xm_E.setText(self.pps.getSingleVal('LE_xm'))
        elif q == 'LE_c01':    
            self.le_c01_E.setText(self.pps.getSingleVal('LE_c01'))
        elif q == 'LE_ex1':    
            self.le_ex1_E.setText(self.pps.getSingleVal('LE_ex1'))     
        elif q == 'LE_c02':    
            self.le_c02_E.setText(self.pps.getSingleVal('LE_c02'))
        elif q == 'LE_ex2':    
            self.le_ex2_E.setText(self.pps.getSingleVal('LE_ex2'))
        
        elif q == 'TE_type':
            self.te_type_E.setText(self.pps.getSingleVal('TE_type'))
        elif q == 'TE_a1':
            self.te_a1_E.setText(self.pps.getSingleVal('TE_a1'))
        elif q == 'TE_b1':  
            self.te_b1_E.setText(self.pps.getSingleVal('TE_b1'))
        elif q == 'TE_x1':
            self.te_x1_E.setText(self.pps.getSingleVal('TE_x1'))
        elif q == 'TE_xm':
            self.te_xm_E.setText(self.pps.getSingleVal('TE_xm'))
        elif q == 'TE_c0':
            self.te_c0_E.setText(self.pps.getSingleVal('TE_c0'))
        elif q == 'TE_y0':
            self.te_y0_E.setText(self.pps.getSingleVal('TE_y0'))
        elif q == 'TE_exp':
            self.te_exp_E.setText(self.pps.getSingleVal('TE_exp'))
            
        elif q == 'Vault_type':
            self.vault_cb.setCurrentIndex( int(self.pps.getSingleVal('Vault_type')) -1 )
        elif q == 'Vault_a1':
            self.vault1_a1_E.setText(self.pps.getSingleVal('Vault_a1'))
        elif q == 'Vault_b1':
            self.vault1_b1_E.setText(self.pps.getSingleVal('Vault_b1'))
        elif q == 'Vault_x1':
            self.vault1_x1_E.setText(self.pps.getSingleVal('Vault_x1'))
        elif q == 'Vault_c1':
            self.vault1_c1_E.setText(self.pps.getSingleVal('Vault_c1'))
        
        elif q == 'Vault_t2_dta':
            self.vault2_r1_E.setText( str(self.pps.getVault_t2_dta(0,0)) )
            self.vault2_r2_E.setText( str(self.pps.getVault_t2_dta(1,0)) )
            self.vault2_r3_E.setText( str(self.pps.getVault_t2_dta(2,0)) )
            self.vault2_r4_E.setText( str(self.pps.getVault_t2_dta(3,0)) )
            self.vault2_a1_E.setText( str(self.pps.getVault_t2_dta(0,1)) )
            self.vault2_a2_E.setText( str(self.pps.getVault_t2_dta(1,1)) )
            self.vault2_a3_E.setText( str(self.pps.getVault_t2_dta(2,1)) )
            self.vault2_a4_E.setText( str(self.pps.getVault_t2_dta(3,1)) )
            
        elif q == 'CellDistT':
            self.cd_type_E.setText(self.pps.getSingleVal('CellDistT'))
        elif q == 'CellDistCoeff':   
            self.cd_coeff_E.setText(self.pps.getSingleVal('CellDistCoeff'))
        elif q == 'CellNum':
            self.cd_num_E.setText(self.pps.getSingleVal('CellNum'))
        
    def writeDataToStore(self):
        '''
        :classmethod: Writes all data back to the central data store.
        '''
        self.pps.setSingleVal('WingName', self.wingName_E.text())
        
        self.pps.setSingleVal('LE_type',self.le_type_E.text())
        self.pps.setSingleVal('LE_a1',self.le_a1_E.text())
        self.pps.setSingleVal('LE_b1',self.le_b1_E.text())
        self.pps.setSingleVal('LE_x1',self.le_x1_E.text())
        self.pps.setSingleVal('LE_x2',self.le_x2_E.text())
        self.pps.setSingleVal('LE_xm',self.le_xm_E.text())
        self.pps.setSingleVal('LE_c01',self.le_c01_E.text())
        self.pps.setSingleVal('LE_ex1',self.le_ex1_E.text())
        self.pps.setSingleVal('LE_c02',self.le_c02_E.text())
        self.pps.setSingleVal('LE_ex2',self.le_ex2_E.text())
        
        self.pps.setSingleVal('TE_type',self.te_type_E.text())
        self.pps.setSingleVal('TE_a1',self.te_a1_E.text())
        self.pps.setSingleVal('TE_b1',self.te_b1_E.text())
        self.pps.setSingleVal('TE_x1',self.te_x1_E.text())
        self.pps.setSingleVal('TE_xm',self.te_xm_E.text())
        self.pps.setSingleVal('TE_c0',self.te_c0_E.text())
        self.pps.setSingleVal('TE_y0',self.te_y0_E.text())
        self.pps.setSingleVal('TE_exp',self.te_exp_E.text())
        
        if self.vault_cb.currentIndex() == 0:
            # SIN-COS
            self.pps.setSingleVal('Vault_type', '1')
            self.pps.setSingleVal('Vault_a1', self.vault1_a1_E.text())
            self.pps.setSingleVal('Vault_b1', self.vault1_b1_E.text())
            self.pps.setSingleVal('Vault_x1', self.vault1_x1_E.text())
            self.pps.setSingleVal('Vault_c1', self.vault1_c1_E.text())
        else:
            # Radius-Angle
            self.pps.setSingleVal('Vault_type', '2')
            self.pps.setVault_t2_dta(0,0, self.vault2_r1_E.text())
            self.pps.setVault_t2_dta(1,0, self.vault2_r2_E.text())
            self.pps.setVault_t2_dta(2,0, self.vault2_r3_E.text())
            self.pps.setVault_t2_dta(3,0, self.vault2_r4_E.text())
            self.pps.setVault_t2_dta(0,1, self.vault2_a1_E.text())
            self.pps.setVault_t2_dta(1,1, self.vault2_a2_E.text())
            self.pps.setVault_t2_dta(2,1, self.vault2_a3_E.text())
            self.pps.setVault_t2_dta(3,1, self.vault2_a4_E.text())
        
        self.pps.setSingleVal('CellDistT',self.cd_type_E.text())
        self.pps.setSingleVal('CellDistCoeff',self.cd_coeff_E.text())
        self.pps.setSingleVal('CellNum',self.cd_num_E.text())
        
            
    def dataStatusChanged(self):
        '''
        :classmethod: Does emit a signal if the user has edited data. 
        '''
        self.dataStatusUpdate.emit(self.__windowName,'edit')
        
    
    

        