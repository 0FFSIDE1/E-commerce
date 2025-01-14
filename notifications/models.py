from django.db import models
import uuid
from customers.models import Customer

# Create your models here.
class Notification(models.Model):
    notification_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_notification')
    title = models.CharField(max_length=100, default=None, blank=False, null=False)
    message = models.CharField(max_length=225, default=None, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(default=None, null=True, blank=True)
    choices = (('unread', 'unread'), ('expired', 'expired'), ('read', 'read'))
    status = models.CharField(choices=choices, default='unread', max_length=10)

    def __str__(self):
        return f"{self.created_at} | {self.customer.first_name} | {self.title} | {self.message}" 
