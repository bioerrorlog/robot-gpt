import os
import logging
from enum import Enum
from typing import List

import openai
from picamera2 import Picamera2
from imageai.Detection import ObjectDetection

model_path = "./models/tiny-yolov3.pt"
openai.api_key = os.environ["OPENAI_API_KEY"]

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


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatWithGPT:
    def __init__(self, objects: List[str]):
        self.messages = [
            {"role": Role.SYSTEM.value, "content": "You are a robot with a camera, fixed to a desk."},
            {"role": Role.USER.value, "content": f"Now you can see the objects: {objects}"}
        ]

    def append_message(self, role: Role, content: str):
        self.messages.append({"role": role.value, "content": content})

    def generate_response(self) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        return response.choices[0].message.content


def main() -> None:
    image_path = capture_image("outputs/captured_image.jpg")
    logger.info(f"Image captured: {image_path}")

    objects = recognize_objects(image_path, model_path)
    logger.info(f"Objects detected: {objects}")

    chatbot = ChatWithGPT(objects)
    message = chatbot.generate_response()
    print(f"ChatGPT says: {message}")


if __name__ == "__main__":
    main()
