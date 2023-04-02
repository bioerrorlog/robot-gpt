# import os
# import cv2
# import openai
import logging
from typing import List
from picamera2 import Picamera2
from imageai.Detection import ObjectDetection

model_path = "./models/tiny-yolov3.pt"
# openai.api_key = os.environ["OPENAI_API_KEY"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def capture_image(image_filename: str) -> str:
    picam2 = Picamera2()
    picam2.start_and_capture_file(image_filename, show_preview=False)

    return image_filename


def recognize_objects(image_path: str, model_path: str) -> List[str]:
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    detections = detector.detectObjectsFromImage(
        input_image=image_path, output_type="array")
    objects_name_list = [i["name"] for i in detections[1]]

    return objects_name_list


# def chat_with_gpt(objects_list: List[str]) -> str:
#     prompt = f"objects: {', '.join(objects_list)}"

#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )

#     message = response.choices[0].text.strip()
#     return message


if __name__ == "__main__":
    image_path = capture_image("outputs/captured_image.jpg")
    if image_path:
        objects = recognize_objects(image_path, model_path)
        logger.info(f"Objects detected: {objects}")
        # response_message = chat_with_gpt(objects)
        # logger.info(f"ChatGPT says: {response_message}")
    else:
        logger.error("No image captured.")
