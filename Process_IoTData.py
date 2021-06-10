#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 18:31:43
"""

import json
from datetime import datetime
from read_json import ManageJson
import mysql.connector as mysql
from General_Functions import (
	Create_PK, Validate_Raw_Data_Length
)




config = {
    'host': 'bluguardprod1.mysql.database.azure.com',
    'user': 'bluguardprod1@bluguardprod1',
    'password': 'DoNotHack2021!',
    'database': 'bluguarddb',
    'client_flags': [mysql.ClientFlag.SSL],
    'ssl_ca': '',
}


def Extract_MetaData(data, key):
	"""Returns the value for the given inside
	data dictionary."""
	return data.get(key)


def Start_Process_IoTData(data_from_gateway):
	pass


def Convert_Hex_To_Decimal(hex_data):
	"""Converts hexadecimal data to decimal.
	Returns decimal data"""
	try:
		decimal_data = int(hex_data, 16)
		return decimal_data
	except (ValueError, TypeError):
		return ''

def Get_Vital_Temp(raw_data,
				   temp_startpos,
				   temp_endpos):
	"""Extracts temperature in hexadecimal and
	returns the temperature in decimal from the rawdata.

	Parameters
	-----------------
	raw_data:		 the raw data to be extracted from
	temp_startpos:	 is the starting position of the temperature
					 in raw data.
	temp_endpos:	 is the ending position (not inclusive) of the
					 temperature in raw data.

	Returns
	------
	temperature:     temperature converted to decimal from hexadecimal

	Exmple:
		>> Get_Vital_Temp('0EFF3412CFE2BBA5F0860301420016',
						20, 24)
	"""
	temp_ = raw_data[temp_startpos:temp_endpos]
	temp_ = temp_[2:4] + temp_[0:2]
	print(f'| raw_temp = {temp_}')
	temperature = Convert_Hex_To_Decimal(temp_) / 10
	return temperature

def Get_Vital_Heart_Rate(raw_data,
						 heart_rate_startpos,
						 heart_rate_endpos):
	"""Extracts and returns the heartrate from the rawdata.

	Implementation of this function follows the same
	logic as the Get_Vital_Temp function above.
	"""
	heart_rate_ = raw_data[heart_rate_startpos:heart_rate_endpos]
	print(f'| raw_heart_rate = {heart_rate_}')
	return Convert_Hex_To_Decimal(heart_rate_)

def Get_Vital_Spo2(raw_data,
				   spo2_startpos,
				   spo2_endpost):
	"""Extracts and returns the spo2 from the rawdata.

	Implementation of this function follows the same
	logic as the Get_Vital_Temp function above.
	"""
	spo2 = raw_data[spo2_startpos:spo2_endpost]
	print(f'| raw_spo2 = {spo2}')
	return Convert_Hex_To_Decimal(spo2)

def Get_Status_Batlevel(raw_data,
				 		batlevel_startpos,
				 		batlevel_endpost):
	"""Extracts and returns the spo2 from the rawdata.

	Implementation of this function follows the same
	logic as the Get_Vital_Temp function above.
	"""
	batlevel = raw_data[batlevel_startpos:batlevel_endpost]
	print(f'| raw_batlevel = {batlevel}')
	return Convert_Hex_To_Decimal(batlevel)


def Get_Device_Type(Device_Mac):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	query = '''
		SELECT Device_Type FROM tbl_device
		WHERE Device_Mac = %s
	'''
	parameter = (Device_Mac,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()
	try:
		results = results[0][0]
	except IndexError:
		results = []
	return results


def HSWB001_Process_Data(raw_data):
	temperature = raw_data[16:18] + raw_data[14:16]
	temperature = int(temperature, 16) / 10
	heart_rate = Get_Vital_Heart_Rate(raw_data, 22, 24)
	spo2 = Get_Vital_Spo2(raw_data, 24, 26)
	batlevel = Get_Status_Batlevel(raw_data, 26, 28)
	vital_data = {
		'temp': temperature,
		'heart_rate': heart_rate,
		'spo2': spo2,
		'batlevel': batlevel
	}
	return vital_data


def Process_RawData(raw_data, device_type):
	"""Extracts temperature, heart_rate, spo2, batlevel
	from raw data based on the device type
	"""
	if device_type == 'HSWB001':
		data = HSWB001_Process_Data(raw_data)
		return data
	elif device_type == 'HSWB002' and len(raw_data) == 56:
		try:
			temperature = raw_data[40:42] + raw_data[38:40]
			temperature = int(temperature, 16) / 100
			heart_rate = Get_Vital_Heart_Rate(raw_data, 52, 54)
		except ValueError:
			pass

		data = {
			'temp': temperature,
			'heart_rate': heart_rate,
			'spo2': 0,
			'batlevel': 0
		}
		return data


def Extract_Device_Mac(data):
	device_macs = []
	for key, value in data.items():
		if key == 'mac':
			if data.get('type') != 'Gateway':
				device_macs.append(value)

	return device_macs


def Populate_MetaData(data, gateway_mac):
	Metadata_ = {}
	Metadata_['timestamp'] = data['timestamp']
	timestamp = data[ 'timestamp'].split('T')
	date = timestamp[0]
	time = datetime.now().time()
	Metadata_['date']  = f'{date}'
	Metadata_['time'] = f'{time}'
	device_macs = Extract_Device_Mac(data)
	Metadata_['gateway_mac'] = gateway_mac
	Metadata_['device_mac'] = data['mac']
	Metadata_['bleName'] = data["bleName"]
	Metadata_['rssi'] = data['rssi']

	return Metadata_



def Process_Quarentine_Band(data, gateway_mac, device_mac, Device_Type):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	query = '''
		SELECT COUNT(*) FROM TBL_Device
		WHERE Device_Mac = %s
	'''
	parameter = (device_mac,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()
	if results[0][0] != 0:
		populate_metadata = Populate_MetaData(data, gateway_mac)
		# print('*' * 10, 'HSWB004', '*' * 10)
		# print(populate_metadata)

		query = '''
			INSERT INTO TBL_Incoming
			(Incoming_ID, Incoming_Device_Mac, Incoming_Gateway_Mac, Incoming_Temp, Incoming_O2,
			 Incoming_HR, Incoming_Date, Incoming_Time, Device_Status,
			 Incorrect_Data_Flag, Device_Bat_Level)
			 VALUES (%s, %s, %s, %s, %s, %s, %s, 'ONLINE", %s, %s)
		'''
		parameters = (Create_PK("IN"), populate_metadata['device_mac'], populate_metadata['gateway_mac]'],
					  0, 0, 0, populate_metadata['date'], populate_metadata['time'], 0, 0)
		Cursor.execute(query, parameters)
		Connector.commit()



def Filter_Message(validated, Device_Type, Raw_Data, data, gateway_mac):
	# print(data)
	populate_metadata = Populate_MetaData(data, gateway_mac)

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''INSERT INTO TBL_Incoming
			(Incoming_ID, Incoming_Device_Mac, Incoming_Gateway_Mac,
			Incoming_Temp, Incoming_O2, Incoming_HR, Incoming_Date,
			Incoming_Time, Device_Status, Incorrect_Data_Flag, Device_Bat_Level)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, "ONLINE", %s, %s)
	'''

	if validated == False:
		json_manager = ManageJson('incorrect_raw_data')
		data_from_json = json_manager.load_json()
		populate_metadata.update({
			'rawData': Raw_Data
		})
		data_from_json.append(populate_metadata)
		json_manager.save_json(data_from_json)
		# print('*' * 10, 'INCORRECT_DATA', '*' * 10)
		# print(populate_metadata)

		parameters = (Create_PK("IN"), populate_metadata['device_mac'], populate_metadata['gateway_mac'],
				  	  0, 0, 0, populate_metadata['date'], populate_metadata['time'], 1, 0)
	elif validated == True:
		# Data is correct
		populate_vitaldata = Process_RawData(Raw_Data, Device_Type)
		populate_vitaldata.update(populate_metadata)
		json_manager = ManageJson()
		data_from_json = json_manager.load_json()
		data_from_json.append(populate_vitaldata)
		json_manager.save_json(data_from_json)
		# print('*' * 10, 'CORRECT_DATA', '*' * 10)
		# print(populate_vitaldata)

		parameters = (Create_PK("IN"), populate_vitaldata['device_mac'], populate_vitaldata['gateway_mac'],
					  populate_vitaldata['temp'], populate_vitaldata['spo2'],
					  populate_vitaldata['heart_rate'], populate_vitaldata['date'],
					  populate_vitaldata['time'], 0, populate_vitaldata['batlevel'])

	Cursor.execute(query, parameters)
	Connector.commit()


	query = '''UPDATE TBL_Device
				SET Device_Status = 'OFFLINE', Device_Bat_Level = %s,
					Device_Temp = %s, Device_HR = %s, Device_O2 = %s
				WHERE TIMEDIFF(CURRENT_TIMESTAMP(),
								CONCAT(Device_Last_Updated_Date, ' ',
								Device_Last_Updated_Time)) > "00:00:10";
	'''
	parameters = (0, 0, 0, 0)
	Cursor.execute(query, parameters)
	Connector.commit()

	query = '''UPDATE TBL_Device
				SET Device_Bat_Level = %s,
					Device_Temp = %s,
					Device_HR = %s, Device_O2 = %s
				WHERE Device_Status = %s OR Incorrect_Data_Flag = %s
	'''
	parameters = (0, 0, 0, 0, 'OFFLINE', 1)
	Cursor.execute(query, parameters)
	Connector.commit()
	print('Filter_Message function executed successfully!')



def Get_Mqtt_Data(data_from_gateway):
	gateway_mac = data_from_gateway[0].get('mac')

	macs = {}
	x = 1
	data_to_save = []
	for data in data_from_gateway:
		print(data)
		keys = list(data.keys())
		for key in keys:
			if key == 'mac':
				macs[f'mac_{x}'] = data['mac']
				x += 1

		Device_Type = Get_Device_Type(data['mac'])
		if Device_Type == 'HSWB004':
			Process_Quarentine_Band(data, gateway_mac, data['mac'], Device_Type)

		for mac_key in list(macs.keys())[1:]:
			for key in keys:
				if key == 'rawData':
					try:
						results = Validate_Raw_Data_Length(Device_Type, data['rawData'])
						Filter_Message(results, Device_Type, data['rawData'], data, gateway_mac=gateway_mac)
					except TypeError:
						pass

	print('\n')



#def Get_Blename(data_from_gateway):
	"""Functionality for this funcion is achieved inside
	Get_Mqtt_Data
	"""
#	pass

#def Get_Band_Details(xml_file):
	"""Functionality for this funcion is achieved inside
	Get_Mqtt_Data
	"""
#	pass


#def Get_Raw_Data(data_from_gateway):
	"""Functionality for this funcion is achieved inside
	Get_Mqtt_Data
	"""
#	pass


#def Get_Gateway_Mac(raw_data):
	"""Functionality for this funcion is achieved inside
	Get_Mqtt_Data
	"""
#	pass

#def Get_Type(raw_data):
	"""Functionality for this funcion is achieved inside
	Get_Mqtt_Data
	"""
#	pass


#def Get_RSSI(raw_data):
	"""Functionality for this funcion is achieved inside
	Get_Mqtt_Data
	"""
#	pass

#def	Get_Status_BandMac(raw_data,
#				gateway_startpos,
#				gateway_endpos):
	"""Functionality for this funcion is achieved inside
	Get_Mqtt_Data
	"""
#	pass





