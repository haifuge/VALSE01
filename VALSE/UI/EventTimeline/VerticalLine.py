from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class VerticalLine(QWidget):
    def __init__(self, _height, _width):
        self.height=_height
        self.width=_width
        self.resize(self.width, self.height)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent")

    def paintEvent(self, qp):
        qp=QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor.black, 1, Qt.SolidLine))
        qp.drawLine(self.width/2, 0, self.width/2, self.height)

