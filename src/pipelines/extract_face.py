import cv2
import mediapipe as mp
import numpy as np


def extract_face(path: str, passport_id: str) -> np.ndarray:
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
    ) as face_detection:

        image = cv2.imread(path)
        if image is None:
            raise ValueError("Failed to read input image.")

        h, w, _ = image.shape
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

        face_crop = image[y_min:y_max, x_min:x_max]

        cv_path = f"/home/tym/projects/test_task/tmp/crop_{passport_id}.png"
        cv2.imwrite(cv_path, face_crop)

        return face_crop
