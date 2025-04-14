import json
import logging
import sys

import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

# Global dictionary to store max CO2 per vehicle
max_co2_per_vehicle = {}

def lambda_handler(event, context):
    """
    Processes incoming MQTT messages containing vehicle CO2 data.
    Updates the maximum CO2 emission per vehicle and publishes the updated value.
    """
    try:
        # Ensure event is a list of records
        records = event if isinstance(event, list) else [event]

        for record in records:
            vehicle_id = record.get('vehicle_id')
            co2_value = float(record.get('vehicle_CO2', 0.0))

            # Update max CO2 value for the vehicle
            current_max = max_co2_per_vehicle.get(vehicle_id, 0.0)
            if co2_value > current_max:
                max_co2_per_vehicle[vehicle_id] = co2_value
                logger.debug(f"Updated max CO2 for vehicle {vehicle_id}: {co2_value}")
            else:
                logger.debug(f"No update needed for vehicle {vehicle_id}: current max {current_max}, new value {co2_value}")

            # Publish the current max CO2 value for the vehicle
            client.publish(
                topic=f"iot/Vehicle_{vehicle_id}",
                queueFullPolicy="AllOrException",
                payload=json.dumps({"max_CO2": max_co2_per_vehicle[vehicle_id]}),
            )

    except Exception as e:
        logger.error(f"Error processing event: {e}")
