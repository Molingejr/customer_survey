from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from .models import Appointment, Calendar


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


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ('provider_name', 'office_location', 'slot_duration', 'working_days', 'start_time', 'end_time')
        exclude = ('company',)
        labels = {
            "provider_name": "Provider Name",
            "office_location": "Office Location",
            "slot_duration": "Slot Duration",
            "working_days": "Working Days",
            "start_time": "Start Time",
            "end_time": "End Time"
        }
        widgets = {
            'start_time': forms.TimeInput(format="%H:%M", attrs={'placeholder': "09:00"}),
            'end_time': forms.TimeInput(format="%H:%M", attrs={'placeholder': "14:00"})
        }