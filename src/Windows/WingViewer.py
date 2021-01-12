'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPen, QBrush
from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QGroupBox, QWidget, QSizePolicy, QGraphicsScene, QGraphicsView 
from Windows.WindowBtnBar import WindowBtnBar
from DataWindowStatus.DataWindowStatus import DataWindowStatus
from DataStores.PreProcessorStore import PreProcessorStore

class WingViewer(QMdiSubWindow):
    '''
    :class: Window to display the outline of the data the Pre-Processor will use to generate the wing basics.  
    '''

    __className = 'WingViewer'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        :method: Constructor
        '''
        logging.debug(self.__className+'.__init__')
        super().__init__()
        self.pps = PreProcessorStore()
        self.dws = DataWindowStatus()

        self.buildWindow()
        self.pps.dataStatusUpdate.connect(self.updateWindow)  
    
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
                windowGrid 
                    tail_F          | side_F
                        tailView    |    sideView
                    -------------------------
                    top_F           |
                        topView     |
                    -------------------------
                                    |    btnBar
        '''
        logging.debug(self.__className + '.buildWindow')
        
        self.setWindowIcon(QIcon('Windows\\favicon.ico'))
        self.win = QWidget()
        self.setWidget(self.win)
        self.win.setMinimumSize(600, 450)

        self.windowGrid = QGridLayout()
        __winGRowL = 0
        __winGRowR = 0
        
        #############################
        # Add window specifics here
        self.setWindowTitle(_("Wing outline viewer"))

        self.grayBrush = QBrush(Qt.gray)
        self.pen = QPen(Qt.red)

        # Tail view
        self.tail_F = QGroupBox()    
        self.tail_F.setTitle(_("Tail view"))
        self.windowGrid.addWidget(self.tail_F, __winGRowL , 0)
         
        self.tail_L = QGridLayout()
        self.tail_F.setLayout(self.tail_L)
         
        self.tail_S  = QGraphicsScene()

        self.tail_V = QGraphicsView()
        self.tail_V.setScene(self.tail_S)
        
        self.tail_L.addWidget(self.tail_V, 0, 0)
 
        __winGRowL += 1
         
        #ellipse = self.tail_S.addEllipse(20,20, 50,50, self.pen, self.grayBrush)
        
        # Side view
        self.side_F = QGroupBox()    
        self.side_F.setTitle(_("Side view"))
        self.windowGrid.addWidget(self.side_F, __winGRowR , 1)
        
        self.side_L = QGridLayout()
        self.side_F.setLayout(self.side_L)
        
        self.sideScene  = QGraphicsScene()
        self.sideView = QGraphicsView()
        self.sideView.setScene(self.sideScene)
        
        self.side_L.addWidget(self.sideView, 0 , 0)
        
        __winGRowR += 1
        
        #ellipseSide = self.sideScene.addEllipse(10,10, 30,30, self.pen, self.grayBrush)
        
        # Top view
        self.top_F = QGroupBox()    
        self.top_F.setTitle(_("Top view"))
        self.windowGrid.addWidget(self.top_F, __winGRowL , 0)
        
        self.top_L = QGridLayout()
        self.top_F.setLayout(self.top_L)
        
        self.topScene  = QGraphicsScene()
        
        self.topView = QGraphicsView()
        self.topView.setScene(self.topScene)
        
        self.top_L.addWidget(self.topView, __winGRowL , 0)
        
        __winGRowL += 1
        __winGRowR += 1
        
        #ellipseTop = self.topScene.addEllipse(10,10, 20,20, self.pen, self.grayBrush)
        
        #############################
        # Commons for all windows
        self.btnBar = WindowBtnBar( 0b0010 )
        self.btnBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.btnBar.my_signal.connect(self.btnPress)
        # @TODO: setup and enable user help
        #self.btnBar.setHelpPage('preproc/preproc.html')
        
        self.windowGrid.addWidget(self.btnBar, __winGRowR ,1, Qt.AlignRight)
        __winGRowR += 1
        
        self.win.setLayout(self.windowGrid)
    
    def btnPress(self, q):
        '''
        :method: Handling of all pressed buttons.
        '''
        if q == 'Apply':
            # self.writeDataToStore()
            # self.dataStatusUpdate.emit(self.__className,'Apply')
            logging.error(self.__className + '.button should be disabled '+q)
            
        elif q == 'Ok':
            # self.writeDataToStore()
            # self.dataStatusUpdate.emit(self.__className,'Ok')
            # self.close()
            logging.error(self.__className + '.button should be disabled '+q)
            
        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className + '.btnPress unrecognized button press '+q)
    
    def calcScaleFactor(self, viewWidth, wingSpan):
        '''
        :method: Does calculate the scale factor based on the size of the graphics view and the wing span
        :param viewWidth: Current view width
        :param wingSpan: Wing span of the current design
        :return: the scale factor
        '''
        scaleFact = (viewWidth/ wingSpan)
        
        # use 90% of the view
        scaleFact = scaleFact * .9

        return scaleFact

    def updateWindow(self, n, q):  # @UnusedVariable
        '''
        :method: If data in central store changes, we will update in here the window.
        '''
        print(self.__className + '.updateWIndow')
        
    def buildDataBuffer(self):
        '''
        :method: Does initially load the window internal data buffer
        '''
        self.__halfWingSpan = self.pps.getSingleVal('LE_xm')
        
        # b1_LE
        # bi_TE
        
    
    def drawTopView(self):
        '''
        :method: Draws the top view based on the window data buffer
        '''
        __midX = self.topView.width()/ 2
        ''':attr: X coordinate in the window middle'''
        __maxY = self.topView.height()
        ''':attr: Max Y coordinate of the view'''
        
        # Scale factor
        # self.calcScaleFactor(self.topView.width(), (self.__halfWingSpan*2) 
