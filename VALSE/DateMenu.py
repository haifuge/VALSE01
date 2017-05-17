import sys
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel,QApplication, QPushButton, QTextEdit, QToolButton, QComboBox
from PyQt5.QtCore import QDate, pyqtSignal, Qt
from PyQt5.QtGui import *

class DateMenu(QWidget):
    startDate=''
    endDate=''
    frequency=''
    location=''
    """description of class"""
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # textEdit position
        txtY=20;
        txtX=100;
        # textEdit size
        txtWidth=120
        txtHeight=27
        # row height
        yInterval=30

        lblName=QLabel(self);
        lblName.setText('Name:')
        lblName.adjustSize()
        lblName.move(20,txtY)
        self.btnName=QPushButton(self)
        self.btnName.setText('New_Window_1')
        self.btnName.resize(txtWidth,txtHeight)
        self.btnName.move(txtX,txtY)

        txtY=txtY+yInterval;
        lblDateStart=QLabel(self)
        lblDateStart.setText('Date Start:')
        lblDateStart.adjustSize()
        lblDateStart.move(20,txtY)
        self.btnDateStart=QPushButton(self)
        self.btnDateStart.setText('MM/DD/YY')
        self.btnDateStart.resize(txtWidth,txtHeight)
        self.btnDateStart.move(txtX,txtY)

        txtY=txtY+yInterval;
        lblDateEnd=QLabel(self)
        lblDateEnd.setText('Date End:')
        lblDateEnd.adjustSize()
        lblDateEnd.move(20,txtY)
        self.btnDateEnd=QPushButton(self)
        self.btnDateEnd.setText('MM/DD/YY')
        self.btnDateEnd.move(txtX,txtY)
        self.btnDateEnd.resize(txtWidth,txtHeight)

        txtY=txtY+yInterval+5;
        lblFrequency=QLabel(self)
        lblFrequency.setText('Frequency:')
        lblFrequency.adjustSize()
        lblFrequency.move(20,txtY)
        self.btnWeekly=QPushButton(self)
        self.btnWeekly.setText('Weekly')
        self.btnWeekly.setCheckable(True)
        self.btnWeekly.move(txtX,txtY)
        self.btnWeekly.resize(txtWidth,txtHeight)

        txtY=txtY+yInterval-4;
        self.btnMonthly=QPushButton(self)
        self.btnMonthly.setText('Monthly')
        self.btnMonthly.setCheckable(True)
        self.btnMonthly.move(txtX,txtY)
        self.btnMonthly.resize(txtWidth,txtHeight)

        txtY=txtY+yInterval-4;
        self.btnYearly=QPushButton(self)
        self.btnYearly.setText('Yearly')
        self.btnYearly.setCheckable(True)
        self.btnYearly.move(txtX,txtY)
        self.btnYearly.resize(txtWidth,txtHeight)

        txtY=txtY+yInterval-4;
        self.btnCustom=QPushButton(self)
        self.btnCustom.setText('Custom...')
        self.btnCustom.setCheckable(True)
        self.btnCustom.move(txtX,txtY)
        self.btnCustom.resize(txtWidth,txtHeight)

        txtY=txtY+yInterval+5;
        lblLocation=QLabel(self)
        lblLocation.setText('Location:')
        lblLocation.adjustSize()
        lblLocation.move(20,txtY)
        self.btnLocation=QComboBox(self)
        self.btnLocation.addItems(['Location1','Location2','Location3'])
        self.btnLocation.move(txtX,txtY)
        self.btnLocation.resize(txtWidth,txtHeight)

        #  btn date click
        self.btnDateStart.clicked.connect(self.btnClicked)
        self.btnDateEnd.clicked.connect(self.btnClicked)
        self.setGeometry(300,300,300,300)
        self.ds=DateSelector(self)
        self.ds.signal[str].connect(self.setbtnText)
        self.ds.setWindowFlags(Qt.FramelessWindowHint)
        self.dialog=self.ds

        # btn frequency click
        self.btnWeekly.clicked.connect(self.frequencyClicked)
        self.btnMonthly.clicked.connect(self.frequencyClicked)
        self.btnYearly.clicked.connect(self.frequencyClicked)
        self.btnCustom.clicked.connect(self.frequencyClicked)

    def frequencyClicked(self):
        self.freqSender=self.sender();
        if self.freqSender!=self.btnWeekly:
            self.btnWeekly.setChecked(False)
        if self.freqSender!=self.btnMonthly:
            self.btnMonthly.setChecked(False)
        if self.freqSender!=self.btnYearly:
            self.btnYearly.setChecked(False)
        if self.freqSender!=self.btnCustom:
            self.btnCustom.setChecked(False)
        frequency=self.freqSender.text()
        
    def btnClicked(self):
        self.btnSender=self.sender()
        point=self.btnSender.rect().topRight()
        global_point=self.btnSender.mapToGlobal(point)
        self.ds.setPosition(global_point.x(), global_point.y())
        self.dialog.show()
    def setbtnText(self, s):
        self.btnSender.setText(s)

class DateSelector(QWidget):
    signal=pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.cal=QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setGeometry(0,0,370,250)
        self.cal.clicked[QDate].connect(self.showDate)
        self.lbl=QLabel(self)
        date=self.cal.selectedDate()
        self.resize(self.cal.size())
        self.setWindowTitle('Calendar')
    def showDate(self, date):
        self.close()
        self.signal.emit(date.toString('MM/dd/yy'))
    def setPosition(self, x,y):
        self.move(x,y)
if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=DateMenu()
    ex.show();
    sys.exit(app.exec_())

