from django.urls import path
from .views import *



urlpatterns = [
    path('api/v1/wishlist/<str:pk>/create', AddToWishlist, name='add-to-wishlist'),
    path('api/v1/wishlist', GetWishlist, name='get-wishlist'),
    path('api/v1/wishlist/<str:pk>/delete', DeleteWishlistItem, name='delete-wishlist'),


]