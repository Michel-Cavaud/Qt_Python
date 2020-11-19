from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import Bieres

class BieresApp(QtWidgets.QMainWindow, Bieres.Ui_ListeBiere):
    def __init__(self, parent=None):
        super(BieresApp, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QApplication(sys.argv)
    form = BieresApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
