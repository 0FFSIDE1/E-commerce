from django.urls import path
from .views import *

urlpatterns = [
    path('add/<str:name>/product', add_to_cart, name='add_to_cart'),
    
]
