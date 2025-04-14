from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd

# Device ID range
device_st = 0
device_end = 5  # Adjust as needed

# Dataset path pattern (e.g., vehicle_0.csv)
data_path = "./vehicle_data/vehicle0.csv"

# Paths to certificates (adjust if certs are per device)
CERTIFICATE_PATH = "/home/patrick/keys/f1df132f186ce9c340f930cdb72a93ffccdca1b31632c0a1dbb8410883b34af9-certificate.pem.crt"
PRIVATE_KEY_PATH = "/home/patrick/keys/f1df132f186ce9c340f930cdb72a93ffccdca1b31632c0a1dbb8410883b34af9-private.pem.key"
ROOT_CA_PATH = "/home/patrick/keys/AmazonRootCA1.pem"

# Greengrass Core local IP or hostname
GREENGRASS_CORE_HOST = "172.20.10.2"

class MQTTClient:
    def __init__(self):
        self.client = AWSIoTMQTTClient("vehicle_emulator")

        # Point to the Greengrass Core MQTT endpoint
        self.client.configureEndpoint(GREENGRASS_CORE_HOST, 8883)
        self.client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

        self.client.configureOfflinePublishQueueing(-1)
        self.client.configureDrainingFrequency(2)
        self.client.configureConnectDisconnectTimeout(10)
        self.client.configureMQTTOperationTimeout(5)
        self.client.onMessage = self.on_message

    def on_message(self, message):
        print(f"Received on {message.topic}: {message.payload.decode()}")

    def publish(self, topic="device/data"):
        try:
            df = pd.read_csv(data_path)
        except FileNotFoundError:
            print("Data file not found.")
            return

        for _, row in df.iterrows():
            payload = json.dumps(row.to_dict())
            print(f"Publishing: {payload}")
            self.client.publishAsync(topic, payload, 0)
            time.sleep(5)
            break  # Remove if you want to send the whole file

print("Connecting simulated devices to Greengrass Core...")
client = MQTTClient()
client.client.connect()

while True:
    cmd = input("Enter 's' to send, 'd' to disconnect: ").strip()
    if cmd == "s":
        client.publish()
    elif cmd == "d":
        client.client.disconnect()
        print("Disconnected all clients.")
        break
    else:
        print("Invalid input.")
    time.sleep(2)
