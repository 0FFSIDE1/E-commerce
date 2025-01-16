from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/order/<str:pk>/update', UpdateOrderView, name='update-order'),
    path('api/v1/order/create-order', CreateOrderView, name='create-order'),
    path('api/v1/vendor/orders', VendorOrder, name='vendor-orders'),
    path('api/v1/customer/orders', CustomerOrder, name='customer-orders'),
    path('api/v1/customer/<str:pk>/orders', CustomerOrderDetail, name='customer-order-detail'),
    path('api/v1/update/<int:pk>/orderitems', VendorUpdateOrderItem, name='update-orderitem'),

]
