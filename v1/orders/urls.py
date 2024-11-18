from django.urls import path
from .views import *

urlpatterns = [
   path("", Order_View.as_view(), name="orders-list")
]
