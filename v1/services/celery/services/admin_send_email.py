from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging
import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def admin_send_mail(to_email, subject, context, body_template_path):
    """
    Function to send an email using smtplib, rendering an HTML email template.
    
    Parameters:
    - to_email (str): Recipient email address.
    - subject (str): Subject of the email.
    - context (dict): Context data for rendering the email template.
    - body_template_path (str): Path to the HTML template for the email body.
    """
    try:
        # Set up the sender and receiver email addresses
        from_email = settings.DEFAULT_FROM_EMAIL  # Can use the default Django settings
        to = to_email
        
        
        # Render the HTML body with context data using the template
        html_body = render_to_string(body_template_path, context)

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach the HTML content
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        
        # Create an SSL context
        context = ssl.create_default_context()

        # Use smtplib to send the email
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, 465, context=context) as connection:
            connection.login('info@offsideint.com', 'Princechid!09')
            connection.sendmail(from_email, to, msg.as_string())

        # Log success
        logging.info(f"Email sent to {to_email} with subject: {subject}")

    except Exception as exc:
        # Log the error if sending email fails
        logger = logging.getLogger(__name__)
        logger.error(f"Error sending email to {to_email}: {str(exc)}")
        
        # Re-raise the exception for further handling if necessary
        raise