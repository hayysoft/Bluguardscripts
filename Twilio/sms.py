
from twilio.rest import Client



account_sid = 'AC94b551c5b69baf19b050d00055ecc79b'
auth_token = '2884c8dcfed52921659f83bd9e945f72'
client = Client(account_sid, auth_token)

def SendWhatsapp(student_record=None,temperature_record=None,contact=None,url=None):
    
   #whatsappMsgBody=""" Student """+str(student_record[0][2])+""" """+str(student_record[0][3])+""" """ +str(student_record[0][4])+""" is having a fever of  """ +str(temperature_record[0][6]) + """C, please click on the link below to acknowledge. 
#
 #   """+str(url)+""""""
    whatsappMsgBody="Student "+str(student_record[0][3])+" "+str(student_record[0][4])+" " +str(student_record[0][5])+" "+"is having a fever of  " +str(temperature_record[0][6]) + " C, please click on the link below to acknowledge."+" \n\n"+str(url)
#sends whatsapp to the number
    print(whatsappMsgBody)
    message1 = client.messages.create(
                            
                            from_='whatsapp:+17863056116',
                            body=whatsappMsgBody,    
                            to="whatsapp:"+ contact 
                              
                          ) 

    print(message1)

def SendSms(student_record,temperature_record,contact,url):
    
    smsBody="Student "+str(student_record[0][3])+" "+str(student_record[0][4])+" " +str(student_record[0][5])+" "+" is having a fever of " +str(temperature_record[0][6]) + "\u2103" +". Temperature recorded as of " + str(temperature_record[0][7]) +" please click on the link below to acknowledge. "+"\n \n"+str(url)
    
    
    message = client.messages \
        .create(
            body=smsBody  ,
            messaging_service_sid='MG7747d061d8c7ea06b781c8db64a1842f',
            to=contact
        )
    

    print(message.sid)
