from rest_framework import serializers
from .models import *

class POInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPOInvoice
        fields = "__all__"

class VehicleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleEntry
        fields = "__all__"

class VehicleExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleExit
        fields = "__all__"
