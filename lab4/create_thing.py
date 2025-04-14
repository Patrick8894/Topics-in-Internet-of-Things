import boto3
import json
import os

# Parameters
thingGroupName = 'thing_group0'
defaultPolicyName = 'policy0'
numThings = 5

thingClient = boto3.client('iot', region_name='us-east-2')

def createThing(thingName, index):

    resp = thingClient.create_thing(thingName=thingName)
    thingArn = resp['thingArn']
    print(f"[{index}] Created Thing: {thingName} (ARN: {thingArn})")

    thingClient.add_thing_to_thing_group(
        thingGroupName=thingGroupName,
        thingName=thingName
    )
    print(f"[{index}] Added to Thing Group: {thingGroupName}")

    cert = thingClient.create_keys_and_certificate(setAsActive=True)
    certificateArn = cert['certificateArn']
    certificatePem = cert['certificatePem']
    publicKey = cert['keyPair']['PublicKey']
    privateKey = cert['keyPair']['PrivateKey']
    print(f"[{index}] Created Certificate: {certificateArn}")

    base = f"{thingName}"
    os.makedirs(base, exist_ok=True)
    with open(f"{base}/certificate.pem.crt", "w") as f:
        f.write(certificatePem)
    with open(f"{base}/public.key", "w") as f:
        f.write(publicKey)
    with open(f"{base}/private.key", "w") as f:
        f.write(privateKey)
    print(f"[{index}] Saved keys in folder ./{base}/")

    thingClient.attach_policy(
        policyName=defaultPolicyName,
        target=certificateArn
    )
    print(f"[{index}] Attached policy: {defaultPolicyName}")

    thingClient.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )
    print(f"[{index}] Attached principal to Thing")

for i in range(numThings):
    thingName = f"thing{i}"
    createThing(thingName, i)
