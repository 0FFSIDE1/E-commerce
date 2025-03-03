from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/customer/<str:pk>/delete', DeleteCustomerView, name='delete-customer'),
    path('api/v1/customer/create', CreateCustomerView, name='create-customer'),
    path('api/v1/customer', GetCustomer, name='customer'),

]
