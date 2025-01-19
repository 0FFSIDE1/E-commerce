from django.contrib import admin
from .models import Feedback
# Register your models here.

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'message')  # Columns in the list view
    list_filter = ('created_at',)  # Filters on the sidebar
    search_fields = ('email', )  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('email', 'message')
        }),
       
    )

   
