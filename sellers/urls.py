from django.urls import path
from .views import *



urlpatterns = [
   path('auth/dashboard/vendor/register', RegisterVendorView.as_view(), name='register-vendor'),
   path('auth/dashboard/vendor/login', LoginVendor, name='login-vendor'),
   path('api/v1/vendor/customers', VendorCustomersView, name='vendor-customers'),
   path('api/v1/vendor/update', UpdateVendor, name='update-vendor'),
   path("adminview/<str:name>", All_View.as_view()),

]

