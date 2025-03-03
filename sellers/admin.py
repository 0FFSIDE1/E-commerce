from django.contrib import admin
from .models import Vendor
# Register your models here.


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'username', 'first_name', 'last_name', 'brand_name', 'phone', 'category', 'is_active') 
    list_filter = ('created_at', )  
    search_fields = ('email', 'username', 'brand_name', 'first_name', 'last_name')
    ordering = ('id',)
    readonly_fields = ('id', 'user' ,'currency')  
    fieldsets = (
        (None, {
            'fields': ('user', 'username', 'first_name', 'last_name', 'brand_name' , 'email', 'phone', 'address', 'city', 'state', 'country', 'category', 'brand_type', 'description', 'total_products', 'total_orders', 'total_orders_delivered', 'total_customers', 'total_reviews','currency')
        }),
        
    )