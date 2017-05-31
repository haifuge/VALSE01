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
        #self.setFixedSize(500,270)
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
        self.timeline.timeRangeChanged.connect(self.timeRangeChanging)
        self.vlb.addWidget(self.timeline)

        self.setLayout(self.vlb)

    def paintEvent(self, e):
        pass
        #qp=QPainter()
        #qp.setPen(Qt.red)
        #qp.begin(self)
        #qp.drawRect(QRect(e.rect()))
        #qp.end()
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
    def timeRangeChanging(self):
        value=self.timeline.getTimePeriodRange()
        self.startTime=value[0]
        self.endTime=value[1]
        self.grid.setTimeRange(self.startTime, self.endTime)

# the bottom timeline
class Tileline(QWidget):
    timeRangeChanged=pyqtSignal()
    # one unit of timeline
    timelineStep=0
    # timeline start time, seconds
    startTime=0
    # timelien end time, seconds
    endTime=24*3600
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # tag for initializing left and right button position
        self.initialPosition=True
        self.setContentsMargins(QMargins(0,0,0,0))
        self.setMinimumSize(350, 50)

        self.btn_y = 3
        self.leftbtn = DragButton("|", self)
        self.leftbtn.resize(10, 20)
        self.leftbtn.setYpos(self.btn_y)

        self.rightbtn = DragButton("|", self)
        self.rightbtn.resize(10, 20)
        self.rightbtn.setYpos(self.btn_y)

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
        leftbtnPos=self.leftbtn.x()+self.leftbtn.size().width();
        if leftbtnPos<self.timelineStep:
            self.startTime=0.0
        else:
            x=(leftbtnPos-self.timelineStep)/self.timelineStep
            # change time to seconds
            self.startTime=int(x*3600)
        # inform grid that time range is changed
        self.timeRangeChanged.emit()
        point=self.leftbtn.rect().topRight()
        global_point=self.leftbtn.mapToGlobal(point)
        QToolTip.showText(QPoint(global_point), Second2Time(self.startTime))
        self.leftbtn.setToolTip(Second2Time(self.startTime))
        
        self.repaint()
    def rightbtnMove(self):
        if self.rightbtn.x()>self.timelineStep*25:
            self.endTime=24.0*3600
        else:
            x=(self.rightbtn.x()-self.timelineStep)/self.timelineStep
            # change time to seconds
            self.endTime=int(x*3600)
        self.timeRangeChanged.emit()
        point=self.rightbtn.rect().topRight()
        global_point=self.rightbtn.mapToGlobal(point)
        QToolTip.showText(QPoint(global_point), Second2Time(self.endTime))
        self.rightbtn.setToolTip(Second2Time(self.endTime))
        
        self.repaint()
    def getTimePeriodRange(self):
        return (self.startTime, self.endTime)

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
        #borderPen=QPen(QColor(255,255,255), 2, Qt.SolidLine)
        width=self.size().width()
        height=self.size().height()
        # draw timeline
        timeline_y=self.size().height()/2
        qp.drawLine(0, timeline_y, width, timeline_y)
        self.timelineStep=width/26
        timelineNumbers=['00:00','04:00','08:00','12:00','16:00','20:00','24:00']
        self.start_x=self.timelineStep
        for i in range(0,25):
            j=i%4
            if(j==0):
                qp.setFont(QFont('Lucida',7))
                metrics = qp.fontMetrics()
                fw = metrics.width(timelineNumbers[int(i/4)])
                qp.drawText(self.timelineStep*i+self.start_x - fw / 2, timeline_y+20, timelineNumbers[int(i/4)])
                qp.drawLine(self.timelineStep * (i) + self.start_x, timeline_y, self.timelineStep * (i) + self.start_x,
                            timeline_y + 7)
            else:
                qp.drawLine(self.timelineStep * (i) + self.start_x, timeline_y, self.timelineStep * (i) + self.start_x,
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

class EventGrid(QWidget):
    cWidth=30
    gridstep=0
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.eventNum=4
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
        # grid left blank margin
        
        # gird right position
        grWidth=int(width-15)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        
        # draw horizontal lines
        for i in range(self.eventNum):
            qp.drawLine(0, i*cHeight, width, i*cHeight)
        qp.drawLine(0, self.eventNum * cHeight-1, width, self.eventNum * cHeight-1)
        # width of each column
        self.gridstep = (width-45) * 0.1
        # draw vertical lines
        qp.setPen(QColor(210,210,222))
        for i in range(11):
            qp.drawLine(self.cWidth+i*self.gridstep, 0, self.cWidth+i*self.gridstep, self.eventNum * cHeight)
        # draw middle horizontal lines
        for i in range(self.eventNum):
            qp.drawLine(0,(i+0.5)*cHeight, width, (i+0.5)*cHeight)
        # draw left and right vertical lines and shadow area behind left and right button
        brush = QBrush(Qt.Dense6Pattern)
        pen = QPen(QColor(122, 122, 32))
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(self.cWidth, 0, self.leftXPos-self.cWidth, height)
        qp.drawRect(self.rightXPos,0,grWidth-self.rightXPos, height)

    def setLeftLineXPos(self, xPos):
        self.leftXPos=xPos
    def setRightLineXPos(self, xPos):
        self.rightXPos=xPos
    def getcWidth(self):
        return self.cWidth
    def getgridstep(self):
        return self.gridstep

class GridArea(QWidget):
    # grid time range
    timeRangeMin=0
    timeRangeMax=24*3600
    timeRange=24*3600
    # grid start time and end time
    startTime=0
    endTime=0
    # grid left blank width
    lbWidth=0
    # grid column width
    columndWidth=0
    # tag for initializing left and right button position
    initialPosition=True
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setContentsMargins(QMargins(0,0,0,0))
        self.widget=EventGrid()
        #self.widget.setGeometry(0,0,self.size().width(), self.widget.eventNum*self.widget.rowHeight)
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

        self.leftbtn=DragButton("|", self)
        self.leftbtn.resize(10, 30)

        self.rightbtn=DragButton("|", self)
        self.rightbtn.resize(10, 30)
        
        self.leftbtn.setRightBtn(self.rightbtn)
        self.rightbtn.setLeftBtn(self.leftbtn)
        self.leftbtn.mouseReleaseSignal.connect(self.leftbtnRelease)
        self.rightbtn.mouseReleaseSignal.connect(self.rightbtnRelease)
        self.leftbtn.mouseMoveSignal.connect(self.leftbtnMove)
        self.rightbtn.mouseMoveSignal.connect(self.rightbtnMove)

    resizetimes=0
    def resizeEvent(self, QResizeEvent):
        gridwidth=self.size().width()-25
        self.widget.setGeometry(0, 0, gridwidth, self.widget.eventNum * self.widget.rowHeight)
        # set leftbtn and rightbtn position and moving range
        self.lbWidth=self.widget.getcWidth()
        leftRange=self.lbWidth-self.leftbtn.size().width()+2
        self.columndWidth=self.widget.getgridstep()
        rightRange=gridwidth*0.97
        yPos=self.size().height()/2-self.leftbtn.size().height()/2;
        self.leftbtn.setYpos(yPos)
        self.rightbtn.setYpos(yPos)
        self.resizetimes=self.resizetimes+1
        if self.initialPosition:
            self.leftbtn.move(leftRange, yPos)
            self.rightbtn.move(rightRange-self.rightbtn.x(), yPos)
            self.leftbtnXPosRatio = (self.leftbtn.x()+self.leftbtn.size().width()-self.lbWidth-2) / self.size().width()
            self.rightbtnXPosRatio = self.rightbtn.x() / (self.size().width()-self.lbWidth)
            self.initialPosition=False
        else:
            if self.resizetimes==2:
                self.leftbtn.move(leftRange,yPos)
                self.rightbtn.move(rightRange, yPos)
                self.leftbtnXPosRatio = (self.leftbtn.x()+self.leftbtn.size().width()-self.lbWidth-2) / self.size().width()
                self.rightbtnXPosRatio = self.rightbtn.x() / (self.size().width()-self.lbWidth)
            else:
                self.leftbtn.move(self.leftbtnXPosRatio*self.size().width()+self.lbWidth-self.leftbtn.size().width()+2, yPos)
                self.rightbtn.move(self.rightbtnXPosRatio*(self.size().width()-self.lbWidth), yPos)
        self.leftbtn.setXrange(leftRange, self.rightbtn.x()-self.leftbtn.size().width()+0.5)
        self.rightbtn.setXrange(self.leftbtn.x()+self.leftbtn.size().width()-0.5, rightRange)
        self.widget.setRightLineXPos(self.rightbtn.x())
        self.widget.setLeftLineXPos(self.leftbtn.x()+self.leftbtn.size().width()-2)
        self.lbWidth=self.widget.getcWidth()
        self.columndWidth=self.widget.getgridstep()
        
    def leftbtnRelease(self):
        self.leftbtnXPosRatio = (self.leftbtn.x()+self.leftbtn.size().width()-self.lbWidth) / self.size().width()

    def rightbtnRelease(self):
        self.rightbtnXPosRatio=self.rightbtn.x()/(self.size().width()-25)
        
    def leftbtnMove(self):
        self.widget.setLeftLineXPos(self.leftbtn.x()+self.leftbtn.size().width()-2)
        # show time as btn moves
        point=self.leftbtn.rect().topRight()
        global_point=self.leftbtn.mapToGlobal(point)
        self.columndWidth=self.widget.getgridstep()
        leftbtnPos=self.leftbtn.x()+self.leftbtn.size().width()-2;
        if leftbtnPos<self.lbWidth:
            self.startTime=self.timeRangeMin
        else:
            x=(leftbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.startTime=int(x)+self.timeRangeMin
        QToolTip.showText(QPoint(global_point), Second2Time(self.startTime))
        self.leftbtn.setToolTip(Second2Time(self.startTime))

        self.widget.repaint()
        
    def rightbtnMove(self):
        self.widget.setRightLineXPos(self.rightbtn.x()+0.5)
        # show time as btn moves
        point=self.rightbtn.rect().topRight()
        self.columndWidth=self.widget.getgridstep()
        global_point=self.rightbtn.mapToGlobal(point)
        rightbtnPos=self.rightbtn.x()+0.5
        if rightbtnPos>(self.lbWidth+self.columndWidth*10):
            self.endTime=self.timeRangeMax
        else:
            x=(rightbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.endTime=int(x)
        self.rightbtn.setToolTip(Second2Time(self.endTime))
        QToolTip.showText(QPoint(global_point), Second2Time(self.endTime))
        self.rightbtn.setToolTip(Second2Time(self.endTime))

        self.widget.repaint()
        
    def setTimeRange(self, sTime, eTime):
        self.timeRangeMin=sTime
        self.timeRangeMax=eTime
        self.timeRange=eTime-sTime

        self.columndWidth=self.widget.getgridstep()
        leftbtnPos=self.leftbtn.x()+self.leftbtn.size().width()-2;
        if leftbtnPos<self.lbWidth:
            self.startTime=self.timeRangeMin
        else:
            x=(leftbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.startTime=int(x)+self.timeRangeMin

        rightbtnPos=self.rightbtn.x()+0.5
        if rightbtnPos>(self.lbWidth+self.columndWidth*10):
            self.endTime=self.timeRangeMax
        else:
            x=(rightbtnPos-self.lbWidth)*self.timeRange/(10*self.columndWidth)
            # change time to seconds
            self.endTime=int(x)

        self.leftbtn.setToolTip(Second2Time(self.startTime))
        self.rightbtn.setToolTip(Second2Time(self.endTime))

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

def Second2Time(second):
    hour=int(second/3600)
    minute=int((second-hour*3600)/60)
    sec=second%60
    return str(hour)+':'+str(minute)+':'+str(int(sec))

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=TimeLine()
    #ex=GridArea()
    #ex=EventGrid()
    # ex=TestDragButton()
    #ex=Tileline()
    ex.show()
    sys.exit(app.exec_())