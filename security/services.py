from procurement_officer.models import PurchaseOrder

import re

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

def verify_po(po_number, vendor, created_by):
    try:
        po = PurchaseOrder.objects.get(po_number=po_number)

        # -------- Vendor Check --------
        vendor_ok = normalize(po.vendor.vendor_name) == normalize(vendor)

        # -------- Created By Check (SMART) --------
        user = po.created_by

        possible_names = [
            user.username,
            user.first_name,
            user.last_name,
            user.get_full_name(),
        ]

        possible_names = [normalize(n) for n in possible_names if n]

        # created_ok = any(normalize(created_by) in name for name in possible_names)
        created_ok = any(name in normalize(created_by) for name in possible_names)

        if vendor_ok and created_ok:
            return True

    except PurchaseOrder.DoesNotExist:
        return False

    return False
