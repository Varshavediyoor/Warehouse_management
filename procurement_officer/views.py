

from django.contrib import messages
from inventory_manager.models import Category, CategoryVariant, Product, ProductVariantValue
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PurchaseOrder, Vendor
from .serializers import PurchaseOrderSerializer, VendorSerializer
from admin_app.models import Notification
from collections import defaultdict


class VendorListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VendorRetrieveUpdateDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Vendor, pk=pk)

    def get(self, request, pk):
        serializer = VendorSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = VendorSerializer(
            self.get_object(pk),
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=204)



@login_required 
def vendor_list_page(request):
    vendors = Vendor.objects.all()
    return render(request, "vendor/vendor_list.html", {"vendors": vendors})

@login_required
def vendor_form_page(request, pk=None):
    vendor = None
    if pk:
        vendor = get_object_or_404(Vendor, pk=pk)

    if request.method == "POST":
        data = {
            "vendor_name": request.POST.get("vendor_name"),
            "email": request.POST.get("email"),
            "phone_number": request.POST.get("phone_number"),
            "address": request.POST.get("address"),
            "contact_person": request.POST.get("contact_person"),
            "gst_no": request.POST.get("gst_no"),
            "is_active": True if request.POST.get("is_active") == "on" else False,
        }

        if vendor:
            for key, value in data.items():
                setattr(vendor, key, value)
            vendor.save()
            messages.success(request, "Vendor updated successfully")
        else:
            Vendor.objects.create(**data)
            messages.success(request, "Vendor created successfully")

        return redirect("vendor_list")

    return render(request, "vendor/vendor_form.html", {"vendor": vendor})

@login_required
def vendor_delete_page(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)

    if request.method == "POST":
        vendor.delete()
        messages.success(request, "Vendor deleted successfully")
        return redirect("vendor_list")

    return render(request, "vendor/vendor_confirm_delete.html", {"vendor": vendor})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import PurchaseOrder, PurchaseOrderItem
# from .forms import PurchaseOrderForm, PurchaseOrderItemForm

@login_required
def purchase_order_list_page(request):
    pos = PurchaseOrder.objects.all().order_by("-id")
    return render(request, "purchase/po_list.html", {"pos": pos})


from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def purchase_order_form_page(request, pk=None):
    po = None

    if pk:
        po = get_object_or_404(PurchaseOrder, pk=pk)
        if po.status != "DRAFT":
            messages.error(request, "Submitted PO cannot be edited")
            return redirect("po_list")

    # 🔹 Products grouped by category
    products_by_category = defaultdict(list)
    for p in Product.objects.select_related("category"):
        products_by_category[p.category_id].append(p)

    # 🔹 Variants grouped by product → variant name
    variants_by_product = defaultdict(lambda: defaultdict(list))
    for pv in ProductVariantValue.objects.select_related("variant", "product"):
        variants_by_product[pv.product_id][pv.variant.name].append(pv)

    if request.method == "POST":

        if "add_item" in request.POST:
            if not po:
                messages.error(request, "Save Purchase Order first")
                return redirect("po_create")

            category_id = request.POST.get("category")
            product_id = request.POST.get("product")
            quantity = request.POST.get("quantity")

            product_variant_values = [
                value for key, value in request.POST.items()
                if key.startswith("variant_") and value
            ]

            item = PurchaseOrderItem.objects.create(
                purchase_order=po,
                category_id=category_id,
                product_id=product_id,
                quantity=quantity,
            )

            if product_variant_values:
                item.product_variant.set(product_variant_values)

            messages.success(request, "Item added successfully")
            return redirect("po_update", pk=po.pk)

        # SAVE / UPDATE PO
        vendor_id = request.POST.get("vendor")
        order_date = request.POST.get("order_date")
        remarks = request.POST.get("remarks")

        if vendor_id and order_date:
            if not po:
                po = PurchaseOrder.objects.create(
                    vendor_id=vendor_id,
                    order_date=order_date,
                    remarks=remarks,
                    created_by=request.user,
                )
                return redirect("po_update", pk=po.pk)
            else:
                po.vendor_id = vendor_id
                po.order_date = order_date
                po.remarks = remarks
                po.save()
                messages.success(request, "Purchase Order updated")

    return render(request, "purchase/po_form.html", {
        "po": po,
        "vendors": Vendor.objects.all(),
        "items": po.items.all() if po else [],
        "categories": Category.objects.all(),
        "products_by_category": dict(products_by_category),
        "variants_by_product": {
            k: dict(v) for k, v in variants_by_product.items()
        },
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from .models import PurchaseOrder

@login_required
def submit_purchase_order(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)

    if not po.items.exists():
        messages.error(request, "Add at least one item before submitting.")
        return redirect("po_items", pk=pk)

    # Submit the PO if not already submitted
    if po.status != "SUBMITTED":
        po.status = "SUBMITTED"
        po.save()

    # ✅ Always notify inventory managers
    inventory_users = User.objects.filter(
        userprofile__role="INVENTORY_MANAGER",
        is_active=True
    )

    for user in inventory_users:
        # Avoid duplicate notifications for the same PO
        if not Notification.objects.filter(recipient=user, message__icontains=po.po_number).exists():
            Notification.objects.create(
                recipient=user,
                message=f"Purchase Order {po.po_number} is pending approval."
            )

    messages.success(request, "Purchase Order submitted for approval.")
    return redirect("po_detail", pk=pk)


@login_required
def submitted_purchase_order_detail(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, "purchase/submitted_po.html", {"po": po})

# @login_required
# def submit_purchase_order(request, pk):
#     po = get_object_or_404(PurchaseOrder, pk=pk)

#     if not po.items.exists():
#         messages.error(request, "Add at least one item")
#         return redirect("po_items", pk=pk)

#     po.status = "SUBMITTED"
#     po.save()
#     messages.success(request, "PO Submitted")
#     return redirect("po_list")

# @login_required
# def po_approve_reject_page(request, pk):
#     po = get_object_or_404(PurchaseOrder, pk=pk)

#     if request.method == "POST":
#         po.status = "APPROVED" if request.POST["action"] == "approve" else "REJECTED"
#         po.approved_by = request.user
#         po.approved_at = timezone.now()
#         po.save()
#         return redirect("po_list")

#     return render(request, "purchase/po_decide.html", {"po": po})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class PurchaseOrderListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pos = PurchaseOrder.objects.all()
        return Response(PurchaseOrderSerializer(pos, many=True).data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PurchaseOrderRUDAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(PurchaseOrder, pk=pk)

    def get(self, request, pk):
        return Response(PurchaseOrderSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        po = self.get_object(pk)
        if po.status != "DRAFT":
            return Response({"error": "Locked"}, status=400)

        serializer = PurchaseOrderSerializer(po, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        po = self.get_object(pk)
        if po.status != "DRAFT":
            return Response({"error": "Cannot delete"}, status=400)
        po.delete()
        return Response(status=204)

class SubmitPurchaseOrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        po = get_object_or_404(PurchaseOrder, pk=pk)
        if po.status != "DRAFT":
            return Response({"error": "Invalid"}, status=400)

        po.status = "SUBMITTED"
        po.save()
        return Response({"status": "submitted"})

# class ApproveRejectPurchaseOrderAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         po = get_object_or_404(PurchaseOrder, pk=pk)
#         action = request.data.get("action")

#         if po.status != "SUBMITTED":
#             return Response({"error": "Invalid state"}, status=400)

#         po.status = "APPROVED" if action == "approve" else "REJECTED"
#         po.approved_by = request.user
#         po.approved_at = timezone.now()
#         po.save()

#         return Response({"status": po.status})
