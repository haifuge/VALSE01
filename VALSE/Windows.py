import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.EventTimeline import TimeLine
from UI.DateMenu import DateMenu
from UI.Sidebar import PeopleSidebar

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

        sidebars=bar.addMenu("Sidebars")
        sidebars.addAction("People")
        sidebars.triggered[QAction].connect(self.windowAction)

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
            self.dateMenu=QMdiSubWindow()
            self.dateWindow=DateMenu.DateMenu()
            self.dateWindow.closeSignal.connect(self.dateWindowClose)
            self.dateMenu.setWidget(self.dateWindow)
            self.dateMenu.setWindowTitle("Date Selection")
            self.dateMenu.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            self.dateMenu.setMaximumWidth(265)
            self.dateMenu.setMaximumHeight(340)
            self.mdi.addSubWindow(self.dateMenu)
            self.dateMenu.show()
        if q.text()=='People':
            peoplesb=QMdiSubWindow()
            peoplesb.setWidget(PeopleSidebar.PeopleSidebar())
            peoplesb.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            peoplesb.setMaximumWidth(265)
            self.mdi.addSubWindow(peoplesb)
            peoplesb.show()

    def dateWindowClose(e):
        self.dateMenu.close()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MainWindow()
    ex.show()
    sys.exit(app.exec_())
