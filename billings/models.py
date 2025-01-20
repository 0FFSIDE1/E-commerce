from django.db import models
from orders.models import Order
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
import secrets

from services.payment.paystack.paystack import Paystack
# from .paystack import Paystack

# Create your models here.
class Payment(models.Model):
	
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)
    ref = models.CharField(max_length=200, default=None)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    verified = models.BooleanField(default=False)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed'),
        ],
        default='Pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.ref:
            ref = uuid.uuid4()
            object_with_similair_ref = Payment.objects.filter(ref=ref)
            if not object_with_similair_ref:
                self.ref = ref

        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount) * 100
    
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified == True
            self.save()
        
        if self.verified:
            return True
        return False


