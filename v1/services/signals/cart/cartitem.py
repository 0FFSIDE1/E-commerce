from django.db.models.signals import post_save
from django.dispatch import receiver
from carts.models import CartItem
from orders.models import Order

@receiver(post_save, sender=CartItem)
def calculate_total_price_of_cartitem(sender, instance, created, **kwargs):
   
    if created:
        # Calculate the total price
        total_price = float(instance.product.price) * float(instance.quantity)
        # Update the total price without triggering the signal again
        CartItem.objects.filter(pk=instance.pk).update(total_price=total_price)
    


@receiver(post_save, sender=CartItem)
def recalculate_total_price(sender, instance, created, **kwargs):
    if not created:  # Only recalculate on updates
        
        # Recalculate total price
        new_total_price = float(instance.product.price) * float(instance.quantity)
        if instance.total_price != new_total_price:
            # Update the total_price directly in the database to avoid recursion
            CartItem.objects.filter(pk=instance.pk).update(total_price=new_total_price)
            


        
        