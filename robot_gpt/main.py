import os
import cv2
import openai
import logging
from typing import List, Optional
# from imageai.Detection import ObjectDetection

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

openai.api_key = os.environ["OPENAI_API_KEY"]


def capture_image(image_filename: str = "captured_image.jpg") -> Optional[str]:
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        logger.error("Failed to capture image.")
        return None
    cam.release()
    cv2.imwrite(image_filename, frame)
    return image_filename


# def recognize_objects(image_path: str) -> List[str]:
#     execution_path = os.getcwd()

#     detector = ObjectDetection()
#     detector.setModelTypeAsRetinaNet()
#     detector.setModelPath(os.path.join(
#         execution_path, "resnet50_coco_best_v2.1.0.h5"))
#     detector.loadModel()

#     detections = detector.detectObjectsFromImage(
#         input_image=image_path, output_image_path="output.jpg")

#     return [detection["name"] for detection in detections]


def chat_with_gpt(objects_list: List[str]) -> str:
    prompt = f"objects: {', '.join(objects_list)}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message


if __name__ == "__main__":
    image_path = capture_image()
    # if image_path:
    #     objects = recognize_objects(image_path)
    #     logger.info(f"Objects detected: {objects}")
    #     response_message = chat_with_gpt(objects)
    #     logger.info(f"ChatGPT says: {response_message}")
    # else:
    #     logger.error("No image captured.")
