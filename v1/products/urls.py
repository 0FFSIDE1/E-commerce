from django.urls import path
from .views import *



urlpatterns = [
   path('', Products_view.as_view(), name='all-Products'),
   path('<str:pk>/product', Product_detail.as_view(), name='Product-detail'),
    
]
