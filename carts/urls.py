from django.urls import path
from .views import *
urlpatterns = [
    path('api/v1/add-to-cart', AddToCartView.as_view(), name="add-to-cart" ),
    path('api/v1/get-cart', CartRetrieveView.as_view(), name="get-cart" ),
    path('api/v1/<int:pk>/update-cart', CartItemUpdateView.as_view(), name="update-cart" ),
    path('api/v1/<int:pk>/delete', CartItemDeleteView.as_view(), name="delete-cart" ),
]
