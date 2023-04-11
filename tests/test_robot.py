import json
import pytest
from robot_gpt.robot import (
    Role,
    RobotGPT,
)


@pytest.mark.parametrize("test_role", [Role.SYSTEM, Role.USER, Role.ASSISTANT])
def test_append_prompt(test_role):
    robot = RobotGPT()
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
    robot = RobotGPT()
    initial_prompts = robot.prompts
    initial_length = len(initial_prompts)

    mocker.patch("robot_gpt.hardware.capture_image", return_value="./outputs/captured_image.jpg")
    mocker.patch("robot_gpt.hardware.recognize_objects", return_value=["object1", "object2"])
    robot.recognize(45, -30)

    updated_prompts = robot.prompts
    updated_length = len(updated_prompts)

    assert updated_length == initial_length + 1

    last_prompt = updated_prompts[-1]
    assert last_prompt["role"] == Role.USER.value


@ pytest.mark.chatgpt
def test_chat_with_gpt_success():
    """Warning: The ChatGPT API will be actually called. The API Key is required."""
    chatbot = RobotGPT()

    chatbot.recognize(0, 0, ["cup", "tvmonitor", "pc"])
    response = chatbot.call_gpt()

    print(response)
    assert isinstance(response, str)
    assert len(response) > 0

    # Response can be parsed in JSON
    json_response = json.loads(response)
    assert isinstance(json_response['NextServoMotor']['Horizontal'], int)
    assert isinstance(json_response['NextServoMotor']['Vertical'], int)
    assert isinstance(json_response['FreeTalk'], str)

    chatbot.append_prompt(Role.USER, "What do you want to do in this place if you have two hands?")
    response = chatbot.call_gpt()

    print(response)
    assert isinstance(response, str)
    assert len(response) > 0

    all_prompts = chatbot.prompts
    for i in all_prompts:
        print(i)
    assert isinstance(all_prompts, list)
    assert len(all_prompts) > 0
