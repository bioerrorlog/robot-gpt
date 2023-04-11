import os
import pytest
from robot_gpt.hardware import (
    capture_image,
    recognize_objects,
    angle,
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

    objects = recognize_objects(image_path)

    assert isinstance(objects, list)
    assert all(isinstance(item, str) for item in objects)
    assert len(objects) >= 1


@pytest.mark.servo
@pytest.mark.parametrize("test_horizontal, test_vertical",
                         [(30, 30), (-30, -30), (90, 90), (-90, -90), (0, 0)])
def test_servo_angle(test_horizontal, test_vertical):
    result_horizontal, result_vertical = angle(test_horizontal, test_vertical)

    assert result_horizontal == test_horizontal
    assert test_vertical == result_vertical
