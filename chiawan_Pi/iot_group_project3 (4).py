import mysql.connector
import serial
import time
import datetime
import signal
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

arduino = serial.Serial('/dev/ttyACM1', 9600)

db_config = {
    'user': 'pi',
    'password': 'pipipi',
    'host': 'localhost',
    'database': 'smart_classroom_system_db'
}

# AWS IoT certificate-based connection
myMQTTClient = AWSIoTMQTTClient("MyRPI")
myMQTTClient.configureEndpoint("a28tye8o84qif9-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert/AmazonRootCA1.pem", "/home/pi/cert/7bd0986fe2b8f6c0abd240f445d91bc25288566c690afe921835728a37edd781-private.pem.key", "/home/pi/cert/7bd0986fe2b8f6c0abd240f445d91bc25288566c690afe921835728a37edd781-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) 


# Signal handler for graceful exit
def signal_handler(signal, frame):
    print("Exiting...")
    myMQTTClient.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Function to fetch the latest data from MySQL tables
def fetch_latest_data_from_tables():
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the latest data from electricityLog table
        query1 = "SELECT * FROM electricityLog ORDER BY id DESC LIMIT 1"
        cursor.execute(query1)
        electricity_data = cursor.fetchall()
        
        # Assign electricityLog column data to variables
        if electricity_data:
            electricity_status = electricity_data[0][1]
            electricity_date = electricity_data[0][2]
            # Add more variables as per the columns in the electricityLog table
        
        # Fetch the latest data from lightingLog table
        query2 = "SELECT * FROM lightingLog ORDER BY id DESC LIMIT 1"
        cursor.execute(query2)
        lighting_data = cursor.fetchall()

        # Assign lightingLog column data to variables
        if lighting_data:
            lighting_status = lighting_data[0][1]
            lighting_date = lighting_data[0][2]
            # Add more variables as per the columns in the lightingLog table

        # Fetch the latest data from airCondLog table
        query3 = "SELECT * FROM airCondLog ORDER BY id DESC LIMIT 1"
        cursor.execute(query3)
        air_cond_data = cursor.fetchall()

        # Assign airCondLog column data to variables
        if air_cond_data:
            air_cond_status = air_cond_data[0][1]
            air_cond_date = air_cond_data[0][2]
            # Add more variables as per the columns in the airCondLog table

        # Fetch the latest data from punishmentTriggeredLog table
        query4 = "SELECT * FROM punishmentTriggeredLog ORDER BY id DESC LIMIT 1"
        cursor.execute(query4)
        punishment_data = cursor.fetchall()

        # Assign punishmentTriggeredLog column data to variables
        if punishment_data:
            punishment_date = punishment_data[0][1]
            # Add more variables as per the columns in the punishmentTriggeredLog table
            
        # Fetch the latest data from electricityLog table
        query1 = "SELECT * FROM sensorValue ORDER BY id DESC LIMIT 1"
        cursor.execute(query1)
        sensor_data = cursor.fetchall()
        
        if sensor_data:
            lightStatus = sensor_data[0][1]
            noise = sensor_data[0][2]
            temperature = sensor_data[0][3]
            humidity = sensor_data[0][4]
            lightLevel = sensor_data[0][5]

        # Close the database connection
        cursor.close()
        conn.close()

        # Return the fetched data as variables
        return (
            electricity_status, electricity_date,
            lighting_status, lighting_date,
            air_cond_status, air_cond_date,
            punishment_date, lightStatus,
            noise, temperature, humidity,
            lightLevel
        )

    except mysql.connector.Error as error:
        print("Error connecting to MySQL database:", error)
        return None, None, None, None, None, None, None, None, None, None, None, None

#check the card owner have the authority to access the class or not
def check_access_class(card):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db") 
    
    cursor = db.cursor()
    query = "SELECT ownerName FROM registeredCardOwners WHERE cardID = '" + card + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    
    if result != None:
        return result[0]
    else:
        return ""
    
    db.close()
            
        

#insert enter or exit record to database entriesLog table
def insert_access_record(card, name, status):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db") 
    dt = datetime.datetime.now()
    dt = dt.strftime("%c")

    cursor = db.cursor()
    cursor.execute("INSERT INTO entriesLog (cardID, user, status, datetime) VALUES (%s, %s, %s, %s)", (card, name, status, dt))
    db.commit()
        
        
    cursor.close()
    
    db.close()
    
def insert_electricity_record(status):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db") 
    dt = datetime.datetime.now()
    dt = dt.strftime("%c")

    cursor = db.cursor()
    cursor.execute("INSERT INTO electricityLog (status, datetime) VALUES (%s, %s)", (status, dt))
    db.commit()
        
        
    cursor.close()
    
    db.close()
    
def insert_lighting_record(status):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db") 
    dt = datetime.datetime.now()
    dt = dt.strftime("%c")

    cursor = db.cursor()
    cursor.execute("INSERT INTO lightingLog (status, datetime) VALUES (%s, %s)", (status, dt))
    db.commit()
        
        
    cursor.close()
    
    db.close()
    
def insert_aircond_record(status):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db") 
    dt = datetime.datetime.now()
    dt = dt.strftime("%c")

    cursor = db.cursor()
    cursor.execute("INSERT INTO airCondLog (status, datetime) VALUES (%s, %s)", (status, dt))
    db.commit()
        
        
    cursor.close()
    
    db.close()
    
def insert_punish_record():
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db") 
    dt = datetime.datetime.now()
    dt = dt.strftime("%c")

    cursor = db.cursor()
    cursor.execute("INSERT INTO punishmentTriggeredLog (triggeredDatetime) VALUES (%s)", (dt, ))
    db.commit()
        
        
    cursor.close()
    
    db.close()
    
def insert_attendance_record(name):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db")
    dt = datetime.datetime.now()
    dt = dt.strftime("%x")
    
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM attendanceList WHERE date = %s AND studentName = %s"
    parameters = (dt, name)
    cursor.execute(query, parameters)
    result = cursor.fetchone()[0]
    
    if (result == 0):
        cursor.execute("INSERT INTO attendanceList (date, studentName) VALUES (%s, %s)", (dt, name))
        print(name, " inserted")
    else:
        print("already have")
        
    db.commit()
    
    
    cursor.close()
    
    db.close()

def insert_sensor_value(lStatus, nValue, tValue, hValue, lValue):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db")


    cursor = db.cursor()
    query = "INSERT INTO sensorValue (lightStatus, noiseValue, tempValue, humidValue, lightValue) VALUES (%s, %s, %s, %s, %s)"
    values = (lStatus, nValue, tValue, hValue, lValue)

    cursor.execute(query, values)
    db.commit()
    
    cursor.close()
    
    db.close()

def get_student_name(card):
    db = mysql.connector.connect(host="localhost", user="pi", password="pipipi", database="smart_classroom_system_db") 
    
    cursor = db.cursor()
    query = "SELECT ownerName FROM registeredCardOwners WHERE role = 'Student' AND cardID = '" + card + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    db.close()
    
    if result != None:
        return result[0]
    else:
        return ""



db_config = {
    'user': 'pi',
    'password': 'pipipi',
    'host': 'localhost',
    'database': 'smart_classroom_system_db'
}


def on_message(client, userdata, message):
    global my_variable  # Declare the variable as global

    payload = message.payload.decode()
    buttonText = None

    try:
        data = json.loads(payload)
        buttonText = data.get("buttonText")
    except json.JSONDecodeError:
        print("Error decoding message payload")

    if buttonText is not None:
        # Extract the status from the buttonText
        status = buttonText.split("buttonText:")[-1].strip()

        if status == "Main Electricity: ON":
            my_variable = "ON"
            print("HELOOOOOOOOOOOOOOOOOO")
        elif status == "Main Electricity: OFF":
            my_variable = "OFF"
            print("BYEEEEEEEEEEEEEEEEEE")
        else:
            print("Invalid status")

    else:
        print("buttonText not found in message payload")
    


my_variable = None
# PROGRAM START HERE
scs = serial.Serial('/dev/ttyACM1', 9600)
myMQTTClient.connect()
myMQTTClient.subscribe("Rpi4/status", 1, on_message)

#variables
peopleInClass = []
entryStatus = ""
currentElectricityStatus = "Off"
currentLightingStatus = "Off"
currentAirCondStatus = "Off"
attendanceRecorded = False

while True:
    
    entryStatus = ""
    attendanceRecorded = False
    

    while (scs.in_waiting == 0):
        pass
    
    line = scs.readline().decode('ascii').rstrip()
    print()
    print(line)
    print()
    print("people in the class = ", peopleInClass)
    
    splittedValues = line.split(',') #split by using CSV method
    print("new people access = ", splittedValues[0])
    print("electricity = ", splittedValues[1])
    print("natural light intensity = ", splittedValues[2])
    print("light = ", splittedValues[3])
    print("indoor temperature = ", splittedValues[4], "°C")
    print("indoor humidity = ", splittedValues[5], "%")
    print("air-cond status = ", splittedValues[6])
    print("noise level = ", splittedValues[7])
    print("During punishment = ", splittedValues[8])
    print("Punishment Triggered = ", splittedValues[9])
    insert_sensor_value(splittedValues[3],splittedValues[7],splittedValues[4],splittedValues[5],splittedValues[2])
    # Fetch the latest data from MySQL tables
    electricity_status, electricity_date,lighting_status, lighting_date, air_cond_status, air_cond_date, punishment_date, lightStatus, noise, temperature, humidity, lightLevel= fetch_latest_data_from_tables()

    if electricity_status is not None and electricity_date is not None and lighting_status is not None and lighting_date is not None and lightStatus is not None and noise is not None and temperature is not None and humidity is not None and lightLevel is not None:
        # Prepare payload
        payload = {
        "electricityStatus" : electricity_status,
        "electricityDate" : electricity_date,
        "lightingStatus" : lighting_status,
        "lightingDate" : lighting_date,
        "airCondStatus" : air_cond_status,
        "airConDate" : air_cond_date,
        "punishmentDate": punishment_date,
        "noise": noise,
        "lightStatus": lightStatus,
        "temperature": temperature,
        "humidity": humidity,
        "lightLevel" : lightLevel
        }

        # Convert payload to JSON
        payload_json = json.dumps(payload)

        # Publish payload to AWS IoT topic
        myMQTTClient.publish("Rpi4/data", payload_json, 1)
 
        print("Data published")
    
    
    cardToTest = splittedValues[0]
    #check in or out
    if cardToTest != "no": #splittedValues[0]: new card presented to rfid scanner?
        check_access_result = check_access_class(splittedValues[0])

        if (check_access_result != ""): #found the owner in the db table and allow access

            if len(peopleInClass) != 0: #got people in class
                for p in peopleInClass:
                    if (p == cardToTest): # mean the person is currently in class
                        peopleInClass.remove(cardToTest)
                        entryStatus = "out"
                        insert_access_record(cardToTest, check_access_result, entryStatus) #inside record to database table
                
                if entryStatus == "": # mean the person is not currently in class
                    peopleInClass.append(cardToTest)
                    entryStatus = "in"
                    insert_access_record(cardToTest, check_access_result, entryStatus) #inside record to database table
            else:
                peopleInClass.append(cardToTest)
                entryStatus = "in"
                insert_access_record(cardToTest, check_access_result, entryStatus) #inside record to database table
            
            #for attendance
            studentName = get_student_name(cardToTest)
            
            if (studentName != ""):
                insert_attendance_record(studentName)
                
        else:
            entryStatus = "no"
    
    # Check if there are people in the classroom
    if len(peopleInClass) != 0:
        if entryStatus == "in":
            scs.write(b"1")
        elif entryStatus == "out":
            scs.write(b"2")
        elif entryStatus == "no":
            scs.write(b"3")
    else:
        if entryStatus == "in":
            scs.write(b"5")
        elif my_variable == "ON":
            scs.write(b"4")
            my_variable = None
        elif my_variable == "OFF":
            scs.write(b"8")
            my_variable = None
            entryStatus = "out"
        elif entryStatus == "out":
            scs.write(b"6")
        elif entryStatus == "no" :
            scs.write(b"7")

    
    #records
    if (currentElectricityStatus != splittedValues[1]):
        insert_electricity_record(splittedValues[1])
        currentElectricityStatus = splittedValues[1]
        
    if (currentLightingStatus != splittedValues[3]):
        insert_lighting_record(splittedValues[3])
        currentLightingStatus = splittedValues[3]
    
    if (currentAirCondStatus != splittedValues[6]):
        insert_aircond_record(splittedValues[6])
        currentAirCondStatus = splittedValues[6]
        
    if (splittedValues[9] == "Yes"):
        insert_punish_record()
time.sleep(1)
