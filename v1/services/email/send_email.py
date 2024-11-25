from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)
def send_email(subject, text_content, path_to_html, to_email, context):
    '''subject = "Welcome to Our Service"
    to_email = 'recipient@example.com'
    context = {'username': 'John Doe'}
    text_content = "Thank you for joining us! Visit our website for more details." 
    path_to_html = 'emails/customers/welcome.html'
    '''
    try:
        # Render the HTML content
        html_content = render_to_string(path_to_html, context)

        # Ensure `to_email` is a list
        if isinstance(to_email, str):
            to_email = [to_email]

        # Create the email object
        email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, to_email)
        email.attach_alternative(html_content, "text/html")
        # Send the email
        email.send()
        logger.info(f"Email sent to {', '.join(to_email)}")

    except Exception as e:
        logger.error(f"Failed to send email to {', '.join(to_email)}: {e}")
        raise



    
   

