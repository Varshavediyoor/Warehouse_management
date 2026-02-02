from django.conf import settings

def settings_processor(request):
    # Get current company from session, fallback to "default"
    current_company = request.session.get("company_code", "default")

    # Get languages for this company from settings
    company_languages = settings.LANGUAGE_OPTIONS.get(current_company, ["en", "ar"])

    return {
        "settings": settings,           # Optional if you need other settings
        "current_company": current_company,
        "company_languages": company_languages,
    }


from admin_app.models import UserSessionTimer

def session_warning(request):
    if not hasattr(request, 'user'):
        return {}

    if request.user.is_authenticated:
        try:
            timer = UserSessionTimer.objects.get(user=request.user)
            mins = timer.minutes_left()

            if 0 < mins <= 5:
                return {'session_warning': mins}
        except UserSessionTimer.DoesNotExist:
            pass

    return {}


from .models import Notification

def admin_unread_notifications(request):
    if request.user.is_authenticated and request.user.is_staff:

        # Hide badge on notification page itself
        if request.resolver_match and request.resolver_match.url_name == "admin_notifications":
            return {"unread_count": 0}

        return {
            "unread_count": Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()
        }

    return {"unread_count": 0}



from django.utils import timezone

def current_time_processor(request):
    """
    Returns the current time in the active timezone
    """
    return {
        'current_time': timezone.localtime(timezone.now())  # respects USE_TZ & TIME_ZONE
    }
