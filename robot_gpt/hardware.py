import os
import time
from typing import List, Tuple
from picamera2 import Picamera2
from imageai.Detection import ObjectDetection
from gpiozero import AngularServo

current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(current_dir, '../models/tiny-yolov3.pt')


class Camera:
    def __init__(self):
        self.picam2 = Picamera2()

    def capture_image(self, image_filename: str) -> str:
        self.picam2.start_and_capture_file(image_filename, show_preview=False)
        return image_filename

    def close(self):
        self.picam2.close()


def recognize_objects(image_path: str) -> List[str]:
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(MODEL_PATH)
    detector.loadModel()

    detections = detector.detectObjectsFromImage(
        input_image=image_path, output_type="array")

    objects_name_list = [i["name"] for i in detections[1]]
    return objects_name_list


def angle(horizontal: int, vertical: int, gpio_horizontal: int = 17, gpio_vertical: int = 18) -> Tuple[int, int]:
    servo_horizontal = AngularServo(gpio_horizontal)
    servo_vertical = AngularServo(gpio_vertical)

    servo_horizontal.angle = horizontal
    servo_vertical.angle = vertical
    time.sleep(0.5)

    return servo_horizontal.angle, servo_vertical.angle
