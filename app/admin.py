from django.contrib import admin
from .models import AdminUser, OneTimePassword, AccountManager, Subscription, SubscriptionPlan
# Register your models here.




admin.site.register(AccountManager)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan','start_date', 'expire_date', 'is_active')  # Columns in the list view
    list_filter = ('is_active', 'plan', 'user', 'expire_date', 'start_date')  # Filters on the sidebar
    search_fields = ('user__username', 'plan')  # Searchable fields
    ordering = ('expire_date',)  # Default ordering
    readonly_fields = ('user',)  # Fields that cannot be edited
    fieldsets = (
        (None, {
            'fields': ('user', 'expire_date', 'is_active')
        }),
        ('Additional Info', {
            'classes': ('collapse',),
            'fields': ('plan',)
        }),
    )


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_in_days',) 
    list_filter = ('name', 'price', )  
    search_fields = ('name', 'price')
    ordering = ('id',)  
    readonly_fields = ('id',)  
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description', 'duration_in_days')
        }),
        
    )


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vendor', 'code',)  
    list_filter = ('user', 'vendor', ) 
    search_fields = ('code', 'user', 'vendor')  
    ordering = ('id',) 
    readonly_fields = ('id',) 
    fieldsets = (
        (None, {
            'fields': ('user', 'vendor', 'code')
        }),   
    )


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'username', 'email', 'phone', 'updated_at') 
    list_filter = ('created_at', )  
    search_fields = ('email', 'username')
    ordering = ('id',)
    readonly_fields = ('id',)  
    fieldsets = (
        (None, {
            'fields': ('user', 'username', 'email', 'phone',)
        }),
        
    )