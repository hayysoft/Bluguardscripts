#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 18:31:43
"""

from datetime import datetime
from read_json import ManageJson
from Update_DB_LastRead_Details import MySQLConnector
import json


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

def Process_RawData(raw_data, type_):
	"""Extracts temperature, heart_rate, spo2, batlevel
	from raw data based on the device type
	"""
	if type_ == 'Unknown': # and len(raw_data) == 30:
		print(f'raw_data length: {len(raw_data)}')
		temperature = Get_Vital_Temp(raw_data, 20, 24)
		heart_rate = Get_Vital_Heart_Rate(raw_data, 24, 26)
		spo2 = Get_Vital_Spo2(raw_data, 26, 28)
		batlevel = Get_Status_Batlevel(raw_data, 28, 30)
		print(f'| temperature = {temperature}')
		print(f'| heart_rate = {heart_rate}')
		print(f'| spo2 = {spo2}')
		print(f'| batlevel = {batlevel}')
		data = {
			'temp': temperature,
			'heart_rate': heart_rate,
			'spo2': spo2,
			'batlevel': batlevel
		}
		return data
	elif type_ == 'HSWB001':
		pass

def Get_Mqtt_Data(data_from_gateway):
	macs = {}
	x = 1
	data_to_save = []
	for data in data_from_gateway:
		keys = list(data.keys())
		for key in keys:
			if key == 'mac':
				macs[f'mac_{x}'] = data['mac']
				x += 1

		for mac_key in list(macs.keys())[1:]:
			for key in keys:
				if key == 'rawData':
					data_ = Process_RawData(data[key], data['type'])
					try:
						data_['timestamp'] = data['timestamp']
						timestamp = data['timestamp'].split('T')
						date = timestamp[0]
						# time = datetime[1].split('.')[0]
						time = datetime.now().time()
						data_['date'] = f'{date}'
						data_['time'] = f'{time}'
						data_['gateway_mac'] = macs['mac_1']
						data_['bleName'] = data["bleName"]
						data_['rssi'] = data['rssi']
						data_.update({'device_mac': macs[mac_key]})
					except TypeError:
						pass

					json_manager = ManageJson()
					data_from_json = json_manager.load_json()
					data_from_json.append(data_)
					json_manager.save_json(data_from_json)

					with open('C:/Users/hayysoft/Documents/Scripts/interview/media/raw_data.json') as fp:
						data_to_db = json.loads(fp.read())

					# connector = MySQLConnector('bluguarddb')
					# connector.add_new_data(data_to_db)

					print(json.dumps(data_, indent=4))

					print(f'| rawData length: {len(data[key])}')
			print(f'| {key}: {Extract_MetaData(data, key)}')

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





