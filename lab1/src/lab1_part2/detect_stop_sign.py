# Code retrieved from https://github.com/tensorflow/examples

# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import time

import cv2
from picamera2 import Picamera2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import utils
import mediapipe as mp

class StopSignDetector():

    def __init__(self):
        model = 'efficientdet_lite0.tflite'
        width = 1280
        height = 960

        # Initialize the camera
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": "RGB888", "size": (width, height)}))
        self.picam2.start()

        # Initialize the object detection model
        base_options = python.BaseOptions(model_asset_path=model)
        options = vision.ObjectDetectorOptions(base_options=base_options,
                                            score_threshold=0.3,
                                            max_results=3)
        self.detector = vision.ObjectDetector.create_from_options(options)

    def run(self) -> bool:
        # Continuously capture images from the camera and run inference
        image = self.picam2.capture_array()
        image = cv2.rotate(image, cv2.ROTATE_180)  # Change the rotation as needed

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        # Run object detection estimation using the model.
        detection_result = self.detector.detect(input_tensor)

        # Chech if it detect stop sign
        for detection in detection_result.detections:
            category = detection.categories[0]
            category_name = category.category_name

            if category_name == "stop sign":
                print("Stop sign detected")
                return True
        
        print("No stop sign detected")
        return False

if __name__ == "__main__":
    stop_sign_detector = StopSignDetector()
    while True:
        stop_sign_detector.run()
        time.sleep(1)

