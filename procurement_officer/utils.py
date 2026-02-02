from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_po_approved_email(po):
    if not po.vendor.email:
        return  # no vendor email, skip

    subject = f"Purchase Order Approved – {po.po_number}"

    context = {
        "po": po,
        "vendor": po.vendor,
        "items": po.items.all(),
    }

    html_content = render_to_string("email/po_approved.html", context)
    text_content = render_to_string("email/po_approved.txt", context)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [po.vendor.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
