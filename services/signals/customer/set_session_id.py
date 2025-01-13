from django.db.models.signals import post_save
from django.dispatch import receiver
from customers.models import Customer
from services.middleware.middleware import get_current_request

@receiver(post_save, sender=Customer)
def set_session_id(sender, instance, created, **kwargs):
    if created and not instance.user:
        request = get_current_request()
        if not request.session.session_key:
            request.session.create()
              
        session_id = request.session.session_key
        instance.session = session_id
        instance.save()
