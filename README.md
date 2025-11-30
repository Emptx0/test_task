# Trainee Test

## Overview
This repository provides a minimal FastAPI application that accepts passport image uploads, runs simple preprocessing,\
OCR with EasyOCR and face detection with MediaPipe. \
Returns the cropped face image as base64 string together with the `passport_id`. \

## Core Features
- Clean environment-based configuration (`.env`).
- FastAPI endpoint for image upload and processing.
- OCR using **EasyOCR** with automatic CPU fallback.
- Face detection using **MediaPipe** with automatic CPU fallback.
- Simple image preprocessing and Base64 encoding utilities.
- Optional saving of cropped faces and intermediate images.
- Full Docker support for containerized deployment.
- Debug mode.

## Detection Pipeline

### 1. OCR (EasyOCR)
**EasyOCR** extracts visible text from the document image. \
If GPU (CUDA/MPS) is not available, it logs a warning and automatically **falls back to CPU**. \
The most lightweight tool for OCR. \
\
Output includes:
- Detected text segments with confidence scores (if enabled via `.env`)
- Selected passport ID from detected text.

### 2. Face Detection (MediaPipe)
The project uses **MediaPipe Face Detection** (`mp.solutions.face_detection`). \
MediaPipe is works on both CPU and GPU. \
**CPU fallback** if no GPU or acceleration backend is available, MediaPipe automatically \
runs on CPU without errors. \
CPU performance is still fast because MediaPipe models are lightweight and quantized. \
\
Output includes:
- Optional detected face bounding box (if enabled via `.env`).
- Cropped face image as `numpy.ndarray`.


## Configurable processing
Controlled via `.env`.\
You can enable/disable:
- Debug mode `DEBUG`.
- Saving detected faces `SAVE_FACES`.
- Saving processed images `SAVE_PROCESSED_IMAGES`.
- Startup preprocessing `START_WITH_PROCESSING`.

## Setup and run locally
1. Create virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2. Create `.env` file in the project root:
    ```aiignore
    DEBUG=false
    SAVE_FACES=true
    SAVE_PROCESSED_IMAGES=false
    START_WITH_PROCESSING=false
    ```
3. Run the server:
    ```bash
    uvicorn src.main:app
    ```

## Setup with Docker
1. Create `.env` file in the project root:
    ```aiignore
    DEBUG=false
    SAVE_FACES=true
    SAVE_PROCESSED_IMAGES=false
    START_WITH_PROCESSING=false
    ```
2. Build image:
    ```bash
    docker build -t passport_app .
    ```
2. Run container:
    ```bash
    docker run -p 8000:8000 --env-file .env --name passport_app passport_app
    ```
    - `-p 8000:8000` - maps port `8000` inside the container to port `8000` on your host machine, \
   allowing you to access the FastAPI app via `http://localhost:8000`.
   -  `--env-file .env` - loads all environment variables from your local `.env` file into the container.
   - `--name passport_app` — assigns a custom name to the container, making it easier to manage \
   (e.g., `docker stop passport_app`, `docker logs passport_app`).
   - `passport_app` - the name of the Docker image to run.

## Example of request
Request (via curl):
 ```bash
 curl -X POST "http://localhost:8000/api/v1/upload" -F "image=@/path/to/passport_image.jpg"
 ```
Response:
 ```aiignore
 {
 "passport_id": "A12345678",
 "face_image": "/9j/4AAQSkZJRgABAQAAAQABAAD... (truncated base64)"
 }
 ```
