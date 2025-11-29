import cv2
import base64
import numpy as np

import time
import logging


logger = logging.getLogger(__name__)


def image_to_base64(image: np.ndarray, verbose: bool = False) -> str:
    start = time.perf_counter()
    if verbose:
        logger.info("Image encoder started...\n")

    success, buffer = cv2.imencode(".jpeg", image)
    if not success:
        raise ValueError("Failed to encode image.")

    img_base64 = base64.b64encode(buffer).decode("utf-8") + " (truncated base64)"

    if verbose:
        duration = time.perf_counter() - start
        logger.info(f"Completed in {duration:.3f} s.\n")

    return img_base64
