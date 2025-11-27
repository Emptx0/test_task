import cv2
import mediapipe as mp

from pathlib import Path


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
IMAGE_DIR = Path("/home/tym/projects/test_task/sample_data")

IMAGE_FILES = [str(p) for p in IMAGE_DIR.iterdir() if p.is_file()]
IMAGE_FILES = ["/home/tym/projects/test_task/sample_data/Examples-of-ID-cards-a-to-c-showcase-examples-of-bona-fide-generated-print.png"]

with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Draw face detections of each face.
        if not results.detections:
            continue
        annotated_image = image.copy()
        for detection in results.detections:
            print('Nose tip:')
            print(mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
            mp_drawing.draw_detection(annotated_image, detection)
        cv2.imwrite('tmp/annotated_image' + str(idx) + '.png', annotated_image)
