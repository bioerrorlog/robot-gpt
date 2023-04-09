import json
import pytest

from robot_gpt.robot import (
    Role,
    ChatWithGPT,
)


@ pytest.mark.chatgpt
def test_chat_with_gpt_success():
    """Warning: The ChatGPT API will be actually called. The API Key is required."""
    chatbot = ChatWithGPT()

    chatbot.append_recognition(0, 0, ["cup", "tvmonitor", "pc"])
    response = chatbot.generate_response()

    print(response)
    assert isinstance(response, str)
    assert len(response) > 0

    # Response can be parsed in JSON
    json_response = json.loads(response)
    assert isinstance(json_response['NextServoMotor']['Horizontal'], int)
    assert isinstance(json_response['NextServoMotor']['Vertical'], int)
    assert isinstance(json_response['FreeTalk'], str)

    chatbot.append_message(Role.USER, "What do you want to do in this place if you have two hands?")
    response = chatbot.generate_response()

    print(response)
    assert isinstance(response, str)
    assert len(response) > 0

    all_messages = chatbot.messages
    for i in all_messages:
        print(i)
    assert isinstance(all_messages, list)
    assert len(all_messages) > 0
