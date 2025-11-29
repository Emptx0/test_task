from typing import Tuple

from src.pipelines import (
    extract_id,
    extract_face,
    image_to_base64,
)


def run_extraction_pipeline(
        path: str,
        verbose: bool = False,
        id_kwargs=None,
        face_kwargs=None
) -> Tuple[str, str]:

    if id_kwargs is None:
        id_kwargs = {}
    if face_kwargs is None:
        face_kwargs = {}

    passport_id = extract_id(
        path,
        verbose=verbose,
        **id_kwargs
    )

    face_img = extract_face(
        path,
        verbose = verbose,
        **face_kwargs
    )

    face_img_encoded = image_to_base64(face_img, verbose)

    return passport_id, face_img_encoded
