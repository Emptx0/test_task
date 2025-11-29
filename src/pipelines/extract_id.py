import easyocr
import cv2
import re

from pathlib import Path
from src.config import PROCESSED_IMAGES_DIR

import time
import logging


logger = logging.getLogger(__name__)

reader = easyocr.Reader(["en"])

FORBIDDEN_RE = re.compile(r"[!@#$%^&*()\[\]{};:'\"<>,./?~\\|+\-=]")


def extract_id(
        path: str,
        verbose: bool = False,
        image_preprocessing: bool = False,
        save_preprocessed_image: bool = False,
        _fallback: bool = False
) -> str:

    start = time.perf_counter()
    if verbose:
        logger.info("ID extraction started...\n")

    image = cv2.imread(path)
    if image is None:
        raise ValueError("Failed to read input image.")

    # Image preprocess
    if image_preprocessing:
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

        processed_image = binary

        if save_preprocessed_image:
            filename = Path(path).name

            try:
                cv2.imwrite(str(PROCESSED_IMAGES_DIR / filename), binary)
                if verbose:
                    logger.info(f"Processed image saved to: {str(PROCESSED_IMAGES_DIR)}\n")
            except Exception as e:
                logger.warning(f"Failed to save preprocessed image:\n{e}")

    else:
        processed_image = image

    # OCR
    try:
        result = reader.readtext(processed_image)
    except Exception:
        raise ValueError("OCR engine failed to process the image.")

    if not result:
        raise ValueError("No text detected.")

    passport_id = None
    best_prob = 0.0

    for _, text, prob in result:

        if verbose:
            logger.info(f"{text}, prob={prob}")

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

        if verbose:
            logger.info(f"\nNo passport id detected.\n"
                        f"Trying image_preprocessing={not image_preprocessing} ...\n")

        if not _fallback:
            return extract_id(
                path=path,
                verbose=verbose,
                image_preprocessing=not image_preprocessing,
                save_preprocessed_image=save_preprocessed_image,
                _fallback=True
            )

        raise ValueError("Passport ID could not be found on the image.")

    if verbose:
        duration = time.perf_counter() - start
        logger.info(f"Completed in {duration:.3f} s.\n")

    return passport_id
