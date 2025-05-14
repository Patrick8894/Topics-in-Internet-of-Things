import serial
import re
import time
from datetime import datetime
from pymongo import MongoClient
import os

# Serial setup
SERIAL_PORT = os.environ.get("SERIAL_PORT", "/dev/ttyUSB0")
BAUD_RATE = 115200

# MongoDB setup
mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(mongo_url)
collection = client["sensor_db"]["readings"]

# Regex to extract sensor data
pattern = re.compile(
    r"Device:\s*(\S+)\s*\|\s*Temp:\s*([-+]?\d*\.\d+|\d+)\s*°C,\s*Humidity:\s*([-+]?\d*\.\d+|\d+)\s*%,\s*Sound Level:\s*(\d+)"
)

def read_and_insert(ser):
    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        match = pattern.match(line)
        if match:
            device_id = match.group(1)
            temperature = float(match.group(2))
            humidity = float(match.group(3))
            sound = int(match.group(4))

            doc = {
                "device_id": device_id,
                "temperature": temperature,
                "humidity": humidity,
                "sound": sound,
                "timestamp": datetime.utcnow()
            }

            collection.insert_one(doc)
            print("Inserted:", doc)

            # time.sleep(30) 
            # break 

# Main loop
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
    print(f"Reading from {SERIAL_PORT} (1 insert every 30 seconds)")
    while True:
        try:
            read_and_insert(ser)
        except Exception as e:
            print("Error:", e)
