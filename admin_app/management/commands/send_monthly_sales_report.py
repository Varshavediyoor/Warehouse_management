from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from admin_app.views import get_filtered_sales_orders, generate_chart_image
from salesofficer.models import SalesOrder
from collections import Counter
from calendar import month_name

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from collections import Counter
from calendar import month_name
from weasyprint import HTML
from django.contrib.auth import get_user_model
 # Replace with your actual app
from admin_app.views import generate_chart_image, get_filtered_sales_orders  # your chart and filter functions
from admin_app.utils import get_monthly_sales_orders
from admin_app.models import AdminProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Send monthly sales report PDF to all registered admins"

    def handle(self, *args, **kwargs):
        # Get orders for current month
        orders_qs = get_monthly_sales_orders()

        # --- Monthly sales chart ---
        current_year = timezone.now().year
        month_labels = [month_name[i] for i in range(1, 13)]
        monthly_totals = [0]*12
        for o in orders_qs:
            if o.order_date.year == current_year:
                monthly_totals[o.order_date.month-1] += float(o.total_amount)
        monthly_sales_chart = generate_chart_image(month_labels, monthly_totals, title="Monthly Sales Overview", chart_type='bar')

        # --- Status pie chart ---
        status_counter = Counter(orders_qs.values_list('status', flat=True))
        status_labels = [label for key, label in SalesOrder.STATUS_CHOICES if key in status_counter]
        status_counts = [status_counter[key] for key, label in SalesOrder.STATUS_CHOICES if key in status_counter]
        status_distribution_chart = generate_chart_image(status_labels, status_counts, title="Order Status Distribution", chart_type="pie")

        # --- Prepare context and PDF ---
        context = {
            'orders': orders_qs,
            'generated_on': timezone.now(),
            'monthly_sales_chart': monthly_sales_chart,
            'status_distribution_chart': status_distribution_chart,
        }
        html_string = render_to_string("reports/sales_order_report_export.html", context)
        pdf_file = HTML(string=html_string).write_pdf()

        # --- Send email to all admin emails ---
        admin_emails = list(AdminProfile.objects.values_list('email', flat=True))
        if not admin_emails:
            self.stdout.write(self.style.WARNING("No admin emails found to send the report."))
            return

        email = EmailMessage(
            subject=f"Monthly Sales Report - {timezone.now().strftime('%B %Y')}",
            body="Please find the attached sales report for this month.",
            from_email="ibinibenny066@gmail.com",
            to=admin_emails,
        )
        email.attach(f"SalesReport_{timezone.now().strftime('%B_%Y')}.pdf", pdf_file, 'application/pdf')
        email.send()
        self.stdout.write(self.style.SUCCESS(f"Monthly sales report sent successfully to {len(admin_emails)} admins."))
