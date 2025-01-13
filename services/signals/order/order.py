from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order


@receiver(post_save, sender=Order)
def create_orderitems(sender, instance, created, **kwargs):
    if created:
        Order.objects.filter(pk=instance.pk).update(total_amount=instance.cart.total_amount)
        for item in instance.cart.items.all():
            instance.orderitems.create(
                name=item.product.name,
                size=item.size,
                color=item.color,
                price=item.product.price,
                quantity=item.quantity,
                total_price=item.total_price,
                order=instance,
            )