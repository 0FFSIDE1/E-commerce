from django.contrib import admin

from wishlist.models import WishlistItem, Wishlist

# Register your models here.
class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0

class WishlistAdmin(admin.ModelAdmin):
    inlines = [
        WishlistItemInline  
    ]
admin.site.register(Wishlist, WishlistAdmin)