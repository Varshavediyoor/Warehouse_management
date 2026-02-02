from datetime import datetime
import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from ..models import QCInspection, QCInspectionAnswer, QCChecklistItem
from .ocr import (
    extract_text_from_pdf,
    extract_invoice_items,
    extract_invoice_fields,
    extract_invoice_fields_with_pdfplumber,
)
from .image_validation import validate_qc_image


# =====================================================
# UTIL
# =====================================================
def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ("%d-%b-%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    return None


# =====================================================
# OCR → CREATE QC
# =====================================================
def create_qc_from_invoice_pdf(pdf_path, inspector):
    items, source = extract_invoice_items(pdf_path)
    if not items:
        raise ValidationError("No items found in invoice")

    text = extract_text_from_pdf(pdf_path)
    invoice_data = extract_invoice_fields(text)

    invoice_number = invoice_data.get("invoice_number")
    category = invoice_data.get("category")

    if not invoice_number or not category:
        raise ValidationError("Invoice number or category missing")

    qc_ids = []

    for item in items:
        qc = QCInspection.objects.create(
            po_number="AUTO-PO",
            product_name=item.get("description", ""),
            category=category,
            invoice_number=invoice_number,
            inspector=inspector,
            received_qty=item.get("quantity", 0),
            approved_qty=0,
            rejected_qty=0,
            batch_number=item.get("batch"),
            expiry_date=parse_date(item.get("expiry")),
            status="HOLD",
        )
        qc_ids.append(qc.id)

    return qc_ids


# =====================================================
# ENSURE CHECKLIST ANSWERS
# =====================================================
def ensure_answers(qc):
    items = QCChecklistItem.objects.filter(
        category=qc.category, active=True
    )
    for item in items:
        QCInspectionAnswer.objects.get_or_create(
            inspection=qc,
            checklist_item=item,
            defaults={"answer": False},
        )


# =====================================================
# PROCESS QC SUBMISSION
# =====================================================
def process_qc_submission(qc, post_data, user):
    qc.inspector = qc.inspector or user
    qc.received_qty = int(post_data.get("received_qty", 0))
    qc.approved_qty = int(post_data.get("approved_qty", 0))
    qc.rejected_qty = int(post_data.get("rejected_qty", 0))
    qc.batch_number = post_data.get("batch_number")
    qc.manufacture_date = parse_date(post_data.get("manufacture_date"))
    qc.expiry_date = parse_date(post_data.get("expiry_date"))

    qc.full_clean()
    qc.save()

    failed = False
    answers = qc.answers.select_related("checklist_item")

    for ans in answers:
        ans.answer = bool(post_data.get(f"check_{ans.id}"))
        ans.remarks = post_data.get(f"remarks_{ans.id}", "")

        photo_data = post_data.get(f"photo_{ans.id}")
        if photo_data:
            fmt, img = photo_data.split(";base64,")
            ext = fmt.split("/")[-1]
            image = ContentFile(
                base64.b64decode(img),
                name=f"check_{ans.id}.{ext}",
            )
            ans.photo.save(image.name, image, save=True)

            error = validate_qc_image(ans.photo.path)
            if error:
                raise ValidationError(error)

        ans.save()

        if ans.checklist_item.is_mandatory and not ans.answer:
            failed = True

    qc.status = "FAIL" if failed else "PASS"
    qc.save()

    return qc.status


# =====================================================
# QC REPORT
# =====================================================
def get_qc_invoice_report(invoice_number):
    return (
        QCInspection.objects
        .filter(invoice_number=invoice_number)
        .prefetch_related("answers__checklist_item")
    )


#################

from .ocr import (
    extract_text_from_pdf,
    extract_invoice_fields,
    extract_invoice_items,
)

def fill_qc_from_gate_invoice(qc):
    """
    QC reads invoice PDF ONLY ONCE (safe)
    """

    if qc.pdf_processed:
        return

    if not qc.security_invoice or not qc.security_invoice.uploaded_invoice:
        return

    pdf_path = qc.security_invoice.uploaded_invoice.path
    print("🔍 QC OCR reading PDF:", pdf_path)

    text = extract_text_from_pdf(pdf_path)
    print("📄 OCR TEXT:\n", text)

    invoice_data = extract_invoice_fields(text)

    # ✅ FIX 1: unpack properly
    items, source = extract_invoice_items(pdf_path)

    data_found = False

    # ---------- HEADER ----------
    if isinstance(invoice_data, dict):
        if invoice_data.get("invoice_number"):
            qc.invoice_number = invoice_data["invoice_number"]
            data_found = True

        if invoice_data.get("category"):
            qc.category = invoice_data["category"]
            data_found = True

    # ---------- ITEM ----------
    if items and isinstance(items, list):
        item = items[0]

        if item.get("description"):
            qc.product_name = item["description"]
            data_found = True

        if item.get("quantity") is not None:
            qc.received_qty = item["quantity"]
            data_found = True

        if item.get("batch"):
            qc.batch_number = item["batch"]

        qc.expiry_date = parse_date(item.get("expiry"))
        qc.manufacture_date = parse_date(item.get("manufacture"))

    # ❌ REMOVE THIS BAD FALLBACK
    # qc.invoice_number = qc.po_number  ❌

    # ✅ ONLY mark processed if OCR worked
    if data_found:
        qc.pdf_processed = True
        qc.save()
        print("✅ QC OCR DONE for QC ID:", qc.id)
    else:
        print("⚠️ QC OCR FAILED — will retry next load")
