import os
import pytest
from robot_gpt.hardware import (
    capture_image,
    recognize_objects,
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
