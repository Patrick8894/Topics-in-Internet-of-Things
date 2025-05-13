from pymongo import MongoClient
from models import SensorData
import os

client = MongoClient(os.environ.get("MONGO_URL", "mongodb://localhost:27017"))
collection = client["sensor_db"]["readings"]

def get_data():
    results = collection.find({}, {"_id": 0})
    return [SensorData(**doc) for doc in results]
