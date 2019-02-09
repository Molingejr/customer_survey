from django import forms
from .models import Customer


OPTIONS = [
    "I am very satisfied and will refer my friends and family to you",
    "I am not satisfied",
    "Not happy with front desk",
    "Not happy with Consultant",
    "This is a billing issue"
]


class FeedBackFormA(forms.ModelForm):
    """First feedback form"""
    CHOICES = [
        (OPTIONS[0], OPTIONS[0]),
        (OPTIONS[1], OPTIONS[1])
    ]

    experience = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={}), label="How was your experience today?")

    class Meta:
        model = Customer
        fields = ['name', 'email', 'cellphone']
        widgets ={
            'name': forms.TextInput(attrs={'readonly': True}),
            'email': forms.EmailInput(attrs={'readonly': True}),
            'cellphone': forms.TextInput(attrs={'readonly': True})
        }


class FeedBackFormB(forms.Form):
    """Second feedback form"""
    CHOICES = [
        (OPTIONS[2], OPTIONS[2]),
        (OPTIONS[3], OPTIONS[3]),
        (OPTIONS[4], OPTIONS[4])
    ]

    experience = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={}),
                                   label="Why are you not happy?")

    comment = forms.CharField(widget=forms.TextInput)


class CustomerForm(forms.ModelForm):
    """Use form to create customer"""

    class Meta:
        model = Customer
        fields = ['name', 'email', 'cellphone']
