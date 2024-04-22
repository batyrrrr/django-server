from django.conf import settings
from django.core.mail import send_mail


def send_and_email_update(self, recipient_email, message, subject):
    """This will send an update to user regarding the changes made to their account."""
    message = message
    subject = subject
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    send_mail(subject, message, from_email, recipient_list)
