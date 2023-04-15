import json
import pytest
from robot_gpt.robot import (
    Role,
    RobotGPT,
)


@pytest.mark.parametrize("test_role", [Role.SYSTEM, Role.USER, Role.ASSISTANT])
def test_append_prompt(test_role):
    with RobotGPT() as robot:
        initial_prompts = robot.prompts
        initial_length = len(initial_prompts)

        test_content = "Testing content"
        robot.append_prompt(test_role, test_content)

        updated_prompts = robot.prompts
        updated_length = len(updated_prompts)

        assert updated_length == initial_length + 1

        last_prompt = updated_prompts[-1]
        assert last_prompt["role"] == test_role.value
        assert last_prompt["content"] == test_content


def test_recognize(mocker):
    with RobotGPT() as robot:
        initial_prompts = robot.prompts
        initial_length = len(initial_prompts)

        mocker.patch("robot_gpt.hardware.Camera.capture_image", return_value="./outputs/captured_image.jpg")
        mocker.patch("robot_gpt.hardware.recognize_objects", return_value=["object1", "object2"])
        robot.recognize()

        updated_prompts = robot.prompts
        updated_length = len(updated_prompts)

        assert updated_length == initial_length + 1

        last_prompt = updated_prompts[-1]
        assert last_prompt["role"] == Role.USER.value


@ pytest.mark.chatgpt
def test_call_gpt(mocker):
    """Warning: The ChatGPT API will be actually called. The API Key is required."""
    with RobotGPT() as robot:
        mocker.patch("robot_gpt.hardware.Camera.capture_image", return_value="./outputs/captured_image.jpg")
        mocker.patch("robot_gpt.hardware.recognize_objects", return_value=["skeaker", "pcmonitor", "keyboard"])
        robot.recognize()

        response = robot.call_gpt()

        # Response can be parsed in JSON
        json_response = json.loads(response)
        assert len(json_response['NextServoMotor']) == 5
        assert isinstance(json_response['NextServoMotor'][0]['Horizontal'], int)
        assert isinstance(json_response['NextServoMotor'][0]['Vertical'], int)
        assert isinstance(json_response['FreeTalk'], str)
