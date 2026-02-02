from django.utils import timezone

class CompanyTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz = request.session.get("company_timezone")

        if tz:
            timezone.activate(tz)
        else:
            timezone.deactivate()

        return self.get_response(request)
