import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PeopleItem(QWidget):
    visible=True;
    def __init__(self):
        super().__init__();
        self.initUI()
    def initUI(self):
        self.height=25
        self.width=220
        self.setMinimumSize(self.width,self.height)
        self.setMaximumSize(self.width,self.height)
        self.setGeometry(300,300,self.width, self.height)

        self.txtName=QtText(self)
        self.txtName.move(2,2)
        self.txtName.setText('Person 1')
        self.txtName.setReadOnly(True)
        self.txtName.setFrame(False)
        bgColor=self.palette().color(QPalette.Background)
        self.txtName.setStyleSheet('background-color: ' + bgColor.name())

        self.btnMarker=MarkerButton(self)
        self.btnMarker.setGeometry(QRect(160,2,20,20))
        self.btnMarker.clicked.connect(self.markerClicked)
        self.btnMarker.setStyleSheet('background-color: ' + bgColor.name()+'; border:none;')

        self.btnVisible=QPushButton(self)
        self.btnVisible.setIcon(QIcon(r'Pictures/visible.png'))
        self.btnVisible.clicked.connect(self.visibleClicked)
        self.btnVisible.setGeometry(190,2,20,20)
        self.btnVisible.setStyleSheet('background-color: ' + bgColor.name()+'; border:none;')
        self.visible=True

    def markerClicked(self):
        print('clicked')
    def visibleClicked(self):
        if self.visible:
            self.visible=False
            self.btnVisible.setIcon(QIcon(r'Pictures/invisible.png'))
        else:
            self.visible=True
            self.btnVisible.setIcon(QIcon(r'Pictures/visible.png'))

class QtText(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(150)
    def focusOutEvent(self, e):
        self.setReadOnly(True)
    def mouseDoubleClickEvent(self, e):
        if self.isReadOnly():
            self.setReadOnly(False)
        else:
            self.setReadOnly(True)
    def keyPressEvent (self, e):
        if e.key()==Qt.Key_Return:
            self.setReadOnly(True)
        else:
            super().keyPressEvent(e)


class MarkerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(20,20)
    def paintEvent(self,e):
        qp=QPainter()
        qp.begin(self)
        self.drawMarker(qp)
        qp.end()
    def drawMarker(self, qp):
        qp.setPen(Qt.red)
        qp.drawRect(1,1,18,18)

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=PeopleItem()
    ex.show()
    sys.exit(app.exec_())
