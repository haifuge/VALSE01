import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.EventTimeline import GridArea
from UI.EventTimeline import Tileline

class TimeLine(QWidget):
    def __init__(self, _data=[]):
        super().__init__()
        self.data=_data
        self.initUI()
    def initUI(self):
        self.setMinimumSize(500,270)
        #self.setFixedSize(500,270)
        self.tab=QTabWidget(self)
        self.tab.move(0,0)
        self.tab.size().width=self.size().width()
        self.tab.size().height=self.size().height()
        verfiedTab=VerifiedTab(self.data)
        self.tab.addTab(verfiedTab,"Verified")
        unverifiedTab=VerifiedTab(self.data)
        self.tab.addTab(unverifiedTab,"Unverified")

    def resizeEvent(self, e):
        self.tab.resize(e.size()+QSize(1,1))

class VerifiedTab(QWidget):
    def __init__(self, _data=[]):
        super().__init__()
        self.data=_data
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
        self.grid=GridArea.GridArea(self.data)
        self.grid.setGeometry(0,0,self.size().width(),self.size().height() - 15)
        self.vlb.addWidget(self.grid)

        self.timeline=Tileline.Tileline()
        self.timeline.setGeometry(0, 0, self.size().width(), 20)
        self.timeline.timeRangeChanged.connect(self.timeRangeChanging)
        self.vlb.addWidget(self.timeline)

        self.setLayout(self.vlb)

    def paintEvent(self, e):
        pass
        #qp=QPainter()z
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
        
    def SetData(self, _data):
        self.data=_data

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=TimeLine()
    #ex=GridArea()
    #ex=EventGrid()
    # ex=TestDragButton()
    #ex=Tileline()
    ex.show()
    sys.exit(app.exec_())