from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

"""Register our all url paths for our app"""

app_name = 'appointment'
urlpatterns = [
    path(r'appointment', views.schedule_appointment, name='schedule_appointment'),
    path(r'appointment/details', views.save_appointment_details, name='save_appointment_details'),
    path(r'appointment/complete', views.complete_appointment, name='complete_appointment'),
]
