from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_register_email(user_email):
    subject = "Welcome To My Expense Tracker"
    message = "Thank  you for register"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list) 
