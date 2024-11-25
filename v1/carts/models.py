from django.db import models
from customers.models import Customer
from uuid import uuid4
from products.models import Product
from django.contrib.sessions.models import Session
import uuid

class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=None)
    session = models.OneToOneField(Session, max_length=255, null=True, blank=True, on_delete=models.CASCADE, help_text="Session ID for anonymous users")  # This is the logic for anonymous users
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart", null=True, blank=True, help_text="Customer who owns this cart")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"Cart for: {self.customer.first_name} |  {self.customer.email}" if self.customer else f"Cart for session id: {self.session_id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", help_text="The cart this item belongs to")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)



    def __str__(self):
        return f"Cart Owner {self.cart.customer if self.cart.customer else f"Cart({self.cart.session_id})"} ordered {self.product.name}: {self.quantity}"
