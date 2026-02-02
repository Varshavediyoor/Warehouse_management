from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


from django.utils import timezone
from datetime import timedelta


from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class UserSessionTimer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)

    SESSION_DURATION = timedelta(minutes=30)

    def is_expired(self):
        return timezone.now() > self.login_time + self.SESSION_DURATION

    def minutes_left(self):
        remaining = (self.login_time + self.SESSION_DURATION) - timezone.now()
        return max(0, int(remaining.total_seconds() // 60))



class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phoneno = models.CharField(max_length=15)
    profile_photo = models.ImageField(upload_to='admin_photos/', blank=True, null=True)

    # OTP fields
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)

    # NEW FIELD → tracks last successful OTP verification
    last_otp_verified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # ---------------------- OTP Helpers ----------------------
    def otp_is_valid(self):
        """Check if OTP is still valid (5 min expiry)."""
        if not self.otp or not self.otp_created_at:
            return False
        expiry_time = self.otp_created_at + timedelta(minutes=5)
        return timezone.now() < expiry_time and not self.otp_verified

    def otp_required(self):
        """
        Returns True if OTP should be asked again.
        We ask OTP only if last verification was more than 2 weeks ago.
        """
        if not self.last_otp_verified_at:
            return True  # never verified → must verify OTP
        
        two_weeks = timedelta(weeks=2)
        return timezone.now() - self.last_otp_verified_at > two_weeks
        
    # ---------------------- OTP Helpers ----------------------
    def otp_is_valid(self):
        """Return True if OTP is valid (not expired and not used)."""
        if not self.otp or not self.otp_created_at:
            return False
        expiry_time = self.otp_created_at + timedelta(minutes=5)
        return timezone.now() < expiry_time and not self.otp_verified





class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("WAREHOUSE_MANAGER", "Warehouse Manager"),
        ("INVENTORY_MANAGER", "Inventory Manager"),
        ("STOREKEEPER", "Storekeeper"),
        ("LOGISTICS", "Logistics/Delivery Staff"),
        ("FINANCE", "Finance/Accounts"),
        ("EXTERNAL", "External User (Vendor/Client)"),
        ("PROCUREMENT_OFFICER", "Procurement Officer"),
        ("SUPPLIER", "Supplier"),
        ("SALES_OFFICER","Sales Officer"),
        ("DELIVERY_BOY", "Delivery Boy"),
        ("MAINTENANCE_STAFF", "Maintenance Staff"),
        ("SECURITY","Security"),
        ("QC_INSPECTOR","quality control")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(
        "admin_app.warehouse",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    nationality = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.warehouse}"



class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier_profile')
    supplier_name = models.CharField(max_length=255, blank=True, null=True, default='')
    address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    gst_no = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.supplier_name or self.user.username

    def save(self, *args, **kwargs):
        if not self.supplier_name:
            self.supplier_name = self.user.username
        super().save(*args, **kwargs)



class DeliveryBoy(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("ON_LEAVE", "On Leave"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_boy_profile')
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)

    joining_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default="ACTIVE")

    assigned_area = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.phone_number})"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.message[:30]}"
    

class UserActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('failed_login', 'Failed Login'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - {self.action} at {self.timestamp}"



# admin_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    reason = models.TextField()
    requested_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='approved_resets', null=True, blank=True, on_delete=models.SET_NULL)
    approved_at = models.DateTimeField(null=True, blank=True)
    processed = models.BooleanField(default=False)  # whether reset link sent

    def __str__(self):
        return f"Password reset request for {self.email} (approved={self.approved})"


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Function(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class RoleFunction(models.Model):
    role = models.CharField(max_length=50, choices=UserProfile.ROLE_CHOICES)
    functions = models.ManyToManyField(Function)

    def __str__(self):
        return self.role
    


class Carrier(models.Model):
    CARRIER_TYPE_CHOICES = [
        ('api', 'API'),
        ('manual', 'Manual'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    carrier_type = models.CharField(max_length=10, choices=CARRIER_TYPE_CHOICES)
    api_base_url = models.URLField(blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class ReportFile(models.Model):
    REPORT_CHOICES = [
        ('Picking', 'Picking'),
        ('Dispatch', 'Dispatch'),
        ('SalesOrder', 'SalesOrder'),
        ('Packing', 'Packing'),
        ('Delivery', 'Delivery'),
        ('Purchase','Purchase'),
        ('Batch','Batch'),
        ('Salesinvoice','Salesinvoice'),
        ('Purchaseinvoice','Purchaseinvoice'),
        ('Stock','Stock'),
        
        
    ]

    report_type = models.CharField(max_length=50, choices=REPORT_CHOICES)
    file = models.FileField(upload_to='reports/%Y/%m/', max_length=500)  # auto year/month folder
    generated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.report_type} - {self.generated_on.strftime('%Y-%m-%d %H:%M')}"

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Database alias like INDIA001, DUBAI001"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"