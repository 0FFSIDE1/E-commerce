from django.urls import path
from .views import *
urlpatterns = [
    path('api/v1/<str:pk>/add-to-cart', AddToCart, name="add-to-cart" ),
    path('api/v1/get-cart', GetCart, name="get-cart" ),
    path('api/v1/<int:pk>/update-cart', UpdateCartItem, name="update-cart" ),
    path('api/v1/<int:pk>/delete', DeleteCartItem, name="delete-cartitem" ),


]
