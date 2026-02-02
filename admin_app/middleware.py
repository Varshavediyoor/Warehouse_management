from .utils import notify_admins
from django.utils import timezone
from django.contrib.auth import logout
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _


from django.shortcuts import redirect
from django.urls import reverse
from admin_app.models import UserSessionTimer

from django.shortcuts import redirect
from django.urls import reverse
from admin_app.models import UserSessionTimer

class SimpleSessionExpiryMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not hasattr(request, 'user'):
            return self.get_response(request)

        if request.user.is_authenticated:

            # ✅ Admins are excluded
            if request.user.is_staff:
                return self.get_response(request)

            try:
                timer = UserSessionTimer.objects.get(user=request.user)

                if timer.is_expired():
                    allowed = [
                        reverse('forgot_password'),
                        reverse('custom_password_reset_confirm'),
                        reverse('user_logout'),
                        reverse('password_expired'),
                    ]

                    if request.path not in allowed:
                        return redirect('password_expired')

            except UserSessionTimer.DoesNotExist:
                pass

        return self.get_response(request)




class UnauthorizedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.is_staff:
            notify_admins(
                f"🚨 Unauthorized access attempt to admin panel from IP {request.META.get('REMOTE_ADDR')} at {timezone.now()}"
            )
        return self.get_response(request)

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            now = timezone.now().timestamp()
            timeout = getattr(settings, "SESSION_COOKIE_AGE", 300)

            last_activity = request.session.get("last_activity")

            if last_activity:
                elapsed = now - last_activity

                # remaining time (in seconds)
                remaining_time = max(timeout - elapsed, 0)
                request.remaining_session_time = int(remaining_time)

                if elapsed > timeout:
                    is_staff = request.user.is_staff
                    logout(request)
                    messages.warning(request, "You have been logged out due to inactivity.")
                    return redirect("admin_login" if is_staff else "user_login")

            request.session["last_activity"] = now
        else:
            request.remaining_session_time = None

        return self.get_response(request)
    

    