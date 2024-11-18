from rest_framework import generics, permissions
from rest_framework.response import Response
from services.serializers.order import OrderSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated, AllowAny


class Order_View(generics.ListAPIView):

    serializer_class = OrderSerializer

    def get_permissions(self):

        return [IsAuthenticated()]

    def get_queryset(self):
     
        user = self.request.user

        # If admin, retrieve all orders
        if user.is_staff:
            queryset = Order.objects.all()
        else:
            # Regular users see only their own orders
            queryset = Order.objects.filter(customer__user=user)

        # Apply status filter if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Sort the orders 
        return queryset.order_by('-created_at')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
