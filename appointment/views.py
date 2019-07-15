# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import AppointmentForm
from .models import Appointment, Contact
from datetime import datetime
from .mail import send_appointment_mail
from .sms import send_appointment_sms

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
            try:
                user = User.objects.get(email=form.data['email'])
            except:
                user = None

            if not user:
                # Register new user if user doesn't already exist
                user = User(first_name=form.data['first_name'], last_name=form.data['last_name'],
                    email=form.data['email'], username=(form.data['first_name']+form.data['last_name']).lower()
                )
                user.password = make_password(form.data['password'])
                user.save()

            # Create new contact details for the user
            contact = Contact(mobilephone=form.data['mobilephone'], user=user)
            contact.save()

            # Save appointment details for the contact
            start_time = request.GET['start_time'].split(" ")[0]
            end_time = request.GET['end_time'].split(" ")[0]
            notes = form.data['notes']
            appointment = Appointment(start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S"), 
                                      end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S"), notes=notes)
            
            appointment.contact = contact
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