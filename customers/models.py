from django.db import models
import uuid
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.models import Session
# Create your models here.

User = get_user_model()
class Customer(models.Model):
    customer_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    session = models.CharField(max_length=255, null=True, blank=True, help_text="Session ID for anonymous users")  # This is the logic for anonymous users
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=25, default=None, blank=True)
    last_name = models.CharField(max_length=25, default=None, blank=True)
    email = models.EmailField(default=None, unique=True, null=False, blank=False)
    phone = PhoneNumberField(_("Phone Number"))
    address = models.CharField(max_length=100, default=None, blank=False, null=False)
    city = models.CharField(max_length=50, default=None, blank=True, null=True)
    country = models.CharField(max_length=50, default=None, blank=True, null=True)

    ip_address = models.GenericIPAddressField(_("ip address"), protocol="both", unpack_ipv4=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    