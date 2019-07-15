from django.core.mail import send_mail
from django.conf import settings


def send_appointment_mail(appointment):
    subject = 'Appointment Schedule'
    message = f"""
        Your appointment details have been scheduled for
        Start at: {appointment.start_time}
        End_at: {appointment.end_time}
        Location: 123 Main office str, Atlanta, GA 30303
        Tel: 678-123-4567
        """

    email_from = settings.EMAIL_HOST_USER
    RECIPIENT = appointment.contact.user.email   # Get user's email
    recipient_list = [RECIPIENT, ]

    send_mail(subject, message, email_from, recipient_list)
