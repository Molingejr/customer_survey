from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

"""Register our all url paths for our app"""

app_name = 'appointment'
urlpatterns = [
    path(r'appointment', views.schedule_appointment, name='schedule_appointment'),
    path(r'appointment/contact/<schedule>', views.save_contact_details, name='save_contact_details'),
    path(r'appointment/complete', views.complete_appointment, name='complete_appointment'),
]
