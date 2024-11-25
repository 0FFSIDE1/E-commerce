# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from services.serializers.order import OrderSerializer
# from .models import Order
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from customers.models import Customer
# from services.utils.order import *
# from django.http import Http404
# from rest_framework.exceptions import NotFound
# from rest_framework import status


# class Order_View(generics.ListAPIView):

#     serializer_class = OrderSerializer

#     def get_permissions(self):

#         return [IsAuthenticated()]

#     def get_queryset(self):
     
#         user = self.request.user

#         # If admin, retrieve all orders
#         if user.is_staff:
#             queryset = Order.objects.all()
#         else:
#             # Regular users see only their own orders
#             try:
#                 customer = Customer.object.get(user=user)
#                 queryset = Order.objects.filter(customer=customer)
#             except Customer.DoesNotExist:
#                 queryset = Order.objects.none()

            

#         # Apply status filter if provided
#         status_filter = self.request.query_params.get('status', None)
#         if status_filter:
#             queryset = queryset.filter(status=status_filter)

#         # Sort the orders 
#         return queryset.order_by('-created_at')

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(
#             get_orders_response(order=serializer.data,
#                                 count = queryset.count(),
#                                 status = status.HTTP_200_OK)
#         )
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(
#              post_order_response(
#                 order=serializer.data
#             ), status = status.HTTP_201_CREATED
#         )

# class Order_DetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def get_object(self):
#         try:
#             return super().get_object()
#         except Http404:
#             raise NotFound(detail="Order not found.", code=404)
        
#     def retrieve(self, request, *args, **kwargs):
#         order = self.get_object()
#         serializer = self.get_serializer(order)
#         return Response(
#             retrieve_order_response_data(
#                 order=serializer.data
#             ),
#             status=status.HTTP_200_OK
#         )
    
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         order = self.get_object()
#         serializer = self.get_serializer(order, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(
#             update_order_response_data(
#                 order=serializer.data
#             ),
#             status=status.HTTP_200_OK
#         )
    
#     def destroy(self, request, *args, **kwargs):
#         order = self.get_object()
#         self.perform_destroy(order)
#         return Response(
#             destroy_order_response_data(),
#             status=status.HTTP_204_NO_CONTENT
#         )


# class OrderList_APIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer



