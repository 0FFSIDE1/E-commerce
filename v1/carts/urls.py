from django.urls import path
from .views import (
    CartItemsView,
    AddOrUpdateCartItemView,
    RemoveCartItemView,
    CheckProductInCartView,
)

urlpatterns = [
    path("items/<str:pk>/", CartItemsView.as_view(), name="cart_items"),
    path("add_or_update/", AddOrUpdateCartItemView.as_view(), name="add_or_update_cart_item"),
    path("remove/", RemoveCartItemView.as_view(), name="remove_cart_item"),
    path("check_product/", CheckProductInCartView.as_view(), name="check_product_in_cart"),
]
