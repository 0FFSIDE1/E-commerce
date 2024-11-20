from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListAPIView, CreateAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response
from .models import CartItem, Product, Cart
from services.utils.cart import get_or_create_cart, get_product_or_404
from services.serializers.cart import CartItemSerializer, CartSerializer
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from uuid import uuid4
from django.db.models import F

# To create a cartitem
class Create_View(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

# TO view cartitem based on a specific user
class Items_View(generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Get customer name from the URL
        customer_name = self.kwargs.get("customer_name")
        if not customer_name:
            raise NotFound("Customer name is required.")

        # Try to find the cart for an authenticated user
        carts = Cart.objects.filter(customer__username=customer_name)

        # If no authenticated user cart, try finding by session ID
        if not carts.exists():
            carts = Cart.objects.filter(session_id=customer_name)

        if not carts.exists():
            raise NotFound(f"No cart found for customer: {customer_name}")

        # Retrieve all CartItems associated with the matching carts
        return CartItem.objects.filter(cart__in=carts)

# To update a cartitem based on a specific user
class Update_View(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # lookup_pk = "customer_name"

class Destroy_View(generics.RetrieveDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Updated successfully"})

    #     else:
    #         return Response({"message": "failed", "details": serializer.errors})


# class listview(generics.ListAPIView):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     lookup_url_kwarg = "customer_name"

# specific based view logic
# class Items_View(generics.RetrieveAPIView):
#     serializer_class = CartItemSerializer

#     def get_object(self):
#         # Get customer name from the URL
#         customer_name = self.kwargs.get("customer_name")
#         if not customer_name:
#             raise NotFound("Customer name is required.")

#         # Try to find the cart for an authenticated user
#         try:
#             cart = Cart.objects.filter(customer__username=customer_name)
#         except Cart.DoesNotExist:
#             # If no authenticated user cart, try finding by session ID
#             try:
#                 cart = Cart.objects.filter(session_id=customer_name)
#             except Cart.DoesNotExist:
#                 raise NotFound(f"No cart found for customer: {customer_name}")

#         # Return the first cart item associated with the cart (or handle as needed)
#         cart_items = CartItem.objects.filter(cart=cart)
#         if not cart_items.exists():
#             raise NotFound(f"No items found in the cart for customer: {customer_name}")

#         return cart_items.objects,filter(cart__in=cart)  # For `RetrieveAPIView`, return a single object


