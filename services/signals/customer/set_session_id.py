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

# This signal is triggered when a new Customer is created. If the Customer is created without a user, the session ID is set to the Customer's session field. The session ID is retrieved from the current request object using the get_current_request() function from the middleware module. If the session ID does not exist, a new session is created using the create() method. The session ID is then saved to the Customer's session field and the instance is saved. This ensures that the session ID is associated with the Customer when it is created.
