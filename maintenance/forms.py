# maintenance/forms.py
from django import forms
from .models import MaintenanceNotification

class MaintenanceNotificationForm(forms.ModelForm):
    class Meta:
        model = MaintenanceNotification
        fields = ['title', 'message', 'start_time', 'end_time', 'active']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
