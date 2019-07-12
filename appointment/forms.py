from django import forms
from .models import Contact, Appointment


class ContactForm(forms.ModelForm):
    """Contact form for appointment schedule user's details"""
    notes = forms.CharField(label="Appointment Notes(Optional)", widget=forms.Textarea, required=False)
    class Meta:
        model = Contact
        fields = ('mobilephone', 'email', 'firstname', 'lastname',)
