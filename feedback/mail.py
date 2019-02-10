from django.core.mail import send_mail
from django.conf import settings
from .models import Answer

# This should be replaced with the recipient email
RECIPIENT = "reciever@gmail.com"


def send_email(customer, survey_id):

    answers = Answer.objects.filter(customer=customer, survey_id=survey_id)
    subject = 'A new filled survey form'
    message = f"""
    A survey form filled
    Customer Name: {customer.name}
    Email: {customer.email}
    CellPhone: {customer.cellphone}
    {[answer.customer_answer, answer.comment] for answer in answers}
    """

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [RECIPIENT, ]

    send_mail(subject, message, email_from, recipient_list)
