import mysql.connector as mysql
from General_Functions import config


Connector = mysql.connect(**config)
Cursor = Connector.cursor()


query = '''
    UPDATE TBL_Device
        SET Device_Status = %s, Device_Bat_Level = %s,
            Device_Temp = %s, Device_HR = %s, Device_O2 = %s
        WHERE TIMEDIFF(CURRENT_TIMESTAMP(),
                    CONCAT(Device_Last_Updated_Date, ' ',
                    Device_Last_Updated_Time)) < "00:00:30";
'''
Device_Status = 'OFFLINE'
Device_Bat_Level = 0
Device_Temp = 0
Device_HR = 0
Device_O2 = 0
parameters = (Device_Status, Device_Bat_Level, Device_Temp, Device_HR, Device_O2)
Cursor.execute(query, parameters)
Connector.commit()
