import time
import json
from datetime import datetime
from twilio.rest import Client
import mysql.connector as mysql
from General_Functions import (
    config, dictfetchall
)

default = lambda obj: obj.isoformat() if isinstance(obj, datetime) else obj

def Get_Alert_Type(Alert_Code):
	Type = ''
	if Alert_Code == 1:
		Type = 'High Temperature'
	elif Alert_Code == 2:
		Type = 'Low Temperature'
	elif Alert_Code == 3:
		Type = 'High Oxygen'
	elif Alert_Code == 4:
		Type = 'Low Oxygen'
	elif Alert_Code == 5:
		Type = 'High Heart Rate'
	elif Alert_Code == 6:
		Type = 'Low Heart Rate'
	elif Alert_Code == 7:
		Type = 'Low Battery Level'
	elif Alert_Code == 8:
		Type = 'Breach'

	return Type



def Send_Notification():
	account_sid = 'AC94b551c5b69baf19b050d00055ecc79b'
	auth_token = '2884c8dcfed52921659f83bd9e945f72'

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = '''
	    SELECT * FROM TBL_Alert
	    WHERE TIMESTAMPDIFF(SECOND, Alert_Datetime, CURRENT_TIMESTAMP()) > %s AND
	          TIMESTAMPDIFF(SECOND, Alert_Datetime, CURRENT_TIMESTAMP()) < %s;    
	'''

	parameters = (30, 80)
	Cursor.execute(query, parameters)
	results = dictfetchall(Cursor)
	for row in results:
		Alert_Code = row['Alert_Code']
		Alert_Datetime = row['Alert_Datetime']
		Device_ID = row['Device_ID']

		query = '''
			SELECT * FROM TBL_User
				WHERE User_ID IN (
					SELECT User_ID FROM TBL_Wearer
						WHERE Wearer_ID IN (
							SELECT Wearer_ID FROM TBL_Device
								WHERE Device_ID = %s
						)
				)
		'''
		parameter = (Device_ID,)
		Cursor.execute(query, parameter)
		results_ = dictfetchall(Cursor)
		for row_ in results_:
			Phone_Nr = row_['Telephone_Number']
			User_Name = row_['User_Name']
			User_ID = row_['User_ID']

			query = '''
				SELECT * FROM TBL_Wearer
					WHERE User_ID = %s
			'''
			parameter = (User_ID,)
			Cursor.execute(query, parameter)
			results_tbl_wearer = dictfetchall(Cursor)

			for row3 in results_tbl_wearer:
				Wearer_Nick = row3['Wearer_Nick']
				Wearer_ID = row3['Wearer_ID']

				Alert_Type = Get_Alert_Type(int(Alert_Code))

			print(json.dumps({
				'Alert_Code': Alert_Code,
				'Alert_Type': Alert_Type,
				'Alert_Datetime': Alert_Datetime,
				'Telephone_Number': Phone_Nr,
				'User_ID': User_ID,
				'User_Name': User_Name,
				'Wearer_Nick': Wearer_Nick,
				'Wearer_ID': Wearer_ID
			}, indent=4, default=default))
			# f'Hi there, please check Wearer "{{1}}" with Wearer ID {{2}} is having "{{3}}", captured at {{4}}.'
			# message_template = f'Hi there, please check Wearer "{Wearer_Nick}" with Wearer ID {Wearer_ID} is having "{Alert_Type}", captured at {Alert_Datetime}.'

			f'Hi there, please check Wearer "{{1}}" with Wearer ID "{{2}}" is having "{{3}}", captured at {{4}}.'
			message_template = f'Hi there, please check Wearer "{Wearer_Nick}" with Wearer ID "{Wearer_ID}" is having "{Alert_Type}", captured at {Alert_Datetime}.'
			print(message_template)

			client = Client(account_sid, auth_token)

			message = client.messages \
				.create(
					from_='whatsapp:+17863056116',
					body=message_template,
		            # messaging_service_sid='MG62b696f0158a1b06e54cc849af789aa9', +6588328156  60143376615
		            to=f'whatsapp:{Phone_Nr}'
			)

			print(f'Notification sent successfully to {Phone_Nr}!')


Send_Notification()


def Testing():
	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query = 'SELECT * FROM TBL_Alert'
	Cursor.execute(query)
	results = dictfetchall(Cursor)
	for row in results:
		Alert_Code = row['Alert_Code']
		Alert_Datetime = row['Alert_Datetime']
		Device_ID = row['Device_ID']

		query = '''
			SELECT * FROM TBL_User
				WHERE User_ID IN (
					SELECT User_ID FROM TBL_Wearer
						WHERE Wearer_ID IN (
							SELECT Wearer_ID FROM TBL_Device
								WHERE Device_ID = %s
						)
				)
		'''
		parameter = (Device_ID,)
		Cursor.execute(query, parameter)
		results_ = dictfetchall(Cursor)
		for row_ in results_:
			Phone_Nr = row_['Telephone_Number']
			User_Name = row_['User_Name']
			User_ID = row_['User_ID']

			query = '''
				SELECT * FROM TBL_Wearer
					WHERE User_ID = %s
			'''
			parameter = (User_ID,)
			Cursor.execute(query, parameter)
			results_tbl_wearer = dictfetchall(Cursor)

			for row3 in results_tbl_wearer:
				Wearer_Nick = row3['Wearer_Nick']
				Wearer_ID = row3['Wearer_ID']

				Alert_Type = Get_Alert_Type(int(Alert_Code))

			print(json.dumps({
				'Alert_Code': Alert_Code,
				'Alert_Type': Alert_Type,
				'Alert_Datetime': Alert_Datetime,
				'Telephone_Number': Phone_Nr,
				'User_ID': User_ID,
				'User_Name': User_Name,
				'Wearer_Nick': Wearer_Nick,
				'Wearer_ID': Wearer_ID
			}, indent=4, default=default))
			# f'Hi there, please check Wearer "{{1}}" with Wearer ID "{{2}}" is having "{{3}}", captured at {{4}}.'
			# message_template = f'Hi there, please check User "{User_Name}" is having "{Alert_Type}", captured at {Alert_Datetime}'
			message_template = f'Hi there, please check Wearer Nickname "{Wearer_Nick}" with Wearer ID "{Wearer_ID}", is having "{Alert_Type}", captured at {Alert_Datetime}.'
			print(message_template)


# Testing()