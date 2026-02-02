from django.db import models

from admin_app.models import Warehouse
from django.core.files import File
from io import BytesIO
import barcode
from barcode.writer import ImageWriter

# Create your models here.

class Zone(models.Model):
    
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Rack(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,null=True, blank=True)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.zone}-{self.number}"


class Shelf(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    level = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rack}-{self.level}"


class Bin(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,null=True, blank=True)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE,null=True, blank=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE,null=True, blank=True)

    bin_number = models.CharField(max_length=10, null=True, blank=True)

    capacity = models.IntegerField(default=100)

    location_code = models.CharField(max_length=100, blank=True)
    barcode_image = models.ImageField(upload_to="location_barcodes/", blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.location_code and self.zone and self.rack and self.shelf:
            self.location_code = f"{self.zone.name}-{self.rack.number}-{self.shelf.level}-{self.bin_number}"

        super().save(*args, **kwargs)

        if not self.barcode_image:
            self.generate_barcode()
            super().save(update_fields=["barcode_image"])


    def generate_barcode(self):
        CODE128 = barcode.get_barcode_class("code128")
        barcode_obj = CODE128(self.location_code, writer=ImageWriter())

        buffer = BytesIO()
        barcode_obj.write(buffer)

        filename = f"{self.location_code}.png"
        self.barcode_image.save(filename, File(buffer), save=False)

    def __str__(self):
        return self.location_code




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    has_expiry = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CategoryVariant(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="variants",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"



class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductVariantValue(models.Model):
    product = models.ForeignKey(Product, related_name="variant_values", on_delete=models.CASCADE)
    variant = models.ForeignKey(CategoryVariant, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product} - {self.variant.name}: {self.value}"





