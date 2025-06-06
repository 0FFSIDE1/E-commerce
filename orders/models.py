from django.db import models
from customers.models import Customer
from carts.models import Cart
import uuid
from django.db.models import Sum
from decimal import Decimal

from products.models import Product
# Create your models here.

class OrderStatus(models.TextChoices):
    CREATED = 'Created', 'Created'
    PAID = 'Paid', 'Paid'
    PENDING = 'Pending', 'Pending'
    SHIPPED = 'Shipped', 'Shipped'
    DELIVERED = 'Delivered', 'Delivered'
    CANCELLED = 'Cancelled', 'Cancelled'

class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None, related_name='cart', help_text="The cart used for this order")
    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.CREATED, max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text="The total amount for the order")

    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"Order {self.order_id}"
    

class OrderItem(models.Model):
    name = models.CharField(max_length=50, default=None, blank=False, null=False)
    size = models.CharField(max_length=20, default=None)
    color = models.CharField(max_length=20, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.name} | {self.price} | {self.quantity} | {self.total_price}"
    

