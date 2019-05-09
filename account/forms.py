from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Our registration form for business owners to register"""
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    company = forms.CharField(max_length=50, help_text='Required. Company to which you belong', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'company', 'password1', 'password2',)
        widgets = {
            'password': forms.PasswordInput
        }


class LoginForm(forms.Form):
    """Our login form for the business owner"""
    name = forms.CharField(label="Name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
