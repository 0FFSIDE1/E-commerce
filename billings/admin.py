from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'order', 'amount','payment_method', 'status',) 
    list_filter = ('created_at', 'amount', 'status')  
    search_fields = ('order', 'payment_id', 'amount', 'status')
    ordering = ('payment_id',)
    readonly_fields = ('order_id',)  
    fieldsets = (
        (None, {
            'fields': ('order_id', 'order', 'amount', 'status', 'payment_method')
        }),
        
    )