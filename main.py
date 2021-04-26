import sys
  
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from QShamsiCalendarWidget import QShamsiCalendarWidget

class MainWindow(QtWidgets.QMainWindow):
  
    def __init__(self, parent = None):
        super().__init__(parent)
        self.init_gui()
  
    def init_gui(self):
        self.window = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
  
        self.calendar = QShamsiCalendarWidget(1399, 1401)
        self.calendar.sel_date_changed.connect(self.date_changed)
  
        self.layout.addWidget(self.calendar)
    
    def date_changed(self):
        print(self.calendar.selected_date)
  
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
  
    win = MainWindow()
    win.show()
  
    sys.exit(app.exec_())