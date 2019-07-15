from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView

from django.utils.decorators import method_decorator
from .decorators import superuser_required

from .forms import SignUpForm, LoginForm, CompanyForm
from .models import Company


def signup(request):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        user_form = SignUpForm(request.POST)

        if user_form.is_valid() and company_form.is_valid():

            user_form.save()

            # Create the user's company which will be used to create Customers
            company = Company(name=company_form.data["company"])
            company.user = User.objects.get(username=user_form.cleaned_data.get('username'))
            company.save()

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('feedback:home')
    else:
        user_form = SignUpForm()
        company_form = CompanyForm()
    return render(request, 'signup.html', {'user_form': user_form, 'company_form': company_form})


def log_in(request):
    """Handles login for admin account"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            return HttpResponse("Invalid email or password")
        
        user = authenticate(username=user.username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('feedback:home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email, password))
            return HttpResponse("Invalid login details given")

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    """Logout the user"""
    logout(request)
    return redirect('feedback:home')


@method_decorator(superuser_required, name='dispatch')
class CompanyListView(ListView):
    """Render customer list"""
    model = Company

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Company.objects.all()
        return None


def no_permission(request):
    """When user is not authorized, he see's this page"""
    return render(request, 'permission.html')
