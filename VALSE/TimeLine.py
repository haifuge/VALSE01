import sys, math
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TimeLine(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(500,270)
        self.tab=QTabWidget(self)
        self.tab.move(0,0)
        self.tab.size().width=self.size().width()
        self.tab.size().height=self.size().height()
        verfiedTab=VerifiedTab()
        self.tab.addTab(verfiedTab,"Verified")
        unverifiedTab=VerifiedTab()
        self.tab.addTab(unverifiedTab,"Unverified")

    def resizeEvent(self, e):
        self.tab.resize(e.size()+QSize(1,1))

class VerifiedTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.originalSpeed=500
        self.speed=500
        self.speedTimes=1.0
        self.start=False
        self.timer=QTimer()
        self.timer.setInterval(self.speed)
        self.timer.timeout.connect(self.timerTick)

        palette=self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)
        self.hlb=QHBoxLayout()
        self.hlb.setSizeConstraint(QLayout.SetFixedSize)
        self.hlb.setContentsMargins(QMargins(5,5,0,5))
        self.playbtn=QPushButton()
        self.playbtn.setIcon(QIcon(r'Pictures/play.png'))
        self.playbtn.clicked.connect(self.playbtnClicked)
        self.stopbtn=QPushButton()
        self.stopbtn.setIcon(QIcon(r'Pictures/stop.png'))
        self.stopbtn.clicked.connect(self.timerReset)
        self.fforwardbtn=QPushButton()
        self.fforwardbtn.setIcon(QIcon(r'Pictures/fforward.png'))
        self.fforwardbtn.clicked.connect(self.timerSpeedUp)
        self.freversebtn=QPushButton()
        self.freversebtn.setIcon(QIcon(r'Pictures/freverse.png'))
        self.freversebtn.clicked.connect(self.timerSlowDown)

        self.hlb.addWidget(self.freversebtn)
        self.hlb.addWidget(self.playbtn)
        self.hlb.addWidget(self.stopbtn)
        self.hlb.addWidget(self.fforwardbtn)
        self.hlb.addStretch(1)

        self.vlb=QVBoxLayout()
        self.vlb.setSpacing(0)
        self.vlb.setContentsMargins(QMargins(0,0,0,0))
        self.vlb.addLayout(self.hlb)
        self.grid=GridArea()
        self.grid.setGeometry(0,0,self.size().width(),self.size().height() - 15)
        self.vlb.addWidget(self.grid)

        self.timeline=Tileline()
        self.timeline.setGeometry(0, 0, self.size().width(), 20)
        self.vlb.addWidget(self.timeline)

        self.setLayout(self.vlb)

    def paintEvent(self, e):
        qp=QPainter()
        qp.setPen(Qt.red)
        qp.begin(self)
        # qp.drawRect(QRect(e.rect()))
        qp.end()
    def timerTick(self):
        pass
    def playbtnClicked(self):
        if self.start:
            self.start=False
            self.timer.stop()
            self.playbtn.setIcon(QIcon(r'Pictures/play.png'))
        else:
            self.start=True
            self.timer.start()
            self.playbtn.setIcon(QIcon(r'Pictures/pause.png'))
    def timerReset(self):
        self.speedTimes=1
        self.speed=self.originalSpeed*self.speedTimes
        self.timer.stop()
    def timerSpeedUp(self):
        self.speedTimes=self.speedTimes/2
        self.speed=self.originalSpeed*self.speedTimes
    def timerSlowDown(self):
        self.speedTimes = self.speedTimes * 2
        self.speed=self.originalSpeed*self.speedTimes

class Tileline(QWidget):
    start_x=0
    end_x=100
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # tag for initializing left and right button position
        self.initialPosition=True
        self.setContentsMargins(QMargins(0,0,0,0))
        self.setMinimumSize(350, 50)
        self.beginTime=time.localtime()
        self.endTime=time.localtime()

        self.start_x = 0
        self.end_x = self.size().width()-155
        self.btn_y = 3
        self.leftbtn = DragButton("|", self)
        self.leftbtn.resize(10, 20)
        self.leftbtn.move(self.start_x, self.btn_y)
        self.leftbtn.setYpos(self.btn_y)
        self.leftbtn.setXrange(self.start_x, self.size().width() - self.start_x)

        self.rightbtn = DragButton("|", self)
        self.rightbtn.resize(10, 20)
        self.rightbtn.move(self.end_x, self.btn_y)
        self.rightbtn.setYpos(self.btn_y)
        self.rightbtn.setXrange(self.start_x, self.size().width() - self.rightbtn.size().width())

        self.leftbtn.setRightBtn(self.rightbtn)
        self.rightbtn.setLeftBtn(self.leftbtn)
        self.leftbtn.mouseReleaseSignal.connect(self.leftbtnRelease)
        self.rightbtn.mouseReleaseSignal.connect(self.rightbtnRelease)
        self.leftbtn.mouseMoveSignal.connect(self.leftbtnMove)
        self.rightbtn.mouseMoveSignal.connect(self.rightbtnMove)

    def resizeEvent(self, QResizeEvent):
        if self.initialPosition==True:
            self.leftbtn.move(0, self.btn_y)
            self.rightbtn.move(self.size().width()-10, self.btn_y)
            self.initialPosition=False
            self.leftbtnXPosRatio = self.leftbtn.x() / self.size().width()
            self.rightbtnXPosRatio = self.rightbtn.x() / self.size().width()
            self.leftbtn.setXrange(self.start_x, self.rightbtn.x())
            self.rightbtn.setXrange(self.leftbtn.x()+self.leftbtn.size().width(), self.rightbtn.x())
        else:
            self.rightbtn.move(self.rightbtnXPosRatio*self.size().width(), self.btn_y)
            self.leftbtn.move(self.leftbtnXPosRatio*self.size().width(), self.btn_y)
            self.rightbtn.setXrange(self.leftbtn.x()+self.leftbtn.size().width(), self.size().width()-self.rightbtn.size().width())
            self.leftbtn.setXrange(0, self.rightbtn.x()-self.leftbtn.size().width())

    def leftbtnRelease(self):
        self.leftbtnXPosRatio=self.leftbtn.x()/self.size().width()
    def rightbtnRelease(self):
        self.rightbtnXPosRatio=self.rightbtn.x()/self.size().width()
    def leftbtnMove(self):
        self.repaint()
    def rightbtnMove(self):
        self.repaint()

    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)
        self.drawTimeline(qp)
        self.drawShadowArea(qp)
        qp.end()

    def drawShadowArea(self, qp):
        brush = QBrush(Qt.Dense6Pattern)
        pen = QPen(QColor(122, 122, 32))
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.leftbtn.x()+self.leftbtn.size().width()-1, self.size().height()/2)
        qp.drawRect(self.rightbtn.x(),0,self.size().width()-self.rightbtn.x(), self.size().height()/2)

    def drawTimeline(self, qp):
        borderPen=QPen(QColor(255,255,255), 2, Qt.SolidLine)
        width=self.size().width()
        height=self.size().height()
        # draw timeline
        timeline_y=self.size().height()/2
        qp.drawLine(0, timeline_y, width, timeline_y)
        timelineStep=width/26
        timelineNumbers=['00:00','04:00','08:00','12:00','16:00','20:00','24:00']
        self.start_x=timelineStep
        self.end_x=width-self.start_x

        for i in range(0,25):
            j=i%4
            if(j==0):
                qp.setFont(QFont('Lucida',7))
                metrics = qp.fontMetrics()
                fw = metrics.width(timelineNumbers[int(i/4)])
                qp.drawText(timelineStep*i+self.start_x - fw / 2, timeline_y+20, timelineNumbers[int(i/4)])
                qp.drawLine(timelineStep * (i) + self.start_x, timeline_y, timelineStep * (i) + self.start_x,
                            timeline_y + 7)
            else:
                qp.drawLine(timelineStep * (i) + self.start_x, timeline_y, timelineStep * (i) + self.start_x,
                            timeline_y + 4)

    def drawMarks(self,qp):
        qp.setPen(QPen(Color.red,2,Qt.SolidLine))
        qp.drawEllipse(10,10,10,10)
        qp.drawRect(20,20,10,10)
        qp.drawLine(50,50,60,60)
        qp.drawLine(50,60,60,50)
        points=QPolygon([QPoint(75,70),QPoint(70,80),QPoint(80,80)])
        qp.drawPolygon(points)

    def drawCircle(self, qp, x, y, color):
        r=10
        x=x-r/2
        y=y-r/2
        qp.setPen(QPen(color,2,Qt.SolidLine))
        qp.drawEllipse(x,y,r,r)

    def drawSquare(self, qp, x,y,color):
        length=10
        x=x-length/2
        y=y-length/2
        qp.setPen(QPen(color, 2, Qt.SolidLine))
        qp.drawRect(x,y,length,length)

    def drawCross(self, qp, x, y, color):
        length=10
        x=x-length/2
        y=y-length/2
        qp.setPen(QPen(color,2,Qt.SolidLine))
        qp.drawLine(x,y,x+length,y+length)
        qp.drawLine(x+length,y,x,y+length)

    def drawTriangle(self, qp, x, y, color):
        r=8
        x1,y1=x,y-r
        x2,y2=x-r*math.sqrt(3)/2,y+r/2
        x3,y3=x+r*math.sqrt(3)/2,y+r/2
        points=QPolygon([QPoint(x1,y1),QPoint(x2,y2),QPoint(x3,y3)])
        qp.setPen(color,1,Qt.SolidLine)

class EventGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.eventNum=5
        self.rowHeight=50
        self.rowWidth=self.size().width()
        self.setMinimumHeight(120)

    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)
        self.drawGrids(qp)
        qp.end()

    def drawGrids(self,qp):
        # row width
        width = self.size().width()
        cHeight=self.rowHeight
        height=self.eventNum*self.rowHeight
        # C1 width
        cWidth=int(width*0.07)
        # gird right width
        grWidth=int(width*0.03)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        # draw horizontal lines
        for i in range(self.eventNum):
            qp.drawLine(0, i*cHeight, width, i*cHeight)
        qp.drawLine(0, self.eventNum * cHeight-1, width, self.eventNum * cHeight-1)
        gridstep = width * 0.1
        # draw vertical lines
        qp.setPen(QColor(210,210,222))
        for i in range(10):
            qp.drawLine(cWidth+i*gridstep, 0, cWidth+i*gridstep, self.eventNum * cHeight)
        # draw middle horizontal lines
        for i in range(self.eventNum):
            qp.drawLine(0,(i+0.5)*cHeight, width, (i+0.5)*cHeight)

class GridArea(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setContentsMargins(QMargins(0,0,0,0))
        self.widget=EventGrid()
        self.widget.setGeometry(0,0,self.size().width(), self.widget.eventNum*self.widget.rowHeight)
        scroll=QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(False)
        scroll.setContentsMargins(QMargins(0,0,0,0))
        scroll.setWidget(self.widget)
        vlayout=QVBoxLayout(self)
        vlayout.setContentsMargins(QMargins(0,0,0,0))
        vlayout.addWidget(scroll)
        self.setLayout(vlayout)

    def resizeEvent(self, QResizeEvent):
        self.widget.setGeometry(0, 0, self.size().width()-25, self.widget.eventNum * self.widget.rowHeight)

class Color(object):
    red = QColor(Qt.red)
    blue = QColor(Qt.blue)
    yellow = QColor(Qt.yellow)
    black = QColor(Qt.black)
    green = QColor(Qt.green)
    gray=QColor(Qt.gray)

class Shape(object):
    sqaure=0
    circle=1
    triangle=2
    cross=3

import itertools
class Mark(object):
    colors=[Color.red, Color.black, Color.blue, Color.yellow, Color.green, Color.gray]
    shapes=[Shape.sqaure, Shape.circle, Shape.triangle, Shape.cross]
    marks=[]
    for x in itertools.product(shapes, colors):
        marks.append(x)
    def printMakrs(self):
        for m in self.marks:
            print(m)

class DragButton(QPushButton):
    # button move range
    minX=0
    maxX=0
    # button y_position at
    ypos=0
    # mouse release signal
    mouseReleaseSignal=pyqtSignal()
    mouseMoveSignal=pyqtSignal()
    def setYpos(self, value):
        self.ypos=value

    def setXrange(self, minX, maxX):
        self.minX=minX
        self.maxX=maxX

    # there are two buttons, left button and right button. left button moving range is from 0 to right button x_pox; right button moving range is from right button to left
    # so right button needs to set its left range when left button moves; left button needs to set its right range when right button moves
    def setLeftRange(self, leftX):
        self.minX=leftX

    def setRightRange(self, rightX):
        self.maxX=rightX

    # these two functions are to set the other button, left or right button.
    # self means its self. no self means the other button.
    # this function means self is right button and set the other button left.
    def setLeftBtn(self, lbtn):
        self.leftBtn=lbtn
        self.rightBtn=self

    # this function means self is left, and set the other is right.
    def setRightBtn(self, rbtn):
        self.rightBtn=rbtn
        self.leftBtn=self;

    def mousePressEvent(self, event):
        self.__mousePressPos=None
        self.__mouseMovePos=None
        if event.button()==Qt.LeftButton:
            self.__mousePressPos=event.globalPos()
            self.__mouseMovePos=event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons()==Qt.LeftButton:
            currPos=self.mapToGlobal(self.pos())
            globalPos=event.globalPos()
            diff=globalPos-self.__mouseMovePos
            newPos=self.mapFromGlobal(currPos+diff)
            newPos.setY(self.ypos)
            if newPos.x()<self.minX:
                newPos.setX(self.minX)
            if newPos.x()>self.maxX:
                newPos.setX(self.maxX)
            self.move(newPos)
            self.__mouseMovePos=globalPos
            # self is right button
            if self.leftBtn != self:
                self.leftBtn.setRightRange(newPos.x()-self.rightBtn.size().width())
            # self is left button
            if self.rightBtn!=self:
                self.rightBtn.setLeftRange(newPos.x()+self.leftBtn.size().width())

        super(DragButton, self).mouseMoveEvent(event)
        self.mouseMoveSignal.emit()

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved=event.globalPos()-self.__mousePressPos
            if moved.manhattanLength()>3:
                event.ignore()
                self.mouseReleaseSignal.emit()
                return

        super(DragButton, self).mouseReleaseEvent(event)
        self.mouseReleaseSignal.emit()

class TestDragButton(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        palette=self.palette()
        palette.setColor(self.backgroundRole(),QColor(125,222,31))
        self.setPalette(palette)
        self.btn=DragButton(self)
        # self.btn.setBackgroundRole()
        self.btn.resize(10,40)
        self.btn.move(50,50)
        self.btn.setYpos(50)
        self.btn.setXrange(10, 200)

        self.setGeometry(400,400,400,400)
        self.show()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=TimeLine()
    # ex=GridArea()
    # ex=EventGrid()
    # ex=TestDragButton()
    # ex=Tileline()
    ex.show()
    sys.exit(app.exec_())