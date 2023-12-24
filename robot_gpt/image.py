import base64
import mimetypes


def img_to_base64(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)

    if not mime_type or not mime_type.startswith('image'):
        raise ValueError("The file type is not recognized as an image")

    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    return f"data:{mime_type};base64,{encoded_string}"
