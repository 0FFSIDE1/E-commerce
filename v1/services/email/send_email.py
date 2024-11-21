from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(subject, text_content, path_to_html, to_email, context):
    '''subject = "Welcome to Our Service"
    to_email = 'recipient@example.com'
    context = {'username': 'John Doe'}
    text_content = "Thank you for joining us! Visit our website for more details." 
    path_to_html = 'emails/customers/welcome.html'
    '''
    # HTML version
    html_content = render_to_string(path_to_html, context)

    # Create the email object
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])

    # Attach the HTML version
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send()



    
   

