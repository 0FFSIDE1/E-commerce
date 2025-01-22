from django.urls import path
from .views import *
urlpatterns = [

    path('api/v1/product/create', AddProductView, name='create-product'),
    path('api/v1/product/<str:pk>/update', UpdateProductView, name='update-product'),
    path('api/v1/product/<str:pk>/delete', DeleteProductView, name='delete-product'),
    path('api/v1/products/<str:pk>/vendor', ProductsForAVendorCustomerView, name='all-vendor-product'),
    path('api/v1/product', AllProducts, name='all-product'),
    path('api/v1/product/vendor', VendorProducts, name='vendor-product'),
    



]
