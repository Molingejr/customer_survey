# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import AppointmentForm
from .models import Appointment
from datetime import datetime
from .mail import send_appointment_mail
from .sms import send_appointment_sms
import re

def schedule_appointment(request):
   return render(request, 'schedule_appointment.html')


def complete_appointment(request):
    return render(request, 'complete_appointment.html')


def save_appointment_details(request, schedule=None):
    """
    View function to handle our create appointment form
    :param request: Contains our request object
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = AppointmentForm(request.POST)

        # check whether it's valid and save it
        if form.is_valid():
            # Save appointment details
            start_time = request.GET['start_time'][:19]
            end_time = request.GET['end_time'][:19]
            #print(start_time, end_time)
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
            print(start_time, end_time)
            mobilephone = form.data['mobilephone']
            email = form.data['email']
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            notes = form.data['notes']

            appointment = Appointment(start_time=start_time, end_time=end_time, first_name=first_name, 
                                      last_name=last_name, email=email, mobilephone=mobilephone, notes=notes)
            appointment.save()
            
            try:
                send_appointment_mail(appointment)  # send appointment details email
            except Exception as exp:
                print(exp)
            
            try:
                send_appointment_sms(appointment)   # send appointment details sms
            except Exception as exp:
                print(exp) 
            
            return redirect('appointment:complete_appointment')
           
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})