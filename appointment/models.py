from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Contact(models.Model):
    mobilephone = PhoneNumberField()
    email = models.EmailField()
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Appointment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='contact'
    )
    notes = models.TextField()

    def __str__(self):
        return "{} {} {}".format(self.time, self.subject, self.user)
