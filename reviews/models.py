from django.db import models
from customers.models import Customer
from products.models import Product
from orders.models import Order
from django.core.exceptions import ValidationError

# Create your models here.
class ProductReview(models.Model):
    customer = models.ForeignKey(Customer, default=None, blank=False, null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, default=None, blank=False, null=False, on_delete=models.CASCADE)
    message = models.TextField(max_length=200, default=None, blank=False, null=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0.0 and 5.0")

    def __str__(self):
        return f"product rating: {self.rating} | {self.product.name}"


class OrderReview(models.Model):
    customer = models.ForeignKey(Customer, default=None, blank=False, null=False, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, default=None, blank=False, null=False, on_delete=models.CASCADE)
    message = models.TextField(max_length=200, default=None, blank=False, null=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0.0 and 5.0")

    def __str__(self):
        return f"Order rating: {self.rating} | {self.order.order_id} | {self.customer.first_name}"
