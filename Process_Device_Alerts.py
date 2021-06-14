import os
import json
import mysql.connector as mysql
from General_Functions import Create_PK


config = {
    'host': 'bluguardprod1.mysql.database.azure.com',
    'user': 'bluguardprod1@bluguardprod1',
    'password': 'DoNotHack2021!',
    'database': 'bluguarddb',
    'client_flags': [mysql.ClientFlag.SSL],
    'ssl_ca': '',
}


def Insert_Alert(Alert_Code, Alert_Reading):
    query = '''
        INSERT INTO TBL_Alert
            (Alert_ID, Alert_Code, Alert_Reading,
             Alert_Date, Alert_Time, Device_ID)
            VALUES(%s, %s, %s, CURDATE(), CURTIME(), %s)
    '''
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    parameters = (Create_PK('ALT'), Alert_Code, Alert_Reading, 'DVC2021-06-10T03:29:15.660760')
    Cursor.execute(query, parameters)
    Connector.commit()


def Check_Highest_Score(Type, low_attr, high_attr, attr_value):
    if Type == 'temp':
        if high_attr == 5:
            Insert_Alert(1, attr_value)
            print('Insert Alert_Code 1')
        elif low_attr == 5:
            Insert_Alert(2, attr_value)
            print('Insert Alert_Code 2')
    elif Type == 'heart_rate':
        if high_attr == 5:
            Insert_Alert(3, attr_value)
            print('Insert Alert_Code 3')
        elif low_attr == 5:
            Insert_Alert(4, attr_value)
            print('Insert Alert_Code 4')
    elif Type == 'spo2':
        if high_attr == 5:
            Insert_Alert(5, attr_value)
            print('Insert Alert_Code 5')
        elif low_attr == 5:
            Insert_Alert(6, attr_value)
            print('Insert Alert_Code 6')


def Process_Score(Type, low_attr, high_attr, attr_value):
    if Type == 'temp':
        if attr_value < 34:
            low_attr += 1
        elif attr_value > 37:
            high_attr += 1
    elif Type == 'heart_rate':
        if attr_value < 40:
            low_attr += 1
        elif attr_value > 100:
            high_attr += 1
    elif Type == 'spo2':
        if attr_value < 80:
            low_attr += 1
        elif attr_value > 98:
            high_attr += 1

    return (low_attr, high_attr, attr_value)


def Process_Individual_File(filename):
    print(f'filename = {filename}')
    with open(filename) as fp:
        data = json.loads(fp.read())

    LtempScore, HtempScore, LastTemp = 0, 0, 0
    LhrScore, HhrScore, LastHR = 0, 0, 0
    L0score, Ho2Score, LastO2 = 0, 0, 0

    for row in data:
        LtempScore, HtempScore, LastTemp = Process_Score('temp', LtempScore,
                                                         HtempScore, row['temp'])
        LhrScore, HhrScore, LastHR = Process_Score('heart_rate', LhrScore,
                                                   HhrScore, row['heart_rate'])
        L0score, Ho2Score, LastO2 = Process_Score('spo2', L0score,
                                                  Ho2Score, row['spo2'])

    print(f'LtempScore = {LtempScore}, HtempScore = {HtempScore}')
    print(f'LastTemp = {LastTemp}')
    print(f'LhrScore = {LhrScore}, HhrScore = {HhrScore}')
    print(f'LastHR = {LastHR}')
    print(f'L0score = {L0score}, Ho2Score = {Ho2Score}')
    print(f'LastO2 = {LastO2}')

    Check_Highest_Score('temp', 5, HtempScore, LastTemp)
    Check_Highest_Score('heart_rate', LtempScore, 5, LastHR)
    Check_Highest_Score('spo2', 5, HtempScore, LastO2)


os.chdir('C:/Users/hayysoft/Documents/Scripts/interview/media')
from glob import glob
files = glob("*.json")
files = [file for file in files if len(file) == len(file) == 17]

for file in files:
    Process_Individual_File(file)


