# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:34:18 2020

@author: jonas
"""


# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:48:11 2020

@author: jonas
"""

import matplotlib.pyplot as plt
import requests
import pprint
import json
import csv
import mysql.connector
import re


def get_profil():
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from patient GROUP BY id"
	id=[]
	
	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
		
		for row in records:
			id.append(row[0])
			
	

	cursor.close()
	mydb.close()
	return id

def get_id_profil(full_name):
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	
	surname,name = re.findall(r'\S+', full_name)
	
	sql_select_Query = "select id from patient where name = '"+name+"' AND surname = '"+surname+"'  GROUP BY id"
	id=0
	
	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
		
		for row in records:
			id = row[0]
			
	

	cursor.close()
	mydb.close()
	return id
def get_name_profil():
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select name,surname from patient GROUP BY id"
	id=[]
	
	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
		
		for row in records:
			id.append(row[1]+" "+row[0])
			
	

	cursor.close()
	mydb.close()
	return id

def save_profil(id,name,surname,height,gender):
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from patient WHERE id = "+str(id)

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount == 0):

	#3) Exucute sql
		sql_insert_query = " INSERT INTO patient (id,name,surname,height,gender) VALUES (%s,%s,%s,%s,%s)"
	
		cursor2 = mydb.cursor()
	
		cursor2.execute(sql_insert_query, (id,name,surname,height,gender))
		mydb.commit()
		cursor2.close()

	cursor.close()
	mydb.close()
	
def read_all_profil(bearer):
	csv_column = ['id','name','surname','height','gender']

	headers = {'Accept': 'application/x.webapi.v1+json','Authorization': bearer,}
	response= requests.get('https://api.libelium.com/mysignals/members', headers=headers)
	print(response.status_code)
	request_response_format= response.json()
	
	dict_data = request_response_format['data']
	import csv
	for data in dict_data:
		
		save_profil(int(data['id']),data['name'],data['surname'],data['height'],data['gender'])

def save_body_pos(id,value,ts,sensor_id,member_id):
	ts = re.sub('\+00$', '', ts)
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from dofy_pos WHERE id = "+str(id)

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount == 0):

	#3) Exucute sql
		sql_insert_query = " INSERT INTO dofy_pos (id,value,ts,sensor_id,member_id) VALUES (%s,%s,%s,%s,%s)"
	
		cursor2 = mydb.cursor()
	
		cursor2.execute(sql_insert_query, (id,value,ts,sensor_id,member_id))
		mydb.commit()
		cursor2.close()

	cursor.close()
	mydb.close()
	
def get_body_pos(ts,te,member_id):
	if(ts == ''):
		ts="2020-01-22 16:23:16+00"
	if(te == ''):
		te="2021-01-22 16:23:16+00"
	value=[]
	time=[]
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select value,ts from dofy_pos WHERE member_id = "+str(member_id)+" AND ts >= '"+ts+"' AND ts <= '"+te+"' order by ts ASC"

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
		for row in records:
			value.append(row[0])
			time.append(row[1])
	

	cursor.close()
	mydb.close()
	return value,time

		
def save_blood_ble_dias(id,value,ts,member_id):
	ts = re.sub('\+00$', '', ts)
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from blood_pres WHERE id = "+str(id)

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount == 0):

	#3) Exucute sql
		sql_insert_query = " INSERT INTO blood_pres (id,blood_ble_dias,ts,id_patient) VALUES (%s,%s,%s,%s)"
	
		cursor2 = mydb.cursor()
	
		cursor2.execute(sql_insert_query, (id,value,ts,member_id))
		mydb.commit()
		cursor2.close()

	cursor.close()
	mydb.close()
	
def save_blood_ble_syst(value,ts,member_id):
	ts = re.sub('\+00$', '', ts)
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from blood_pres WHERE id_patient = "+str(member_id)+" AND ts = '"+ts+"' AND blood_ble_syst IS NULL"

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
		
	#3) Exucute sql
		sql_insert_query = " update blood_pres set blood_ble_syst = %s WHERE id = %s"
	
		cursor2 = mydb.cursor()
	
		cursor2.execute(sql_insert_query, (value,records[0][0]))
		mydb.commit()
		cursor2.close()

	cursor.close()
	mydb.close()
	
	
def save_blood_ble_bpm(value,ts,member_id):
	ts = re.sub('\+00$', '', ts)
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from blood_pres WHERE id_patient = "+str(member_id)+" AND ts = '"+ts+"' AND blood_ble_bpm IS NULL"

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
	
	#3) Exucute sql
		sql_insert_query = " update blood_pres set blood_ble_bpm = %s WHERE id = %s"
	
		cursor2 = mydb.cursor()
	
		cursor2.execute(sql_insert_query, (value,records[0][0]))
		mydb.commit()
		cursor2.close()

	cursor.close()
	mydb.close()

def get_blood(ts,te,member_id):
	if(ts == ''):
		ts="2020-01-22 16:23:16+00"
	if(te == ''):
		te="2021-01-22 16:23:16+00"
	blood_ble_dias=[]
	blood_ble_syst =[]
	blood_ble_bpm =[]
	time = []
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select blood_ble_dias,blood_ble_syst,blood_ble_bpm, ts from blood_pres WHERE id_patient = "+str(member_id)+" AND ts >= '"+ts+"' AND ts <= '"+te+"' order by ts ASC"

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
		for row in records:
			blood_ble_dias.append(row[0])
			blood_ble_syst.append(row[1])
			blood_ble_bpm.append(row[2])
			time.append(row[3])
	

	cursor.close()
	mydb.close()
	return blood_ble_dias,blood_ble_syst,blood_ble_bpm, time

def save_spo2_ble_oxy(id,value,ts,member_id):
	ts = re.sub('\+00$', '', ts)
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from spo2 WHERE id = "+str(id)

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount == 0):

	#3) Exucute sql
		sql_insert_query = " INSERT INTO spo2 (id,spo2_ble_oxy,ts,id_patient) VALUES (%s,%s,%s,%s)"
	
		cursor2 = mydb.cursor()
	
		cursor2.execute(sql_insert_query, (id,value,ts,member_id))
		mydb.commit()
		cursor2.close()

	cursor.close()
	mydb.close()
	
def save_spo2_ble_bpm(value,ts,member_id):
	ts = re.sub('\+00$', '', ts)
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select id from spo2 WHERE id_patient = "+str(member_id)+" AND ts = '"+ts+"' AND spo2_ble_bpm IS NULL"

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
	
	#3) Exucute sql
		sql_insert_query = " update spo2 set spo2_ble_bpm = %s WHERE id = %s"
	
		cursor2 = mydb.cursor()
	
		cursor2.execute(sql_insert_query, (value,records[0][0]))
		mydb.commit()
		cursor2.close()

	cursor.close()
	mydb.close()
	
def get_spo2(ts,te,member_id):
	if(ts == ''):
		ts="2020-01-22 16:23:16+00"
	if(te == ''):
		te="2021-01-22 16:23:16+00"
	spo2_ble_oxy=[]
	spo2_ble_bpm =[]
	time = []
	mydb=mysql.connector.connect(
			  host="localhost",
			  user="root",
			  password="",
			  database= "libelium"
			)
	

	sql_select_Query = "select spo2_ble_oxy,spo2_ble_bpm,ts from spo2 WHERE id_patient = "+str(member_id)+" AND ts >= '"+ts+"' AND ts <= '"+te+"' order by ts ASC"

	cursor = mydb.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	if( cursor.rowcount != 0):
		for row in records:
			spo2_ble_oxy.append(row[0])
			spo2_ble_bpm.append(row[1])
			time.append(row[2])

	cursor.close()
	mydb.close()
	return spo2_ble_oxy,spo2_ble_bpm,time

def read_data(csv_column,sensor_id,member_id,ts_start,ts_end,limit,cursor,order,bearer):

	csv_file = 'lib_data_temp_2.csv'	
	headers = {'Accept': 'application/x.webapi.v1+json','Authorization': bearer,}
	response= requests.get('https://api.libelium.com/mysignals/values',params = {'csv_column':csv_column,'csv_file':csv_file,'sensor_id':sensor_id,'member_id':member_id,'ts_start':ts_start,'ts_end':ts_end,'limit':limit,'cursor':cursor,'order':order}, headers=headers)
	print(response.status_code)
	request_response_format= response.json()
	
	
	dict_data = request_response_format['data']
	import csv
	for data in dict_data:
		if(sensor_id ==  "position"):
			save_body_pos(int(data['id']),int(data['value']),data['ts'],data['sensor_id'],int(data['member_id']))
		elif(sensor_id ==  "blood_ble_dias"):
			save_blood_ble_dias(int(data['id']),int(data['value']),data['ts'],int(data['member_id']))
		elif(sensor_id ==  "blood_ble_syst"):
			save_blood_ble_syst(int(data['value']),data['ts'],int(data['member_id']))
		elif(sensor_id ==  "blood_ble_bpm"):
			save_blood_ble_bpm(int(data['value']),data['ts'],int(data['member_id']))
		elif(sensor_id ==  "spo2_ble_oxy"):
			save_spo2_ble_oxy(int(data['id']),int(data['value']),data['ts'],int(data['member_id']))
		elif(sensor_id ==  "spo2_ble_bpm"):
			save_spo2_ble_bpm(int(data['value']),data['ts'],int(data['member_id']))
			
	
def update_database(member_id,ts_start,ts_end,bearer):
	if(ts_start == ''):
		ts_start="2020-01-22 16:23:16+00"
	if(ts_end == ''):
		ts_end="2021-01-22 16:23:16+00"
	csv_column = ['id','value','ts','sensor_id','member_id']
	limit="100"
	cursor="0"
	order="asc"
	sensor_id="position"
	read_data(csv_column, sensor_id, member_id, ts_start, ts_end, limit, cursor, order, bearer)
	sensor_id="blood_ble_dias"
	read_data(csv_column, sensor_id, member_id, ts_start, ts_end, limit, cursor, order, bearer)
	sensor_id="blood_ble_syst"
	read_data(csv_column, sensor_id, member_id, ts_start, ts_end, limit, cursor, order, bearer)
	sensor_id="blood_ble_bpm"
	read_data(csv_column, sensor_id, member_id, ts_start, ts_end, limit, cursor, order, bearer)
	sensor_id="spo2_ble_oxy"
	read_data(csv_column, sensor_id, member_id, ts_start, ts_end, limit, cursor, order, bearer)
	sensor_id="spo2_ble_bpm"
	read_data(csv_column, sensor_id, member_id, ts_start, ts_end, limit, cursor, order, bearer)

