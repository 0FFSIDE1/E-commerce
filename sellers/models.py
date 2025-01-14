from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
# Create your models here.
currency = (
    ("NGN", "Naira"),
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
    ("GBP", "British Pound"),
    ("JPY", "Japanese Yen"),
    ("INR", "Indian Rupee"),
    ("AUD", "Australian Dollar"),
    ("CAD", "Canadian Dollar"),
)

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="vendor")
    full_name = models.CharField(max_length=50, default=None, blank=False, null=False)
    brand_name = models.CharField(max_length=50, default=None, blank=False, null=False)
    address = models.CharField(max_length=225, default=None, blank=False, null=False)
    email = models.EmailField(max_length=50, default=None, blank=False, null=False, unique=True)
    phone = PhoneNumberField(_("Phone Number"), unique=True)
    total_products = models.CharField(max_length=100, default=0, null=True, blank=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_orders_delivered = models.PositiveIntegerField(default=0)
    total_customers = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)


    currency = models.CharField(choices=currency, default="NGN", max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name