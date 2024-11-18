from django.urls import path
from .views import *

urlpatterns = [
   path("", OrderserializerView.as_view(), name="orders-list")
]
