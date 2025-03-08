import picar_4wd as fc
from picar_4wd.utils import pi_read

direction = "N/A"
turning = "N/A"

def control(message: str):
    global direction, turning
    if message == "forward":
        direction = "Forward"
        turning = "N/A"
        fc.forward(50)
    elif message == "backward":
        direction = "Backward"
        turning = "N/A"
        fc.backward(50)
    elif message == "left":
        direction = "N/A"
        turning = "Left"
        fc.turn_left(50)
    elif message == "right":
        direction = "N/A"
        turning = "Right"
        fc.turn_right(50)
    elif message == "stop":
        direction = "N/A"
        turning = "N/A"
        fc.stop()
    else:
        print("Invalid message")

def getCarInfo() -> dict:
    car_info = pi_read()
    car_info["movingDirection"] = direction
    car_info["turning"] = turning
    return car_info