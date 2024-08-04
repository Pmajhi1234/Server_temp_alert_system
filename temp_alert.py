from boltiot import Sms,Email, Bolt
import json, time
import os


API_KEY = os.environ['API_KEY'] # Bolt API Key
DEVICE_ID = os.environ['DEVICE_ID']# Bolt device ID
SID = os.environ['SID']# Twilio account SID
AUTH_TOKEN = os.environ['AUTH_TOKEN']# Twilio auth token
TO_NUMBER= os.environ['TO_NUMBER']# Recipient's number
FROM_NUMBER= os.environ['FROM_NUMBER']#The number that sends the SMS

MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY'] # Mailgun API Key
SANDBOX_URL= os.environ['SANDBOX_URL'] # Mailgun sandbox URL
SENDER_EMAIL = os.environ['SENDER_EMAIL'] # Sender's email
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL'] # Recipient's email where messeges will be sent
maximum_limit = 30  #Maximum Temperature Limit


mybolt = Bolt(API_KEY, DEVICE_ID) # Create a new object to connect to the Bolt cloud
sms = Sms(SID, AUTH_TOKEN, TO_NUMBER, FROM_NUMBER) # Create a new object to send SMS
mailer = Email(MAILGUN_API_KEY,SANDBOX_URL,SENDER_EMAIL, RECIPIENT_EMAIL) # Create a new object to send Email


while True: 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0')  # Read the sensor value
    data = json.loads(response)         # Convert the JSON response into a Python dictionary
    print("Sensor value is: " + str(data['value']))
    try: 
        sensor_value = int(data['value']) # Convert the sensor value into an integer
        temperatue=(100*sensor_value)/1024 # Convert the sensor value into a temperature
        print("Temperature is: " + str(temperatue))
        print(end='\n')
        if temperatue > maximum_limit:
            print("Temperature crossed the thresold limit 30 degree.")
            print("Switching on the Buzzer")
            mybolt.digitalWrite('1', 'HIGH')
            time.sleep(5)
            mybolt.digitalWrite('1','LOW')
            print(end='\n')
            print("Making request to Twilio to send Sms")
            response1 = sms.send_sms("Warning,The Current temperature sensor value is " +str(temperatue)) # Send an SMS to the number and store the resonse in variable
            print(end='\n')
            print("Response received from Twilio is: " + str(response1))
            print("Status of SMS at Twilio is :" + str(response1.status))
            time.sleep(5)
            print(end='\n')
            print(end='\n')
        
            print("Making request to Mail Gun to send Email")
            print(end='\n')
            response2 = mailer.send_email("Alert", "Warning,The Current temperature sensor value is " +str(temperatue))   # Send an Email to the recipient and store the resonse in variable
            response_text = json.loads(response2.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
        
          
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    
    print("Wait for 30 sec.")
    print(end='\n')
    time.sleep(30)

