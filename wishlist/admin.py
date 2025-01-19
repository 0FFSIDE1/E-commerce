from django.contrib import admin

from wishlist.models import WishlistItem, Wishlist

# Register your models here.
class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0




@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', )  # Columns in the list view
    list_filter = ('created_at',)  # Filters on the sidebar
    search_fields = ('user', )  # Searchable fields
    ordering = ('created_at',)  # Default ordering
    
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
       
    )
    inlines = [WishlistItemInline]
