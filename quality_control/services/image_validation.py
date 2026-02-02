import cv2

def validate_qc_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return "Image could not be read"

    # 🔍 Blur detection
    blur_score = cv2.Laplacian(img, cv2.CV_64F).var()

    if blur_score < 100:
        return f"Image is blurry (score={int(blur_score)}). Please retake."

    # 🔆 Brightness check
    brightness = img.mean()

    if brightness < 30:
        return f"Image is too dark (brightness={int(brightness)}). Please retake."

    return None
