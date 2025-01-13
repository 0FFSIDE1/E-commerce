from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from services.middleware.middleware import get_current_request
from services.payment.paystack.paystack import initialize_payment

@receiver(post_save, sender=Order)
def initialize_payment_signal(sender, instance, created, **kwargs):
    if created:
        # initialize_payment(order=instance)
        pass
        
