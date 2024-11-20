from django.contrib import admin
from .models import *
# Register your models here.
# class PaymentAdmin(admin.ModelAdmin):
# 	list_display = ["payment_id", "ref", 'amount', "status", "created_at", "payment_method"]


admin.site.register(Payment)
admin.site.register(Invoice)
