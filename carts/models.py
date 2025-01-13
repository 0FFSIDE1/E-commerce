from django.db import models
from customers.models import Customer
from uuid import uuid4
from products.models import Product
import uuid
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.contrib.auth.models import User

class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=None)
    session = models.CharField(max_length=255, null=True, blank=True, help_text="Session ID for anonymous users")  # This is the logic for anonymous users
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", null=True, blank=True, help_text="User who owns this cart")  # This is the logic for logged in users
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart", null=True, blank=True, help_text="Customer who owns this cart")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    total_amount = models.FloatField(default=0.0, help_text="The total amount for the cartitems")

    

    def calculate_total_amount(self):
        # Calculate the total amount for the  cart items
        return self.items.aggregate(total=Sum('total_price'))['total'] or 0

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cart for: {self.customer.first_name} |  {self.customer.email}" if self.customer else f"Cart for session id: {self.session}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", help_text="The cart this item belongs to")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    size = models.CharField(max_length=10, default=None, blank=True, null=True)
    color = models.CharField(max_length=20, default=None, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField(default=0.00, blank=True, null=True)
    

    def __str__(self):
        cart_owner = f"Cart Owner {self.cart.customer}" if self.cart.customer else f"Cart {self.cart.session}"
        return f"{cart_owner} added {self.product.name}: {self.quantity} to cart"