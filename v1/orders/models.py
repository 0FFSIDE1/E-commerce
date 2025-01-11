from django.db import models
from customers.models import Customer
from carts.models import Cart
import uuid
from django.db.models import Sum
# Create your models here.
class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None, related_name='cart', help_text="The cart used for this order")
    choices = (('Created','Created'), ('Paid','Paid'), ('Pending','Pending'), ('Shipped','Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'))
    status = models.CharField(choices=choices, default='Created', max_length=15)
    total_amount = models.FloatField(default=0.0, help_text="The total amount for the order")

    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"Order {self.order_id} by {self.customer.first_name} | {self.total_amount}"
    

class OrderItem(models.Model):
    name = models.CharField(max_length=50, default=None, blank=False, null=False)
    size = models.CharField(max_length=20, default=None, blank=False, null=False)
    color = models.CharField(max_length=20, default=None, blank=False, null=False)
    price = models.CharField(max_length=50, default=None, blank=False, null=False)
    quantity = models.CharField(max_length=50, default=None, blank=False, null=False)
    total_price = models.CharField(max_length=20, default=None, blank=False, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None, related_name='orderitems')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.name} | {self.price} | {self.quantity} | {self.total_price}"
    

