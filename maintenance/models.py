from django.db import models

# Create your models here.
# maintenance/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class MaintenanceNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_read = models.ManyToManyField(User, blank=True)  # optional if you want "mark as read"

    def __str__(self):
        return self.title
