from pathlib import Path
from dotenv import load_dotenv
from os import getenv
import logging


load_dotenv()
DEBUG = getenv("DEBUG", "false").lower() == "true"  # Debug mode from .env
SAVE_FACES = getenv("SAVE_FACES", "false").lower() == "true"
SAVE_PROCESSED_IMAGES = getenv("SAVE_PROCESSED_IMAGES", "false").lower() == "true"
START_WITH_PROCESSING = getenv("START_WITH_PROCESSING", "false").lower() == "true"

# logging config
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s"
)

BASE_DIR = Path(__file__).resolve().parent.parent  # Project directory

FACES_DIR = BASE_DIR / "data/faces"  # Directory for saving facial images
PROCESSED_IMAGES_DIR = BASE_DIR / "data/processed_images"  # Directory for saving processed images
UPLOAD_DIR = BASE_DIR / "uploads"  # Directory for saving uploaded images

FACES_DIR.mkdir(exist_ok=True)
PROCESSED_IMAGES_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
