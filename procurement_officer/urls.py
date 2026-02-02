
from django import views
from django.urls import path
from .views import (
    
    vendor_list_page,
    vendor_form_page,
    vendor_delete_page,
    VendorListCreateAPI,
    VendorRetrieveUpdateDeleteAPI,
    # HTML pages
    purchase_order_list_page,
    purchase_order_form_page,
    submit_purchase_order,submitted_purchase_order_detail,
    # po_approve_reject_page,

    # APIs
    PurchaseOrderListCreateAPI,
    PurchaseOrderRUDAPI,
    SubmitPurchaseOrderAPI,
    # ApproveRejectPurchaseOrderAPI,
)

urlpatterns = [

    # ---------- HTML PAGES ----------
    path("api/vendors/", vendor_list_page, name="vendor_list"),
    path("api/vendors/create/", vendor_form_page, name="vendor_create"),
    path("api/vendors/<int:pk>/edit/", vendor_form_page, name="vendor_update"),
    path("api/vendors/<int:pk>/delete/", vendor_delete_page, name="vendor_delete"),

    # ---------- APIs ----------
    path("api/vendors/", VendorListCreateAPI.as_view(), name="api_vendor_list_create"),
    path("api/vendors/<int:pk>/", VendorRetrieveUpdateDeleteAPI.as_view(), name="api_vendor_rud"),

    # =======================
    # HTML PAGES
    # =======================

    # List all Purchase Orders
    path("purchase-orders/", purchase_order_list_page, name="po_list"),
    path("purchase-orders/create/", purchase_order_form_page, name="po_create"),
    path("purchase-orders/<int:pk>/edit/", purchase_order_form_page, name="po_update"),


    # Submit Purchase Order
    path(
        "purchase-orders/<int:pk>/submit/",
        submit_purchase_order,
        name="po_submit",
    ),

    

    path(
    "submit/<int:pk>/",
    submitted_purchase_order_detail,
    name="po_detail",
    ),

    # # Approve / Reject (View-only before decision)
    # path(
    #     "purchase-orders/<int:pk>/decision/",
    #     po_approve_reject_page,
    #     name="po_decide",
    # ),

    # =======================
    # REST APIs (DRF)
    # =======================

    # List + Create PO
    path(
        "api/purchase-orders/",
        PurchaseOrderListCreateAPI.as_view(),
        name="api_po_list_create",
    ),

    # Retrieve / Update / Delete (DRAFT only)
    path(
        "api/purchase-orders/<int:pk>/",
        PurchaseOrderRUDAPI.as_view(),
        name="api_po_rud",
    ),

    # Submit PO
    path(
        "api/purchase-orders/<int:pk>/submit/",
        SubmitPurchaseOrderAPI.as_view(),
        name="api_po_submit",
    ),

    # # Approve / Reject PO
    # path(
    #     "api/purchase-orders/<int:pk>/decision/",
    #     ApproveRejectPurchaseOrderAPI.as_view(),
    #     name="api_po_decide",
    # ),

    
]
