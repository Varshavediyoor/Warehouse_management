import os
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from security.models import SecurityPOInvoice


# 🔹 QC CHECKLIST MASTER
class QCChecklistItem(models.Model):
    CATEGORY_CHOICES = [
        ("ELECTRONICS", "Electronics"),
        ("FOOD", "Food"),
        ("MEDICAL", "Medical"),
        ("CLOTHING", "Clothing"),
        ("CHEMICALS", "Chemicals"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # 🔹 What this check is about
    description = models.TextField(blank=True)

    # 🔹 How to inspect (step-by-step)
    inspection_instructions = models.TextField(blank=True)

    # 🔹 Visual reference
    reference_image = models.ImageField(
        upload_to="qc_checklist/",
        null=True,
        blank=True
    )

    is_mandatory = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


# 🔹 QC INSPECTION (STANDALONE)
class QCInspection(models.Model):
    STATUS_CHOICES = [
        ("PASS", "Pass"),
        ("FAIL", "Fail"),
        ("HOLD", "Hold"),
    ]

    security_invoice = models.ForeignKey(     # 👈 ADD THIS FIELD
        SecurityPOInvoice,
        on_delete=models.CASCADE,
        related_name="qc_inspections",
        null=True,
        blank=True
    )

    # 🔹 BASIC REFERENCES
    po_number = models.CharField(max_length=50)
    po_item_id = models.IntegerField(null=True, blank=True)  # reference only

    product_name = models.CharField(max_length=255)
    variant_name = models.CharField(max_length=255, blank=True)

    # 🔹 CATEGORY (USED FOR RULES)
    category = models.CharField(
        max_length=50,
        help_text="ELECTRONICS / FOOD / MEDICAL / CLOTHING /CHEMICALS",
    )

    invoice_number = models.CharField(max_length=50)

    inspector = models.ForeignKey(User, on_delete=models.PROTECT,null=True,
    blank=True)

    # 🔹 QUANTITY
    received_qty = models.PositiveIntegerField()
    approved_qty = models.PositiveIntegerField()
    rejected_qty = models.PositiveIntegerField()

    # 🔹 EXPIRY + BATCH (NEW)
    batch_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Mandatory for FOOD / MEDICAL",
    )

    manufacture_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text="Mandatory for FOOD / MEDICAL",
    )

    # 🔹 RESULT
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)

    inspected_at = models.DateTimeField(auto_now_add=True)

    pdf_processed = models.BooleanField(default=False)

    def clean(self):
        errors = {}

        # ================= CATEGORY RULES =================

        if self.category == "FOOD":
            if not self.expiry_date:
                errors["expiry_date"] = "Expiry date is mandatory for FOOD"
            if not self.manufacture_date:
                errors["manufacture_date"] = "Manufacture date is mandatory for FOOD"
            if not self.batch_number:
                errors["batch_number"] = "Batch number is mandatory for FOOD"

        elif self.category == "MEDICAL":
            if not self.expiry_date:
                errors["expiry_date"] = "Expiry date is mandatory for MEDICAL"
            if not self.batch_number:
                errors["batch_number"] = "Batch number is mandatory for MEDICAL"

        elif self.category == "CHEMICALS":
            if not self.expiry_date:
                errors["expiry_date"] = "Expiry date is mandatory for CHEMICALS"
            if not self.batch_number:
                errors["batch_number"] = "Batch number is mandatory for CHEMICALS"
            # manufacture_date intentionally NOT required

        # ELECTRONICS / CLOTHING → no date rules

        # ================= COMMON VALIDATIONS =================

        if self.expiry_date and self.expiry_date < timezone.now().date():
            errors["expiry_date"] = "Product is expired"

        if (
            self.received_qty is not None
            and self.approved_qty is not None
            and self.rejected_qty is not None
        ):
            if self.approved_qty + self.rejected_qty != self.received_qty:
                errors["quantity"] = (
                    "Approved + Rejected quantity must equal Received quantity"
                )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.product_name} | {self.status}"
    

# 🔹 PHOTO PATH (✔ CORRECT LOCATION)
import os
from datetime import datetime

def qc_photo_path(instance, filename):
    # sanitize invoice number
    invoice_no = instance.inspection.invoice_number.replace("/", "_")

    # checklist id
    checklist_id = instance.checklist_item.id

    # file extension
    ext = filename.split(".")[-1]

    # current date & time
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H-%M-%S")

    # final filename
    new_filename = f"{time}_check_{checklist_id}.{ext}"

    return os.path.join(
        "qc_photos",
        year,
        month,
        day,
        "po-invoice",
        invoice_no,
        "qc_checklist",
        new_filename,
    )



# 🔹 CHECKLIST ANSWERS


class QCInspectionAnswer(models.Model):
    inspection = models.ForeignKey(
        QCInspection,
        related_name="answers",
        on_delete=models.CASCADE
    )
    checklist_item = models.ForeignKey(
        QCChecklistItem,
        on_delete=models.CASCADE
    )

    answer = models.BooleanField()  # checkbox
    remarks = models.TextField(blank=True)

    photo = models.ImageField(
        upload_to=qc_photo_path,
        null=True,
        blank=True
    )
