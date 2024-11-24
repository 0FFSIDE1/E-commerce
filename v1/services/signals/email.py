from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from customers.models import Customer
from services.middleware.middleware import get_current_request

@receiver(post_save, sender=Customer)
def send_email(sender, instance, created, **kwargs):
    if created:
        # Get the current request to retrieve the user
        request = get_current_request()
        if request and hasattr(request, 'user'):
            user = request.user
            
            # Prepare the email content
            subject = "Welcome to Our Platform!"
            message = f"Hi {user.first_name},\n\nThank you for creating a profile with us! We're thrilled to have you on board."
            from_email = "ezexavier103@gmail.com"
            recipient_list = [user.email]
            
            # Send the email
            send_mail(subject, message, from_email, recipient_list)
