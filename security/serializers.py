from rest_framework import serializers
from .models import *
from django.urls import reverse

class POInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPOInvoice
        fields = "__all__"


class VehicleEntrySerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(source="po_invoice.po_number", read_only=True)
    checked_by = serializers.CharField(source="checked_by.username", read_only=True)

    entry_pass_url = serializers.SerializerMethodField()
    report_url = serializers.SerializerMethodField()

    front_image_url = serializers.SerializerMethodField()
    rear_image_url = serializers.SerializerMethodField()
    side_image_url = serializers.SerializerMethodField()
    driver_image_url = serializers.SerializerMethodField()
    barcode_url = serializers.SerializerMethodField()

    class Meta:
        model = VehicleEntry
        fields = [
            "id",
            "po_number",
            "gate_no",
            "vehicle_name",
            "vehicle_number",
            "driver_name",
            "checked_by",
            "entry_time",
            "entry_pass_url",
            "report_url",
            "front_image_url",
            "rear_image_url",
            "side_image_url",
            "driver_image_url",
            "barcode_url",
        ]

    # ---------- helpers ----------
    def _abs(self, request, url):
        return request.build_absolute_uri(url) if request and url else None

    # ---------- links ----------
    def get_entry_pass_url(self, obj):
        request = self.context.get("request")
        if not request:
            return None

        url = reverse(
            "security:entry_pass_preview",
            kwargs={"entry_id": obj.id}
        )
        return request.build_absolute_uri(url)

    def get_report_url(self, obj):
        request = self.context.get("request")
        if not request:
            return None

        url = reverse("security:scan_barcode")
        code = f"{obj.po_invoice.po_number}|{obj.gate_no}"
        return request.build_absolute_uri(f"{url}?code={code}")

    # ---------- images ----------
    def get_front_image_url(self, obj):
        request = self.context.get("request")
        return self._abs(request, obj.front_image.url if obj.front_image else None)

    def get_rear_image_url(self, obj):
        request = self.context.get("request")
        return self._abs(request, obj.rear_image.url if obj.rear_image else None)

    def get_side_image_url(self, obj):
        request = self.context.get("request")
        return self._abs(request, obj.side_image.url if obj.side_image else None)

    def get_driver_image_url(self, obj):
        request = self.context.get("request")
        return self._abs(request, obj.driver_image.url if obj.driver_image else None)

    def get_barcode_url(self, obj):
        request = self.context.get("request")
        return self._abs(request, obj.barcode.url if obj.barcode else None)


class VehicleExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleExit
        fields = "__all__"
