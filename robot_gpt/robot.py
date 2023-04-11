import os
import json
from enum import Enum
from typing import List
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


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

    def recognize(self, horizontal: int, vertical: int, objects: List[str]):
        content = {
            "CurrentServoMotor": {"Horizontal": horizontal, "Vertical": vertical},
            "SeenObjects": objects,
        }
        self.append_prompt(Role.USER, json.dumps(content))

    def generate_response(self) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._prompts
        )

        response_content = response.choices[0].message.content
        self._prompts.append({"role": Role.ASSISTANT.value, "content": response_content})

        return response_content
