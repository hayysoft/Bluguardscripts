import json
import time
import datetime as dt
from datetime import datetime
import requests
import mysql.connector as mysql
from General_Functions import config


"""
{
    “subject_id”: [int],
    “device_id”: [string],
    “datetime”: [int],
    “fever”: [int],
    “breathing”: [int],
    “coughing”: [int],
    “eating”: [int],
    “tiredness”: [int],
    “doctor”: [int],
    “photo”: [varbinary], *For CQ01 & CQ02, other devices use 0
    “cough_sound”: [varbinary], *For CQ01 & CQ02, other devices use 0
}
"""


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]



def Get_Device_ID_For_Symptom_Check_In(Wearer_ID):
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Device_ID,
            CURRENT_TIMESTAMP() AS Datetime,
            Device_Tag
        FROM TBL_Device
        WHERE Wearer_ID = %s
    '''
    parameter = (Wearer_ID,)
    Cursor.execute(query, parameter)
    results = Cursor.fetchall()
    try:
        Device_ID = results[0][0]
        Datetime = results[0][1]
        Device_Tag = results[0][2]
    except Exception:
        return None, None, None

    return Device_ID, Datetime, Device_Tag


default = lambda obj: obj.isoformat() if isinstance(obj, datetime) else obj


def Check_In_Symptoms():
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    global Subject_ID

    query = '''
        SELECT Daily_Survey_ID, Daily_Survey_Q2_Y1,
               Daily_Survey_Q2_Y2, Daily_Survey_Q2_Y3,
               Daily_Survey_Q2_Y4, Daily_Survey_Q2_Y5,
               Wearer_ID
        FROM tbl_daily_survey
        WHERE Sent_To_Crest = %s
    '''
    parameter = (0,)
    Cursor.execute(query, parameter)
    results = Cursor.fetchall()
    data = [
        {
            'subject_id': 0,
            'device_id': 0,
            'datetime': '',
            'fever': row[1],
            'breathing': row[2],
            'coughing': row[3],
            'eating': row[4],
            'tiredness': row[5],
            'doctor': 1,
            'photo': 0,
            'cough_sound': 0
        } for row in results
    ]
    Wearer_IDs = [row[5] for row in results]
    Survey_Ids = [row[0] for row in results]

    Device_IDs = []
    # for index, wearer_id in enumerate(Wearer_IDs):
    for row, wearer_id in zip(data, Wearer_IDs):
        results = Get_Device_ID_For_Symptom_Check_In(wearer_id)
        Device_ID = results[0]
        Datetime = results[1]
        row['device_id'] = Device_ID
        row['datetime'] = Datetime

        Device_Tag = results[2]
        query = '''
            SELECT Patient_Tag AS subject_id
            FROM TBL_Crest_Patient
            WHERE Device_Tag = %s AND
                  Patient_Discharged = %s
        '''
        parameter = (Device_Tag, 0)
        Cursor.execute(query, parameter)
        Patient_ID = dictfetchall(Cursor)
        try:
            Subject_ID = int(Patient_ID[0]['subject_id'])
            print(f'Subject_ID = {Subject_ID}')
            data[index].update({
                'subject_id': Subject_ID
            })
        except LookupError:
            row.update({
                'subject_id': 1
            })

        try:
            datetime_val = int(row['datetime'].timestamp())
            row['datetime'] = datetime_val
        except AttributeError:
            pass


        print(json.dumps(row, default=default, indent=4))
        url = 'http://dhri.crc.gov.my/patient/checkin_symptoms'
        response = requests.post(url, data=json.dumps(row), headers={
            'Authorization': 'Token 7c1899d4eab19ad83c585390c84586f3e385610c',
            'Content-Type': 'application/json'
        })

        print(f'Response: {response.json()}')
        print(f'Reason: {response.reason}')

        if response.status_code == 200:
            print(f'Status:{response.status_code}')
            query = '''
                UPDATE TBL_Crest_Patient
                SET Last_Survey_Datetime = CURRENT_TIMESTAMP()
                WHERE Patient_Tag = %s
            '''

            Subject_ID_query = '''
                SELECT Patient_Tag AS subject_id
                FROM TBL_Crest_Patient
                WHERE Wearer_ID = %s AND
                      Patient_Discharged = %s
            '''
            parameter = (wearer_id, 0)
            Cursor.execute(Subject_ID_query, parameter)
            Patient_ID = dictfetchall(Cursor)
            try:
                Subject_ID = int(Patient_ID[0]['subject_id'])
                parameter = (Subject_ID,)
                print(f'Subject_ID = {Subject_ID}')
                Cursor.execute(query, parameter)
                Connector.commit()
            except LookupError:
                pass







    # for row in data:
    #     try:
            # datetime_val = int(row['datetime'].timestamp())
            # row['datetime'] = datetime_val
    #     except AttributeError:
    #         pass




        # After successfull POST request
        # UPDATED Last_Survey_Datetime inside tbl_patient
        #

        # if response.status_code == 200:
        #     for Survey_Id in Survey_Ids:
        #         query = '''
        #             UPDATE TBL_Daily_Survey
        #             SET Sent_To_Crest = %s AND
        #                 Daily_Survey_ID = %s
        #         '''
        #         parameters = (1, Survey_Id)
        #         Cursor.execute(query, parameters)
        #         Connector.commit()


Check_In_Symptoms()


# data = {
#     "subject_id": 1,
#     "device_id": "DVC2021-05-04T15:49:27.649073",
#     "datetime": 1623787941,
#     "fever": 0,
#     "breathing": 0,
#     "coughing": 0,
#     "eating": 0,
#     "tiredness": 0,
#     "doctor": 1,
#     "photo": 0,
#     "cough_sound": 0
# }



# url = 'http://dhri.crc.gov.my/patient/checkin_symptoms'
# data = json.dumps(data)
# response = requests.post(url, data=data, headers={
#     'Authorization': 'Token 7c1899d4eab19ad83c585390c84586f3e385610c',
#     'Content-Type': 'application/json'
# })
# print(f'Status:{response.status_code}')
# print(f'Response: {response.json()}')
# print(f'Reason: {response.reason}')
