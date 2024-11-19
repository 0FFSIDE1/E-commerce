from django.db import models
from customers.models import Customer
from products.models import Product
# Create your models here.
class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, default=None, blank=True, null=True)
    items = models.ManyToManyField(Product, through = "CartItem")
    
    def __str__(self):
        return f"{self.customer}"
    
class CartItem(models.Model):
    cart =models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.item_name}: ({self.quantity})"