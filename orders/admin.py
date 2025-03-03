from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'created_at', 'total_amount', 'status',) 
    list_filter = ('created_at', 'status',)  
    search_fields = ('order_id', 'customer', 'total_amount')
    ordering = ('order_id',)
    readonly_fields = ('order_id', 'total_amount', 'cart')  
    fieldsets = (
        (None, {
            'fields': ('customer', 'cart', 'total_amount', 'status')
        }),
        
    )
    inlines = [OrderItemInline]