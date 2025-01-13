from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/order/<str:pk>/update', UpdateOrderView, name='update-order'),
    path('api/v1/order/create-order', CreateOrderView, name='create-order'),


]
