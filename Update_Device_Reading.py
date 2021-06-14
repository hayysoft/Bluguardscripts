import datetime
import mysql.connector as mysql
from read_json import ManageJson


config = {
    'host': 'bluguardprod1.mysql.database.azure.com',
    'user': 'bluguardprod1@bluguardprod1',
    'password': 'DoNotHack2021!',
    'database': 'bluguarddb',
    'client_flags': [mysql.ClientFlag.SSL],
    'ssl_ca': '',
}


def Clear_Raw_Data_Json():
    with open('C:/Users/hayysoft/Documents/Scripts/interview/media/raw_data.json', 'w') as fp:
        fp.write('[]')



def Update_Device():
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    file_reader = ManageJson()
    data = file_reader.load_json()
    data_to_save = {}
    for row in data:
        data_to_save[row['device_mac']] = row


    for row in data_to_save.items():
        row_data = row[1]
        object_update = ManageJson(row[0])
        object_update_data = object_update.load_json()
        object_update_data.append(row_data)
        object_update.save_json(object_update_data)
        print(row_data)

        query = '''
            UPDATE TBL_Device
            SET Device_Last_Updated_Date = %s,
                Device_Last_Updated_Time = %s,
                Device_Temp = %s,
                Device_HR = %s,
                Device_O2 = %s,
                Device_Bat_Level = %s
        '''
        Device_Date = row_data['date']
        Device_Time = row_data['time']
        Device_Temp = row_data['temp']
        Device_HR = row_data['heart_rate']
        Device_O2 = row_data['spo2']
        Device_RSSI = row_data['rssi']
        Device_Bat_Level = row_data['batlevel']
        parameters = (Device_Date, Device_Time,
                      Device_Temp, Device_HR,
                      Device_O2, Device_Bat_Level)
        Cursor.execute(query, parameters)
        Connector.commit()



Update_Device()
Clear_Raw_Data_Json()
print('File cleared successfully!')

