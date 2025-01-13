from django.contrib import admin
from .models import *
# Register your models here.

class InvoiceInline(admin.TabularInline):
    model = Invoice

class PaymentAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceInline
    ]
admin.site.register(Payment, PaymentAdmin)
