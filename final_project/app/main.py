from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from db import get_data
from models import SensorData

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Raspberry Pi!"}

@app.get("/home")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/data", response_model=list[SensorData])
def fetch_data():
    return get_data()
