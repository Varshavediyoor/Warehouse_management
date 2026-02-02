from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('password-expired/', views.password_expired, name='password_expired'),
    path("reset-password/", views.reset_password, name="reset_password"),
    path('admin-access-key/', views.admin_access_key, name='admin_access_key'),
    path('switch-language/<str:lang_code>/', views.switch_language, name='switch_language'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('verify-admin-login/', views.verify_admin_login, name='verify_admin_login'),
    path('resend-admin-otp/', views.resend_admin_otp, name='resend_admin_otp'),
    path('admin-dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-logs/', views.admin_logs, name='admin_logs'),
    path('admin-dashboard//profile/', views.admin_profile_view, name='admin_profile_view'),
    path('admin-dashboard/users/', views.admin_user_list, name='admin_user_list'),
    path('admin-dashboard/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin-dashboard/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-dashboard/register/', views.register_user, name='register_user'),
    path('user-login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('admin-dashboard/notifications/', views.admin_notifications, name='admin_notifications'),
    path('dashboard/warehouse-manager/', views.warehouse_manager_dashboard, name='warehouse_manager_dashboard'),
    path('dashboard/inventory-supervisor/', views.inventory_supervisor_dashboard, name='inventory_supervisor_dashboard'),
    path('dashboard/storekeeper/', views.storekeeper_dashboard, name='storekeeper_dashboard'),
    path('dashboard/logistics/', views.logistics_dashboard, name='logistics_dashboard'),
    path('dashboard/finance/', views.finance_dashboard, name='finance_dashboard'),
    path('dashboard/external/', views.external_user_dashboard, name='external_user_dashboard'),
    path('dashboard/procurement-officer', views.procurement_officer_dashboard, name='procurement_officer_dashboard'),
    path('dashboard/supplier', views.supplier_dashboard, name='supplier_dashboard'),
    path('dashboard/inventory-manager', views.inventory_manager_dashboard, name='inventory_manager_dashboard'),
    path('dashboard/salesofficer', views.salesofficer_dashboard, name='salesofficer_dashboard'),
    path('dashboard/delivery_boy', views.delivery_boy_dashboard, name='delivery_boy_dashboard'),
    path('maintenance-dashboard/', views.maintenance_dashboard, name='maintenance_staff_dashboard'),
    path("security/dashboard/", views.security_dashboard, name="security_dashboard"),
    path('dashboard/quality_control',views.qc_dashboard,name='quality_control'),

    #-------------------- profile and notification links ---------------------------------
    path('forgot-password/', views.forgot_password_request, name='forgot_password'),
    path('admin-reset-requests/', views.admin_reset_requests, name='admin_reset_requests'),
    path('approve-reset/<int:request_id>/', views.approve_reset_request, name='approve_reset_request'),
    path('reset-password/<uidb64>/<token>/', views.custom_password_reset_confirm, name='custom_password_reset_confirm'),
    path('profile/', views.user_profile, name='user_profile'),
    path('user-notifications/', views.user_notification, name='user_notifications'),

    path('admin-dashboard/reports/', views.admin_reports, name='admin_reports'),
    path('admin-dashboard/reports/purchase/', views.purchase_report, name='purchase_report'),
    path('admin-dashboard/reports/purchase/excel/', views.purchase_report_excel, name='purchase_report_excel'),
    path('admin-dashboard/reports/purchase/pdf/', views.purchase_report_pdf, name='purchase_report_pdf'),

    path('admin-dashboard/reports/batch/', views.batch_report, name='batch_report'),
    path('admin-dashboard/reports/batch/excel/', views.batch_report_excel, name='batch_report_excel'),
    path('admin-dashboard/reports/batch/pdf/', views.batch_report_pdf, name='batch_report_pdf'),

    # Picking Report URLs
    path('admin-dashboard/reports/picking/', views.picking_report, name='picking_report'),
    path('admin-dashboard/reports/picking/excel/', views.picking_report_excel, name='picking_report_excel'),
    path('admin-dashboard/reports/picking/pdf/', views.picking_report_pdf, name='picking_report_pdf'),

    # Reports
    path('admin-dashboard/reports/packing/', views.packing_report, name='packing_report'),
    path('admin-dashboard/reports/packing/excel/', views.packing_report_excel, name='packing_report_excel'),
    path('admin-dashboard/reports/packing/pdf/', views.packing_report_pdf, name='packing_report_pdf'),

        # Dispatch Report URLs
    path('admin-dashboard/reports/dispatch/', views.dispatch_report, name='dispatch_report'),
    path('admin-dashboard/reports/dispatch/excel/', views.dispatch_report_excel, name='dispatch_report_excel'),
    path('admin-dashboard/reports/dispatch/pdf/', views.dispatch_report_pdf, name='dispatch_report_pdf'),

    path('admin-dashboard/reports/delivery/', views.delivery_report, name='delivery_report'),
    path('admin-dashboard/reports/delivery/excel/', views.delivery_report_excel, name='delivery_report_excel'),
    path('admin-dashboard/reports/delivery/pdf/', views.delivery_report_pdf, name='delivery_report_pdf'),


    path('admin-dashboard/reports/stock/', views.stock_report, name='stock_report'),
    path('admin-dashboard/reports/stock/excel/', views.stock_report_excel, name='stock_report_excel'),
    path('admin-dashboard/reports/stock/pdf/', views.stock_report_pdf, name='stock_report_pdf'),

    path('admin-dashboard/reports/salesorder/', views.sales_order_report, name='sales_order_report'),
    path('admin-dashboard/reports/salesorder/excel/', views.sales_order_report_excel, name='sales_order_report_excel'),
    path('admin-dashboard/reports/salesorder/pdf/', views.sales_order_report_pdf, name='sales_order_report_pdf'),

    path('admin-dashboard/reports/salesinvoice/', views.sales_invoice_report, name='sales_invoice_report'),
    path('admin-dashboard/reports/salesinvoice/excel/', views.sales_invoice_report_excel, name='sales_invoice_report_excel'),
    path('admin-dashboard/reports/salesinvoice/pdf/', views.sales_invoice_report_pdf, name='sales_invoice_report_pdf'),

    path('admin-dashboard/reports/purchaseinvoice/', views.purchase_invoice_report, name='purchase_invoice_report'),
    path('admin-dashboard/reports/purchaseinvoice/excel/', views.purchase_invoice_report_excel, name='purchase_invoice_report_excel'),
    path('admin-dashboard/reports/purchaseinvoice/pdf/', views.purchase_invoice_report_pdf, name='purchase_invoice_report_pdf'),
    
    path('admin-dashboard/reports/finance-summary/', views.finance_summary_report, name='finance_summary_report'),
    path('admin-dashboard/profile/edit/', views.admin_profile_edit, name='admin_profile_edit'),

    path("profile/edit/", views.user_profile_edit, name="user_profile_edit"),
    path("admin-dashboard/roles/", views.role_list, name="role_list"),

    path("roles/<str:role_name>/assign/", views.assign_role_functions, name="assign_role_functions"),
    path("<str:company>/home/", views.company_home, name="company_home"),
    path("set-company/", views.set_company, name="set_company"),



    path('admin-dashboard/carriers/', views.carrier_list, name='carrier_list'),
    path('admin-dashboard/carriers/add/', views.add_carrier, name='add_carrier'),
    path('admin-dashboard/carriers/<int:pk>/edit/', views.edit_carrier, name='edit_carrier'),
    path('admin-dashboard/carriers/<int:pk>/delete/', views.delete_carrier, name='delete_carrier'),

    path("dashboard/notifications/delete-all/",views.delete_all_notifications,name="delete_all_notifications"),
    path("notifications/delete-all/",views.user_delete_all_notifications,name="user_delete_all_notifications"),
    path('user-notifications/delete/<int:notification_id>/', views.user_delete_notification, name='user_delete_notification'),

    path('sales-order-chart-data/', views.sales_order_chart_data, name='sales_order_chart_data'),
    path('password-expired/', views.password_expired, name='password_expired'),










]

