from django.db import models

# Create your models here.
from django.db import models

from inventory_manager.models import Category, CategoryVariant, Product, ProductVariantValue


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    gst_no = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.vendor_name
    

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max
from inventory_manager.models import Category, Product, ProductVariantValue
 # adjust import if needed

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50, unique=True, blank=True)
    order_date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_pos"
    )
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_pos"
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            year = timezone.now().year
            last = PurchaseOrder.objects.filter(
                po_number__startswith=f"PO-{year}"
            ).aggregate(Max("po_number"))["po_number__max"]

            num = int(last.split("-")[-1]) + 1 if last else 1
            self.po_number = f"PO-{year}-{num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.po_number


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, related_name="items", on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category_variant = models.ManyToManyField(
        CategoryVariant, blank=True
    )
    product_variant = models.ManyToManyField(
        ProductVariantValue, blank=True
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} ({self.quantity})"
    
    