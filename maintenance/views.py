from django.shortcuts import render

# Create your views here.
# maintenance/views.py
from django.shortcuts import render, redirect
from .forms import MaintenanceNotificationForm
from .utils import send_maintenance_email  # optional email
from .models import MaintenanceNotification
from django.shortcuts import render, get_object_or_404, redirect

def add_maintenance_notification(request):
    if request.method == 'POST':
        form = MaintenanceNotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            
            # send email to all users if active
            if notification.active:
                send_maintenance_email(notification)
                # Add a success message
                messages.success(request, "Maintenance notification saved and emails have been sent!")
            else:
                messages.success(request, "Maintenance notification saved!")
            
            return redirect('admin_index')  # or wherever you want
    else:
        form = MaintenanceNotificationForm()

    return render(request, 'maintenance/add_notification.html', {'form': form})

def notification_list(request):
    notifications = MaintenanceNotification.objects.all().order_by('-created_at')
    return render(request, "maintenance/notification_list.html", {
        "notifications": notifications
    })

def notification_detail(request, pk):
    notification = get_object_or_404(MaintenanceNotification, pk=pk)
    return render(request, "maintenance/notification_detail.html", {
        "notification": notification
    })

def toggle_notification_status(request, pk):
    notification = get_object_or_404(MaintenanceNotification, pk=pk)
    notification.active = not notification.active  # toggle state
    notification.save()
    return redirect("notification_detail", pk=pk)

def maintenance_page(request):
    return render(request, "maintenance/maintenance_page.html")

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import MaintenanceNotification

def delete_notification(request, pk):
    notification = get_object_or_404(MaintenanceNotification, pk=pk)
    if request.method == "POST":
        notification.delete()
        messages.success(request, "Notification deleted successfully!")
        return redirect('notification_list')

