from django.urls import path
from .views import (
    POInvoiceUploadView,
    VehicleEntryView,
    entry_pass_pdf_view,
    entry_pass_preview,
    entry_pass_view,
    VehicleExitView,
    supervisor_dashboard,
    scan_barcode_view,
    vehicle_entry_dashboard_page, 
    VehicleEntryListAPI

)

app_name = 'security'
urlpatterns = [
    path("upload-po/", POInvoiceUploadView.as_view(), name="security_upload_po"),
    path("vehicle-entry/<int:invoice_id>/", VehicleEntryView.as_view(), name="vehicle_entry"),
    path("entry-pass/<int:entry_id>/", entry_pass_view, name="entry_pass"),
    path("vehicle-exit/<int:entry_id>/", VehicleExitView.as_view(), name="vehicle_exit"),
    path("supervisor/", supervisor_dashboard, name="supervisor_dashboard"),
    path("scan/", scan_barcode_view, name="scan_barcode"),
    path("entry-pass/view/<int:entry_id>/", entry_pass_preview, name="entry_pass_preview"),
    path("entry-pass/pdf/<int:entry_id>/", entry_pass_pdf_view, name="entry_pass_pdf"),
    path("vehicle-dashboard/", vehicle_entry_dashboard_page, name="vehicle_dashboard"),
    path("api/vehicle-entries/", VehicleEntryListAPI.as_view(), name="api_vehicle_entry_list"),

]
