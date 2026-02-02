from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .models import QCInspection
from .services.qc_service import (
    ensure_answers,
    process_qc_submission,
    get_qc_invoice_report,
)


# =====================================================
# QC DETAIL (HTML)
# =====================================================
@login_required
def qc_detail(request, qc_id):
    """
    Render-only view.
    All data loading & submission handled via APIs.
    """
    return render(
        request,
        "quality_control/qc_detail.html",
        {
            "qc_id": qc_id   # 👈 REQUIRED FOR JS → API
        }
    )

# =====================================================
# QC LIST (HTML)
# =====================================================
@login_required
def qc_inspection_list(request):
    inspections = QCInspection.objects.all().order_by("-inspected_at")
    return render(
        request,
        "quality_control/qc_inspection_list.html",
        {"inspections": inspections},
    )


# =====================================================
# QC INVOICE REPORT (HTML)
# =====================================================
@login_required
def qc_invoice_report(request, invoice_number):
    inspections = get_qc_invoice_report(invoice_number)
    if not inspections:
        return render(request, "404.html")

    return render(
        request,
        "quality_control/qc_invoice_report.html",
        {
            "invoice_number": invoice_number,
            "inspections": inspections,
        }
    )


##UPLOAD INVOICE####

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def qc_invoice_upload(request):
    return render(
        request,
        "quality_control/qc_invoice_upload.html"
    )



from django.contrib.auth.decorators import login_required
from .models import QCInspection
from security.models import VehicleEntry


@login_required
def qc_work_page(request):
    """
    QC work page for gate-verified invoices only
    """

    qc_list = (
        QCInspection.objects
        .select_related("security_invoice")
        .filter(security_invoice__system_verified=True)
        .order_by("-inspected_at")
    )

    rows = []

    for qc in qc_list:
        vehicle_entry = (
            VehicleEntry.objects
            .filter(po_invoice=qc.security_invoice)
            .order_by("-entry_time")
            .first()
        )

        rows.append({
            "qc": qc,
            "vehicle_entry": vehicle_entry,
        })

    return render(
        request,
        "quality_control/qc_work_page.html",
        {
            "inspections": rows
        }
    )


from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os

from weasyprint import HTML

from .models import QCInspection


def qc_invoice_report_pdf(request, invoice_number):
    inspections = (
        QCInspection.objects
        .filter(invoice_number=invoice_number)
        .prefetch_related("answers__checklist_item")
    )

    if not inspections.exists():
        return HttpResponse("No QC data found", status=404)

    template = get_template("quality_control/qc_invoice_report_pdf.html")

    html = template.render({
        "invoice_number": invoice_number,
        "inspections": inspections,
    })

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="QC_Report_{invoice_number}.pdf"'
    )
    return response
