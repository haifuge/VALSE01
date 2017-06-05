import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PeopleItem(QWidget):
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
        print(bgColor)
        self.txtName.setStyleSheet('background-color: ' + bgColor.name())

class QtText(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(150)
    def focusOutEvent(self, e):
        self.setReadOnly(True)
    def mouseDoubleClickEvent(self, e):
        print('double clicked')
        if self.isReadOnly():
            self.setReadOnly(False)
        else:
            self.setReadOnly(True)
    def keyPressEvent (self, e):
        if e.key()==Qt.Key_Return:
            self.setReadOnly(True)
        else:
            super().keyPressEvent(e)

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=PeopleItem()
    ex.show()
    sys.exit(app.exec_())
