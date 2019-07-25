# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize

from .forms import AppointmentForm, CalendarForm
from .models import Appointment, Calendar, LazyEncoder
from datetime import datetime
from .mail import send_appointment_mail
from .sms import send_appointment_sms
from .utils import jsonify
import re

def schedule_appointment(request):
   return render(request, 'schedule_appointment.html')


def complete_appointment(request, calendar_id):
    calendar = Calendar.objects.get(pk=calendar_id)
    return render(request, 'complete_appointment.html', {'calendar': calendar})


def calendar_view(request, calendar_id):
    """View a customized calendar"""
    calendar_obj = Calendar.objects.get(pk=calendar_id)
    try:
        appointments = Appointment.objects.all().filter(calendar=calendar_obj)
        appointments = jsonify(appointments)
    except:
        appointments = []
    calendar_obj = calendar_obj.serialize()
    calendar_obj["non_working_days"] = [day for day in [0, 1, 2, 3, 4, 5, 6] if day not in calendar_obj["working_days"]]
    return render(request, 'calendar_view.html', {'calendar_obj': calendar_obj, 'appointments': appointments})


def save_appointment_details(request, calendar_id):
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
            
            mobilephone = form.data['mobilephone']
            email = form.data['email']
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            notes = form.data['notes']

            appointment = Appointment(start_time=start_time, end_time=end_time, first_name=first_name, 
                                      last_name=last_name, email=email, mobilephone=mobilephone, notes=notes)
            
            calendar_obj = Calendar.objects.get(pk=calendar_id)
            appointment.calendar = calendar_obj
            appointment.save()

            try:
                send_appointment_mail(appointment)  # send appointment details email
            except Exception as exp:
                print(exp)
            
            try:
                send_appointment_sms(appointment)   # send appointment details sms
            except Exception as exp:
                print(exp) 
            
            return redirect(reverse('appointment:complete_appointment', args=[calendar_id]))
           
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})


def delete_appointment(request, appointment_id):
    #data = request.get_json()
    appointment_id = appointment_id#data.get("appointment_id")

    if not appointment_id:
        return HttpResponse("Please provide an appointment Id"), 406
    
    try:
        appointment = Appointment.objects.get(id=int(appointment_id))
    except:
        return HttpResponse("No appointment with that ID exist")
   
    appointment.delete()
    return HttpResponse("Successfully Deleted")

class CalendarListView(ListView):
    """Render Calendar list"""
    model = Calendar

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Calendar.objects.all()
        return Calendar.objects.all()


def create_calendar(request):
    """Creates a customisable calendar"""
    if request.method == 'POST':
        form = CalendarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment:calendar_list')
    else:
        form = CalendarForm()
    return render(request, 'calendar_form.html', {'form': form}) 
