from django import forms
from django.forms import ModelForm


class FeedBackFormA(ModelForm):
    """First feedback form"""
    option1 = forms.RadioSelect()
    option2 = forms.RadioSelect()


class FeedBackFormB(ModelForm):
    """Second feedback form"""
    option3 = forms.RadioSelect()
    option4 = forms.RadioSelect()
    option5 = forms.RadioSelect()
    comment = forms.TextInput()
