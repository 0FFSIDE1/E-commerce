from django.contrib import admin
from .models import AdminUser, OneTimePassword, AccountManager, Subscription, SubscriptionPlan
# Register your models here.
admin.site.register(AdminUser)
admin.site.register(OneTimePassword)
admin.site.register(AccountManager)

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0

class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [
        SubscriptionInline
    ]
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)