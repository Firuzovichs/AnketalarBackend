import cv2
from dataclasses import dataclass

@dataclass
class FaceCheckResult:
    has_face: bool
    faces_count: int = 0
    reason: str | None = None

def detect_face_opencv(image_path: str) -> FaceCheckResult:
    img = cv2.imread(image_path)
    if img is None:
        return FaceCheckResult(False, reason="image_read_failed")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

    return FaceCheckResult(bool(len(faces)), faces_count=len(faces), reason=None if len(faces) else "no_face_detected")
