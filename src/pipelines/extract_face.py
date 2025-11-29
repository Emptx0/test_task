import cv2
import mediapipe as mp
import numpy as np

import time

from pathlib import Path
from src.config import FACES_DIR


def extract_face(
        path: str,
        verbose: bool = False,
        save_face_crop: bool = True,
) -> np.ndarray:

    start = time.perf_counter()
    if verbose:
        print("\nFace extraction started...\n")

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
            print(f"Image size: {w}x{h}")

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
            filename = Path(path).name
            try:
                cv2.imwrite(str(FACES_DIR / filename), face_crop)
                if verbose:
                    print(f"Cropped image saved to: {FACES_DIR}\n")
            except Exception as e:
                print(f"Warning: failed to save cropped image:\n{e}")

        if verbose:
            duration = time.perf_counter() - start
            print("Bounding box:")
            print(f"\tx_min={x_min}, y_min={y_min}, x_max={x_max}, y_max={y_max}")
            print(f"\n---- extract_face completed in {duration:.3f} s.\n")

        return face_crop