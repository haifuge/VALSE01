import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DateMenu(QWidget):
    startDate=''
    endDate=''
    frequency=[]
    location=''
    """description of class"""
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,240,300)
        # textEdit position
        txtY=15;
        txtX=90;
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

        # location
        txtY=txtY+yInterval+5;
        lblLocation=QLabel(self)
        lblLocation.setText('Location:')
        lblLocation.adjustSize()
        lblLocation.move(20,txtY)
        self.btnLocation=QComboBox(self)
        self.btnLocation.addItems(['Location1','Location2','Location3'])
        self.location='Location1'
        self.btnLocation.move(txtX,txtY)
        self.btnLocation.resize(txtWidth,txtHeight)
        self.btnLocation.currentTextChanged.connect(self.setLocation)

        txtY=txtY+yInterval+5;
        self.btnCancel=QPushButton(self)
        self.btnCancel.setText('Cancel')
        self.btnCancel.resize(QSize(70,30))
        self.btnCancel.move(35,txtY)
        self.btnCancel.clicked.connect(self.btnDecClicked)
        self.btnConfirm=QPushButton(self)
        self.btnConfirm.setText('Confirm')
        self.btnConfirm.resize(QSize(70,30))
        self.btnConfirm.clicked.connect(self.btnDecClicked)
        self.btnConfirm.move(150,txtY)

        #  btn date click
        self.btnDateStart.clicked.connect(self.btnDateClicked)
        self.btnDateEnd.clicked.connect(self.btnDateClicked)
        self.ds=DateSelector(self)
        self.ds.signal[str].connect(self.setbtnText)
        self.ds.setWindowFlags(Qt.FramelessWindowHint)
        
        # btn frequency click
        self.btnWeekly.clicked.connect(self.frequencyClicked)
        self.btnMonthly.clicked.connect(self.frequencyClicked)
        self.btnYearly.clicked.connect(self.frequencyClicked)
        self.btnCustom.clicked.connect(self.frequencyClicked)

    def setLocation(self):
        self.location=self.btnLocation.currentText()
    def btnDecClicked(self):
        s=self.sender()
        if s==self.btnCancel:
            self.close()
        if s==self.btnConfirm:
            #self.close()
            print(self.startDate, self.endDate, self.frequency, self.location, sep=', ')

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
        if self.freqSender==self.btnCustom:
            self.btnCustom.setChecked(True)
            self.cp=CustomFrequencyPanel(self)
            self.cp.setWindowFlags(Qt.FramelessWindowHint)
            point=self.btnCustom.rect().topRight()
            global_point=self.btnCustom.mapToGlobal(point)
            self.cp.setPosition(global_point.x(),global_point.y())
            self.cp.signal.connect(self.emitFrequency)
            self.cp.exec_()
        frequency=self.freqSender.text()
    def emitFrequency(self, arr):
        self.frequency=arr
    def btnDateClicked(self):
        self.btnSender=self.sender()
        point=self.btnSender.rect().topRight()
        global_point=self.btnSender.mapToGlobal(point)
        self.ds.setPosition(global_point.x(), global_point.y())
        self.ds.exec_()
    def setbtnText(self, s):
        self.btnSender.setText(s)
        if self.btnSender==self.btnDateStart:
            self.startDate=s
        if self.btnSender==self.btnDateEnd:
            self.endDate=s

class DateSelector(QDialog):
    signal=pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.cal=QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setGeometry(0,0,370,250)
        self.cal.clicked[QDate].connect(self.emitDate)
        self.lbl=QLabel(self)
        self.resize(self.cal.size())
        self.setWindowTitle('Calendar')
    def emitDate(self, date):
        self.close()
        self.signal.emit(date.toString('MM/dd/yy'))
    def setPosition(self, x,y):
        self.move(x,y)

class CustomFrequencyPanel(QDialog):
    signal=pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
    def initUI(self):
        vlayout=QVBoxLayout(self)
        self.cf=FrequencySelectionBtns()
        vlayout.addWidget(self.cf)
        self.ws=WeeklySelectionPanel()
        vlayout.addWidget(self.ws)
        hlayout=QHBoxLayout()
        self.btnCancel=QPushButton(self)
        self.btnCancel.setText('Cancel')
        self.btnCancel.resize(QSize(60,27))
        self.btnCancel.clicked.connect(self.btnClicked)
        hlayout.addWidget(self.btnCancel)
        hlayout.addStretch(1)
        self.btnConfirm=QPushButton(self)
        self.btnConfirm.setText('Confirm')
        self.btnConfirm.resize(QSize(60,27))
        self.btnConfirm.clicked.connect(self.btnClicked)
        hlayout.addWidget(self.btnConfirm)
        vlayout.addLayout(hlayout)
        self.setLayout(vlayout)
        self.resize(QSize(250,300))
    def setPosition(self, x,y):
        self.move(x,y)
    def btnClicked(self):
        s=self.sender()
        if s==self.btnCancel:
            self.close()
        if s==self.btnConfirm:
            self.close()
            frequency=[]
            frequency.append(self.ws.weeks)
            frequency.append(self.ws.getTimes())
            self.signal.emit(frequency)


class FrequencySelectionBtns(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(200,200)
        txtX=85
        txtY=20
         # textEdit size
        txtWidth=120
        txtHeight=27
        # row height
        yInterval=30
        lblFrequency=QLabel(self)
        lblFrequency.setText('Frequency:')
        lblFrequency.adjustSize()
        lblFrequency.move(10,txtY)
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

        self.btnWeekly.clicked.connect(self.frequencyClicked)
        self.btnMonthly.clicked.connect(self.frequencyClicked)
        self.btnYearly.clicked.connect(self.frequencyClicked)

    def frequencyClicked(self):
        self.freqSender=self.sender();
        if self.freqSender!=self.btnWeekly:
            self.btnWeekly.setChecked(False)
        if self.freqSender!=self.btnMonthly:
            self.btnMonthly.setChecked(False)
        if self.freqSender!=self.btnYearly:
            self.btnYearly.setChecked(False)

class WeeklySelectionPanel(QWidget):
    weeks=[0,0,0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        btnsTxt=['S','M','T','W','T','F','S']
        lblevery=QLabel(self)
        lblevery.setText('Every')
        lblevery.move(10,5)
        lblevery.adjustSize()
        self.txtTimes=QTextEdit(self)
        self.txtTimes.move(45,1)
        self.txtTimes.resize(QSize(35,28))
        self.txtTimes.setText('1')
        lblUnit=QLabel(self)
        lblUnit.setText('week(s) on:')
        lblUnit.move(85,5)
        lblUnit.adjustSize()
        a=25
        btns=[]
        self.btnSun=QPushButton(self)
        self.btnSun.clicked.connect(lambda: self.weekClicked(0))
        self.btnMon=QPushButton(self)
        self.btnMon.clicked.connect(lambda: self.weekClicked(1))
        self.btnTue=QPushButton(self)
        self.btnTue.clicked.connect(lambda: self.weekClicked(2))
        self.btnWed=QPushButton(self)
        self.btnWed.clicked.connect(lambda: self.weekClicked(3))
        self.btnThu=QPushButton(self)
        self.btnThu.clicked.connect(lambda: self.weekClicked(4))
        self.btnFri=QPushButton(self)
        self.btnFri.clicked.connect(lambda: self.weekClicked(5))
        self.btnSat=QPushButton(self)
        self.btnSat.clicked.connect(lambda: self.weekClicked(6))
        btns=[self.btnSun, self.btnMon,self.btnTue,self.btnWed,self.btnThu,self.btnFri,self.btnSat]
        for i in range(len(btns)):
            btns[i].setText(btnsTxt[i])
            btns[i].setCheckable(True)
            btns[i].resize(QSize(a,a))
            btns[i].move(25+i*27, 40)
        
    def weekClicked(self, n):
        s=self.sender()
        if s.isChecked():
            self.weeks[n]=1
        else:
            self.weeks[n]=0
    def getTimes(self):
        return self.txtTimes.toPlainText()


class UnitFrequency(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        pass

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=DateMenu()
    ex.show();
    sys.exit(app.exec_())

