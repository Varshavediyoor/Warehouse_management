from datetime import datetime
import os
from time import timezone

import cv2
from django.conf import settings
import numpy as np
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .serializers import *
from .services import verify_po
from .ocr import extract_vehicle_number
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
# ---------------------------
# 1. UPLOAD PO INVOICE
# ---------------------------
from .document_reader import read_text_from_image, read_text_from_pdf, extract_po_details

# class POInvoiceUploadView(APIView):

#     def get(self, request):
#         return render(request, "security/upload_invoice.html")

#     def post(self, request):

#         # -------------------------
#         # STEP A — FILE UPLOAD
#         # -------------------------
#         if "uploaded_invoice" in request.FILES:

#             uploaded = request.FILES["uploaded_invoice"]
#             now = datetime.now()

#             # temp_path = f"{settings.BASE_DIR}/PO_Invoices/{str(now.year)}/{str(now.month)}/{str(now.day)}/{now.strftime("%H_%M_%S")}/{uploaded.name}"
#             temp_path = os.path.join(
#                 settings.BASE_DIR,
#                 "PO_Invoices",
#                 str(now.year),
#                 f"{now.month:02}",
#                 f"{now.day:02}",
#                 now.strftime("%H_%M_%S"),
#             )
#             os.makedirs(temp_path, exist_ok=True)

#         # --- force filename as PO number ---
#             # po_no = request.POST.get("po_number") or "UNKNOWN_PO"
#             po_no = os.path.splitext(uploaded.name)[0]
#             ext = os.path.splitext(uploaded.name)[1]  # .pdf
#             filename = f"{po_no}{ext}"

#             full_path = os.path.join(temp_path, filename)

#             # --- save file ---
            
#             with open(full_path, "wb+") as f:
#                 for chunk in uploaded.chunks():
#                     f.write(chunk)

#             # READ CONTENT
#             if uploaded.name.lower().endswith(".pdf"):
#                 text = read_text_from_pdf(temp_path)
#             else:
#                 text = read_text_from_image(temp_path)

#             po_no, vendor, created_by = extract_po_details(text)

#             # SAVE OCR RESULT (NOT VERIFIED YET)
#             invoice = SecurityPOInvoice.objects.create(
#                 po_number=po_no or "",
#                 vendor_name=vendor or "",
#                 created_by=created_by or "",
#                 uploaded_invoice=uploaded,
#                 system_verified=False,
#                 remarks="Waiting for manual confirmation",
#                 checked_by=request.user
#             )

#             # SHOW CONFIRMATION PAGE
#             return render(request, "security/confirm_invoice.html", {
#                 "invoice": invoice
#             })
class POInvoiceUploadView(LoginRequiredMixin, View):

 

    def get(self, request):
        return render(request, "security/upload_invoice.html")

    def post(self, request):

        # =====================================================
        # STEP 1 — FILE UPLOAD + OCR
        # =====================================================
        if "uploaded_invoice" in request.FILES:

            uploaded = request.FILES["uploaded_invoice"]
            now = datetime.now()

            # ✅ SAVE INSIDE MEDIA_ROOT (CRITICAL FIX)
            folder_path = os.path.join(
                settings.MEDIA_ROOT,
                "PO_Invoices",
                str(now.year),
                f"{now.month:02}",
                f"{now.day:02}",
                now.strftime("%H_%M_%S"),
            )
            os.makedirs(folder_path, exist_ok=True)

            # ---------- TEMP FILE SAVE ----------
            ext = os.path.splitext(uploaded.name)[1].lower()
            temp_filename = uploaded.name
            temp_file_path = os.path.join(folder_path, temp_filename)

            with open(temp_file_path, "wb+") as f:
                for chunk in uploaded.chunks():
                    f.write(chunk)

            # ---------- OCR READ ----------
            if ext == ".pdf":
                text = read_text_from_pdf(temp_file_path)
            else:
                text = read_text_from_image(temp_file_path)

            # MUST RETURN 4 VALUES
            po_no, vendor, created_by, category = extract_po_details(text)

            # ---------- RENAME FILE USING PO NUMBER ----------
            final_po_no = po_no or "UNKNOWN_PO"
            final_filename = f"{final_po_no}{ext}"
            final_file_path = os.path.join(folder_path, final_filename)

            if temp_file_path != final_file_path:
                os.rename(temp_file_path, final_file_path)

            # ---------- SAVE DB RECORD ----------
            invoice = SecurityPOInvoice.objects.create(
                po_number=final_po_no,
                vendor_name=vendor or "",
                created_by=created_by or "",
                category=category,
                uploaded_invoice=final_file_path.replace(
                    str(settings.MEDIA_ROOT) + os.sep, ""
                ),
                system_verified=False,
                remarks="Waiting for manual confirmation",
                checked_by=request.user
            )

            return render(
                request,
                "security/confirm_invoice.html",
                {"invoice": invoice}
            )

        # =====================================================
        # STEP 2 — MANUAL CONFIRM
        # =====================================================
        else:

            invoice_id = request.POST.get("invoice_id")
            invoice = SecurityPOInvoice.objects.get(id=invoice_id)

            invoice.po_number = request.POST.get("po_number")
            invoice.vendor_name = request.POST.get("vendor_name")
            invoice.created_by = request.POST.get("created_by")

            # Allow manual category correction
            invoice.category = request.POST.get(
                "category",
                invoice.category
            )

            verified = verify_po(
                invoice.po_number,
                invoice.vendor_name,
                invoice.created_by
            )

            invoice.system_verified = verified
            invoice.remarks = "" if verified else "Manual verification failed"
            invoice.save()

            if verified:
                return redirect("security:vehicle_entry", invoice.id)

            return render(
                request,
                "security/rejected.html",
                {"invoice": invoice}
            )

# ---------------------------
# 2. VEHICLE ENTRY
# ---------------------------
from .barcode_utils import generate_barcode_image
from django.core.files.base import ContentFile
from quality_control.models import QCInspection

def save_opencv_image(uploaded_file, filename):
    """
    uploaded_file: InMemoryUploadedFile
    filename: final filename (front_1.jpg etc)
    """

    # Read bytes → numpy
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)

    # Decode image using OpenCV
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image file")

    # Encode back to JPG
    success, encoded = cv2.imencode(".jpg", img)
    if not success:
        raise ValueError("OpenCV encoding failed")

    return ContentFile(encoded.tobytes(), name=filename)

class VehicleEntryView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "security/vehicle_entry.html"
    permission_classes = [IsAuthenticated]  # 🔹 Only logged-in users allowed

    def get(self, request, invoice_id):
        return Response({"invoice_id": invoice_id})

    def post(self, request, invoice_id):

        # Fetch invoice safely
        invoice = get_object_or_404(SecurityPOInvoice, id=invoice_id)

        # ✅ request.user is guaranteed to be a User instance because of IsAuthenticated
        user = request.user

        entry = VehicleEntry.objects.create(
            po_invoice=invoice,
            checked_by=user,
            vehicle_name=request.POST["vehicle_name"],
            vehicle_number=request.POST.get("vehicle_number_manual", ""),
            driver_name=request.POST.get("driver_name", ""),
            gate_no=request.POST["gate_no"],
        )

        # -------- OPEN-CV IMAGE SAVE --------
        def save_image(file_list, attr_name, filename):
            if file_list:
                setattr(
                    entry,
                    attr_name,
                    save_opencv_image(file_list[0], filename)
                )

        save_image(request.FILES.getlist("front_images"), "front_image", "front_1.jpg")
        save_image(request.FILES.getlist("rear_images"), "rear_image", "rear_1.jpg")
        save_image(request.FILES.getlist("side_images"), "side_image", "side_1.jpg")
        if "driver_image" in request.FILES:
            entry.driver_image = save_opencv_image(request.FILES["driver_image"], "driver.jpg")

        # -------- BARCODE --------
        barcode_text = f"{invoice.po_number}|{entry.gate_no}"
        barcode_img = generate_barcode_image(barcode_text)
        entry.barcode.save(
            f"{invoice.po_number}_entry.png",
            ContentFile(barcode_img.read()),
            save=False
        )

        entry.save()

        # -------- CREATE QC FOR VERIFIED INVOICE --------
        QCInspection.objects.get_or_create(
            security_invoice=invoice,
            defaults={
                "po_number": invoice.po_number,
                "invoice_number": "",
                "category": invoice.category,
                "product_name": "",
                "received_qty": 0,
                "approved_qty": 0,
                "rejected_qty": 0,
                "status": "HOLD",
            }
        )

        return redirect("security:entry_pass_preview", entry.id)

# class VehicleEntryView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = "security/vehicle_entry.html"

#     def get(self, request, invoice_id):
#         return Response({"invoice_id": invoice_id})
#     def post(self, request, invoice_id):

#         invoice = SecurityPOInvoice.objects.get(id=invoice_id)

#         user = request.user if request.user.is_authenticated else None

#         entry = VehicleEntry.objects.create(
#             po_invoice=invoice,
#             checked_by=user,
#             vehicle_name=request.POST["vehicle_name"],
#             driver_name=request.POST.get("driver_name", ""),
#             gate_no=request.POST["gate_no"],
#         )

#         # -------- OCR VEHICLE NUMBER FROM FIRST FRONT IMAGE --------
#         front_images = request.FILES.getlist("front_images")
#         entry.vehicle_number = request.POST.get("vehicle_number_manual", "")
 
#     # -------- SAVE IMAGES DIRECTLY INTO VehicleEntry --------

#         if request.FILES.getlist("front_images"):
#             entry.front_image = request.FILES.getlist("front_images")[0]

#         if request.FILES.getlist("rear_images"):
#             entry.rear_image = request.FILES.getlist("rear_images")[0]

#         if request.FILES.getlist("side_images"):
#             entry.side_image = request.FILES.getlist("side_images")[0]

#         if "driver_image" in request.FILES:
#             entry.driver_image = request.FILES["driver_image"]

#         # -------- BARCODE --------
#         barcode_text = f"{invoice.po_number}|{entry.gate_no}"
#         barcode_img = generate_barcode_image(barcode_text)

#         entry.barcode.save(
#             f"{invoice.po_number}_entry.png",
#             ContentFile(barcode_img.read()),
#             save=False
#         )
#         entry.save()

#         return redirect("Security:entry_pass_preview", entry.id)

def entry_pass_preview(request, entry_id):
    entry = get_object_or_404(
        VehicleEntry.objects.select_related("po_invoice", "checked_by"),
        id=entry_id
    )

    return render(request, "security/entry_pass_view.html", {
        "entry": entry
    })

from django.http import FileResponse
from .Utils import generate_entry_pass_pdf

def entry_pass_pdf_view(request, entry_id):

    entry = get_object_or_404(
        VehicleEntry.objects.select_related("po_invoice", "checked_by"),
        id=entry_id
    )
    
    barcode_path = entry.barcode.path if entry.barcode else None

    pdf_path = generate_entry_pass_pdf(entry, barcode_path)

    return FileResponse(
        open(pdf_path, "rb"),
        as_attachment=True,
        filename=f"EntryPass_{entry.po_invoice.po_number}.pdf"
    )

# ---------------------------
# 3. ENTRY PASS
# ---------------------------
from django.http import FileResponse
from .Utils import generate_entry_pass_pdf

def entry_pass_view(request, entry_id):

    # entry = VehicleEntry.objects.select_related("po_invoice").get(id=entry_id)
    entry = VehicleEntry.objects.select_related("po_invoice", "checked_by").get(id=entry_id)

    barcode_path = entry.barcode.path if entry.barcode else None

    pdf_path = generate_entry_pass_pdf(entry, barcode_path)

    return FileResponse(
        open(pdf_path, "rb"),
        as_attachment=True,
        filename=f"EntryPass_{entry.po_invoice.po_number}.pdf"
    )


# ---------------------------
# 4. VEHICLE EXIT
# ---------------------------
class VehicleExitView(APIView):
    def get(self, request, entry_id):
        return render(request, "security/vehicle_exit.html", {"entry_id": entry_id})

    def post(self, request, entry_id):
        entry = VehicleEntry.objects.get(id=entry_id)
        barcode_text = f"EXIT|ENTRY:{entry.id}|TIME:{timezone.now()}"

        VehicleExit.objects.create(
            entry=entry,
            returned_qty=request.POST["returned_qty"],
            remarks=request.POST.get("remarks", ""),
            front_image=request.FILES["front"],
            rear_image=request.FILES["rear"],
            side_image=request.FILES["side"],
        )
        return redirect("security:supervisor_dashboard")

# ---------------------------
# 5. SUPERVISOR PAGE
# ---------------------------
def supervisor_dashboard(request):
    entries = VehicleEntry.objects.all().select_related("po_invoice")
    return render(request, "security/supervisor_dashboard.html", {"entries": entries})

def scan_barcode_view(request):
    code = request.GET.get("code")  # PO-2026-0016|3

    po_no, gate_no = code.split("|")

    entry = VehicleEntry.objects.select_related(
        "po_invoice", "checked_by"
    ).get(
        po_invoice__po_number=po_no,
        gate_no=gate_no
    )

    return render(request, "security/scan_result.html", {"entry": entry})

def entry_pass_preview(request, entry_id):
    entry = get_object_or_404(
        VehicleEntry.objects.select_related("po_invoice", "checked_by"),
        id=entry_id
    )

    return render(request, "security/entry_pass_view.html", {
        "entry": entry
    })
