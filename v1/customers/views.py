from django.shortcuts import render
from rest_framework import generics 
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Customer
from rest_framework import status
from services.serializers.customer import CustomerSerializer
from services.utils.response.customers import *
from services.utils.response.error import Error_Response
from django.http import Http404

# Create your views here.
class Customers_view(generics.ListCreateAPIView):
        """
        GET: Retrieves all customer record
        POST: Add new customer record
        queryset: All rows in customer Entity (total number of customers)
        serializer_class: All columns in customer Entity
        """
        queryset = Customer.objects.all()
        serializer_class = CustomerSerializer
        
        # GET
        def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(get_customers_response(
                queryset = queryset.count(), 
                customer = serializer.data),
                status = status.HTTP_200_OK,
            )

        # POST
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(post_customers_response(
                customer = serializer.data,     
            ), status = status.HTTP_201_CREATED)
        

class Customer_detail(generics.RetrieveUpdateDestroyAPIView):
    """
       GET: Retrieves specific Customer record
       PUT and PATCH: update specific Customer record
       DELETE: delete specific Customer record
       queryset: all row in Customer Entity
       serializer_class: All columns in Customer Entity
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail=Error_Response(error="CustomerNotFound", message="Customer"), code=404)
       
    # def check_permissions(self, request):
    #     if not request.user.has_perm('Customers.change_Customer'):
    #         raise PermissionDenied({"error": "You do not have permission to update this object."})
    #     return super().check_permissions(request)

    # GET
    def retrieve(self, request, *args, **kwargs):
        Customer = self.get_object()
        serializer = self.get_serializer(Customer)
        return Response(retrieve_customer_response_data(
            customer = serializer.data,
        ), status=status.HTTP_200_OK)

    # Update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(update_customer_response_data(
            Customer = serializer.data,
        ), status=status.HTTP_200_OK)
    
    # Delete
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(destroy_customer_response_data(), 
                        status=status.HTTP_204_NO_CONTENT)