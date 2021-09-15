import os
import time
from twilio.rest import Client
import mysql.connector as mysql
from General_Functions import (
    config, dictfetchall
)


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC94b551c5b69baf19b050d00055ecc79b'
auth_token = '2884c8dcfed52921659f83bd9e945f72'

# Connector = mysql.connect(**config)
# Cursor = Connector.cursor()

# query = '''
#     SELECT * FROM TBL_Gateway
#     WHERE TIMESTAMPDIFF(SECOND, Last_Updated_Time, CURRENT_TIMESTAMP()) > %s AND
#           TIMESTAMPDIFF(SECOND, Last_Updated_Time, CURRENT_TIMESTAMP()) < %s;    
# '''
# parameters = (30, 80)
# Cursor.execute(query, parameters)
# results = dictfetchall(Cursor)

if True: #len(results) != 0:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             from_='whatsapp:+17863056116',
             # body=f'"Hi Nela, this is to inform that the Main_Program went down at {time.ctime()}"',
             body=f'Hi Nela, this is to inform that Gateway MAC FEFDD727C6F5 went OFFLINE at {time.ctime()}.',
             # messaging_service_sid='MG62b696f0158a1b06e54cc849af789aa9', +6588328156  60143376615
             to='whatsapp:+60143376615'
         )

    print(message)
    print('Notification sent successfully!')
else:
    print('Notification not sent!')