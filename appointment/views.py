# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
from apscheduler.triggers.date import DateTrigger

from .forms import AppointmentForm, CalendarForm
from .models import Appointment, Calendar, LazyEncoder
from datetime import datetime, timedelta
from .mail import send_appointment_mail
from .sms import send_appointment_sms
from .utils import jsonify
from .jobs import scheduler
import re


def complete_appointment(request, calendar_id):
    """Render view to show appointment has been scheduled successfully
    :param calendar_id: ID of the calendar which appointment belongs to
    """
    calendar = Calendar.objects.get(pk=calendar_id)
    return render(request, 'complete_appointment.html', {'calendar': calendar})


def calendar_view(request, calendar_id):
    """View a customized calendar
    :param calendar_id: ID of the calendar which appointment belongs to
    """
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
    :param calendar_id: ID of the calendar which appointment belongs to
    """
    def schedule_mail(reminder_date, appointment):
        # Configure our scheduler for reminder
        try:
            trigger = DateTrigger(run_date=reminder_date)
            scheduler.add_job(send_appointment_mail, args=[appointment], trigger=trigger)
        except Exception as exp:
            print(exp)
            
    def schedule_sms(reminder_date, appointment):
        # Configure our scheduler for reminder
        try:
            trigger = DateTrigger(run_date=reminder_date)
            scheduler.add_job(send_appointment_sms, args=[appointment], trigger=trigger)
        except Exception as exp:
            print(exp)
    
    start_time = request.GET['start_time'][:19]
    end_time = request.GET['end_time'][:19]
     
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
    
    calendar_obj = Calendar.objects.get(pk=calendar_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = AppointmentForm(request.POST)

        # check whether it's valid and save it
        if form.is_valid():
            # Save appointment details
            
            mobilephone = form.data['mobilephone']
            email = form.data['email']
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            notes = form.data['notes']

            appointment = Appointment(start_time=start_time, end_time=end_time, first_name=first_name, 
                                      last_name=last_name, email=email, mobilephone=mobilephone, notes=notes)
            
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
            
            # Calculate reminder schedule dates
            reminder1 = start_time - timedelta(hours=2)
            reminder2 = start_time - timedelta(hours=24)
            reminder3 = start_time - timedelta(days=7)

            # Schedule mails
            schedule_mail(reminder1, appointment)
            schedule_mail(reminder2, appointment)
            schedule_mail(reminder3, appointment)
            
            # Schedule sms
            schedule_sms(reminder1, appointment)
            schedule_sms(reminder2, appointment)
            schedule_sms(reminder3, appointment)
            
            return redirect(reverse('appointment:complete_appointment', args=[calendar_id]))
           
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form, 'start_time': start_time, 'end_time': end_time,
                                                     'office_location': calendar_obj.office_location})


def delete_appointment(request, appointment_id):
    """Delete an appointment from the appointment table
    :param appointment_id: ID of the appointment
    """
    appointment_id = appointment_id

    if not appointment_id:
        return HttpResponse("Please provide an appointment Id"), 406
    
    try:
        appointment = Appointment.objects.get(id=int(appointment_id))
    except:
        return HttpResponse("No appointment with that ID exist"), 404
   
    appointment.delete()
    return HttpResponse("Successfully Deleted")

class CalendarListView(ListView):
    """Render Calendar list"""
    model = Calendar

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Calendar.objects.all()
        return Calendar.objects.filter(company=self.request.user.company)


def create_calendar(request):
    """Creates a customisable calendar"""
    if request.method == 'POST':

        form = CalendarForm(request.POST)
        
        if form.is_valid():
            calendar = form.save(commit=False)  # prvent form from saving since we need to link company
            calendar.company = request.user.company
            calendar.save()
            return redirect('appointment:calendar_list')
    else:
        form = CalendarForm()
    return render(request, 'calendar_form.html', {'form': form}) 
