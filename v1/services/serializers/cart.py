from rest_framework import serializers
from carts.models import Cart, CartItem
from services.serializers.product import ProductSerializer
from products.models import Product

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    product_details = ProductSerializer(source="product", read_only=True)
    total_price = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()


    class Meta:
        model = CartItem
        fields = "__all__"

    def get_total_price(self, obj):
        return float(obj.product.price) * obj.quantity
    
    def get_customer_name(self, obj):
        """
        Retrieve the customer's username from the associated Cart object.
        If no customer is linked, return None.
        """
        if obj.cart.customer:
            return obj.cart.customer.username
        return obj.cart.session_id