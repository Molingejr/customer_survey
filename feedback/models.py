from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    """Schema to hold customer data"""
    name = models.CharField(max_length=50)
    email = models.EmailField()
    cellphone = PhoneNumberField()

    def __str__(self):
        return "{} {}".format(self.name, self.email)


# Todo: Add Comment field to Answer model
# Todo: Link all customer answers for each complete survey
class Answer(models.Model):
    """Schema to hold question answers"""
    customer_answer = models.CharField(max_length=50)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='answers'
    )

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
