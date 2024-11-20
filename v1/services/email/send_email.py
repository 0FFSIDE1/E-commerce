import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(subject, path_to_html, from_email, to_email, context):
    '''subject = "Welcome to Our Service"
    from_email = 'your_email@example.com'
    to_email = 'recipient@example.com'
    context = {'username': 'John Doe'} 
    path_to_html = 'emails/customers/welcome.html'
    '''
    
    # Plain-text version
    
    text_content = "Thank you for joining us! Visit our website for more details."

    # HTML version
    html_content = render_to_string(path_to_html, context)

    # Create the email object
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])

    # Attach the HTML version
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send()



    
   

