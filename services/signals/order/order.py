from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from django.db.models import signals

@receiver(post_save, sender=Order)
def create_orderitems(sender, instance, created, **kwargs):
    if created:
        # Disconnect the signal to prevent infinite loop
        signals.post_save.disconnect(create_orderitems, sender=Order)
        try:
            Order.objects.filter(pk=instance.pk).update(total_amount=instance.cart.total_amount)
            for item in instance.cart.items.all():
                instance.orderitems.create(
                    name=item.product.name,
                    size='M',
                    color='Black',
                    price=item.product.price,
                    quantity=item.quantity,
                    total_price=item.total_price,
                    order=instance,
                    product=item.product,
                )
        finally:
            # Reconnect the signal
            signals.post_save.connect(create_orderitems, sender=Order)