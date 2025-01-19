from django.db import models
import uuid
from sellers.models import Vendor

# Create your models here.
class Product(models.Model):
    product_category = (
        ('New Arrivals', 'New Arrivals'), 
        ('Black Friday', 'Black Friday'), 
        ('Flashsales', 'Flashsales'), 
        ('Special Offers', 'Special Offers'), 
        ('Sponsored products', 'Sponsored products'), 
        ('Deals of the day', 'Deals of the day'))
    product_type = (
        ('Appliances', 'Appliances'),
        ('Outdoor & Sports', 'Outdoor & Sports'),
        ('Electrical and Electronics', 'Electrical and Electronics'),
        ('Kitchen Appliances', 'Kitchen Appliances'),
        ('Books & Education', 'Books & Education'), 
        ('Interior Decorations', 'Interior Decorations'), 
        ('Lightings & Chandeliars', 'Lightings & Chandeliars'), 
        ('Exterior Decoratrions', 'Exterior Decoratrions'), 
        ('Phone Accessories', 'Phone Accessories'), 
        ('Phones & Tablets', 'Phones & Tablets'), 
        ('Foodstuffs', 'Foodstuffs'), 
        ('Health & Beauty', 'Health & Beauty'), 
        ('Home & Office', 'Home & Office'), 
        ('Gaming', 'Gaming'), 
        ('Computing', 'Computing'), 
        ('Kids and Toys', 'Kids and toys'),
        ('Fitness and Exercise', 'Fitness and Exercise'),
        ('Gadget and Accessories', 'Gadget and Accessories'),
        ('Baby care', 'Baby care'), 
        ('Men Fashion', 'Men Fashion'), 
        ('Men accessories', 'Men accessories'),
        ('Men skincare', 'Men Skincare'),
        ('Women Fashion', 'Women Fashion'), 
        ('Women accessories', 'Women accessories'),
        ('Women skincare', 'women Skincare'),
        ('Kids skincare', 'Kids Skincare'),
        ('Kids Fashion', 'Kids Fashion'),
        ('Kids accessories', 'Kids accessories'),
        )

    item_id = models.UUIDField(max_length=7, primary_key=True, default=uuid.uuid4)
    name =  models.CharField(max_length=125, default=None, blank=False, null=False, unique=True)
    description = models.TextField(max_length=None, default=None, null=True, blank=True)
    price =  models.PositiveIntegerField(default=0, blank=False, null=False)
    quantity = models.PositiveIntegerField(default=1, blank=False, null=False)
    category = models.CharField(choices=product_category, max_length=50, default=None, blank=False, null=False)
    product_type = models.CharField(choices=product_type, max_length=50, default=None, blank=False)
    photo_1 =  models.URLField(default=None, blank=True, null=True,) 
    photo_2 =  models.URLField(default=None, blank=True, null=True,) 
    available_sizes = models.JSONField(default=list, null=True, blank=True)
    available_colors = models.JSONField(default=list, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    previous_price = models.CharField(max_length=125, default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_id}| {self.name} | {self.category} | {self.product_type}"
    
    