# maintenance/urls.py
from django.urls import path
from . import views
from .views import add_maintenance_notification


urlpatterns = [
    path('add/', views.add_maintenance_notification, name='add_maintenance_notification'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/', views.notification_detail, name='notification_detail'),
    path('notifications/<int:pk>/toggle/', views.toggle_notification_status, name='toggle_notification_status'),
    path("maintenance/", views.maintenance_page, name="maintenance_page"),
    path('notification/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    
]
