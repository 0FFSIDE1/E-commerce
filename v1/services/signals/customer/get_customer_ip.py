from django.db.models.signals import post_save
from django.dispatch import receiver
from customers.models import Customer
from services.middleware.middleware import get_current_request

@receiver(post_save, sender=Customer)
def set_customer_ip(sender, instance, created, **kwargs):
   
    if created and not instance.ip_address:
       
        # Get the current request
        request = get_current_request()
        if request:
            # Extract the IP address from the request
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
            instance.ip_address = ip
            instance.save()

