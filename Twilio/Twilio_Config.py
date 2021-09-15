import os
import time
from random import randint
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC94b551c5b69baf19b050d00055ecc79b'
auth_token = '2884c8dcfed52921659f83bd9e945f72'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         from_='whatsapp:+17863056116',
         body=f'"Hi Nela, this is to inform that the Main_Program went down at {time.ctime()}"',
         # messaging_service_sid='MG62b696f0158a1b06e54cc849af789aa9',
         to='whatsapp:+60143376615'
     )

print(message)