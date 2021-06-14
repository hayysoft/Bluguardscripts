import datetime
import mysql.connector as mysql


config = {
    'host': 'bluguardprod1.mysql.database.azure.com',
    'user': 'bluguardprod1@bluguardprod1',
    'password': 'DoNotHack2021!',
    'database': 'bluguarddb',
    'client_flags': [mysql.ClientFlag.SSL],
    'ssl_ca': '',
}



def Create_PK(ID):
    """Creates a primary_key for a given table
    with ID parameter specifying the initials of the table name

    parameter
    ---------
        Create_PK("IN")
            >> IN2021-06-10T12:53:45.513819
    """
    return ID + 'T'.join(str(datetime.datetime.now()).split(' '))



def Validate_Raw_Data_Length(device_type, raw_data_length):
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Raw_Data_Length FROM TBL_Device_Raw_Length
        WHERE Device_Type = %s AND Raw_Data_Length = %s
    '''
    parameters = (device_type, len(raw_data_length))
    Cursor.execute(query, parameters)
    results = Cursor.fetchall()
    # print(results)
    return True if len(results) != 0 else False
    # if results[0][0] != 0:
    #     return True

    # return False

# 0201060AFF34126A016601486253

# print(Validate_Raw_Data_Length('HSWB002', '0201060503F5FEE7FE09FF000006CB8867030205FFCDAB0000'))
