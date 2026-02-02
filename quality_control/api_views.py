from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication

from .models import QCInspection
from .serializers import (
    QCInspectionSerializer,
    QCInspectionDetailSerializer,
)

from .services.qc_service import (
    create_qc_from_invoice_pdf,
    process_qc_submission,
    get_qc_invoice_report,
)


# =====================================================
# CSRF EXEMPT AUTH (DEFINED ONCE)
# =====================================================
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# =====================================================
# QC LIST + CREATE
# =====================================================
class QCListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        inspections = QCInspection.objects.filter(
            security_invoice__system_verified=True
        )

        status_param = request.GET.get("status")
        invoice_param = request.GET.get("invoice")

        if status_param:
            inspections = inspections.filter(status=status_param.upper())
        if invoice_param:
            inspections = inspections.filter(invoice_number=invoice_param)

        inspections = inspections.order_by("-inspected_at")
        serializer = QCInspectionSerializer(inspections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QCInspectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(inspector=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# =====================================================
# QC DETAIL
# =====================================================

from quality_control.services.qc_service import (
    ensure_answers,
    fill_qc_from_gate_invoice,
)

class QCDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, qc_id):
        try:
            qc = QCInspection.objects.select_related(
                "security_invoice"
            ).get(id=qc_id)

            # 1️⃣ Read PDF only ONCE
            fill_qc_from_gate_invoice(qc)

            # 2️⃣ Guarantee category
            if not qc.category:
                qc.category = "FOOD"
                qc.save()

            # 3️⃣ Create checklist
            ensure_answers(qc)

            serializer = QCInspectionDetailSerializer(qc)
            return Response(serializer.data)

        except Exception as e:
            print("QC DETAIL ERROR:", e)
            return Response(
                {"error": str(e)},
                status=500
            )


# =====================================================
# OCR UPLOAD → CREATE QC
# =====================================================

import tempfile
import os
class QCOCRUploadAPI(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):

        pdf_file = request.FILES.get("invoice")
        if not pdf_file:
            return Response(
                {"error": "Invoice PDF required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        inspector = request.user if request.user.is_authenticated else None

        try:
            # ✅ SAVE UPLOADED FILE TO TEMP PATH
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                for chunk in pdf_file.chunks():
                    tmp.write(chunk)
                pdf_path = tmp.name

            qc_ids = create_qc_from_invoice_pdf(
                pdf_path=pdf_path,
                inspector=inspector
            )

            # optional cleanup
            os.remove(pdf_path)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "OCR processed successfully",
                "qc_ids": qc_ids,
            },
            status=status.HTTP_201_CREATED,
        )

# =====================================================
# FINAL QC SUBMIT (PASS / FAIL)
# =====================================================
from django.http import QueryDict
from django.core.exceptions import ValidationError

class QCSubmitAPI(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, qc_id):
        qc = QCInspection.objects.get(id=qc_id)

        post_data = QueryDict("", mutable=True)

        # quantities
        post_data["received_qty"] = str(request.data.get("received_qty", 0))
        post_data["approved_qty"] = str(request.data.get("approved_qty", 0))
        post_data["rejected_qty"] = str(request.data.get("rejected_qty", 0))

        # batch details
        post_data["batch_number"] = request.data.get("batch_number", "")
        post_data["manufacture_date"] = request.data.get("manufacture_date", "")
        post_data["expiry_date"] = request.data.get("expiry_date", "")

        # checklist answers
        for ans in request.data.get("answers", []):
            answer_id = ans["answer_id"]

            if ans.get("answer"):
                post_data[f"check_{answer_id}"] = "on"

            post_data[f"remarks_{answer_id}"] = ans.get("remarks", "")

            if ans.get("photo"):
                post_data[f"photo_{answer_id}"] = ans["photo"]

        # ✅ HANDLE VALIDATION ERRORS PROPERLY
        try:
            final_status = process_qc_submission(
                qc,
                post_data,
                request.user,
            )

        except ValidationError as e:
            return Response(
                {
                    "message": "QC validation failed",
                    "errors": e.messages,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "QC completed",
                "final_status": final_status,
            },
            status=status.HTTP_200_OK,
        )
# =====================================================
# QC INVOICE REPORT
# =====================================================
class QCInvoiceReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, invoice_number):
        inspections = get_qc_invoice_report(invoice_number)

        if not inspections.exists():
            return Response(
                {"error": "Invoice not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = []

        for qc in inspections:
            answers = []
            for ans in qc.answers.all():
                answers.append({
                    "checklist_item": ans.checklist_item.name,
                    "answer": ans.answer,
                    "remarks": ans.remarks,
                    "photo": ans.photo.url if ans.photo else None,
                })

            data.append({
                "inspection_id": qc.id,
                "product_name": qc.product_name,
                "category": qc.category,
                "received_qty": qc.received_qty,
                "approved_qty": qc.approved_qty,
                "rejected_qty": qc.rejected_qty,
                "status": qc.status,
                "answers": answers,
            })

        return Response({
            "invoice_number": invoice_number,
            "inspection_count": inspections.count(),
            "inspections": data,
        })
