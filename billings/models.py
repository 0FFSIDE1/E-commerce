from django.db import models
from orders.models import Order
import uuid


# Create your models here.
class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed'),
        ],
        default='Pending',
    )
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_id} | {self.order} | {self.status}"
    

