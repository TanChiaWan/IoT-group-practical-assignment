import time
import signal
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import mysql.connector
import serial

db_config = {
    'user': 'pi',
    'password': 'kevinpassword',
    'host': 'localhost',
    'database': 'smart_classroom_system_db'
}

myMQTTClient = AWSIoTMQTTClient("MyRPI4")# change this to any name, preferably the same name as in Things Dashboard eg:- MyRPI2
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("a28tye8o84qif9-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/AmazonRootCA1.pem", "/home/pi/certs/8258dfa67d46e37ee1db45f756791545b8a5b8c36914392b70a29b4a957e4954-private.pem.key", "/home/pi/certs/8258dfa67d46e37ee1db45f756791545b8a5b8c36914392b70a29b4a957e4954-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


# Connect to AWS IoT
myMQTTClient.connect()

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

        # Close the database connection
        cursor.close()
        conn.close()

        # Return the fetched data as variables
        return (
            electricity_status, electricity_date,
            lighting_status, lighting_date,
            air_cond_status, air_cond_date,
            punishment_date
        )

    except mysql.connector.Error as error:
        print("Error connecting to MySQL database:", error)
        return None, None, None, None, None, None, None, None, None, None, None, None

# Main loop
while True:
    # Fetch the latest data from MySQL tables
    electricity_status, electricity_date,lighting_status, lighting_date, air_cond_status, air_cond_date, punishment_date= fetch_latest_data_from_tables()

    if electricity_status is not None and electricity_date is not None and lighting_status is not None and lighting_date is not None:
        # Prepare payload
        payload = {
        "electricityStatus" : electricity_status,
        "electricityDate" : electricity_date,
        "lightingStatus" : lighting_status,
        "lightingDate" : lighting_date,
        "airCondStatus" : air_cond_status,
        "airConDate" : air_cond_date,
        "punishmentDate": punishment_date
        }

        # Convert payload to JSON
        payload_json = json.dumps(payload)

        # Publish payload to AWS IoT topic
        myMQTTClient.publish("Rpi4/data", payload_json, 1)
 
        print("Data published")

    # Delay before fetching data again
    time.sleep(5)
    

