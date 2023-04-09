import os
from typing import List
from picamera2 import Picamera2
from imageai.Detection import ObjectDetection

current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(current_dir, '../models/tiny-yolov3.pt')


def capture_image(image_filename: str) -> str:
    picam2 = Picamera2()
    picam2.start_and_capture_file(image_filename, show_preview=False)

    return image_filename


def recognize_objects(image_path: str) -> List[str]:
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(MODEL_PATH)
    detector.loadModel()

    detections = detector.detectObjectsFromImage(
        input_image=image_path, output_type="array")

    objects_name_list = [i["name"] for i in detections[1]]
    return objects_name_list
