import cv2
import mediapipe as mp
import numpy as np

from pathlib import Path
from src.config import FACES_DIR

import time
import logging


logger = logging.getLogger(__name__)


def extract_face(
        path: str,
        verbose: bool = False,
        save_face_crop: bool = True,
) -> np.ndarray:

    start = time.perf_counter()
    if verbose:
        logger.info("Face extraction started...\n")

    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
    ) as face_detection:

        image = cv2.imread(path)
        if image is None:
            raise ValueError("Failed to read input image.")

        h, w, _ = image.shape
        if verbose:
            logger.info(f"Image size: {w}x{h}")

        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.detections:
            raise ValueError("No face detected on the image.")

        if len(results.detections) > 1:
            raise ValueError("Multiple faces detected.")

        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box

        x_min = int(bbox.xmin * w - 40)
        y_min = int(bbox.ymin * h - 100)
        box_w = int(bbox.width * w + 60)
        box_h = int(bbox.height * h + 170)

        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w, x_min + box_w)
        y_max = min(h, y_min + box_h)

        face_crop = image[y_min:y_max, x_min:x_max]

        if save_face_crop:
            name = Path(path).name
            original_name = f"original_{Path(path).name}"
            cropped_name = f"cropped_{name}"
            try:
                cv2.imwrite(str(FACES_DIR / cropped_name), face_crop)
                cv2.imwrite(str(FACES_DIR / original_name), image)
                if verbose:
                    logger.info(f"Cropped and original images saved to: {FACES_DIR}\n")
            except Exception as e:
                logger.warning(f"Failed to save images: {e}")

        if verbose:
            duration = time.perf_counter() - start
            logger.info("Bounding box:"
                        f"x_min={x_min}, y_min={y_min}, x_max={x_max}, y_max={y_max}")
            logger.info(f"Completed in {duration:.3f} s.\n")

        return face_crop
