from typing import Tuple
import extract_id, extract_face


def run_extraction_pipeline(path: str, verbose: bool = False):  # TODO -> Tuple[str, str]:
    passport_id = extract_id.extract_id(
        path,
        verbose=verbose,
    )
    face_img = extract_face.extract_face(
        path,
        verbose = verbose,
    )

    return passport_id, face_img