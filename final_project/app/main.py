from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()
client = MongoClient(os.environ["MONGO_URL"])
db = client["mydb"]
collection = db["items"]

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Raspberry Pi!"}

@app.post("/add/{name}")
def add_item(name: str):
    collection.insert_one({"name": name})
    return {"status": "ok", "name": name}

@app.get("/list")
def list_items():
    return {"items": list(collection.find({}, {"_id": 0}))}
