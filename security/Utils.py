import os
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from django.conf import settings

# def po_invoice_upload_path(instance, filename):
#     today = date.today()
#     ext = filename.split('.')[-1]
#     return f"Invoices/po_invoices/{today.year}/{today.month}/{today.day}/{instance.po_number}.{ext}"

from django.utils import timezone

from datetime import date

import os
from datetime import datetime

# def po_invoice_upload_path(instance, filename):
#     today = datetime.now()
#     ext = filename.split(".")[-1]
#     return f"invoices/po_invoices/{today.year}/{today.month:02}/{today.day:02}/{instance.po_number}.{ext}"

def po_invoice_upload_path(instance, filename):
    now = datetime.now()
    ext = filename.split(".")[-1]
    time_str = f"{now.hour:02}{now.minute:02}{now.second:02}"
    return (
        # f"{settings.BASE_DIR}/PO_Invoices/{str(now.year)}/{str(now.month)}/{str(now.day)}/{time_str}/{instance.po_number}.{ext}"   
    
        f"PO_Invoices/"
        f"{now.year}/{now.month:02}/{now.day:02}/"
        f"{time_str}/"
        f"{instance.po_number}.{ext}"
    )
# def vehicle_entry_image_path(instance, filename):
#     today = datetime.now()
#     ext = filename.split(".")[-1]
#     return (
#         f"Security/{today.year}/{today.month:02}/{today.day:02}/"
#         f"/po-invoice/{instance.po_invoice.po_number}/Security/entry/{filename}"
#     )


def vehicle_entry_image_path(instance, filename):
    today = datetime.now()
    return (
        f"security/{today.year}/{today.month:02}/{today.day:02}/"
        f"po-invoice/{instance.po_invoice.po_number}/Security/entry/{filename}"
    )


def vehicle_exit_image_path(instance, filename):
    today = datetime.now()
    return (
        f"Security/{today.year}/{today.month:02}/{today.day:02}/"
        f"/po-invoice/{instance.po_invoice.po_number}/Security/exit/{filename}"
    )




def generate_entry_pass_pdf(entry, barcode_path):

    file_name = f"entry_pass_{entry.id}.pdf"
    folder = os.path.join(settings.MEDIA_ROOT, "security", "entry_pass")
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, file_name)
    security_name = entry.checked_by.username if entry.checked_by else "N/A"

    doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>WAREHOUSE ENTRY PASS</b>", styles["Title"]))
    elements.append(Spacer(1, 8))

    data = [
        ["PO Number", entry.po_invoice.po_number],
        ["Vehicle No", entry.vehicle_number or "Not Detected"],
        
        ["Gate No", entry.gate_no],
        ["Entry Time", entry.entry_time.strftime("%d-%m-%Y %I:%M %p")],
        ["Security", security_name],
    ]

    table = Table(data, colWidths=[80*mm, 80*mm])
    elements.append(table)
    elements.append(Spacer(1, 10))

    if barcode_path:
        elements.append(Image(barcode_path, width=120, height=40))

    doc.build(elements)

    return file_path
