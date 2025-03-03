from django.db.models.signals import post_save
from django.dispatch import receiver
from carts.models import Cart
from services.middleware.middleware import get_current_request


@receiver(post_save, sender=Cart)
def set_session_id(sender, instance, created, **kwargs):
    """
    Signal to set the session ID for a newly created Cart.

    Args:
        sender: The Cart model.
        instance: The Cart instance being saved.
        created: A boolean; True if a new Cart instance is created.
        kwargs: Additional arguments passed by the signal.
    """
    if created:
        request = get_current_request()

        # Ensure request and session are valid
        if request and hasattr(request, 'session'):
            if not request.session.session_key:
                request.session.create()  # Initialize session if not created

            instance.session = request.session.session_key
            instance.save()
    else:
         
        # Recalculate total amount of cart
        new_total_amount = instance.calculate_total_amount()
        if instance.total_amount != new_total_amount:
            # Update the total_amount directly in the database to avoid recursion
            Cart.objects.filter(pk=instance.pk).update(total_amount=new_total_amount)
