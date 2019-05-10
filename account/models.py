from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """Schema to hold company data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)
