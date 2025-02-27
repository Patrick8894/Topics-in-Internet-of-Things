from picamera2 import Picamera2
import cv2
import numpy as np

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (1280, 960)}))
picam2.start()

while True:
    frame = picam2.capture_array()

    # Rotate the frame
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)  # Change the rotation as needed

    cv2.imshow('Camera Test', rotated_frame)

    if cv2.waitKey(1) == 27:  # Press ESC to exit
        break

cv2.destroyAllWindows()
picam2.stop()