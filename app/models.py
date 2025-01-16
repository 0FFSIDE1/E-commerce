import uuid
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from sellers.models import Vendor

User = get_user_model()
# Create your models here.
class AdminUser(models.Model):
    username = models.CharField(max_length=30, default=None, blank=False, null=False)
    email = models.CharField(max_length=50, default=None, blank=False, null=False)
    phone = PhoneNumberField(_("Phone Number"), unique=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} | {self.email}"
    
class OneTimePassword(models.Model):
    user = models.OneToOneField(AdminUser, on_delete=models.CASCADE, default=None)
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, default=None)
    code = models.CharField(max_length=6, blank=True, null=True)

class AccountManager(models.Model):
    account_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account_name= models.CharField(max_length=50, default=None, blank=False, null=False)
    bank_name = models.CharField(max_length=50, blank=False, null=False, default=None)
    account_number = models.CharField(max_length=50, default=None, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    updated_at = models.DateTimeField(auto_now=True, blank=False)

  
    
    
    def __str__(self):
        return f"{self.account_name} | {self.account_number}" 

