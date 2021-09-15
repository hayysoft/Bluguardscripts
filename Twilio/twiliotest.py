# Download the helper library from https://www.twilio.com/docs/python/install
from datetime import datetime
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC94b551c5b69baf19b050d00055ecc79b'
auth_token = '2884c8dcfed52921659f83bd9e945f72'
client = Client(account_sid, auth_token)

messages = client.messages.list(
                               date_sent=datetime.now(),
                               from_='+14155238886',
                               to='+60143376615',
                               limit=20
                           )

for record in messages:
    print(messages)
