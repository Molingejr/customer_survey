from django.contrib import admin
from appointment.models import Contact, Appointment

# We register our models here
admin.site.register(Contact)
admin.site.register(Appointment)
