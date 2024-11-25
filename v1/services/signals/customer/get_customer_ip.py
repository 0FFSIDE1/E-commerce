from django.db.models.signals import post_save
from django.dispatch import receiver
from customers.models import Customer
from services.middleware.middleware import get_current_request
from services.email.send_email import send_email

@receiver(post_save, sender=Customer)
def set_customer_ip(sender, instance, created, **kwargs):
    """Get customer ip address and send welcome email
    """
    subject = 'Welcome, Glad to have you on board'
    text_content = 'Glad to Have you on board'
    path_to_html = 'emails/customers/welcome.html'
    


    if created and not instance.ip_address:
        # send_email(subject=subject, path_to_html=path_to_html, text_content=text_content, to_email=[instance.email], context={'username': instance.first_name})
        # Get the current request
        request = get_current_request()
        if request:
            # Extract the IP address from the request
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
            instance.ip_address = ip
            instance.save()

