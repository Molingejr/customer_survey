from django.contrib import admin
from appointment.models import Appointment, Calendar

# We register our models here
admin.site.register(Appointment)
admin.site.register(Calendar)
