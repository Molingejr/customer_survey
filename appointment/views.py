# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import ContactForm
from .models import Appointment, Contact


def schedule_appointment(request):
   return render(request, 'schedule_appointment.html')


def complete_appointment(request):
    return render(request, 'complete_appointment.html')


def save_contact_details(request, schedule=None):
    """
    View function to handle our create appointment form
    :param request: Contains our request object
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)

        # check whether it's valid and save it
        if form.is_valid():
            contact = Contact(mobilephone=form.data['mobilephone'], email=form.data['email'], firstname=form.data['firstname'], lastname=form.data['lastname'])
            contact.save()

            return redirect('appointment:complete_appointment')
           
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    start_date, end_date = schedule.split(',')
    return render(request, 'contact_form.html', {'form': form})