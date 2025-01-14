from django.db.models.signals import post_save
from django.dispatch import receiver
from billings.models import Payment
from orders.models import Order


@receiver(post_save, sender=Order)
def create_payment(sender, instance, created, **kwargs):
    if created:
    
        try:
            payment = Payment.objects.get_or_create(order=instance, amount=instance.total_amount)
        finally:
            pass