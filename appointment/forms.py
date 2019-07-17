from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """Appointment details"""

    class Meta:
        model = Appointment
        fields = ('mobilephone', 'email', 'first_name', 'last_name', 'notes')
        exclude = ('start_time', 'end_time')
        labels = {
            'mobilephone': 'Mobile Phone',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'notes': 'Appointment Notes (optional)',
        }
        widgets = {
            "notes": forms.Textarea(attrs={
                'placeholder': "Add a note to your appointment. To protect your privacy, do not include any privileged material such as personal health information.", 
                "required": "false"}
                ),
            
        }
