from PyQt5 import QtGui, QtWidgets

from gui.elements.LineEdit import LineEdit


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.lineEdit= LineEdit()
        self.lineEdit.en_int_validator(5, 15)
        # self.lineEdit.setValidator(
        #     QtGui.QDoubleValidator(
        #         0.0, # bottom
        #         100.0, # top
        #         6, # decimals
        #         notation=QtGui.QDoubleValidator.StandardNotation
        #     )
        # )
        self.setCentralWidget(self.lineEdit)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())