from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Appointment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()  
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)
    mobilephone = PhoneNumberField()  
    notes = models.TextField(blank=True)

    def __str__(self):
        return "{} {} {}".format(self.start_time, self.end_time, self.notes)
