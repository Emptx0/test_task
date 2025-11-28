import cv2
import mediapipe as mp

from pathlib import Path


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
IMAGE_DIR = Path("/home/tym/projects/test_task/sample_data")

IMAGE_FILES = [str(p) for p in IMAGE_DIR.iterdir() if p.is_file()]

with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        h, w, _ = image.shape
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.detections:
            continue

        for i, detection in enumerate(results.detections):
            bbox = detection.location_data.relative_bounding_box

            x_min = int(bbox.xmin * w - 20)
            y_min = int(bbox.ymin * h - 75)
            box_w = int(bbox.width * w + 20)
            box_h = int(bbox.height * h + 90)

            # Коректуємо межі, щоб не вилізти за картинку
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(w, x_min + box_w)
            y_max = min(h, y_min + box_h)

            # Вирізаємо обличчя
            face_crop = image[y_min:y_max, x_min:x_max]

            # Зберігаємо
            cv_path = f"tmp/crop_{idx}_{i}.png"
            cv2.imwrite(cv_path, face_crop)
