from rest_framework import serializers
from .models import (
    QCInspection,
    QCInspectionAnswer,
)


# =====================================================
# BASE QC INSPECTION (LIST, SIMPLE DETAIL)
# =====================================================
class QCInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCInspection
        fields = "__all__"
        read_only_fields = ["inspector"]


# =====================================================
# QC DECISION (STATUS UPDATE ONLY)
# =====================================================
class QCDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCInspection
        fields = ["status", "remarks"]


# =====================================================
# QC CHECKLIST ANSWER (NESTED - FULL DETAILS)
# =====================================================
class QCInspectionAnswerSerializer(serializers.ModelSerializer):
    checklist_name = serializers.CharField(
        source="checklist_item.name",
        read_only=True
    )
    mandatory = serializers.BooleanField(
        source="checklist_item.is_mandatory",
        read_only=True
    )
    description = serializers.CharField(
        source="checklist_item.description",
        read_only=True,
        allow_blank=True,
        allow_null=True
    )
    inspection_instructions = serializers.CharField(
        source="checklist_item.inspection_instructions",
        read_only=True,
        allow_blank=True,
        allow_null=True
    )
    reference_image = serializers.SerializerMethodField()

    class Meta:
        model = QCInspectionAnswer
        fields = [
            "id",
            "checklist_item",
            "checklist_name",
            "mandatory",
            "description",
            "inspection_instructions",
            "reference_image",
            "answer",
            "remarks",
        ]

    def get_reference_image(self, obj):
        if obj.checklist_item.reference_image:
            return obj.checklist_item.reference_image.url
        return None


# =====================================================
# QC DETAIL (WITH FULL CHECKLIST INFO)
# =====================================================
class QCInspectionDetailSerializer(serializers.ModelSerializer):
    answers = QCInspectionAnswerSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = QCInspection
        fields = "__all__"
        read_only_fields = ["inspector"]
