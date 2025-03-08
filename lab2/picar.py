import picar_4wd as fc

def control(message: str):
    if message == "forward":
        fc.forward(50)
    elif message == "backward":
        fc.backward(50)
    elif message == "left":
        fc.turn_left(50)
    elif message == "right":
        fc.turn_right(50)
    elif message == "stop":
        fc.stop()
    else:
        print("Invalid message")

def getCarInfo() -> dict:
    car_info = {
        "battery": "80%",
        "movingDirection": "forward",
        "turning": "none"
    }
    return car_info