from django.contrib import admin
from .models import ProductReview, VendorReview, OrderReview
# Register your models here.
admin.site.register(ProductReview)
admin.site.register(VendorReview)
admin.site.register(OrderReview)