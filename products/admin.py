from django.contrib import admin
from .models import Product
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'price', 'quantity', 'category', 'product_type', 'in_stock', 'vendor') 
    list_filter = ('created_at', 'name', 'price', 'category', 'product_type' )  
    search_fields = ('name', 'vendor',)
    ordering = ('item_id',)
    readonly_fields = ('item_id', 'vendor' ,)  
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'previous_price', 'category', 'quantity' , 'product_type', 'photo_1', 'photo_2', 'available_sizes', 'available_colors',  'in_stock',  'vendor',)
        }),
        
    )