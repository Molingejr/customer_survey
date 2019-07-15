from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobilephone = PhoneNumberField()
   
    def __str__(self):
        return "{} {}: {}".format(
            self.user.first_name, self.user.last_name, self.mobilephone)

class Appointment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='contact'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return "{} {} {}".format(self.start_time, self.end_time, self.notes)
