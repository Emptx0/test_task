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

DATA_DIR = BASE_DIR / "data"

DEBUG_DIR = DATA_DIR / "debug"
FACES_DIR = DATA_DIR / "faces"  # Directory for saving facial images

PROCESSED_IMAGES_DIR = DEBUG_DIR / "processed_images"  # Directory for saving processed images
UPLOAD_DIR = DEBUG_DIR / "temp_uploads"  # Temporary storage for uploaded images during API requests

DATA_DIR.mkdir(exist_ok=True)
DEBUG_DIR.mkdir(exist_ok=True)
FACES_DIR.mkdir(exist_ok=True)
PROCESSED_IMAGES_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
