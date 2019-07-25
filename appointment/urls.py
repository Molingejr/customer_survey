from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

"""Register our all url paths for our app"""

app_name = 'appointment'
urlpatterns = [
    path(r'appointment', views.schedule_appointment, name='schedule_appointment'),
    path(r'appointment/calendar/<calendar_id>/details', views.save_appointment_details, name='save_appointment_details'),
    path(r'appointment/calendar/<calendar_id>/complete', views.complete_appointment, name='complete_appointment'),
    path(r'appointment/create_calendar', login_required(views.create_calendar, 
                                                        login_url='account:log_in'), name='create_calendar'),
    path('appointment/calendar', login_required(views.CalendarListView.as_view(),
                                                login_url='account:log_in'), name='calendar_list'),
    path('appointment/calendar/<calendar_id>', login_required(views.calendar_view,
                                                login_url='account:log_in'), name='calendar_view'),
    path('appointment/<appointment_id>', login_required(views.delete_appointment,
                                                login_url='account:log_in'), name='delete_appointment')
]
