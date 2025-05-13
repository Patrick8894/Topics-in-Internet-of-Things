from pymongo import MongoClient
from models import SensorData
from datetime import datetime, timedelta
import os

client = MongoClient(os.environ.get("MONGO_URL", "mongodb://localhost:27017"))
collection = client["sensor_db"]["readings"]

def get_latest_per_device():
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$device_id",
            "timestamp": {"$first": "$timestamp"},
            "temperature": {"$first": "$temperature"},
            "humidity": {"$first": "$humidity"},
            "sound": {"$first": "$sound"}
        }}
    ]
    results = collection.aggregate(pipeline)
    return [
        SensorData(
            device_id=doc["_id"],
            timestamp=doc["timestamp"],
            temperature=doc["temperature"],
            humidity=doc["humidity"],
            sound=doc["sound"]
        )
        for doc in results
    ]

def get_history(device_id: str):
    cutoff = datetime.utcnow() - timedelta(days=3)
    cursor = collection.find({
        "device_id": device_id,
        "timestamp": {"$gte": cutoff}
    }, {"_id": 0}).sort("timestamp", 1)
    return [SensorData(**doc) for doc in cursor]
