from django.db import models
from django.contrib.auth.models import User
from .Utils import po_invoice_upload_path, vehicle_entry_image_path, vehicle_exit_image_path

# -------------------------
# PO INVOICE VERIFICATION
# -------------------------
class SecurityPOInvoice(models.Model):

    CATEGORY_CHOICES = [
        ("FOOD", "Food"),
        ("CHEMICALS", "Chemicals"),
        ("MEDICAL", "Medical"),
        ("ELECTRONICS", "Electronics"),
        ("CLOTHING", "Clothing"),
    ]
    po_number = models.CharField(max_length=30)
    vendor_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)

    
    # ✅ NEW FIELD (IMPORTANT)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True
    )


    uploaded_invoice = models.FileField(upload_to=po_invoice_upload_path)

    system_verified = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    checked_at = models.DateTimeField(auto_now_add=True)

# -------------------------
# VEHICLE ENTRY
# -------------------------

from django.contrib.auth import get_user_model
User = get_user_model()

class VehicleEntry(models.Model):
    po_invoice = models.ForeignKey(SecurityPOInvoice, on_delete=models.CASCADE, related_name="vehicle_entries")
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    vehicle_number = models.CharField(max_length=50, blank=True, null=True)
    vehicle_name = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=50, blank=True)

    front_image = models.ImageField(upload_to=vehicle_entry_image_path,  null=True, blank=True)
    rear_image = models.ImageField(upload_to=vehicle_entry_image_path,  null=True, blank=True)
    side_image = models.ImageField(upload_to=vehicle_entry_image_path,  null=True, blank=True)
    driver_image = models.ImageField(upload_to=vehicle_entry_image_path, null=True, blank=True)

    gate_no = models.CharField(max_length=10)
    entry_time = models.DateTimeField(auto_now_add=True)

    barcode = models.ImageField(upload_to="security/barcodes/", null=True, blank=True)

# -------------------------
# VEHICLE EXIT
# -------------------------
class VehicleExit(models.Model):
    entry = models.OneToOneField(VehicleEntry, on_delete=models.CASCADE, related_name="vehicleexit")

    returned_qty = models.PositiveIntegerField(default=0)
    remarks = models.TextField(blank=True)

    front_image = models.ImageField(upload_to=vehicle_exit_image_path)
    rear_image = models.ImageField(upload_to=vehicle_exit_image_path)
    side_image = models.ImageField(upload_to=vehicle_exit_image_path)

    exit_time = models.DateTimeField(auto_now_add=True)
