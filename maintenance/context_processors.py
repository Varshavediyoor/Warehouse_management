from .models import MaintenanceNotification

def maintenance_notifications(request):
    # Only load for authenticated users
    if not request.user.is_authenticated:
        return {}

    # Optional: If only staff should see these
    # if not request.user.is_staff:
    #     return {}

    notifications = MaintenanceNotification.objects.filter(active=True).order_by('-created_at')

    return {
        'maintenance_notifications': notifications
    }
