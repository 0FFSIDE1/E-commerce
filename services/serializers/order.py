from rest_framework import serializers
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['name', 'size', 'color', 'price', 'quantity', 'total_price',]

class OrderSerializer(serializers.ModelSerializer):
    # Serialize related order items
    items = OrderItemSerializer(source='orderitems', many=True, read_only=True)

    # Include detailed customer information
    customer = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'order_id', 'customer', 'items', 'total_amount', 'status', 'created_at',
        ]
        read_only_fields = ['order_id', 'total_amount', 'created_at', 'items']
    
    def get_customer(self, obj):
        """
        Get detailed customer information using CustomerSerializer.
        """
        customer = obj.customer
        return {
            "id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": str(customer.phone),
            "address": customer.address,  # Assuming you have an address field
        }
    
    def validate(self, data):
        """
        Validate the status field to ensure it uses a valid status choice.
        """
        if 'status' in data and data['status'] not in dict(Order.STATUS_CHOICES):
            raise serializers.ValidationError({'status': 'Invalid order status.'})
        return data

    def create(self, validated_data):
        """
        Create a new Order instance and associate order items.
        """
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order