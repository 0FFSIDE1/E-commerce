from django.shortcuts import render
from services.serializers.order import OrderSerializer
from rest_framework import generics
from orders.models import Order
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class Order_View(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  

    # To retrieve the order based on the status
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(customer=user)

        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset
    
    # Saving the order associated with the user
     # def perform_create(self, serializer):
     #   serializer.save(user=self.request.user)
