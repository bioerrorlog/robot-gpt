import os
import json
import pytest
from robot_gpt.hardware import (
    capture_image,
    recognize_objects,
)
from robot_gpt.robot import (
    Role,
    ChatWithGPT,
)


@pytest.mark.camera
def test_capture_image_success():
    """A connected camera required"""
    image_filename = "outputs/test_captured_image.jpg"

    result = capture_image(image_filename)

    assert result == image_filename
    assert os.path.exists(image_filename)

    # Clean up the test image file.
    os.remove(image_filename)


@pytest.mark.recognize
def test_recognize_objects_success():
    """Download pre-trained model before running this test. See README."""
    image_path = "outputs/unittest.jpg"
    model_path = "models/tiny-yolov3.pt"

    objects = recognize_objects(image_path, model_path)

    assert isinstance(objects, list)
    assert all(isinstance(item, str) for item in objects)
    assert len(objects) >= 1


@pytest.mark.chatgpt
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
