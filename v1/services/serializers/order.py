from rest_framework import serializers
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    # product_name = serializers.CharField(source='product.name')
    # product_price = serializers.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     source='product.price')

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'order_id', 'customer', 'customer_name', 'status', 
            'total_amount', 'created_at', 'items'
        ]
        read_only_fields = ['order_id', 'total_amount', 'created_at', 'customer_name', ]
    
    def validate(self, data):
        if 'status' in data and data['status'] not in dict(Order.STATUS_CHOICES):
            raise serializers.ValidationError({'status': 'Invalid order status.'})
        return data

    def create(self, validated_data):
        """
        Create a new Order instance
        """
        order = Order.objects.create(**validated_data)
        return order