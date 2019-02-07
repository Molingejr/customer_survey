from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Our registration form for business owners to register"""
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        widgets = {
            'password': forms.PasswordInput
        }


class LoginForm(forms.Form):
    """Our login form for the business owner"""
    name = forms.CharField(label="Name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
