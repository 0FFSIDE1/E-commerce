from django.db import models
from customers.models import Customer
from products.models import Product
import uuid
# Create your models here.
class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    products = models.ManyToManyField(Product, default=None)
    choices = (('Pending','Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled'))
    status = models.CharField(choices=choices, default='Pending', max_length=15)
    total_price = models.CharField(max_length=20, default=None, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer
