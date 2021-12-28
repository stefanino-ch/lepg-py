'''


@author: Stefan Feuz; http://www.laboratoridenvol.com
@license: General Public License GNU GPL 3.0
'''

from PyQt5.QtWidgets import QMdiSubWindow, QGridLayout, QWidget, QSizePolicy

from gui.elements.WindowBtnBar import WindowBtnBar
from gui.elements.WindowHelpBar import WindowHelpBar

class SimpleMdiWindow(QMdiSubWindow):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        
        Layout
        
        data field 0
        data field 1
        data field 2
        data field 3
        help window
        buttons
        '''
        super().__init__()
                
        win = QWidget()
        self.setWidget(win)
        
        self.help = WindowHelpBar()
        
        
        self.bottom = WindowBtnBar()
        self.bottom.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.bottom.my_signal.connect(self.windowaction)
        
        grid = QGridLayout()
        grid.addWidget(self.help,0,0)
        grid.addWidget(self.bottom,1,0)
        
        win.setLayout(grid)
        
        self.help.setText('multi\nline\ntext')
        
    def windowaction(self, q):
        print(q)
    
        