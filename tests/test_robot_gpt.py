import os
import pytest
from robot_gpt.main import capture_image


@pytest.mark.camera
def test_capture_image_success():
    """A connected camera required"""
    image_filename = "outputs/test_captured_image.jpg"

    result = capture_image(image_filename)

    assert result == image_filename
    assert os.path.exists(image_filename)

    # Clean up the test image file.
    os.remove(image_filename)
