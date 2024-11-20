from django.db import models
from django.conf import settings
from uuid import uuid4
from products.models import Product

class Cart(models.Model):
    session_id = models.CharField(max_length=255, null=True, blank=True)  # This is the logic for anonymous users
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.customer.username if self.customer else f"Cart ({self.session_id})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return float(self.product.name) * self.quantity

    def __str__(self):
        return f"Cart Owner {self.cart.customer.username if self.cart.customer else f"Cart({self.cart.session_id})"} ordered {self.product.name}: {self.quantity}"
