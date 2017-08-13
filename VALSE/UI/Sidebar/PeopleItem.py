import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.Sidebar import MarkerButton
from UI.Sidebar import MarkerSelection
from Common import CommonTools

class PeopleItem(QWidget):
    visible=True;
    def __init__(self, tId, _name='Person 1', _color=CommonTools.Color.red, _shape=CommonTools.Shape.square):
        super().__init__();
        self.id=tId
        self.markerColor=_color
        self.markerShape=_shape
        self.initUI(_name)

    def initUI(self, _name):
        self.height=25
        self.width=250
        self.setMinimumSize(self.width,self.height)
        self.setMaximumSize(self.width,self.height)
        self.setGeometry(300,300,self.width, self.height)

        self.txtName=QtText(self)
        self.txtName.move(2,1)
        self.txtName.setText(_name)
        self.txtName.setReadOnly(True)
        self.txtName.setFrame(False)
        self.bgColor=self.palette().color(QPalette.Background)
        self.txtName.setStyleSheet('background-color: ' + self.bgColor.name())
        self.txtName.click.connect(self.mouseClick)

        self.btnMarker=MarkerButton.MarkerButton(self, self.markerShape, self.markerColor)
        self.btnMarker.setGeometry(QRect(200,2,20,20))
        self.btnMarker.clicked.connect(self.markerClicked)
        self.btnMarker.setStyleSheet('background-color: ' + self.bgColor.name()+'; border:none;')

        self.btnVisible=QPushButton(self)
        self.btnVisible.setIcon(QIcon(r'Pictures/visible.png'))
        self.btnVisible.clicked.connect(self.visibleClicked)
        self.btnVisible.setGeometry(225,2,20,20)
        self.btnVisible.setStyleSheet('background-color: ' + self.bgColor.name()+'; border:none;')
        self.visible=True

    def markerClicked(self):
        ms=MarkerSelection.MarkerSelection()
        ms.setWindowFlags(Qt.FramelessWindowHint)
        point=self.btnMarker.rect().topRight()
        global_point=self.btnMarker.mapToGlobal(point)
        ms.move(global_point.x(),global_point.y())
        ms.signal.connect(self.markerSelected)
        ms.SetMarker(self.markerColor, self.markerShape)
        ms.exec_()

    def markerSelected(self, markerInfo):
        self.markerColor=markerInfo[0]
        self.markerShape=markerInfo[1]
        self.btnMarker.SetMarker(self.markerColor, self.markerShape)

    def SetMarker(self, _color, _shape):
        self.markerColor=_color
        self.markerShape=_shape
        self.btnMarker.SetMarker(self.markerColor, self.markerShape)

    def visibleClicked(self):
        if self.visible:
            self.visible=False
            self.btnVisible.setIcon(QIcon(r'Pictures/invisible.png'))
        else:
            self.visible=True
            self.btnVisible.setIcon(QIcon(r'Pictures/visible.png'))

    selected=False
    def mouseClick(self):
        if self.selected:
            self.txtName.setStyleSheet('background-color:'+self.bgColor.name())
            self.selected=False
        else:
            self.txtName.setStyleSheet('background-color:#778899')
            self.selected=True


class QtText(QLineEdit):
    click=pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(23)
        self.setFixedWidth(190)
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

    def mousePressEvent(self, QMouseEvent):
        self.click.emit()



if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=PeopleItem()
    ex.show()
    sys.exit(app.exec_())
