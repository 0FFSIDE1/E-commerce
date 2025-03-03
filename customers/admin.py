from django.contrib import admin
from .models import Customer
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'first_name', 'last_name', 'email', 'phone', 'address', 'user', 'country')  # Columns in the list view
    list_filter = ('created_at',)  # Filters on the sidebar
    search_fields = ('first_name', 'last_name', 'user', 'email')  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name',  'email', 'phone', 'address', 'city', 'country', )
        }),
       
    )

   
