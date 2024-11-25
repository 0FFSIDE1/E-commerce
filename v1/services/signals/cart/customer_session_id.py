from django.db.models.signals import post_save
from django.dispatch import receiver
from carts.models import Cart
from services.middleware.middleware import get_current_request

@receiver(post_save, sender=Cart)
def set_session_id(sender, instance, created, **kwargs):
    if created and not instance.customer:
        request = get_current_request()
        if not request.session.session_key:
            request.session.create()
              
        session_id = request.session.session_key
        instance.Session = session_id
        instance.save()
