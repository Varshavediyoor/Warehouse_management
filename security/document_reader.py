import pytesseract
import cv2
import pdfplumber
import re
import os
from django.conf import settings
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"






def read_text_from_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not readable")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)
    return text


def read_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# -------- FIELD EXTRACTOR ----------
import re

def extract_po_details(text):

    po_no = ""
    vendor = ""
    created_by = ""
    category = ""

    clean = re.sub(r'\s+', ' ', text).upper()

    # ----------------
    # PO NUMBER
    # ----------------
    po_match = re.search(r'PO[-\s]*\d{4}[-\s]*\d+', clean)
    if po_match:
        po_no = po_match.group().replace(" ", "")

    # ----------------
    # VENDOR / SUPPLIER
    # ----------------
    vendor_patterns = [
        r'VENDOR\s*[:\-]\s*(.*?)(CREATED|PREPARED|ISSUED|APPROVED|DATE|PO\s|INVOICE)',
        r'SUPPLIER\s*[:\-]\s*(.*?)(CREATED|PREPARED|ISSUED|APPROVED|DATE|PO\s|INVOICE)',
        r'VENDOR NAME\s*[:\-]\s*(.*?)(CREATED|PREPARED|ISSUED|APPROVED|DATE|PO\s|INVOICE)',
    ]

    for p in vendor_patterns:
        m = re.search(p, clean)
        if m:
            vendor = m.group(1).strip().title()
            break

    # ----------------
    # CREATED / PREPARED / ISSUED BY
    # ----------------
    created_patterns = [
        r'CREATED\s*BY\s*[:\-]\s*(.*?)(APPROVED|SIGNATURE|DEPARTMENT|DATE|PO\s|INVOICE|$)',
        r'PREPARED\s*BY\s*[:\-]\s*(.*?)(APPROVED|SIGNATURE|DEPARTMENT|DATE|PO\s|INVOICE|$)',
        r'ISSUED\s*BY\s*[:\-]\s*(.*?)(APPROVED|SIGNATURE|DEPARTMENT|DATE|PO\s|INVOICE|$)',
        r'PROCUREMENT\s*OFFICER\s*[:\-]\s*(.*?)(APPROVED|SIGNATURE|DEPARTMENT|DATE|PO\s|INVOICE|$)',
    ]

    for p in created_patterns:
        m = re.search(p, clean)
        if m:
            created_by = m.group(1).strip().title()
            break

    # ----------------
    # CATEGORY (NEW + IMPORTANT)
    # ----------------
    CATEGORY_KEYWORDS = {
        "FOOD": ["FOOD", "GROCERY", "EDIBLE"],
        "CHEMICALS": ["CHEMICAL", "CHEMICALS", "ACID", "SOLVENT"],
        "MEDICAL": ["MEDICAL", "PHARMA", "DRUG"],
        "ELECTRONICS": ["ELECTRONIC", "ELECTRONICS"],
        "CLOTHING": ["CLOTHING", "GARMENT", "APPAREL"],
    }

    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in clean:
                category = cat
                break
        if category:
            break

    print("EXTRACTED =>", po_no, "|", vendor, "|", created_by, "|", category)

    return po_no, vendor, created_by, category
