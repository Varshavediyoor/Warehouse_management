from django.shortcuts import get_object_or_404, render
from inventory_manager.models import Bin, CategoryVariant, Category,  Rack, Shelf, Zone
from inventory_manager.serializers import BinSerializer, CategoryVariantSerializer, CategorySerializer, RackSerializer, ShelfSerializer, ZoneSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required


class LocationMasterAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "zones": ZoneSerializer(Zone.objects.all(), many=True).data,
            "racks": RackSerializer(Rack.objects.all(), many=True).data,
            "shelves": ShelfSerializer(Shelf.objects.all(), many=True).data,
            "bins": BinSerializer(Bin.objects.all(), many=True).data,
        })

    def post(self, request):
        action = request.data.get("action")

        if action == "add_zone":
            serializer = ZoneSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "ok"})

        elif action == "add_rack":
            serializer = RackSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "ok"})

        elif action == "add_shelf":
            serializer = ShelfSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "ok"})

        elif action == "add_bin":

            shelf_id = request.data.get("shelf")
            bin_number = request.data.get("bin_number")
            capacity = request.data.get("capacity", 100)

            if not shelf_id or not bin_number:
                return Response({"error": "Shelf and Bin number required"}, status=400)

            shelf = Shelf.objects.get(id=shelf_id)
            rack = shelf.rack
            zone = rack.zone

            bin_obj = Bin.objects.create(
                zone=zone,
                rack=rack,
                shelf=shelf,
                bin_number=bin_number,
                capacity=capacity,
            )

            return Response({
                "status": "ok",
                "bin_id": bin_obj.id,
                "location": bin_obj.location_code
            })


        elif action == "delete_zone":
            Zone.objects.filter(id=request.data.get("id")).delete()
            return Response({"status": "deleted"})

        elif action == "delete_rack":
            Rack.objects.filter(id=request.data.get("id")).delete()
            return Response({"status": "deleted"})

        elif action == "delete_shelf":
            Shelf.objects.filter(id=request.data.get("id")).delete()
            return Response({"status": "deleted"})

        elif action == "delete_bin":
            Bin.objects.filter(id=request.data.get("id")).delete()
            return Response({"status": "deleted"})

        return Response({"error": "Invalid action"}, status=400)
    
@login_required
def location_master_page(request):
    return render(request, "inventory/location/location_master.html")


# master/views.py
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, CategoryVariant, Product
from .serializers import CategorySerializer, ProductSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("variants").all()
    serializer_class = CategorySerializer



@api_view(["DELETE"])
def delete_variant(request, pk):
    try:
        variant = CategoryVariant.objects.get(pk=pk)
        variant.delete()
        return Response({"message": "Variant deleted"})
    except CategoryVariant.DoesNotExist:
        return Response({"error": "Not found"}, status=404)




@login_required
def category_master_page(request):
    return render(request, "inventory/product/category_master.html")




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related("variant_values__variant")
    serializer_class = ProductSerializer


class CategoryListAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related("variants")
    serializer_class = CategorySerializer


@login_required
def product_master_page(request):
    return render(request, "inventory/product/product_master.html")



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from procurement_officer.models import PurchaseOrder
from procurement_officer.utils import send_po_approved_email

@login_required
def po_approve_reject_page(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)

    # Optional but recommended: allow only submitted POs
    if po.status != "SUBMITTED":
        return redirect("po_list")

    if request.method == "POST":
        action = request.POST.get("action")

        po.approved_by = request.user
        po.approved_at = timezone.now()

        if action == "approve":
            po.status = "APPROVED"
            po.save()

            # ✅ Send email to vendor
            send_po_approved_email(po)

        elif action == "reject":
            po.status = "REJECTED"
            po.save()

        return redirect("po_list")

    return render(request, "purchase/po_decide.html", {"po": po})



class ApproveRejectPurchaseOrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        po = get_object_or_404(PurchaseOrder, pk=pk)
        action = request.data.get("action")

        if po.status != "SUBMITTED":
            return Response({"error": "Invalid state"}, status=400)

        po.status = "APPROVED" if action == "approve" else "REJECTED"
        po.approved_by = request.user
        po.approved_at = timezone.now()
        po.save()

        return Response({"status": po.status})



@login_required
def purchase_order_list(request):
    pos = PurchaseOrder.objects.all().order_by("-id")
    return render(request, "purchase/po_list.html", {"pos": pos})