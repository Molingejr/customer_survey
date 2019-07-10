from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView

from django.utils.decorators import method_decorator


def schedule_appointment(request):
    if request.method == 'POST':
        pass
    return render(request, 'schedule_appointment.html')