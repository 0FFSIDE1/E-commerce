from rest_framework import serializers
from carts.models import Cart, CartItem
from serializers.product import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Includes product details

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_total_price(self, obj):
        return float(obj.product.item_price) * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.items.all())
