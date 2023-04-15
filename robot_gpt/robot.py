import os
import json
import logging
from enum import Enum
import openai
from robot_gpt.hardware import (
    Camera,
    recognize_objects,
    angle,
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
    def __init__(self, horizontal: int = 0, vertical: int = 0):
        self._prompts = [
            {"role": Role.SYSTEM.value, "content": """
You are a robot with a camera, composed of 2 servo motors: horizontal & vertical.
Horizontal: min -90 left, max 90 right.
Vertical: min -90 down, max 90 up.
Your behavior principles: [curiosity, inquisitiveness, playfulness].
Your answer MUST be in this JSON format: {"NextServoMotor": [{"Horizontal": int(-90~90), "Vertical": int(-90~90)}] "FreeTalk": string}
Constraint: len(your_answer["NextServoMotor"]) == 5
Answer example: {"NextServoMotor": [{"Horizontal": -60, "Vertical": -30},{"Horizontal": 0, "Vertical": 0},{"Horizontal": 90, "Vertical": -45},{"Horizontal": 0, "Vertical": 60},{"Horizontal": -30, "Vertical": -60}],"FreeTalk": "Based on what I've seen, I'm curious about the PC and mouse. I wonder what you use them for and what kind of work or play they are involved in?"}
"""},
        ]
        self._horizontal = horizontal
        self._vertical = vertical
        self._next_horizontal = 0
        self._next_vertical = 0
        self._camera = Camera()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def prompts(self):
        return self._prompts

    def append_prompt(self, role: Role, content: str):
        self._prompts.append({"role": role.value, "content": content})

    def look(self):
        self._horizontal, self._vertical = angle(self._next_horizontal, self._next_vertical)

    def recognize(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '../outputs/captured_image.jpg')
        self._camera.capture_image(image_path)
        logger.info(f"Image captured: {image_path}")

        objects = recognize_objects(image_path)
        logger.info(f"Objects detected: {objects}")

        content = {
            "CurrentServoMotor": {"Horizontal": self._horizontal, "Vertical": self._vertical},
            "SeenObjects": objects,
        }
        self.append_prompt(Role.USER, json.dumps(content))

    def close(self):
        self._camera.close()

    def call_gpt(self) -> str:
        logger.info("Start OpenAI API call.")
        logger.info(f"Prompts: {self.prompts}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=self.prompts
        )
        content = response.choices[0].message.content
        logger.info(f"Response content: {content}")

        self.append_prompt(Role.ASSISTANT, content)

        return content

    def call_and_recognize(self):
        response = self.call_gpt()
        json_response = json.loads(response)

        for next_servo_motor in json_response['NextServoMotor']:
            self._next_horizontal = next_servo_motor['Horizontal']
            self._next_vertical = next_servo_motor['Vertical']
            self.look()
            self.recognize()

    def talk(self, message: str) -> str:
        self.append_prompt(Role.USER, message)
        self.append_prompt(Role.SYSTEM, "You can answer in free format only once.")

        return self.call_gpt()
