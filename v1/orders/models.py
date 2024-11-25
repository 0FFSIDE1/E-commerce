from django.db import models
from customers.models import Customer
from carts.models import Cart
import uuid
from django.db.models import Sum
# Create your models here.
class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, default=None, related_name='cart', help_text="The cart used for this order")
    choices = (('Created','Created'), ('Pending','Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled'))
    status = models.CharField(choices=choices, default='Created', max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="The total amount for the order")

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_amount(self):
        # Calculate the total amount for the order based on cart items
        return self.cart.items.aggregate(total=Sum('total_price'))['total'] or 0

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} by {self.customer.first_name}"
    

