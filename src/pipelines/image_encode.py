import cv2
import base64
import numpy as np


def image_to_base64(image: np.ndarray, verbose: bool = False) -> str:
    if verbose:
        print("\nImage encoder started...\n")

    success, buffer = cv2.imencode(".jpeg", image)
    if not success:
        raise ValueError("Failed to encode image.")

    img_base64 = base64.b64encode(buffer).decode("utf-8") + " (truncated base64)"
    return img_base64
