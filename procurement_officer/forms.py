from django import forms
from .models import PurchaseOrder, PurchaseOrderItem

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ["vendor", "order_date", "remarks"]
        widgets = {
            "order_date": forms.DateInput(attrs={"type": "date"}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
        }


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ["category", "product", "product_variant", "quantity"]
