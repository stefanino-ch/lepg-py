'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QHeaderView
from gui.elements.TableView import TableView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from data.ProcModel import ProcModel

class Marks(QMdiSubWindow):
    '''
    :class: Window to display and edit Seewing allowances data  
    '''

    __className = 'Marks'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.marks_M = ProcModel.MarksModel()
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
                    marks_T
                ---------------------------
                            help_bar | btn_bar
        '''
        logging.debug(self.__className + '.build_window')
        
        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(250, 200)

        self.windowLayout = QVBoxLayout()
        
        self.helpBar = WindowHelpBar()
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Marks"))

        marks_T = TableView()
        marks_T.setModel( self.marks_M )
      
        marks_T.hideColumn(self.marks_M.columnCount() -1 ) # hide the ID column which is always at the end of the model
        marks_T.verticalHeader().setVisible(False)
        marks_T.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        marks_T.setHelpBar(self.helpBar)
        
        marks_T.setHelpText(ProcModel.MarksModel.MarksSpCol, _('Marks-MarksSpacingDesc'))
        marks_T.setHelpText(ProcModel.MarksModel.PointRadCol, _('Marks-PointRadiusDesc'))
        marks_T.setHelpText(ProcModel.MarksModel.PointDisplCol, _('Marks-PointsDisplacementDesc'))

        marks_T.enableDoubleValidator(ProcModel.MarksModel.MarksSpCol, ProcModel.MarksModel.PointDisplCol, 0, 10, 2)
        
        marks_T.setFixedHeight(2 + marks_T.horizontalHeader().height() + marks_T.rowHeight(0))

        self.windowLayout.addWidget(marks_T)

        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar(0b0101)
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        self.btnBar.setHelpPage('proc/marks.html')

        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()        
        bottomLayout.addWidget(self.helpBar)
        bottomLayout.addWidget(self.btnBar)
        self.windowLayout.addLayout(bottomLayout)
        
        self.win.setLayout(self.windowLayout)
    
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
            logging.error(self.__className + '.btn_press unrecognized button press '+q)
    