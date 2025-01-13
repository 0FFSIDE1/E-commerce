from django.contrib import admin
from .models import AdminUser, OneTimePassword, AccountManager
# Register your models here.
admin.site.register(AdminUser)
admin.site.register(OneTimePassword)
admin.site.register(AccountManager)