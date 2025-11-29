from fastapi import APIRouter, UploadFile, File, HTTPException

from pathlib import Path
from src.config import UPLOAD_DIR

from src.pipelines import run_extraction_pipeline


router = APIRouter(prefix="/api/v1")

@router.post("/upload")
async def upload(image: UploadFile = File(...)):
    if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG/PNG allowed.")

    image_path = Path(UPLOAD_DIR) / image.filename

    try:
        contents = await image.read()
        with open(image_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file:{e}")

    try:
        passport_id, face_img_encoded = run_extraction_pipeline(path=str(image_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error:{e}")

    return {
        "passport_id": passport_id,
        "face_image": face_img_encoded
    }
