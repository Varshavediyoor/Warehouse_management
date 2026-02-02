from django.core.management.base import BaseCommand
from quality_control.models import QCChecklistItem


class Command(BaseCommand):
    help = "Seed full detailed QC checklist with correct mandatory rules"

    def handle(self, *args, **kwargs):

        # ⚠️ CLEAR EXISTING CHECKLIST
        QCChecklistItem.objects.all().delete()

        checklist = [

            # ================= ELECTRONICS =================
            {
                "category": "ELECTRONICS",
                "mandatory": "ALL",
                "items": [

                    ("Carton box condition",
                     "Outer carton must protect electronic items.",
                     "Inspect carton for dents, tears, punctures, or moisture."),

                    ("Seal integrity",
                     "Seals indicate tampering.",
                     "Inspect outer and inner seals."),

                    ("Tilt Watch indicator verification",
                     "Tilt Watch detects improper handling during transit.",
                     "GREEN → PASS, RED → FAIL."),

                    ("Shock indicator verification",
                     "Shock indicator shows impact during transit.",
                     "Triggered indicator → FAIL."),

                    ("Moisture indicator verification",
                     "Moisture indicator detects humidity exposure.",
                     "Color change → FAIL."),

                    ("Box label accuracy",
                     "Box label must match order details.",
                     "Verify SKU, model, and description."),

                    ("Serial number on box verification",
                     "Box serial number must be readable.",
                     "Missing or unreadable → FAIL."),

                    ("Laptop serial number verification",
                     "Laptop serial number must match box and invoice.",
                     "Open ONE box and verify serial number."),

                    ("Laptop model verification",
                     "Laptop model must match PO.",
                     "Mismatch → FAIL."),

                    ("Laptop physical condition",
                     "Laptop must be free from physical damage.",
                     "Cracks / dents → FAIL."),

                    ("Laptop power-on test",
                     "Laptop must boot successfully.",
                     "Boot failure → FAIL."),

                    ("Charger presence",
                     "Charger must be present.",
                     "Missing → FAIL."),

                    ("Charger rating verification",
                     "Charger rating must match laptop.",
                     "Mismatch → FAIL."),

                    ("Power cable presence",
                     "Power cable must be present.",
                     "Missing → FAIL."),

                    ("Mouse presence",
                     "Mouse must be present if included.",
                     "Missing → FAIL."),

                    ("Carry bag / sleeve presence",
                     "Carry bag must be present if specified.",
                     "Missing → FAIL."),

                    ("Manual / warranty card presence",
                     "Documentation must be included.",
                     "Missing → FAIL."),

                    ("All items as per BOM present",
                     "Box must contain all items as per BOM.",
                     "Missing item → FAIL."),
                ],
            },

            # ================= FOOD =================
            {
                "category": "FOOD",
                "mandatory": "ALL",
                "items": [

                    ("Primary packaging integrity",
                     "Primary packaging must be intact.",
                     "Damage → FAIL."),

                    ("Secondary packaging integrity",
                     "Secondary packaging must protect product.",
                     "Damage → FAIL."),

                    ("Seal verification",
                     "Seal ensures freshness.",
                     "Broken seal → FAIL."),

                    ("Leakage check",
                     "Food must not leak.",
                     "Leakage → FAIL."),

                    ("Expiry / best-before validation",
                     "Expired food is unsafe.",
                     "Expired → FAIL."),

                    ("Manufacture date verification",
                     "Manufacture date must be present.",
                     "Missing → FAIL."),

                    ("Batch / lot number verification",
                     "Batch enables traceability.",
                     "Missing → FAIL."),

                    ("Label readability & compliance",
                     "Label must be readable.",
                     "Illegible → FAIL."),

                    ("Ingredient list presence",
                     "Ingredients must be declared.",
                     "Missing → FAIL."),

                    ("Allergen information presence",
                     "Allergen info required.",
                     "Missing → FAIL."),

                    ("Storage condition compliance",
                     "Storage instructions must be met.",
                     "Non-compliance → FAIL."),

                    ("Temperature abuse indicator",
                     "Temperature abuse must not occur.",
                     "Triggered → FAIL."),

                    ("Contamination check",
                     "Food must be contamination-free.",
                     "Contaminated → FAIL."),

                    ("Odor check",
                     "Unusual odor indicates spoilage.",
                     "Abnormal odor → FAIL."),
                ],
            },

            # ================= MEDICAL =================
            {
                "category": "MEDICAL",
                "mandatory": "ALL",
                "items": [

                    ("Sterile packaging integrity",
                     "Sterile barrier must be intact.",
                     "Damage → FAIL."),

                    ("Tamper-evident seal verification",
                     "Tamper seal ensures safety.",
                     "Broken → FAIL."),

                    ("Regulatory labeling compliance",
                     "Medical labeling must comply.",
                     "Missing → FAIL."),

                    ("License number presence",
                     "License number must be present.",
                     "Missing → FAIL."),

                    ("Product name accuracy",
                     "Product name must match PO.",
                     "Mismatch → FAIL."),

                    ("Batch / lot verification",
                     "Batch ensures traceability.",
                     "Missing → FAIL."),

                    ("Expiry date validation",
                     "Expired medical items unsafe.",
                     "Expired → FAIL."),

                    ("Storage condition compliance",
                     "Storage requirements must be met.",
                     "Non-compliance → FAIL."),

                    ("IFU availability",
                     "Instructions for use required.",
                     "Missing → FAIL."),

                    ("IFU language compliance",
                     "IFU must be readable.",
                     "Unreadable → FAIL."),

                    ("Packaging cleanliness",
                     "Packaging must be clean.",
                     "Dirty → FAIL."),

                    ("Transport damage check",
                     "Transport must not damage product.",
                     "Damage → FAIL."),

                    ("Traceability barcode check",
                     "Barcode must be scannable.",
                     "Unreadable → FAIL."),

                    ("Recall status verification",
                     "Product must not be recalled.",
                     "Recalled → FAIL."),

                    ("Shelf-life remaining compliance",
                     "Adequate shelf life required.",
                     "Insufficient → FAIL."),
                ],
            },

            # ================= CLOTHING =================
            {
                "category": "CLOTHING",
                "mandatory": "ALL",
                "items": [

                    ("Fabric condition",
                     "Fabric must be defect-free.",
                     "Defect → FAIL."),

                    ("Fabric shade consistency",
                     "Shade must match approved sample.",
                     "Mismatch → FAIL."),

                    ("Stitching quality",
                     "Stitching must be uniform.",
                     "Loose threads → FAIL."),

                    ("Seam strength check",
                     "Seams must be strong.",
                     "Weak seam → FAIL."),

                    ("Size label verification",
                     "Size must match order.",
                     "Mismatch → FAIL."),

                    ("Brand label presence",
                     "Brand label required.",
                     "Missing → FAIL."),

                    ("Care label presence",
                     "Care instructions required.",
                     "Missing → FAIL."),

                    ("Color bleeding check",
                     "Color bleeding unacceptable.",
                     "Bleeding → FAIL."),

                    ("Button / zipper functionality",
                     "Fasteners must work.",
                     "Faulty → FAIL."),

                    ("Loose thread check",
                     "Loose threads unacceptable.",
                     "Excess threads → FAIL."),

                    ("Measurement tolerance check",
                     "Measurements within tolerance.",
                     "Out of tolerance → FAIL."),

                    ("Packaging cleanliness",
                     "Packaging must be clean.",
                     "Dirty → FAIL."),

                    ("Folding & presentation",
                     "Presentation must meet standard.",
                     "Poor presentation → FAIL."),

                    ("Quantity verification",
                     "Quantity must match invoice.",
                     "Mismatch → FAIL."),
                ],
            },

            # ================= CHEMICALS =================
            {
                "category": "CHEMICALS",
                "mandatory": [
                    "Container integrity",
                    "Cap / seal tightness",
                    "Leakage verification",
                    "Corrosion / bulging check",
                    "Hazard symbol presence",
                    "GHS labeling compliance",
                    "Chemical name & concentration",
                    "Expiry / retest date validation",
                    "MSDS availability",
                    "MSDS version validity",
                    "Storage segregation compliance",
                    "Transport damage check",
                    "Odor / vapor leakage check",
                    "Regulatory compliance statement",
                ],
                "items": [

                    ("Container integrity",
                     "Container must prevent leakage.",
                     "Damage → FAIL."),

                    ("Cap / seal tightness",
                     "Cap must be tightly sealed.",
                     "Loose → FAIL."),

                    ("Leakage verification",
                     "Chemical leakage hazardous.",
                     "Leakage → FAIL."),

                    ("Corrosion / bulging check",
                     "Container must not deform.",
                     "Found → FAIL."),

                    ("Hazard symbol presence",
                     "GHS hazard symbols required.",
                     "Missing → FAIL."),

                    ("GHS labeling compliance",
                     "GHS labeling must comply.",
                     "Non-compliance → FAIL."),

                    ("Chemical name & concentration",
                     "Chemical identification must be clear.",
                     "Missing → FAIL."),

                    ("Batch / lot verification",
                     "Batch enables traceability if applicable.",
                     "Missing only if applicable."),

                    ("Expiry / retest date validation",
                     "Expired chemicals unsafe.",
                     "Expired → FAIL."),

                    ("MSDS availability",
                     "MSDS required for safety.",
                     "Missing → FAIL."),

                    ("MSDS version validity",
                     "MSDS must be current.",
                     "Outdated → FAIL."),

                    ("Storage segregation compliance",
                     "Chemical segregation required.",
                     "Incorrect → FAIL."),

                    ("Transport damage check",
                     "Transport must not damage container.",
                     "Damage → FAIL."),

                    ("Odor / vapor leakage check",
                     "No abnormal odor allowed.",
                     "Strong odor → FAIL."),

                    ("Secondary containment presence",
                     "Secondary containment required if specified.",
                     "Missing only if specified."),

                    ("Regulatory compliance statement",
                     "Compliance statement required.",
                     "Missing → FAIL."),
                ],
            },
        ]

        # ================= INSERT =================
        for group in checklist:
            category = group["category"]
            mandatory_rule = group["mandatory"]

            for name, description, instructions in group["items"]:
                is_mandatory = (
                    True if mandatory_rule == "ALL"
                    else name in mandatory_rule
                )

                QCChecklistItem.objects.create(
                    name=name,
                    category=category,
                    description=description,
                    inspection_instructions=instructions,
                    is_mandatory=is_mandatory,
                    active=True,
                )

        self.stdout.write(
            self.style.SUCCESS("✅ FULL QC checklist seeded successfully (FINAL)")
        )
