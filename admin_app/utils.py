from django.utils import timezone
from django.contrib.auth.models import User
from .models import Notification
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def notify_admins(message):
    """Create a notification for all active admin/staff users."""
    admins = User.objects.filter(is_staff=True, is_active=True)
    for admin in admins:
        Notification.objects.create(
            recipient=admin,
            message=message
        )
    print(f"✅ Notification sent to {admins.count()} admin(s): {message}")
import random

from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    """Send OTP to admin's registered email using HTML template"""

    subject = "Your Admin Login OTP"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]

    # Plain text version (fallback)
    text_content = f"Your one-time login verification code is: {otp}"

    # Render HTML from template
    html_content = render_to_string('admin_app/otp_email.html', {
        'otp': otp,
        'year': timezone.now().year
    })

    # Send email
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# ✅ Staff check for decorators
def staff_required(user):
    """Return True if the user is staff/admin."""
    return user.is_staff


from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from admin_app.models import UserActivityLog  # ensure this model exists


# ✅ Utility: get client IP
def get_client_ip(request):
    """Return user's IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ✅ Utility: log user actions (login, logout, edit, delete, etc.)
def log_user_activity(user, username, action, request=None):
    """
    Logs user activity for login/logout/edit/delete actions.
    user: User instance (can be None for failed login)
    username: string
    action: string e.g. 'login', 'logout', 'edit_user', 'delete_user'
    """
    ip = get_client_ip(request) if request else None
    UserActivityLog.objects.create(
        user=user,
        username=username,
        action=action,
        ip_address=ip,
        timestamp=timezone.now()
    )
#-------------User-login api------------------------------------

from django.contrib.auth import authenticate
# from django.utils import timezone

def user_login_internal(username, password):
    """
    Handles normal user login (NO OTP).
    Returns dict with status, messages, and user_id.
    """

    user = authenticate(username=username, password=password)

    if user is None:
        return {
            "status": "error",
            "message": "Invalid username or password."
        }

    if not user.is_active:
        return {
            "status": "error",
            "message": "Your account is disabled. Contact support."
        }

    return {
        "status": "success",
        "user_id": user.id,
        "otp_required": False,
        "message": "Login successful."
    }

def staff_required(user):
    return user.is_staff

# import os
# from datetime import datetime
# from django.conf import settings
# from .models import ReportFile

# def save_report(file_name, report_type, data_bytes, user=None):
#     """
#     Saves a report file in media/reports/<year>/<month>/ and creates a DB entry.

#     Parameters:
#         file_name (str): e.g. 'picking_report.xlsx'
#         report_type (str): must match REPORT_CHOICES
#         data_bytes (bytes): file content (Excel, PDF, CSV)
#         user (User): optional user who generated the report
#     Returns:
#         ReportFile instance
#     """
#     now = datetime.now()
#     year = now.strftime("%Y")
#     month = now.strftime("%m")

#     folder_path = os.path.join(settings.MEDIA_ROOT, 'reports', year, month)
#     os.makedirs(folder_path, exist_ok=True)

#     full_path = os.path.join(folder_path, file_name)

#     # Save the file
#     with open(full_path, 'wb') as f:
#         f.write(data_bytes)

#     # Save record in DB
#     report_file = ReportFile.objects.create(
#         report_type=report_type,
#         file=os.path.join('reports', year, month, file_name),
#         created_by=user
#     )

#     return report_file

# # admin_app/utils/monthly_sales_report.py


# # ================= MONTHLY SALES EMAIL =================

# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.utils.timezone import now
# from salesofficer.models import SalesOrder
# from django.db.models import Sum
# from django.contrib.auth.models import User
# from django.conf import settings

# from django.utils.timezone import now
# from django.db.models import Sum
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.contrib.auth.models import User
# from weasyprint import HTML
# from salesofficer.models import SalesOrder

# def send_monthly_sales_report():
#     today = now()
#     month = today.month
#     year = today.year

#     # Filter orders for the current month
#     orders = SalesOrder.objects.filter(
#         order_date__year=year,
#         order_date__month=month
#     )

#     # Summary statistics
#     total_orders = orders.count()
#     total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

#     total_cost = 0
#     for order in orders:
#         order_cost = sum(item.unit_price * item.quantity for item in order.items.all())
#         total_cost += order_cost

#     total_profit = total_revenue - total_cost

#     # Context for email and PDF
#     context = {
#         'month_name': today.strftime('%B'),
#         'year': year,
#         'total_orders': total_orders,
#         'total_revenue': total_revenue,
#         'total_cost': total_cost,
#         'total_profit': total_profit,
#         'company_name': 'Your Company Name'
#     }

#     # Render email body
#     subject = f"Monthly Sales Order Report - {today.strftime('%B %Y')}"
#     body = render_to_string('emails/monthly_sales_report.html', context)

#     # Generate PDF
#     html_string = render_to_string('reports/sales_order_report_export.html', context)
#     pdf_file = HTML(string=html_string).write_pdf()

#     # Get all active admin emails
#     admin_emails = list(User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True))

#     if admin_emails:
#         email = EmailMessage(
#             subject,
#             body,
#             settings.DEFAULT_FROM_EMAIL,
#             admin_emails,
#         )
#         email.content_subtype = 'html'
#         # Attach PDF
#         email.attach(f"SalesReport_{today.strftime('%B_%Y')}.pdf", pdf_file, 'application/pdf')
#         email.send(fail_silently=False)
#         print(f"✅ Monthly sales report sent to: {', '.join(admin_emails)}")
#     else:
#         print("⚠️ No active admin emails found.")




# def get_monthly_sales_orders(search=None, status=None, month=None, year=None):
#     """
#     Returns SalesOrder queryset for current month by default.
#     Optional filters: search, status, month, year
#     """
#     qs = SalesOrder.objects.all()
#     now = timezone.now()

#     # Default to current month/year
#     month = month or now.month
#     year = year or now.year

#     qs = qs.filter(order_date__month=month, order_date__year=year)

#     if search:
#         qs = qs.filter(Q(order_no__icontains=search) | Q(customer_name__icontains=search))

#     if status:
#         qs = qs.filter(status=status)

#     return qs
