import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.EventTimeline import TimeLine
from UI.DateMenu import DateMenu

class MainWindow(QMainWindow):
    count=0
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('VALSE')
        self.resize(1200, 700)
        self.mdi=QMdiArea()
        self.setCentralWidget(self.mdi)
        bar=self.menuBar()
        file=bar.addMenu("File")
        file.addAction("New")
        file.addAction("Cascade")
        file.addAction("Tiled")
        file.triggered[QAction].connect(self.windowAction)

        datePanel=bar.addMenu("Date Panel")
        datePanel.addAction("Show Date Panel")
        datePanel.triggered[QAction].connect(self.windowAction)

    def windowAction(self, q):
        if q.text()=="New":
            self.count=self.count+1
            sub=QMdiSubWindow()
            sub.setWidget(TimeLine.TimeLine())
            sub.setWindowTitle("TimeLine")
            self.mdi.addSubWindow(sub)
            sub.show()
        if q.text()=='Cascade':
            self.mdi.cascadeSubWindows()
        if q.text()=='Titled':
            self.mdi.tileSubWindows()
        if q.text()=='Show Date Panel':
            dateMenu=QMdiSubWindow()
            dateMenu.setWidget(DateMenu.DateMenu())
            dateMenu.setWindowTitle("Datetiem Selection")
            self.mdi.addSubWindow(dateMenu)
            dateMenu.show()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MainWindow()
    ex.show()
    sys.exit(app.exec_())
