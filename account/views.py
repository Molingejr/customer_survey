from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('feedback:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def log_in(request):
    """Handles login for admin account"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST.get('name')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('feedback:home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    """Logout the user"""
    logout(request)
    return redirect('feedback:home')
