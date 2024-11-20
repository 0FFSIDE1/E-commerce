from celery import shared_task
from services.email.send_email import send_email

@shared_task
def send_html_email_task(subject, path_to_html, from_email, to_email, context):
    """Task to send an HTML email."""
    send_email(subject, path_to_html, from_email, to_email, context)
   
