from django.urls import path
from .views import qc_invoice_upload
from .views import (
    qc_detail,
    qc_inspection_list,
    qc_invoice_report,
    qc_invoice_report_pdf
)
from .api_views import (
    QCListCreateAPI,
    QCDetailAPI,
    QCOCRUploadAPI,
    QCSubmitAPI,
    QCInvoiceReportAPI,
)
from .views import qc_work_page



urlpatterns = [
    # =========================
    # REST APIs
    # =========================
    path("api/qc/", QCListCreateAPI.as_view(), name="api_qc_list"),
    path("api/qc/<int:qc_id>/", QCDetailAPI.as_view(), name="api_qc_detail"),
    path("api/qc/ocr/", QCOCRUploadAPI.as_view(), name="api_qc_ocr"),
    path("api/qc/<int:qc_id>/submit/", QCSubmitAPI.as_view(), name="api_qc_submit"),
    path(
        "api/qc/report/<str:invoice_number>/",
        QCInvoiceReportAPI.as_view(),
        name="api_qc_invoice_report",
    ),

    # =========================
    # HTML PAGES
    # =========================
    path("qc/", qc_inspection_list, name="qc_list"),
    path("qc/<int:qc_id>/", qc_detail, name="qc_detail"),
    path(
        "qc/report/<str:invoice_number>/",
        qc_invoice_report,
        name="qc_invoice_report",
    ),

    path("qc/invoice/upload/", qc_invoice_upload, name="qc_invoice_upload"),

    path("qc/work/", qc_work_page, name="qc_work_page"),

    path(
    "qc/report/<str:invoice_number>/pdf/",
    qc_invoice_report_pdf,
    name="qc_invoice_report_pdf",
),


]
