import mysql.connector as mysql


config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    # 'client_flags': [mysql.ClientFlag.SSL],
    # 'ssl_ca': 'C',
    'port': '3306'
}

Connector = mysql.connect(**config)
Cursor = Connector.cursor()

query = '''UPDATE TBL_Device
        SET Device_Status = %s, Device_Bat_Level = %s,
            Device_Temp = %s, Device_HR = %s, Device_O2 = %s
        WHERE TIMEDIFF(CURRENT_TIMESTAMP(),
                    TIMESTAMP(CONCAT(Device_Last_Updated_Date, ' ',
                    Device_Last_Updated_Time))) > TIME("00:00:10");
'''
parameters = ('OFFLINE', 0, 0, 0, 0)

# query = '''UPDATE TBL_Device
#            SET Device_Bat_Level = %s
#            WHERE TIMEDIFF(CURRENT_TIMESTAMP(),
#                     CONCAT(Device_Last_Updated_Date, ' ',
#                     Device_Last_Updated_Time)) > TIME("00:00:10");
# '''
# parameters = (5,)


Cursor.execute(query, parameters)
Connector.commit()

