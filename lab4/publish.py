# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2mco967mdeub9-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "/home/patrick/keys/f1df132f186ce9c340f930cdb72a93ffccdca1b31632c0a1dbb8410883b34af9-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "/home/patrick/keys/f1df132f186ce9c340f930cdb72a93ffccdca1b31632c0a1dbb8410883b34af9-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/home/patrick/keys/AmazonRootCA1.pem"
MESSAGE = "Hello World"
TOPIC = "device/data"
RANGE = 3

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

myAWSIoTMQTTClient.connect()
print('Begin Publish')
for i in range (RANGE):
    data = "{} [{}]".format(MESSAGE, i+1)
    message = {"message" : data}
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'device/data'")
    t.sleep(0.1)
print('Publish End')
myAWSIoTMQTTClient.disconnect()