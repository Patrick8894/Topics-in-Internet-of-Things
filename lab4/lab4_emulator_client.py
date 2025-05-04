# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np
import argparse

#TODO 1: modify the following parameters
#Starting and end index, modify this
parser = argparse.ArgumentParser(description="MQTT Emulator Client")
parser.add_argument("--device", type=int, default=0, help="device index")
args = parser.parse_args()

# Set device_st and device_end from arguments
device_st = args.device
device_end = args.device + 1
# device_st = 0
# device_end = 1

#Path to the dataset, modify this
data_path = "vehicle_data/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "thing{}/certificate.pem.crt"
key_formatter = "thing{}/private.key"

class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a2mco967mdeub9-ats.iot.us-east-2.amazonaws.com", 8883)
        self.client.configureCredentials("keys/AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2) # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10) # 10 sec
        self.client.configureMQTTOperationTimeout(5) # 5 sec
        self.client.onMessage = self.customOnMessage

    def customOnMessage(self,message):
        #TODO 3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, topic="device/data"):
    # Load the vehicle's emission data
        df = pd.read_csv(data_path.format(self.device_id))

        # Limit to the first 10 rows
        for index, row in df.head(10).iterrows():
            # Create a JSON payload from the row data
            payload = json.dumps(row.to_dict())

            # Publish the payload to the specified topic
            # print(f"Publishing: {payload} to {topic}")
            self.client.publishAsync(topic, payload, 0, ackCallback=self.customPubackCallback)

            # Sleep to simulate real-time data publishing
            time.sleep(0.01)



print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))

    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))

    client.client.connect()
    clients.append(client)

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish()

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)