from importss import *

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
	