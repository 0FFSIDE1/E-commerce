from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order


@receiver(post_save, sender=Order)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    Signal to reduce the quantity of products in the vendor's inventory 
    when an order is created and its status is set to 'Delivered'.

    Args:
        sender: The model class sending the signal.
        instance: The Order instance being saved.
        created: A boolean; True if a new record was created.
        kwargs: Additional keyword arguments.
    """
    if created and instance.status == 'Delivered':
        cart_items = instance.cart.items.all()  # Assuming `cart` has a related_name `items`
        for cart_item in cart_items:
            product = cart_item.product
            if product.quantity >= cart_item.quantity:
                product.quantity -= cart_item.quantity
                product.save()
            else:
                # Log or handle the case where stock is insufficient
                raise ValueError(f"Insufficient stock for product {product.name}")