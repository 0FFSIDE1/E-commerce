from django.db import models
import uuid
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = get_user_model()
class Customer(models.Model):
    customer_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    email = models.EmailField(default=None, unique=True, null=False, blank=False)
    phone = PhoneNumberField(_("Phone Number"), unique=True)
    address = models.CharField(max_length=100, default=None, blank=False, null=False)
    ip_address = models.GenericIPAddressField(_("ip address"), protocol="both", unpack_ipv4=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.email}"