from django.urls import path
from .views import WaitlistVendors

urlpatterns = [
    path('api/v1/vendor/waitlist', WaitlistVendors.as_view(), name='waitlist-vendors'),
]
