from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def send_maintenance_email(notification):
    users = User.objects.all()
    subject = f"Maintenance Notification: {notification.title}"
    message = notification.message
    from_email = settings.DEFAULT_FROM_EMAIL

    for user in users:
        if user.email:
            send_mail(
                subject,
                message,
                from_email,
                [user.email],  # send individually
                fail_silently=True
            )
