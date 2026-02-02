from django.utils.deprecation import MiddlewareMixin
from .models import MaintenanceNotification

class MaintenanceModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if maintenance is active
        maintenance_active = MaintenanceNotification.objects.filter(active=True).exists()
        request.maintenance_active = maintenance_active

        # Allow maintenance staff and superusers to bypass
        if request.user.is_authenticated:
            role = getattr(getattr(request.user, 'userprofile', None), 'role', '').upper()
            if role == "MAINTENANCE_STAFF" or request.user.is_superuser:
                return None  # bypass maintenance restrictions

        # Detect language prefix
        path = request.path
        parts = path.strip("/").split("/")
        lang_prefix = "/" + parts[0] if len(parts) > 0 and len(parts[0]) == 2 else ""

        # Allowed URLs even during maintenance
        allowed_paths = [
            f"{lang_prefix}/user-login/",
            f"{lang_prefix}/maintenance/",  # maintenance page itself
            f"{lang_prefix}/",              # home page
        ]

        for p in allowed_paths:
            if path.startswith(p):
                return None

        # For all other users during maintenance, the template can show a popup
        if maintenance_active:
            return None
