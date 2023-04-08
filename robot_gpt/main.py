import os
import logging
import json
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
    def __init__(self):
        self._messages = [
            {"role": Role.SYSTEM.value, "content": "You are a robot with a camera, composed of 2 servo motors: horizontal & vertical"},
            {"role": Role.SYSTEM.value, "content": "Horizontal: min -90 left, max 90 right"},
            {"role": Role.SYSTEM.value, "content": "Vertical: min -90 down, max 90 up"},
            {"role": Role.SYSTEM.value, "content": "Your behavior principles: [curiosity, inquisitiveness, playfulness]"},
            {"role": Role.SYSTEM.value, "content": 'Your answer must be in this JSON format: {"NextServoMotor": {"Horizontal": int(-90~90), "Vertical": int(-90~90)} "FreeTalk": string}'},
        ]

    @property
    def messages(self):
        return self._messages

    def append_recognition(self, horizontal: int, vertical: int, objects: List[str]):
        content = {
            "CurrentServoMotor": {"Horizontal": horizontal, "Vertical": vertical},
            "SeenObjects": objects,
        }

        self._messages.append({
            "role": Role.USER.value,
            "content": json.dumps(content),
        })

    def append_message(self, role: Role, content: str):
        self._messages.append({"role": role.value, "content": content})

    def generate_response(self) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._messages
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
