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
        self.setGeometry(300,300,250,300)
        self.setMinimumSize(250, 300)
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
        if self.freqSender==self.btnWeekly:
            self.btnWeekly.setChecked(True)
            self.btnMonthly.setChecked(False)
            self.btnYearly.setChecked(False)
            self.frequency=[1,1,1,1,1,1,1]
        if self.freqSender==self.btnMonthly:
            self.btnWeekly.setChecked(False)
            self.btnMonthly.setChecked(True)
            self.btnYearly.setChecked(False)
            self.frequency=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        if self.freqSender==self.btnYearly:
            self.btnWeekly.setChecked(False)
            self.btnMonthly.setChecked(False)
            self.btnYearly.setChecked(True)
            self.frequency=[1,1,1,1,1,1,1,1,1,1,1,1]
        if self.freqSender==self.btnCustom:
            self.btnWeekly.setChecked(False)
            self.btnMonthly.setChecked(False)
            self.btnYearly.setChecked(False)
            self.btnCustom.setChecked(True)
            self.cp=CustomFrequencyPanel(self)
            self.cp.setWindowFlags(Qt.FramelessWindowHint)
            point=self.btnCustom.rect().topRight()
            global_point=self.btnCustom.mapToGlobal(point)
            self.cp.setPosition(global_point.x(),global_point.y())
            self.cp.signal.connect(self.emitFrequency)
            self.cp.exec_()
        #frequency=self.freqSender.text()
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
        self.cal.setGeometry(0,0,390,250)
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
    # weekly height
    weeklyHeight=230
    monthlyHeight=380
    yearlyHeight=350
    signal=pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.vlayout=QVBoxLayout()
        self.h1layout=QHBoxLayout()
        self.cf=FrequencySelectionBtns()
        self.cf.resize(QSize(250,160))
        self.cf.daysSelection[str].connect(self.daysSelected)
        self.h1layout.addWidget(self.cf)
        self.h1layout.setSizeConstraint(QLayout.SetFixedSize)
        self.vlayout.addLayout(self.h1layout)

        self.ws=WeeklySelectionPanel()
        self.vlayout.addWidget(self.ws)
        self.vlayout.addStretch(1)
        self.hlayout=QHBoxLayout()
        self.btnCancel=QPushButton()
        self.btnCancel.setText('Cancel')
        self.btnCancel.resize(QSize(60,27))
        self.btnCancel.clicked.connect(self.btnClicked)
        self.hlayout.addWidget(self.btnCancel)
        self.hlayout.addStretch(1)
        self.btnConfirm=QPushButton()
        self.btnConfirm.setText('Confirm')
        self.btnConfirm.resize(QSize(60,27))
        self.btnConfirm.clicked.connect(self.btnClicked)
        self.hlayout.addWidget(self.btnConfirm)
        self.vlayout.addLayout(self.hlayout)
        self.setLayout(self.vlayout)
        
    def daysSelected(self, days):
        self.vlayout.removeWidget(self.ws)
        self.ws.deleteLater()
        self.ws=None
        if days=='weekly':
            self.ws=WeeklySelectionPanel()
        if days=='monthly':
            self.ws=MonthlySelectionPanel()
        if days=='yearly':
            self.ws=YearlySelectionPanel()
        self.vlayout.insertWidget(1,self.ws)
        self.resize(QSize(220,200))

    def setPosition(self, x,y):
        self.move(x,y)
    def btnClicked(self):
        s=self.sender()
        if s==self.btnCancel:
            self.close()
        if s==self.btnConfirm:
            self.close()
            frequency=[]
            frequency.append(self.ws.customDays)
            frequency.append(self.ws.getTimes())
            self.signal.emit(frequency)

class FrequencySelectionBtns(QWidget):
    daysSelection=pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(QSize(220,100))
        self.setMaximumSize(QSize(220,100))
        txtX=85
        txtY=15
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
        self.btnWeekly.setChecked(True)

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
        if self.freqSender==self.btnWeekly:
            self.btnWeekly.setChecked(True)
            self.btnMonthly.setChecked(False)
            self.btnYearly.setChecked(False)
            self.daysSelection.emit('weekly')
        if self.freqSender==self.btnMonthly:
            self.btnWeekly.setChecked(False)
            self.btnMonthly.setChecked(True)
            self.btnYearly.setChecked(False)
            self.daysSelection.emit('monthly')
        if self.freqSender==self.btnYearly:
            self.btnWeekly.setChecked(False)
            self.btnMonthly.setChecked(False)
            self.btnYearly.setChecked(True)
            self.daysSelection.emit('yearly')

# custom panel, buttons of 7-day panel
class WeeklySelectionPanel(QWidget):
    customDays=[0,0,0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(220,80)
        self.setMaximumSize(220,80)
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
            self.customDays[n]=1
        else:
            self.customDays[n]=0
    def getTimes(self):
        return self.txtTimes.toPlainText()

# custom panel, buttons of 31-day panel
class MonthlySelectionPanel(QWidget):
    customDays=[0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(220,180)
        self.setMaximumSize(220,180)
        lblevery=QLabel(self)
        lblevery.setText('Every')
        lblevery.move(10,5)
        lblevery.adjustSize()
        self.txtTimes=QTextEdit(self)
        self.txtTimes.move(45,1)
        self.txtTimes.resize(QSize(35,28))
        self.txtTimes.setText('1')
        lblUnit=QLabel(self)
        lblUnit.setText('month(s) on:')
        lblUnit.move(85,5)
        lblUnit.adjustSize()
        a=25
        for i in range(len(self.customDays)):
            btn=QPushButton(self)
            btn.setText(str(i+1))
            btn.setCheckable(True)
            btn.resize(QSize(a,a))
            btn.move(25+(i%7)*27, 40+27*(i//7))
            btn.clicked.connect(self.btnClicked)
        
    def btnClicked(self):
        s=self.sender()
        if s.isChecked():
            self.customDays[int(s.text())]=1
        else:
            self.customDays[int(s.text())]=0
    def getTimes(self):
        return self.txtTimes.toPlainText()

#custom panel, buttons of 12-month 
class YearlySelectionPanel(QWidget):
    customDays=[0,0,0,0,0,0,
                0,0,0,0,0,0]
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(220,170)
        self.setMaximumSize(220,170)
        lblevery=QLabel(self)
        lblevery.setText('Every')
        lblevery.move(10,5)
        lblevery.adjustSize()
        self.txtTimes=QTextEdit(self)
        self.txtTimes.move(45,1)
        self.txtTimes.resize(QSize(35,28))
        self.txtTimes.setText('1')
        lblUnit=QLabel(self)
        lblUnit.setText('year(s) on:')
        lblUnit.move(85,5)
        lblUnit.adjustSize()
        btnsTxt=['JAN','FEB','MAR','APR','MAY','JUN',
                 'JUL','AUG','SEP','OCT','NOV','DEC']
        a=40
        btns=[]
        self.btnJan=QPushButton(self)
        self.btnJan.clicked.connect(lambda: self.weekClicked(0))
        self.btnFeb=QPushButton(self)
        self.btnFeb.clicked.connect(lambda: self.weekClicked(1))
        self.btnMar=QPushButton(self)
        self.btnMar.clicked.connect(lambda: self.weekClicked(2))
        self.btnApr=QPushButton(self)
        self.btnApr.clicked.connect(lambda: self.weekClicked(3))
        self.btnMay=QPushButton(self)
        self.btnMay.clicked.connect(lambda: self.weekClicked(4))
        self.btnJun=QPushButton(self)
        self.btnJun.clicked.connect(lambda: self.weekClicked(5))
        self.btnJul=QPushButton(self)
        self.btnJul.clicked.connect(lambda: self.weekClicked(6))
        self.btnAug=QPushButton(self)
        self.btnAug.clicked.connect(lambda: self.weekClicked(7))
        self.btnSep=QPushButton(self)
        self.btnSep.clicked.connect(lambda: self.weekClicked(8))
        self.btnOct=QPushButton(self)
        self.btnOct.clicked.connect(lambda: self.weekClicked(9))
        self.btnNov=QPushButton(self)
        self.btnNov.clicked.connect(lambda: self.weekClicked(10))
        self.btnDec=QPushButton(self)
        self.btnDec.clicked.connect(lambda: self.weekClicked(11))
        btns=[self.btnJan, self.btnFeb, self.btnMar, self.btnApr, self.btnMay, self.btnJun,
              self.btnJul, self.btnAug, self.btnSep, self.btnOct, self.btnNov, self.btnDec]
        for i in range(len(btns)):
            btns[i].setText(btnsTxt[i])
            btns[i].setCheckable(True)
            btns[i].resize(QSize(a,a))
            btns[i].move(25+(i%4)*42, 40+42*(i//4))

    def weekClicked(self, n):
        s=self.sender()
        if s.isChecked():
            self.customDays[n]=1
        else:
            self.customDays[n]=0
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
    #ex=YearlySelectionPanel()
    ex.show();
    sys.exit(app.exec_())

