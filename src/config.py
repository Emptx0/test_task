from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # Project directory
FACES_DIR = BASE_DIR / "data/faces"  # Directory for saving facial images
PROCESSED_IMAGES_DIR = BASE_DIR / "data/processed_images"  # Directory for saving processed images

FACES_DIR.mkdir(exist_ok=True)
PROCESSED_IMAGES_DIR.mkdir(exist_ok=True)