from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    timestamp: datetime 
    temperature: float
    humidity: float
    sound: float
    device_id: str