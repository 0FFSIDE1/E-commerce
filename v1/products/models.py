from django.db import models
import uuid
from sellers.models import Vendor

# Create your models here.
class Product(models.Model):
    section_choices = (
        ('New Arrivals', 'New Arrivals'), 
        ('Black Friday', 'Black Friday'), 
        ('Flashsales', 'Flashsales'), 
        ('Special Offers', 'Special Offers'), 
        ('Sponsored products', 'Sponsored products'), 
        ('Deals of the day', 'Deals of the day'))
    category_choices = (
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

    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name =  models.CharField(max_length=125, default=None, blank=False, null=False)
    description = models.TextField(max_length=None, default=None, blank=True, null=True)
    price = models.CharField(max_length=25, default=None, blank=False, null=False)
    previous_price = models.CharField(max_length=25, default=None, blank=True, null=True)
    product_type = models.CharField(max_length=20, default=None, blank=False, null=False)
    brand = models.CharField(max_length=20, default=None)
    in_stock = models.BooleanField(default=True)
    quantity = models.CharField(max_length=20, default=None, blank=False, null=False)
    section = models.CharField(choices=section_choices, max_length=50, default='New Arrivals', blank=True, null=True)
    category = models.CharField(choices=category_choices, max_length=50, default=None, blank=False, null=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor', default="OFFSIDE STORES", blank=True, null=True)
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    