from django.contrib import admin
from .models import Cart, CartItem
# 
# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0




@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'user', 'session', 'created_at', 'modified_at')  # Columns in the list view
    list_filter = ('total_amount', 'customer', 'user', 'session', 'created_at')  # Filters on the sidebar
    search_fields = ('user', 'customer')  # Searchable fields
    ordering = ('cart_id',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('user', 'customer', 'session',  'total_amount', )
        }),
       
    )

    inlines = [CartItemInline]