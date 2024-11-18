from services.serializers.cart import CartSerializer
from rest_framework import generics
from carts.models import Cart
from rest_framework.permissions import AllowAny, IsAuthenticated

class CartSerializerView(generics.ListAPIView):
    queryset = Cart
    serializer_class = CartSerializer
    permission_classes = AllowAny
