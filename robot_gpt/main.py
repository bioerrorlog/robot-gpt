import logging
from typing import List
from picamera2 import Picamera2
from imageai.Detection import ObjectDetection
from robot_gpt.robot import ChatWithGPT

model_path = "./models/tiny-yolov3.pt"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


def capture_image(image_filename: str) -> str:
    picam2 = Picamera2()
    picam2.start_and_capture_file(image_filename, show_preview=False)

    return image_filename


def recognize_objects(image_path: str, model_path: str) -> List[str]:
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    detections = detector.detectObjectsFromImage(
        input_image=image_path, output_type="array")

    objects_name_list = [i["name"] for i in detections[1]]
    return objects_name_list


def main() -> None:
    image_path = capture_image("outputs/captured_image.jpg")
    logger.info(f"Image captured: {image_path}")

    objects = recognize_objects(image_path, model_path)
    logger.info(f"Objects detected: {objects}")

    chatbot = ChatWithGPT()
    message = chatbot.generate_response()
    print(f"ChatGPT says: {message}")


if __name__ == "__main__":
    main()
