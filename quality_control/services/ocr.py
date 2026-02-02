import pytesseract
from pdf2image import convert_from_path


import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import shutil
import os
import sys


def set_tesseract_cmd():
    # 1. Check if user set an environment variable
    env_path = os.environ.get("TESSERACT_CMD")
    if env_path and os.path.exists(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
        return

    # 2. Common Windows paths
    if sys.platform.startswith("win"):
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for path in common_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return

    # 3. Linux / MacOS (assumes tesseract installed via package manager)
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return

    # 4. If nothing found, raise informative error
    raise EnvironmentError(
        "Tesseract executable not found. "
        "Install Tesseract OCR: https://github.com/tesseract-ocr/tesseract "
        "or set the TESSERACT_CMD environment variable."
    )

# Set it once
set_tesseract_cmd()
POPPLER_PATH = r"C:\poppler\Library\bin"


def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH,
        dpi=300
    )

    full_text = ""
    for page in pages:
        full_text += pytesseract.image_to_string(
            page,
            config=(
                "--psm 6 "
                "-c tessedit_char_whitelist="
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "abcdefghijklmnopqrstuvwxyz"
                "0123456789.-"
            )
        )

    return full_text

import re

def extract_items(ocr_text):
    items = []
    lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]

    for line in lines:
        # STRICT match: item + quantity is mandatory
        match = re.match(
            r"^(ITM-\d+)\s+(.+?)\s+(\d+)$",
            line
        )

        if match:
            items.append({
                "item_code": match.group(1),
                "description": match.group(2).strip(),
                "quantity": int(match.group(3)),
            })

    return items



import re

def extract_invoice_fields(ocr_text):
    """
    Extract header-level invoice fields from OCR/PDF text
    """

    def find(pattern):
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    invoice_number = (
        find(r"Invoice\s*Number[:\s]*([A-Z0-9\-]+)")
        or find(r"InvoiceNumber\s*([A-Z0-9\-]+)")
    )

    category = (
        find(r"Category[:\s]*([A-Z]+)")
        or find(r"Category([A-Z]+)")
    )

    return {
        "invoice_number": invoice_number,
        "category": category,
    }

####pdf plumber###
def extract_items_with_pdfplumber(pdf_path):
    items = []

    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    for line in lines:
        # FOOD invoice pattern
        match = re.match(
            r"^([A-Z0-9\-]+)\s+(.+?)\s+([A-Z0-9\-]+)\s+(\d{2}-\w{3}-\d{4})\s+(\d{2}-\w{3}-\d{4})\s+(\d+)$",
            line
        )
        if match:
            items.append({
                "item_code": match.group(1),
                "description": match.group(2),
                "batch": match.group(3),
                "manufacture": match.group(4),
                "expiry": match.group(5),
                "quantity": int(match.group(6)),
            })

    return items



def extract_invoice_items(pdf_path):
    """
    Smart extractor:
    1️⃣ Try pdfplumber
    2️⃣ Fallback to OCR
    """

    # 🔹 Try structured PDF first
    items = extract_items_with_pdfplumber(pdf_path)
    if items:
        return items, "PDF"

    # 🔹 Fallback to OCR
    text = extract_text_from_pdf(pdf_path)
    items = extract_items(text)

    return items, "OCR"



def extract_invoice_fields_with_pdfplumber(pdf_path):
    import pdfplumber
    import re

    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    def find(pattern, group=1):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(group).strip() if match else None

    return {
        # group(2) → actual invoice value
        "invoice_number": find(
            r"Invoice\s*(?:No|Number)[:\s]*([A-Z0-9\-]+)",
            group=1,
        ),

        "category": find(
            r"Category[:\s]*([A-Z]+)",
            group=1,
        ),
    }


