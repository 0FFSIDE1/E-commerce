from django.db.models.signals import post_save
from django.dispatch import receiver
from carts.models import CartItem


@receiver(post_save, sender=CartItem)
def calculate_total_price_of_cartitem(sender, instance, created, **kwargs):
   
    if created:
        total_price = float(instance.product.price) * float(instance.quantity)
        instance.total_price = float(total_price)
        instance.save()

