import cv2
import tempfile

def capture_temp_photo():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise Exception("Camera not accessible")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise Exception("Failed to capture image")

    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    cv2.imwrite(tmp.name, frame)
    return tmp.name



