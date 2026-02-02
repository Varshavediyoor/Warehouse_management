from django.urls import path
from .views import (
    ApproveRejectPurchaseOrderAPI,
    CategoryListAPI,
    CategoryViewSet,
    ProductViewSet,
    location_master_page,
    category_master_page,
    LocationMasterAPI,
    po_approve_reject_page,
    product_master_page
)

app_name = "inventory_manager"

urlpatterns = [

    # ---------------- PAGES ----------------
    path("locations/", location_master_page, name="location_master"),
    path("categories/", category_master_page, name="category_master"),
    # -------- PRODUCT PAGE --------
    path("products/", product_master_page, name="product_master"),

    # ---------------- APIs -----------------
    path("api/locations/", LocationMasterAPI.as_view(), name="api_locations"),

    # CATEGORY APIs (LIST + CREATE)
    path(
        "api/categories/",
        CategoryViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="api_categories",
    ),

    # CATEGORY APIs (RETRIEVE + UPDATE + DELETE)
    path(
        "api/categories/<int:pk>/",
        CategoryViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }),
        name="api_category_detail",
    ),
    

    # -------- APIs --------
    path(
        "api/products/",
        ProductViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "api/products/<int:pk>/",
        ProductViewSet.as_view({
            "put": "update",
            "delete": "destroy",
        })),

    path("api/category-list/", CategoryListAPI.as_view({
        "get": "list",
    })),

    # Approve / Reject (View-only before decision)
    path(
        "purchase-orders/<int:pk>/decision/",
        po_approve_reject_page,
        name="po_decide",
    ),

    # Approve / Reject PO
    path(
        "api/purchase-orders/<int:pk>/decision/",
        ApproveRejectPurchaseOrderAPI.as_view(),
        name="api_po_decide",
    ),
]
