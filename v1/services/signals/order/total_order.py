from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order

@receiver(post_save, sender=Order)
def update_vendor_total_orders(sender, instance, created, **kwargs):
    if created:
        # Increment the total orders for each vendor associated with the cart items
        for item in instance.cart.items.all():
            vendor = item.product.vendor
            vendor.total_orders += 1
            vendor.save()



@receiver(post_save, sender=Order)
def update_delivered_orders_for_vendor(sender, instance, **kwargs):
    """
    Signal to update the total number of delivered orders for vendors.
    Triggered whenever an Order is created or updated.
    """
    if instance.status == 'Delivered':
        # Iterate through all cart items in the order's cart
        for item in instance.cart.items.all():
            vendor = item.product.vendor
            # Recalculate the total delivered orders for the vendor
            vendor.total_orders_delivered = Order.objects.filter(
                cart__items__product__vendor=vendor,
                status='Delivered'
            ).distinct().count()
            vendor.save()


