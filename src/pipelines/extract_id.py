import easyocr
import cv2
import re


reader = easyocr.Reader(["en"])


FORBIDDEN_RE = re.compile(r"[!@#$%^&*()\[\]{};:\'\"<>,./?~\\|+\-=]")


def extract_id(path: str) -> str:
    image = cv2.imread(path)
    if image is None:
        raise ValueError("Failed to read input image.")

    # Image preprocess
    try:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception:
        raise ValueError("Failed to convert image to grayscale.")

    try:
        _, binary = cv2.threshold(
            grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    except Exception:
        raise ValueError("Failed to apply thresholding to the image.")

    # OCR
    passport_id = None
    best_prob = 0.0

    try:
        result = reader.readtext(binary)
    except Exception:
        raise ValueError("OCR engine failed to process the image.")

    if not result:
        raise ValueError("No text detected.")

    for _, text, prob in result:
        for word in text.split():

            if len(word) != 9:
                continue
            if not any(c.isdigit() for c in word):
                continue
            if word.isalpha():
                continue
            if any(c.islower() for c in word):
                continue
            if FORBIDDEN_RE.search(word):
                continue

            if prob > best_prob:
                best_prob = prob
                passport_id = word

    if passport_id is None:
        raise ValueError("Passport ID could not be found on the image.")

    return passport_id
