import cv2
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# def extract_vehicle_number(image_path):

#     img = cv2.imread(image_path)
#     h, w, _ = img.shape

#     # Crop center where number plate usually exists
#     crop = img[int(h*0.4):int(h*0.7), int(w*0.2):int(w*0.8)]

#     gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
#     gray = cv2.bilateralFilter(gray, 11, 17, 17)

#     text = pytesseract.image_to_string(gray)

#     match = re.search(r'[A-Z]{2}\s*\d{1,2}\s*[A-Z]{1,2}\s*\d{3,4}', text.replace("\n", " "))
#     if match:
#         return match.group().replace(" ", "")

    # return None
# def extract_vehicle_number(image_path):

#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     text = pytesseract.image_to_string(gray)

#     # Indian vehicle pattern example: KL07AB1234
#     match = re.search(r'[A-Z]{2}\s?\d{2}\s?[A-Z]{1,2}\s?\d{3,4}', text)

#     if match:
#         return match.group().replace(" ", "")

#     return None
import cv2
import numpy as np
import pytesseract

def extract_vehicle_number(uploaded_file):
    """
    Accepts Django InMemoryUploadedFile or TemporaryUploadedFile
    """

    # ---- Read image from uploaded file ----
    file_bytes = uploaded_file.read()

    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        print("OCR ERROR: Image decode failed")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    print("VEHICLE OCR TEXT:", text)

    return text.strip()
