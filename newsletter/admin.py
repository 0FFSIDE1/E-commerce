from django.contrib import admin
from .models import Newsletter
# Register your models here.

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')  # Columns in the list view
    list_filter = ('created_at',)  # Filters on the sidebar
    search_fields = ('email', )  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('email',)
        }),
       
    )

   