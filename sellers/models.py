import uuid
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

class Category(models.TextChoices):
    ELECTRICAL_AND_ELECTRONICS = 'Electrical & Electronics', 'Electrical & Electronics'
    FASHION_AND_CLOTHING = 'Fashion & Clothing', 'Fashion & Clothing'
    HOME_AND_FURNITURE = 'Home & Furniture', 'Home & Furniture'
    BEAUTY_AND_HEALTH = 'Beauty & Health', 'Beauty & Health'
    SPORTS_AND_OUTDOORS = 'Sports & Outdoors', 'Sports & Outdoors'
    BOOKS_AND_STATIONERY = 'Books & Stationery', 'Books & Stationery'
    FOOD_AND_BEVERAGES = 'Food & Beverages', 'Food & Beverages'
    AUTOMOTIVE = 'Automotive', 'Automotive'
    TOYS_AND_BABY_PRODUCTS = 'Toys & Baby Products', 'Toys & Baby Products'
    JEWELRY_AND_ACCESSORIES = 'Jewelry & Accessories', 'Jewelry & Accessories'
    PET_SUPPLIES = 'Pet Supplies', 'Pet Supplies'
    MUSIC_AND_INSTRUMENTS = 'Music & Instruments', 'Music & Instruments'
    GAMING = 'Gaming', 'Gaming'
    OFFICE_SUPPLIES = 'Office Supplies', 'Office Supplies'
    GARDEN_AND_OUTDOORS = 'Garden & Outdoors', 'Garden & Outdoors'
    MEDICAL_AND_HEALTHCARE = 'Medical & Healthcare', 'Medical & Healthcare'
    TRAVEL_AND_LUGGAGE = 'Travel & Luggage', 'Travel & Luggage'
    INDUSTRIAL_AND_SCIENTIFIC = 'Industrial & Scientific', 'Industrial & Scientific'
    ARTS_AND_CRAFTS = 'Arts & Crafts', 'Arts & Crafts'
    SOFTWARE_AND_APPS = 'Software & Apps', 'Software & Apps'
    ENTERTAINMENT_AND_MEDIA = 'Entertainment & Media', 'Entertainment & Media'
    DIGITAL_PRODUCTS = 'Digital Products', 'Digital Products'
    LIGTHINGS_AND_CHANDELIERS = 'Ligthings & Chandelier', 'Ligthings & Chandelier'
    ADMIN = 'Admin', 'Admin'

class Store(models.TextChoices):
    ONLINE_STORE = 'Online Store', 'Online Store'
    PHYSICAL_STORE = 'Physical Store', 'Physical Store'
    BOTH = 'Online & Physical Store', 'Online & Physical Store'
    

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="vendor")
    vendor_id = models.UUIDField(default=uuid.uuid4, editable=False, )
    username = models.CharField(max_length=50, default=None, blank=False, null=False, unique=True)
    brand_name = models.CharField(unique=True, max_length=50, default=None, blank=False, null=False)
    first_name = models.CharField(max_length=50, default=None, blank=False, null=False)
    last_name = models.CharField(max_length=50, default=None, blank=False, null=False)
    email = models.EmailField(max_length=50, default=None, blank=False, null=False, unique=True)
    phone = PhoneNumberField(_("Phone Number"), unique=True)
    
    address = models.CharField(max_length=225, default=None, blank=False, null=False)
    city = models.CharField(max_length=225, default=None)
    state = models.CharField(max_length=225, default=None)
    country = models.CharField(max_length=225, default=None)

    category = models.CharField(choices=Category, max_length=50, default=None, blank=False, null=False)
    brand_type = models.CharField(choices=Store, max_length=50, default=None, blank=False, null=False)
    description = models.TextField(max_length=500, default=None, blank=True, null=True)
    
    total_products = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_orders_delivered = models.PositiveIntegerField(default=0)
    total_customers = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)


    currency = models.CharField(choices=currency, default="NGN", max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username