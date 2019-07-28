from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
import json
from datetime import datetime, timedelta
from account.models import Company


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, type(datetime)):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, type(datetime.date)):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, type(datetime.time)):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, type(timedelta)):
            return str(obj)
        return super().default(obj)


BUSINESS_DAYS = (
        (0, 'sunday'),
        (1, 'monday'),
        (2, 'tuesday'),
        (3, 'wednesday'),
        (4, 'thursday'),
        (5, 'friday'),
        (6, 'saturday')
    )


class Calendar(models.Model):
    """Holds details about a customized calendar"""
    provider_name = models.CharField(max_length=50)
    office_location = models.CharField(max_length=50)
    slot_duration = models.DurationField(default='00:15:00')
    working_days = MultiSelectField(choices=BUSINESS_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company'
    )

    def __str__(self):
        return "{} {} {} - {}".format(self.provider_name, self.office_location, self.start_time, self.end_time)
    
    @staticmethod
    def convert_to_numbers(days):
        day_conversion = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6}
        day_list = days.split(",")

        return [day_conversion[day.strip(" ")] for day in day_list]
        
    def serialize(self):
        return {
            "pk": self.pk,
            "provider_name": str(self.provider_name),
            "office_location": str(self.office_location),
            "slot_duration": str(self.slot_duration),#LazyEncoder().encode(self.sappointment/create_calendarlot_duration),
            "working_days": self.convert_to_numbers(str(self.working_days)),
            "start_time": LazyEncoder().encode(self.start_time).strip(r"\""),
            "end_time": LazyEncoder().encode(self.end_time).strip(r"\""),
            "company": self.company
        }

class Appointment(models.Model):
    """Holds our appointment details"""
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()  
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)
    mobilephone = PhoneNumberField()  
    notes = models.TextField(blank=True)
    calendar = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, related_name='calendar'
    )

    def __str__(self):
        return "{} {} {}".format(self.start_time, self.end_time, self.notes)

    def serialize(self):
        return {
            "pk": self.pk,
            "start_time":  LazyEncoder().encode(self.start_time).strip(r"\""),
            "end_time": LazyEncoder().encode(self.end_time).strip(r"\""),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobilephone": self.mobilephone,
            "notes": self.notes
        }

