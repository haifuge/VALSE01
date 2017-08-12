import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.EventTimeline import TimeLine
from UI.DateMenu import DateMenu
from UI.Sidebar import PeopleSidebar
from UI.MapWindow import VectorTrail
from Common import DBOperation

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

        map=bar.addMenu("Map")
        map.addAction("Map")
        map.triggered[QAction].connect(self.windowAction)


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
        if q.text()=='Map':
            mapWindow=QMdiSubWindow()
            mapWindow.setWidget(VectorTrail.VectorTrail())
            mapWindow.setWindowFlags(Qt.Window|Qt.WindowTitleHint|Qt.CustomizeWindowHint)
            self.mdi.addSubWindow(mapWindow)
            mapWindow.show()


    def dateWindowClose(self, l):
        # [startDate, endDate, weekday, location]
        print('main: ',l)
        self.dateInfo=l
        self.dateMenu.close()
        if len(l)==1:
            pass
        else:
            self.getData()

    def getData(self):
        dbop=DBOperation.DBOperator()
        self.mapInfo=dbop.ExecSql('select location_id, map_url, max_x, max_y from location where name=\''+self.dateInfo[3]+'\';',4)
        location_id=str(self.mapInfo[0][0])
        sql=''
        if self.dateInfo[2][0]==1:
            # date time to long 
            startDate=QDateTime.fromString(self.dateInfo[0],'MM/dd/yy').addYears(100).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
            endDate=QDateTime.fromString(self.dateInfo[1],'MM/dd/yy').addYears(100).addDays(1).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
            sql='select d.target_id, d.x, d.y, d.date_time from target t, detection d \
                 where t.location_id='+location_id+' and t.target_id=d.target_id and d.ts between '+str(startDate)+' and '+str(endDate)
        else:
            # cusomize date
            startDate=QDate.fromString(self.dateInfo[0],'MM/dd/yy').addYears(100)
            endDate=QDate.fromString(self.dateInfo[1],'MM/dd/yy').addYears(100).addDays(1)
            sql='select target_id, x, y, date_time from detection where target_id=-1 '
            if len(self.dateInfo[2])==7 or len(self.dateInfo[2])==31:
                # weekly, monthly count by day
                t=startDate
                while t<endDate:
                    if self.dateInfo[2][t.dayOfWeek()-1]!=0:
                        sDate=QDateTime(t).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        eDate=QDateTime(t.addDays(1)).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        sql+=' union all select d.target_id, d.x, d.y, d.date_time from target t, detection d \
                              where t.location_id='+location_id+' and t.target_id=d.target_id and d.ts between '+str(sDate)+' and '+str(eDate)+' '
                    t=t.addDays(1)
                
            elif len(self.dateInfo[2])==12:
                # yearly count by month
                # deal with first month of date period
                if self.dateInfo[2][startDate.month()-1]!=0:
                        sDate=QDateTime(startDate).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        eDate=QDateTime(startDate.year(), startDate.month()+1, 1, 0,0).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        sql+=' union all select d.target_id, d.x, d.y, d.date_time from target t, detection d \
                                  where t.location_id='+location_id+' and t.target_id=d.target_id and d.ts between '+str(sDate)+' and '+str(eDate)+' '
                t=startDate.addMonths(1)
                t=QDate(t.year(), t.month(), t.day())
                while t<endDate:
                    if t.month()==endDate.month():
                        break;
                    if self.dateInfo[2][t.month()-1]!=0:
                        sDate=QDateTime(t).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        eDate=QDateTime(t.year, startDate.month+1, 1, 0,0).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                        sql+=' union all select d.target_id, d.x, d.y, d.date_time from target t, detection d \
                                  where t.location_id='+location_id+' and t.target_id=d.target_id and d.ts between '+str(sDate)+' and '+str(eDate)+' '
                    t=t.addMonths(1)
                # deal with last month of date period
                if self.dateInfo[2][t.month()-1]!=0:
                    sDate=QDateTime(t).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                    eDate=QDateTime(endDate).toOffsetFromUtc(QDateTime().offsetFromUtc()).toMSecsSinceEpoch()
                    sql+=' union all select d.target_id, d.x, d.y, d.date_time from target t, detection d \
                                where t.location_id='+location_id+' and t.target_id=d.target_id and d.ts between '+str(sDate)+' and '+str(eDate)+' '
        #self.objInfo=dbop.ExecSql(sql, 4)
        #print(objInfo)
        print(sql)
        print(self.mapInfo)

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MainWindow()
    ex.show()
    sys.exit(app.exec_())
