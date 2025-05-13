from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from db import get_latest_per_device, get_history
from models import SensorData

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

@app.get("/device/{device_id}")
def serve_device(device_id: str):
    return FileResponse("static/device.html")

@app.get("/api/latest", response_model=list[SensorData])
def api_latest():
    return get_latest_per_device()

@app.get("/api/history/{device_id}", response_model=list[SensorData])
def api_history(device_id: str):
    return get_history(device_id)