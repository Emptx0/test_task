import cv2
import mediapipe as mp
import numpy as np

from pathlib import Path
from src.config import FACES_DIR


def extract_face(
        path: str,
        verbose: bool = False
) -> np.ndarray:

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

        x_min = int(bbox.xmin * w - 20)
        y_min = int(bbox.ymin * h - 75)
        box_w = int(bbox.width * w + 20)
        box_h = int(bbox.height * h + 95)

        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w, x_min + box_w)
        y_max = min(h, y_min + box_h)

        if verbose:
            print(f"Bounding box:")
            print(f"\tx_min={x_min}, y_min={y_min}, x_max={x_max}, y_max={y_max}")

        face_crop = image[y_min:y_max, x_min:x_max]

        filename = Path(path).name
        try:
            cv2.imwrite(str(FACES_DIR / filename), face_crop)
            if verbose:
                print(f"Cropped image saved to: {FACES_DIR}")
        except Exception as e:
            print(f"Warning: failed to save cropped image:\n{e}")

        return face_crop
