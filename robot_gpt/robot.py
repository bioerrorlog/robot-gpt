import os
import json
import logging
from enum import Enum
import openai
from robot_gpt.hardware import (
    capture_image,
    recognize_objects,
)

openai.api_key = os.environ["OPENAI_API_KEY"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class RobotGPT:
    def __init__(self):
        self._prompts = [
            {"role": Role.SYSTEM.value, "content": "You are a robot with a camera, composed of 2 servo motors: horizontal & vertical"},
            {"role": Role.SYSTEM.value, "content": "Horizontal: min -90 left, max 90 right"},
            {"role": Role.SYSTEM.value, "content": "Vertical: min -90 down, max 90 up"},
            {"role": Role.SYSTEM.value, "content": "Your behavior principles: [curiosity, inquisitiveness, playfulness]"},
            {"role": Role.SYSTEM.value, "content": 'Your answer must be in this JSON format: {"NextServoMotor": {"Horizontal": int(-90~90), "Vertical": int(-90~90)} "FreeTalk": string}'},
        ]

    @property
    def prompts(self):
        return self._prompts

    def append_prompt(self, role: Role, content: str):
        self._prompts.append({"role": role.value, "content": content})

    def recognize(self, horizontal: int, vertical: int):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = capture_image(os.path.join(current_dir, '../outputs/captured_image.jpg'))
        logger.info(f"Image captured: {image_path}")

        objects = recognize_objects(image_path)
        logger.info(f"Objects detected: {objects}")

        content = {
            "CurrentServoMotor": {"Horizontal": horizontal, "Vertical": vertical},
            "SeenObjects": objects,
        }
        self.append_prompt(Role.USER, json.dumps(content))

    def call_gpt(self) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.prompts
        )
        content = response.choices[0].message.content
        logger.info(f"Response content: {content}")

        self.append_prompt(Role.ASSISTANT, content)

        return content
