from celery import shared_task
from services.email.send_email import send_email

@shared_task
def send_email_task(subject, text_content, path_to_html, to_email, context):
    """Task to send an HTML email."""
    send_email(subject,text_content, path_to_html, to_email, context)
   
