'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from Windows.TableView import TableView
from Windows.WindowHelpBar import WindowHelpBar
from Windows.WindowBtnBar import WindowBtnBar
from DataStores.ProcessorModel import ProcessorModel

class PlanMarks(QMdiSubWindow):
    '''
    :class: Window to display and edit Seewing allowances data  
    '''

    __className = 'PlanMarks'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        
        self.marks_M = ProcessorModel.MarksModel()
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
                windowLayout 
                    marks_T
                ---------------------------
                            helpBar | btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
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
        marks_T.setHelpBar(self.helpBar)
        
        marks_T.setHelpText(ProcessorModel.MarksModel.MarksSpCol, _('Marks-MarksSpacingDesc'))
        marks_T.setHelpText(ProcessorModel.MarksModel.PointRadCol, _('Marks-PointRadiusDesc'))
        marks_T.setHelpText(ProcessorModel.MarksModel.PointDisplCol, _('Marks-PointsDisplacementDesc'))

        marks_T.enableDoubleValidator(ProcessorModel.MarksModel.MarksSpCol, ProcessorModel.MarksModel.PointDisplCol, 0, 10, 2)
        
        marks_T.setFixedHeight(2 + marks_T.horizontalHeader().height() + marks_T.rowHeight(0))
        marks_T.setFixedWidth(2 +marks_T.columnWidth(0)+marks_T.columnWidth(1)+marks_T.columnWidth(2) )

        editLayout = QHBoxLayout()
        editLayout.addWidget(marks_T)
        editLayout.addStretch()

        self.windowLayout.addLayout(editLayout)

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
        logging.debug(self.__className+'.btnPress')
        if q == 'Apply':
            pass
                        
        elif q == 'Ok':
            self.close()
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    