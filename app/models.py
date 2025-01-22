import uuid
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta, datetime
from sellers.models import Vendor

User = get_user_model()
# Create your models here.
class AdminUser(models.Model):
    username = models.CharField(max_length=30, default=None, blank=False, null=False)
    email = models.CharField(max_length=50, default=None, blank=False, null=False)
    phone = PhoneNumberField(_("Phone Number"), unique=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_days = models.PositiveIntegerField(default=None, blank=False, null=False)  # Duration of the plan
    sub_code = models.CharField(max_length=50, default=None, blank=True, null=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, default=None, related_name="subscriptions")
    start_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s Subscription to {self.plan.name} Plan: From {self.start_date} to {self.expire_date} | {self.is_active}"
    

    @property
    def remaining_days(self):
        if self.expire_date:
            remaining = (self.expire_date - date.today()).days
            return max(remaining, 0)  # Return 0 if the subscription has expired
        return None


    def deactivate(self):
        self.is_active = False
        self.save()

    
        
