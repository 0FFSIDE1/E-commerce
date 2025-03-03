from django.contrib import admin
from .models import Coupon
# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('created_at','coupon_name', 'discount', 'code',)  # Columns in the list view
    list_filter = ('created_at',)  # Filters on the sidebar
    search_fields = ('coupon_name', 'discount', 'code')  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    readonly_fields = ('code',)
    fieldsets = (
        (None, {
            'fields': ('coupon_name', 'discount', 'code', )
        }),
       
    )

   
