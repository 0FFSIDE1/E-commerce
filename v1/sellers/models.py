from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=50, default=None, blank=False, null=False)
    address = models.CharField(max_length=225, default=None, blank=False, null=False)
    email = models.EmailField(max_length=50, default=None, blank=False, null=False)
    phone = PhoneNumberField(_("Phone Number"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name