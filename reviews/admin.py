from django.contrib import admin
from .models import ProductReview, VendorReview, OrderReview
# Register your models here.



@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'product', 'message', 'rating', 'customer')  # Columns in the list view
    list_filter = ('created_at', 'product', 'rating',)  # Filters on the sidebar
    search_fields = ('rating', 'customer', )  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('product', 'message', 'rating', 'customer')
        }),
       
    )



@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'vendor', 'message', 'rating', 'customer')  # Columns in the list view
    list_filter = ('created_at', 'rating', 'vendor')  # Filters on the sidebar
    search_fields = ('rating', 'customer', )  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('vendor', 'message', 'rating', 'customer')
        }),
       
    )

   



@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'order', 'message', 'rating', 'customer')  # Columns in the list view
    list_filter = ('created_at', 'rating', 'order')  # Filters on the sidebar
    search_fields = ('rating', 'customer', )  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('order', 'message', 'rating', 'customer')
        }),
       
    )

   

