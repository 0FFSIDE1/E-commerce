from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound, PermissionDenied
from sellers.models import Vendor

def get_vendor_by_name(name):
    try:
        vendor = Vendor.objects.get(name=name)
    except Vendor.DoesNotExist:
        raise NotFound(f"No vendor found with the name '{name}'.")
    return vendor

def check_if_user_is_staff(username):
    try:
        user = User.objects.get(username=username, is_staff=True)
    except User.DoesNotExist:
        raise PermissionDenied(f"Only staff members can access this resource.")
    return user

def get_vendor_queryset_for_user(user, name):
    if user.is_staff:
        return Vendor.objects.all()  # Admin can see all profiles
    elif name:
        return Vendor.objects.filter(name=name)  # Non-admin can only see their profile
    raise NotFound("Name not found")
