# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:40:58 2020

@author: jonas
"""

#----------------------------------------------------------------------------

#								Function

#----------------------------------------------------------------------------
def play(self):
	
	self.Play = True
	self.read()

def pause(self):
	
	self.Play = False
	self.thread._stop()
	
def connect(self):
	self.window1.show()
	
def Add_func(self):
	self.Window3.show()

def Get_data(self):
	self.Body_positionView.clear()
	self.SP02View.clear()
	self.Blood_pressurView.clear()
	
	self.SP02View.addLegend()
	self.Body_positionView.addLegend()
	self.blbox =  QtWidgets.QVBoxLayout()
	pos = []
	blood_ble_dias = []
	blood_ble_syst = []
	blood_ble_bpm = []
	spo2_ble_oxy = []
	spo2_ble_bpm = []

	
	pos ,time_pos = get_body_pos(self.edit_time_start.text(), self.edit_time_end.text(), get_id_profil(str(self.comboBox.currentText())))
	blood_ble_dias,blood_ble_syst,blood_ble_bpm ,time_blood= get_blood(self.edit_time_start.text(), self.edit_time_end.text(), get_id_profil(str(self.comboBox.currentText())))
	spo2_ble_oxy,spo2_ble_bpm ,time_spo2 = get_spo2(self.edit_time_start.text(), self.edit_time_end.text(), get_id_profil(str(self.comboBox.currentText())))
	
	pen1 = pg.mkPen(color=(255, 0, 0))
	pen2 = pg.mkPen(color=(0, 255, 0))
	pen3 = pg.mkPen(color=(0, 0, 255))
	
	pos_x=[]
	for i in range(0,len(pos)):
		pos_x.append(i)
	
	curve1 = self.Body_positionView.plot(pos, pen=pen1,name='pos')


	if(len(pos)>0):
		ay = self.Body_positionView.getAxis('bottom')
		ay.setTicks([[(v, time_pos[v]) for v in range(0,len(time_pos),int(len(time_pos)/5)) ]])
	
	
	
	spo2_x=[]
	for i in range(0,len(spo2_ble_oxy)):
		spo2_x.append(i)
	curve1 = self.SP02View.plot(spo2_ble_oxy, pen=pen3,name ='spo2_ble_oxy')
	curve2 = self.SP02View.plot(spo2_ble_bpm, pen=pen1,name ='spo2_ble_bpm')

	if(len(spo2_ble_oxy)>0):
		ay = self.SP02View.getAxis('bottom')
		ay.setTicks([[(v, time_spo2[v]) for v in range(0,len(time_spo2),int(len(time_spo2)/5)) ]])
	
		
	blood_x=[]
	for i in range(0,len(blood_ble_dias)):
		blood_x.append(i)
	
	curve3 = self.Blood_pressurView.plot(blood_ble_dias, pen=pen3,name ='blood_ble_dias')

	curve4 = self.Blood_pressurView.plot(blood_ble_syst, pen=pen1, name ='blood_ble_syst')

	curve5 = self.Blood_pressurView.plot(blood_ble_bpm, pen=pen2, name ='blood_ble_bpm')

	
	if(len(blood_ble_dias)>0):
		ay = self.Blood_pressurView.getAxis('bottom')
		ay.setTicks([[(v, time_blood[v]) for v in range(0,len(time_blood),int(len(time_blood)/5)) ]])
	self.Body_positionView.addLegend()
	self.SP02View.addLegend()
	self.Blood_pressurView.addLegend()
	
#----------------------------------------------------------------------------

#								CLASS

#----------------------------------------------------------------------------
from importss import*
import multiprocessing

class TestThread(threading.Thread):
	count = 0
	bearer =''
	connecte = False
	ts_start =''
	
	def __init__(self, name='TestThread'):
		""" constructor, setting initial variables """
		self._stopevent = threading.Event(  )
		self._sleepperiod = 3
		fmt = '%Y-%m-%d %H:%M:%S'
		#2) preparation données
		now = datetime.datetime.now()
		self.ts_start = now.strftime(fmt)+'+00'
		threading.Thread.__init__(self, name=name)
	
	def run(self):
		""" main control loop """
		print( "%s starts",self.getName(  ))
		print(self.connecte)
		if(self.connecte == True):
			
			while not self._stopevent.isSet(  ):
				
				if(Ui_MainWindow.Play ==True):
					fmt = '%Y-%m-%d %H:%M:%S'
					#2) preparation données
					now = datetime.datetime.now()
					ts_end = now.strftime(fmt)+'+00'
					print(self.ts_start,ts_end)
					print(get_id_profil(str(Ui_MainWindow.comboBox.currentText())))
					print(str(Ui_MainWindow.comboBox.currentText()))
					update_database(get_id_profil(str(Ui_MainWindow.comboBox.currentText())),self.ts_start,ts_end,self.bearer)
					Ui_MainWindow().Get_data()
					print("yes")
				self._stopevent.wait(self._sleepperiod)
			print(self.getName(  ))
		
	def join(self, timeout=None):
		""" Stop the thread. """
		self._stopevent.set(  )
		threading.Thread.join(self, timeout)

class AnotherWindow(QWidget):
	
	def conncetion_func(self):
		TestThread.bearer = 'Bearer '+self.titleEdit.text()
		read_all_profil(TestThread.bearer)
		member = get_name_profil()
		for name in member:
				Ui_MainWindow.comboBox.addItem(name)
		try:
			
			TestThread.connecte= True
			
			Ui_MainWindow.testthread.start()
			
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Connection")
			msg.setInformativeText('you are connected')
			msg.setWindowTitle("Connection")
			msg.exec_()
					
	
			Ui_MainWindow.Document.setEnabled(True)
			Ui_MainWindow.End_TR.setEnabled(True)
			Ui_MainWindow.Start_TR.setEnabled(True)
			self.hide()
		except :
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Unablr to connect to API')
			msg.setWindowTitle("Error")
			msg.exec_()
		
	def __init__(self):
		super().__init__()
		self.connection = False
		ber = QLabel('key ')
	
		
		self.titleEdit = QLineEdit()
		
		okButton = QPushButton("Connection")
		okButton.clicked.connect(self.conncetion_func)
		
		
		grid = QGridLayout()
		grid.setSpacing(10)
		
		grid.addWidget(ber, 1, 0)
		grid.addWidget(self.titleEdit, 1, 1)
		
		
		grid.addWidget(okButton, 3, 1)
		
		
		self.setLayout(grid)
		
		self.setGeometry(300, 300, 900, 300)
		self.setWindowTitle('Connexion to MySignal API')
		
		
class DocumentWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
		
        grid.addWidget(okButton, 9, 0)
        grid.addWidget(cancelButton, 9, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        
class ADDWindow(QWidget):
    
	def Add_Patient(self):
		Ui_MainWindow.comboBox.addItem(self.NameEdit.text())
		self.hide()
	
	def __init__(self):
		super().__init__()
		self.connection = False
		Name = QLabel('Name')
		
		
		self.NameEdit = QLineEdit()
		
		
		okButton = QPushButton("ADD")
		okButton.clicked.connect(self.Add_Patient)
		
		
		grid = QGridLayout()
		grid.setSpacing(10)
		
		grid.addWidget(Name, 1, 0)
		grid.addWidget(self.NameEdit, 1, 1)
		
		grid.addWidget(okButton, 2, 1)
		
		
		self.setLayout(grid)
		
		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Add Patient')
		
class Ui_MainWindow(object):
	
	testthread = TestThread()
	w = testthread.count
	test = [0]
	Body_positionView  = pg.plot()
	Body_positionView.setWindowTitle('pyqtgraph example: Legend')
	Body_positionView.addLegend()
	SP02View =  pg.plot()
	Blood_pressurView  =  pg.plot()
	tab = QtWidgets.QWidget()
	edit_time_end = QtWidgets.QLineEdit()
	edit_time_start = QtWidgets.QLineEdit()
	Start_TR = QPushButton(tab)
	End_TR = QPushButton(tab)
	Document = QPushButton(tab)
	Play = False
	comboBox =QComboBox(tab)	
	
	def Get_data(self):
		Get_data(self)
	def play(self):
		Ui_MainWindow.Play =True

	def pause(self):
		Ui_MainWindow.Play = False

	def toggle_window1(self, checked):
		if self.window1.isVisible():
			self.window1.hide()
		else:
			self.window1.show()
			
	def toggle_window2(self, checked):
		if self.window2.isVisible():
			self.window2.hide()
		else:
			self.window2.show()
	def connect(self):
		connect(self)
	def Add_func(self):
		Add_func(self)
	
	def get_patient(self):
		try:
			
			member = get_name_profil()
		
			for row in member:
				self.comboBox.addItem(row[0])
			
		except Error as e:
		    print("Error reading data from MySQL table", e)
		

	def setupUi(self, MainWindow,x,y):
		self.window1 = AnotherWindow()
		self.window2 = DocumentWindow()
		self.Window3 = ADDWindow()
		self.Show = True
		self.Play = False
		self.x =[]
		self.interval = 2
		self.connection = False


		#-----------------------------------
		#          Window declaration
		#-----------------------------------
		self.MainWindow = MainWindow
		self.MainWindow.setWindowTitle("MainWindow")
		self.MainWindow.resize(x,y)

		#-----------------------------------
		#           Frame Parameter
		#-----------------------------------
		self.centralwidget = QtWidgets.QWidget(self.MainWindow)
		self.gridLayout = QVBoxLayout()
		self.gridLayout.setObjectName("gridLayout")
		#-----------------------------------
		#           Table
		#-----------------------------------
		self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
		self.tab = QtWidgets.QWidget()
		self.tab.setAutoFillBackground(True)
		palette = self.tab.palette()
		palette.setColor(self.tab.backgroundRole(), QColor(45, 45, 45, 255))
		self.tab.setPalette(palette)

		self.Tab_1_Layout = QtWidgets.QGridLayout(self.tab)
		self.Tab_1_Layout.setContentsMargins(-1, 11, -1, -1)

		self.tabWidget.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.Tab_2_Layout = QtWidgets.QHBoxLayout(self.tab_2)
		self.tab_2.setAutoFillBackground(True)
		palette = self.tab_2.palette()
		palette.setColor(self.tab_2.backgroundRole(), QColor(45, 45, 45, 255))
		self.tab_2.setPalette(palette)
		self.tabWidget.addTab(self.tab_2, "")


		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab)," Analyse")
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Profile Patient")


		#-----------------------------------
		#       SP02 Group Box
		#-----------------------------------
		self.SP02GroupBox = QtWidgets.QGroupBox("SP02",self.tab)
		self.SP02GroupBox.setObjectName("SP02")
		self.SP02GroupBox.setStyleSheet('QGroupBox#SP02 {color: rgb(255 ,255 ,255 ); border: 2px solid gray;}')
		
		self.vbox =  QtWidgets.QVBoxLayout()
		self.vbox.addWidget(self.SP02View)
		self.SP02GroupBox.setLayout(self.vbox)


		

		self.Body_positionGroupBox = QtWidgets.QGroupBox("Body_position",self.tab)
		self.Body_positionGroupBox.setObjectName("Body_position")
		self.Body_positionGroupBox.setStyleSheet('QGroupBox#Body_position {color: rgb(255 ,255 ,255 ); border: 2px solid gray;}')
		
		self.bbox =  QtWidgets.QVBoxLayout()
		self.bbox.addWidget(self.Body_positionView)
		self.Body_positionGroupBox.setLayout(self.bbox)

		self.Blood_pressurGroupBox = QtWidgets.QGroupBox("Blood_pressur",self.tab)
		self.Blood_pressurGroupBox.setObjectName("Blood_pressur")
		self.Blood_pressurGroupBox.setStyleSheet('QGroupBox#Blood_pressur {color: rgb(255 ,255 ,255 ); border: 2px solid gray;}')
		self.Blood_pressurView.addLegend()
		self.blbox =  QtWidgets.QVBoxLayout()
		self.blbox.addWidget(self.Blood_pressurView)
		self.Blood_pressurGroupBox.setLayout(self.blbox)

		self.AutreGroupBox = QtWidgets.QGroupBox("Autre",self.tab)
		self.AutreGroupBox.setObjectName("Autre")
		self.AutreGroupBox.setStyleSheet('QGroupBox#Autre {color: rgb(255 ,255 ,255 ); border: 2px solid gray;}')

		#-----------------------------------
		#         Parameter Group Box
		#-----------------------------------
		self.ParameterGroupBox = QtWidgets.QGroupBox( "Parameter",self.tab)
		self.ParameterGroupBox.setObjectName("Parameter")
		self.ParameterGroupBox.setStyleSheet('QGroupBox#Parameter {color: rgb(255 ,255 ,255 ); border: 2px solid gray;}')
		self.ParameterGroupBox.setMaximumSize(QtCore.QSize(250, 9999))
		self.ParameterLayout = QtWidgets.QFormLayout(self.ParameterGroupBox)


		#-----------------------------------
		#           Menu Bar
		#-----------------------------------
		self.menubar = QtWidgets.QMenuBar(self.MainWindow)
		self.menuLoad = self.menubar.addMenu("Load")
		self.actionFrom_Folder = QtWidgets.QAction(self.MainWindow)
		self.actionFrom_Folder.setText("From Folder")
		self.menuLoad.addAction(self.actionFrom_Folder)
		self.menubar.addAction(self.menuLoad.menuAction())
		self.Tools =self.menubar.addMenu("Tools")
		self.resetb = QtWidgets.QAction(self.MainWindow)
		self.resetb.setText("Reset View")
		self.Tools.addAction(self.resetb)
		self.help = self.menubar.addMenu("help")

		#-----------------------------------
		#          Button Parameters
		#-----------------------------------
				#-----------------------------------
		#          Button Parameters
		#-----------------------------------
		self.Connection = QPushButton(self.ParameterGroupBox)
		self.Connection.setText("Connection")
		self.ParameterLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.Connection)
		self.Connection.clicked.connect(self.connect)
		
		
		self.Add = QPushButton(self.ParameterGroupBox)
		self.Add.setText("Add Patient")
		self.ParameterLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.Add)
		self.Add.clicked.connect(self.Add_func)
		
		
		self.ParameterLayout.addRow(self.comboBox)
		
		
		self.Plot_data = QPushButton(self.ParameterGroupBox)
		self.Plot_data.setText("Plot save data")
		self.ParameterLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.Plot_data)
		self.Plot_data.clicked.connect(self.Get_data)
		
	
		self.pr = QtWidgets.QLabel(" \n           API Parameters : \n",self.ParameterGroupBox)
		self.pr.setObjectName("pr")
		self.pr.setStyleSheet('QLabel#pr {color: rgb(255 ,255 ,255 );}')
		self.ParameterLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.pr)
		

		self.edit_time_start_label = QtWidgets.QLabel("Date start",self.ParameterGroupBox)
		self.edit_time_start_label.setObjectName("Num_Dotslabel")
		self.edit_time_start_label.setStyleSheet('QLabel#Num_Dotslabel {color: rgb(255 ,255 ,255 );}')
		self.ParameterLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.edit_time_start_label)

		self.edit_time_start= QtWidgets.QLineEdit(self.ParameterGroupBox)
		self.ParameterLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.edit_time_start)

		self.edit_time_end_label = QtWidgets.QLabel("Date End",self.ParameterGroupBox)
		self.edit_time_end_label.setObjectName("Num_Dotslabel")
		self.edit_time_end_label.setStyleSheet('QLabel#Num_Dotslabel {color: rgb(255 ,255 ,255 );}')
		self.ParameterLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.edit_time_end_label)

		self.edit_time_end = QtWidgets.QLineEdit(self.ParameterGroupBox)
		self.ParameterLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.edit_time_end)

		
		self.csv_file = 'lib_data_temp_2.csv'

		
		self.rt = QtWidgets.QLabel("\n            Real Time : \n",self.ParameterGroupBox)
		self.rt.setObjectName("rt")
		self.rt.setStyleSheet('QLabel#rt {color: rgb(255 ,255 ,255 );}')
		self.ParameterLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.rt)
		
		self.Start_TR.setText("Start Real Time")
		self.ParameterLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.Start_TR)
		self.Start_TR.clicked.connect(self.play)
		self.Start_TR.setEnabled(False)

	
		self.End_TR.setText("End Real Time")
		self.ParameterLayout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.End_TR)
		self.End_TR.clicked.connect(self.pause)
		self.End_TR.setEnabled(False)
		
		#self.Bodi_position_GroupBoxLayout.setContentsMargins(15,25,15,15)

		self.ParameterLayout.setContentsMargins(15,25,15,15)
		self.bbox.setContentsMargins(15,25,15,15)
		self.vbox.setContentsMargins(15,25,15,15)
		self.blbox.setContentsMargins(15,25,15,15)

	
		self.Tab_1_Layout.addWidget(self.ParameterGroupBox, 0, 0, 2, 1)
		self.Tab_1_Layout.addWidget(self.SP02GroupBox, 0, 1, 1, 1)
		self.Tab_1_Layout.addWidget(self.Body_positionGroupBox, 1, 1, 1, 1)
		self.Tab_1_Layout.addWidget(self.Blood_pressurGroupBox, 0, 2, 1, 1)
		self.Tab_1_Layout.addWidget(self.AutreGroupBox, 1, 2, 1, 1)



		self.gridLayout.setContentsMargins(0,0,0,0)
		self.tabWidget.setContentsMargins(0,0,0,0)
		self.gridLayout.addWidget(self.menubar)
		self.gridLayout.addWidget(self.tabWidget)
		self.MainWindow.setLayout(self.gridLayout)
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
		self.MainWindow.show()


class MyWindow( QtWidgets.QWidget):
	testthread = Ui_MainWindow.testthread
	def closeEvent(self,event):
		result = QtGui.QMessageBox.question(self,"Confirm Exit...","Are you sure you want to exit ?",QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
		event.ignore()
		if result == QtGui.QMessageBox.Yes:
			if(MyWindow.testthread.connecte== True):
				try:
					MyWindow.testthread.join()
				except Error as e:
					print("Error reading data from MySQL table", e)
			event.accept()



if __name__ == "__main__":
       import sys

       app = QtWidgets.QApplication(sys.argv)
       screen = app.primaryScreen()
       size = screen.size()
       app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
       MainWindow = MyWindow()
       ui = Ui_MainWindow()
       ui.setupUi(MainWindow,size.width()-size.width()*0.015, size.height()-size.height()*0.08)
       sys.exit(app.exec_())

