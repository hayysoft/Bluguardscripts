import json
from read_json import ManageJson
from Update_DB_LastRead_Details import MySQLConnector
from Clear_TBL_Incoming import Clear_TBL_Incoming


def Clear_Raw_Data():
	"""Clear data inside raw_data after appending in the
	respective band_mac files. This function is called every 
	60 seconds.
	"""
	
	# with open('D:/Scripts/interview/media/raw_data.json') as fp:
	# 	data = json.loads(fp.read())

	# connector = MySQLConnector('bluguarddb')
	# connector.add_new_data(data)

	with open('D:/Scripts/interview/media/raw_data.json', 'w') as fp:
		fp.write('[]')



def Read_And_Append():
	"""Reads and loops through the data inside raw_data.json. 
	For every loop save the data in a file named after
	the band_mac, respectively.
	-------------
	"""
	json_manager = ManageJson()
	data_from_json = json_manager.load_json()
	for row in data_from_json:
		try:
			json_manager_ = ManageJson(row['band_mac'])
			json_manager_data = json_manager_.load_json()
			json_manager_data.append(row)
			json_manager_.save_json(json_manager_data)
		except TypeError:
			pass


"""
	This file is used to generate Update_Device_Reading.exe
	for setting up the scheduler.

	Instructions for generating Update_Device_Reading.exe can
	be found at https://datatofish.com/executable-pyinstaller/
"""

print('From scheduler...')
Read_And_Append() 
Clear_Raw_Data()




