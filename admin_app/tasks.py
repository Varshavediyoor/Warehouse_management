from celery import shared_task
from .utils import send_monthly_sales_report

@shared_task(name="admin_app.send_monthly_sales_report_task")
def send_monthly_sales_report_task():
    print("✅ Monthly sales report task started")
    send_monthly_sales_report()
    print("✅ Monthly sales report task finished")
