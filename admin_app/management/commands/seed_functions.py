from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from admin_app.models import Function

ALL_FUNCTIONS = [
    "Add Stock",
    "Edit Stock",
    "Delete Stock",
    "View Stock",
    "View Stock History",
    "Adjust Inventory",
    "View Inventory Levels",
    "Inventory Valuation",
    "Stock Movement Report",
    "Expiry Alert",
    "Low Stock Alert",
    "Create Sales Order",
    "Sales Orders",
    "View Sales Orders",
    "Edit Sales Order",
    "Cancel Sales Order",
    "Approve Sales Order",
    "Assign Delivery Boy",
    "Update Delivery Status",
    "View Delivery Assignments",
    "Generate Picklist",
    "View Picklist",
    "Ready For Delivery",
    "Assign Picklist to Staff",
    "Create Purchase Order",
    "View Purchase Order List",
    "Edit Purchase Order",
    "Cancel Purchase Order",
    "Approve Purchase Order",
    "Create GRN",
    "View GRN",
    "Edit GRN",
    "Approve GRN",
    "Review GRN",
    "View Delivery List",
    "Approve Budgets",
    "View Transaction History",
    "View Invoices",
    "Generate Invoices",
    "View Payment Status",
    "Generate Financial Reports",
    "Generate Budget Reports",
    "View Supplier List",
    "Add Supplier",
    "Edit Supplier",
    "View Customer List",
    "Add Customer",
    "Manage Products",
    "Manage Categories",
    "Manage Racks",
    "Manage Zones",
    "Manage Units",
    "Dashboard Access",
    "Notifications Access",
    "View Users",
    "Add Users",
    "Edit Users",
    "Block/Unblock Users",
    "Stock Report",
    "Picklist Report",
    "Daily Activity Report",
    "Inventory Report",
    "Financial Report",
    "Approve Dispatch",
    "Submit Sales Order",
    "QC_Task",
    "Record Payment",
    "View Purchase Invoices",
    "Record Purchase Payment",
    "Download Invoice PDF",
    "Create Sales Order",
    "Process Refund",
]

class Command(BaseCommand):
    help = "Seed default function permissions in all company databases, including default"

    def handle(self, *args, **kwargs):
        # ✅ Include default DB now
        company_dbs = settings.DATABASES.keys()

        for db in company_dbs:
            created = 0
            self.stdout.write(f"\nSeeding functions for DB: {db}")

            # Test if Function table exists
            try:
                cursor = connections[db].cursor()
                cursor.execute("SELECT 1 FROM admin_app_function LIMIT 1;")
            except Exception:
                self.stdout.write(self.style.ERROR(
                    f"Table 'Function' missing in {db}. Run migrations first."
                ))
                continue

            # Insert functions
            for f in ALL_FUNCTIONS:
                obj, was_created = Function.objects.using(db).get_or_create(name=f)
                if was_created:
                    created += 1

            self.stdout.write(self.style.SUCCESS(
                f"Inserted {created} functions successfully in {db}!"
            ))
