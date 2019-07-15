from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from .models import Contact, Appointment


class AppointmentForm(forms.ModelForm):
    """Appointment details"""
    mobilephone = PhoneNumberField()
    email = forms.EmailField(label="Email", max_length=254, help_text='Enter a valid email address.')
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    password = forms.CharField(max_length=32, help_text='Enter password for your new account or reuse your existing one.', widget=forms.PasswordInput())
    class Meta:
        model = Appointment
        fields = ('mobilephone', 'first_name', 'last_name', 'notes')
        exclude = ('start_time', 'end_time')
        labels = {
            'notes': 'Appointment Notes (optional)',
        }
        widgets = {
            "notes": forms.Textarea(attrs={
                'placeholder': "Add a note to your appointment. To protect your privacy, do not include any privileged material such as personal health information.", 
                "required": "false"}
                ),
            
        }
