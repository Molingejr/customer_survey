from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from account.models import Company


class Customer(models.Model):
    """Schema to hold customer data"""
    name = models.CharField(max_length=50)
    email = models.EmailField()
    cellphone = PhoneNumberField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='customer'
    )

    def __str__(self):
        return "{} {}".format(self.name, self.email)


class Answer(models.Model):
    """Schema to hold question answers"""
    customer_answer = models.CharField(max_length=50)
    comment = models.TextField()
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='answers'
    )
    survey_id = models.IntegerField(default=1)

    def __str__(self):
        return self.customer_answer


class Note(models.Model):
    """Schema to hold notes"""
    title = models.CharField(max_length=50)
    content = models.TextField()
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='notes'
    )

    def __str__(self):
        return self.title
