import logging
from robot_gpt.robot import RobotGPT
from robot_gpt.hardware import (
    capture_image,
    recognize_objects,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


def main() -> None:
    image_path = capture_image("outputs/captured_image.jpg")
    logger.info(f"Image captured: {image_path}")

    objects = recognize_objects(image_path)
    logger.info(f"Objects detected: {objects}")

    chatbot = RobotGPT()
    message = chatbot.generate_response()
    print(f"ChatGPT says: {message}")


if __name__ == "__main__":
    main()
