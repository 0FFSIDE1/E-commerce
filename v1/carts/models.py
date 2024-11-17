from django.db import models
from customers.models import Customer
from products.models import Product
# Create your models here.
class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, default=None, blank=True, null=True)
    product = models.ManyToManyField(Product, default=None)
    
    def __str__(self):
        return f"{self.product} | {self.customer}"